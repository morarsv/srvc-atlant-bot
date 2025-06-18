import logging
import httpx
from aiogram.types import CallbackQuery
from bot.config_data.config import Config, load_config
from bot.lexicon.lexicon_web import LEXICON_API_DATA
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from bot.utils.bot_func import err_msg_api_atlant_web
from bot.utils.bot_func import bot_current_time


configuration: Config = load_config()

_username: str = LEXICON_API_DATA['USER']
_password: str = LEXICON_API_DATA['PASSWORD']

_chat_id = LEXICON_TG_BOT['CHAT_ID_ERR_REPORT']


async def generate_dag(logger: logging,
                       project_title: str,
                       project_id: int,
                       company_name: str,
                       start_date: str,
                       callback: CallbackQuery
                       ) -> None:
    url = configuration.msvc_generator.url + configuration.msvc_generator.yaml
    data = {
        "project_title": project_title,
        "project_id": project_id,
        "company_name": company_name,
        "start_date": start_date,
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              json=data,
                              auth=httpx.BasicAuth(username=_username,
                                                   password=_password)
                              )

        if r.status_code == 409:
            return
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            time = await bot_current_time()
            msg = ('Something bad has happened.\n'
                   'For security reasons detailed information about the error is not logged.\n'
                   'You should check your webserver logs and retrieve details of this error.')
            err_text = msg if r.status_code == 500 else r.text
            await err_msg_api_atlant_web(
                time=time,
                chat_id=_chat_id,
                callback=callback,
                code=str(r.status_code),
                err_text=err_text
            )
