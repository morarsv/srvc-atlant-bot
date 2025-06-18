import asyncio
import logging
import os
import pytz
from typing import Optional

from asyncio.exceptions import CancelledError
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.base import BaseStorage
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub
from bot.config_data.config import Config, load_config
from bot.utils.i18n import create_translator_hub
from bot.utils.nuts_connect import connect_to_nats
from bot.storage.nats_storage import NatsStorage
from bot.database.models import async_database_run
from bot.support_models.models import SupportSessionUser, CustomFormatter
from bot.utils.set_cmd_menu import set_main_menu
from bot.utils.bot_func import bot_current_time
# Роутеры и диалоги
from bot.handlers.faq import faq_router
from bot.handlers.start import start_router
from bot.handlers.authorization import authorization_router
from bot.handlers.info import info_router
from bot.handlers.help import help_router

from bot.dialogs.authorization.dialog import authorization_dialog
from bot.dialogs.start.dialog import start_dialog
from bot.dialogs.atlant_administration.dialog import atlant_administration_dialog
from bot.dialogs.atlant_administration.add_edit_user.dialog import atlant_administration_add_edit_user_dialog
from bot.dialogs.atlant_administration.add_company.dialog import atlant_administration_add_company_dialog
from bot.dialogs.atlant_administration.user.dialog import atlant_administration_user_dialog
from bot.dialogs.atlant_administration.project.dialog import atlant_administration_project_dialog
from bot.dialogs.projects.dialog import project_dialog
from bot.dialogs.projects.edit_add_project.dialog import project_edit_add_dialog
from bot.dialogs.projects.ya_direct.dialog import ya_direct_add_logins_dialog
from bot.dialogs.projects.ya_direct.settings.dialog import ya_direct_settings_logins_dialog
from bot.dialogs.projects.ya_direct.advertiser.dialog import ya_direct_add_advertiser_logins_dialog
from bot.dialogs.projects.ya_direct.agency.dialog import ya_direct_add_agency_logins_dialog
from bot.dialogs.projects.ya_direct.representative.dialog import ya_direct_add_representative_logins_dialog
from bot.dialogs.projects.ya_metrika.dialog import ya_metrika_list_counters_dialog
from bot.dialogs.projects.ya_metrika.metrika_config.dialog import ya_metrika_config_counter_dialog
from bot.dialogs.company_administration.dialog import company_admin_dialog
from bot.dialogs.company_administration.project.dialog import company_admin_project_dialog
from bot.dialogs.company_administration.add_edit_user.dialog import company_admin_add_edit_user_dialog
from bot.dialogs.viewers.dialog import viewers_dialog
from bot.dialogs.viewers.add_user.dialog import viewers_add_viewer_dialog
from bot.dialogs.faq.dialog import faq_dialog
from bot.dialogs.help.dialog import help_dialog
from bot.dialogs.connect_user.dialog import connect_user_dialog
from bot.dialogs.info.dialog import info_dialog

from bot.middlewares.i18n import TranslatorRunnerMiddleware


def setup_dp(storage: Optional[BaseStorage] = None):
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        start_router,
        info_router,
        help_router,
        faq_router,
        authorization_router,
        authorization_dialog,
        start_dialog,
        atlant_administration_dialog,
        atlant_administration_add_edit_user_dialog,
        atlant_administration_add_company_dialog,
        atlant_administration_user_dialog,
        atlant_administration_project_dialog,
        faq_dialog,
        help_dialog,
        project_dialog,
        project_edit_add_dialog,
        ya_direct_add_logins_dialog,
        ya_direct_settings_logins_dialog,
        ya_direct_add_advertiser_logins_dialog,
        ya_direct_add_agency_logins_dialog,
        ya_direct_add_representative_logins_dialog,
        ya_metrika_list_counters_dialog,
        ya_metrika_config_counter_dialog,
        viewers_dialog,
        viewers_add_viewer_dialog,
        company_admin_dialog,
        company_admin_project_dialog,
        company_admin_add_edit_user_dialog,
        connect_user_dialog,
        info_dialog
    )
    setup_dialogs(dp)
    return dp


async def main():
    config: Config = load_config()

    log_directory = config.paths.log_err
    time = await bot_current_time()
    timezone = pytz.timezone("Asia/Novosibirsk")
    os.makedirs(log_directory, exist_ok=True)
    log_file_path = os.path.join(log_directory, f'err_bot_{time[:10]}.log')

    file_handler = logging.FileHandler(filename=log_file_path, mode='a', encoding='utf-8')
    log_format = '[{asctime}] #{levelname:<8} {filename} - {lineno} - {name} - {message}'
    date_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        style='{',
        handlers=[
            logging.StreamHandler()
        ]
    )
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(
        CustomFormatter(fmt=log_format, datefmt=date_format, style='{', tz=timezone)
    )
    logging.getLogger().addHandler(file_handler)

    nc, js = await connect_to_nats(servers=config.nats.servers)
    storage: NatsStorage = await NatsStorage(nc=nc, js=js).create_storage()
    translator_hub: TranslatorHub = create_translator_hub()

    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = setup_dp(storage=storage)
    dp.update.middleware(TranslatorRunnerMiddleware())

    online_users: dict[int, SupportSessionUser] = {}
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await async_database_run()
    try:
        await dp.start_polling(bot,
                               _translator_hub=translator_hub,
                               _online_users=online_users)
    except Exception as e:
        logging.exception(e)
    finally:
        await nc.close()
        logging.info('Connection to NATS closed')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt or CancelledError:
        logging.error("Shutting down...")
