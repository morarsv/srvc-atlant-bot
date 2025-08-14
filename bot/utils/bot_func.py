import pytz
import re
import logging
from uuid import UUID
from dateutil.relativedelta import relativedelta
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime, timedelta
from fluentogram import TranslatorRunner
from aiogram_dialog import DialogManager
from bot.database.models import Users
from bot.database import query
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from typing import TYPE_CHECKING
from bot.config_data.config import Config, load_config
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from bot.support_models.models import SupportSessionUser
from bot.lexicon.constants.constant import PoolingConstant as poolConst

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)

configuration: Config = load_config()

alert_bot = Bot(token=configuration.tg_bot.alerts_token)


async def send_alert_to_chat(text: str,
                             chat_id: str) -> None:
    try:
        await alert_bot.send_message(chat_id=chat_id,
                                     text=text)
    except TelegramError as e:
        logging.error(f"Не удалось отправить сообщение в Telegram: {e}")


def clean_text(text: str) -> str:
    clean = re.sub(r'^[\s\u2068]+|[\s\u2069]+$', '', text)
    return clean


def get_session_data(
        tg_id: int,
        dialog_manager: DialogManager
) -> tuple[str, str, int, UUID, int, str]:
    middleware_data = dialog_manager.middleware_data
    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]
    user: SupportSessionUser = online_users.get(tg_id)
    username: str = user['username']
    login: str = user['login']
    role_id: int = user['role_id']
    user_uuid: UUID = user['user_uuid']
    company_id: int = user['company_id']
    company_name: str = user['company_name']

    return username, login, role_id, user_uuid, company_id, company_name


async def bot_current_time() -> str:
    current_time_zone = datetime.now(pytz.utc)
    utc_plus_7 = current_time_zone.astimezone(pytz.timezone("Asia/Novosibirsk"))
    time = utc_plus_7.strftime("%Y-%m-%d %H:%M:%S")
    return time


async def bot_start_end_airflow_dag(created_date: str) -> tuple[str, str]:
    created_date = datetime.strptime(created_date[:19], "%Y-%m-%d %H:%M:%S")
    current_time = datetime.strptime(await bot_current_time(), "%Y-%m-%d %H:%M:%S")
    end_date = current_time - timedelta(days=1)
    start_date = (created_date - relativedelta(months=3)).replace(day=1)
    return str(start_date)[:10], str(end_date)[:10]


async def err_msg_airflow_connection(time: str,
                                     project_id: str,
                                     counter_login: str,
                                     chat_id: str,
                                     i18n: TranslatorRunner,
                                     callback: CallbackQuery,
                                     code: str,
                                     err_text: str) -> None:
    user: Users = await query.get_user_by_tg_id(tg_id=callback.from_user.id)
    company_name = user.company.company
    try:
        await send_alert_to_chat(chat_id=chat_id,
                                 text=i18n.error.airflow.add.connection.direct(
                                     user=f'{user.full_name} / {user.login}',
                                     company=company_name,
                                     project_id=project_id,
                                     counter_login=counter_login,
                                     time=time,
                                     code=code,
                                     err_text=err_text
                                 ))
    except TelegramBadRequest as e:
        logger.exception(f'TelegramBadRequest: {e}')


async def err_msg_airflow_start_dag(project_id: str,
                                    company_name: str,
                                    i18n: TranslatorRunner,
                                    callback: CallbackQuery,
                                    code: str,
                                    err_text: str) -> None:
    time: str = await bot_current_time()
    chat_id = LEXICON_TG_BOT['CHAT_ID_ERR_REPORT']
    user: Users = await query.get_user_by_tg_id(tg_id=callback.from_user.id)
    try:
        await send_alert_to_chat(chat_id=chat_id,
                                 text=i18n.error.airflow.start.dag(
                                     user=f'{user.full_name} / {user.login}',
                                     company=company_name,
                                     project_id=project_id,
                                     time=time,
                                     code=code,
                                     err_text=err_text
                                 ))
    except TelegramBadRequest as e:
        logger.exception(f'TelegramBadRequest: {e}')


async def err_msg_api_atlant_web(time: str,
                                 chat_id: str,
                                 code: str,
                                 err_text: str) -> None:
    try:
        await send_alert_to_chat(chat_id=chat_id,
                                 text=f'Time: {time}\n'
                                      f'Code: {code}\n'
                                      f'Err text: {err_text}')
    except TelegramBadRequest as e:
        logging.error(f'TelegramBadRequest: {e}')


async def alert_msg_to_chat(chat_id: str,
                            msg: str,
                            logger: logging) -> None:
    try:
        await send_alert_to_chat(chat_id=chat_id,
                                 text=msg)
    except TelegramBadRequest as e:
        logger.error(f'TelegramBadRequest: {e}')


async def detect_language(text: str) -> str:
    pattern = r"[^\w\s_-]"

    rus_to_lat = str.maketrans({
        "а": "a", "б": "b", "в": "v", "г": "g",
        "д": "d", "е": "e", "ё": "yo", "ж": "zh",
        "з": "z", "и": "i", "й": "y", "к": "k",
        "л": "l", "м": "m", "н": "n", "о": "o",
        "п": "p", "р": "r", "с": "s", "т": "t",
        "у": "u", "ф": "f", "х": "kh", "ц": "ts",
        "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "",
        "ы": "y", "ь": "", "э": "e", "ю": "yu",
        "я": "ya",
        " ": "_",
    })

    text = text.lower()
    text = re.sub(pattern, "_", text)
    text = text.translate(rus_to_lat)

    return text
