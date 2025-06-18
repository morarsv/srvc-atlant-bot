import logging
from aiogram.types import User
from typing import TYPE_CHECKING
from aiogram_dialog import DialogManager, ShowMode
from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import StartDataConstant as StDataConst

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         event_from_user: User,
                         i18n: TranslatorRunner,
                         **_kwargs):
    try:
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    except AttributeError as e:
        dialog_manager.show_mode = ShowMode.SEND
        logger.error(f'Error deleting message: {e}')

    start_data = dialog_manager.start_data

    authorized = start_data[StDataConst.authorized.value]
    unauthorized = start_data[StDataConst.unauthorized.value]

    menu_text = i18n.authorization.authorized() if authorized else i18n.authorization.unauthorized()
    authorized = [1] if authorized else None
    unauthorized = [1] if unauthorized else None
    return {
        'menu_text': menu_text,
        'btn_login': i18n.button.login(),
        'btn_logout': i18n.button.logout(),
        'unauthorized': unauthorized,
        'authorized': authorized
    }


async def input_getter(dialog_manager: DialogManager,
                       event_from_user: User,
                       i18n: TranslatorRunner,
                       **_kwargs):
    return {
        'input_password': i18n.authorization.input.password(),
        'input_login': i18n.authorization.input.login()
    }


async def fail_getter(dialog_manager: DialogManager,
                      event_from_user: User,
                      i18n: TranslatorRunner,
                      **_kwargs):
    return {
        'menu_text': i18n.authorization.fail(),
        'btn_login': i18n.button.login()
    }
