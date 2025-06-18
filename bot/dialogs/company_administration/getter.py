import logging

from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import StartDataConstant as StDataConst

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    start_data = dialog_manager.start_data

    projects = start_data[StDataConst.list_projects.value]
    users = start_data[StDataConst.list_users.value]

    preview_text = i18n.company.admin.description.button.add.user()
    preview_text = f'{preview_text}\n\n{i18n.company.admin.description.button.list.projects()}' if projects \
        else preview_text
    preview_text = f'{preview_text}\n\n{i18n.company.admin.description.button.list.users()}' if users \
        else preview_text
    preview_text = f'{preview_text}\n\n{i18n.company.admin.description.button.logout.frm.sessions()}'

    projects = 1 if projects else None
    users = 1 if users else None

    return {
        'preview_text': preview_text,
        'btn_add_user': i18n.button.add.user(),
        'btn_list_projects': i18n.button.list.projects(),
        'btn_list_users': i18n.button.list.users(),
        'btn_logout_from_sessions': i18n.button.web.logout.frm.sessions(),
        'btn_back': i18n.button.back(),
        'projects': projects,
        'users': users
    }


async def list_projects_getter(dialog_manager: DialogManager,
                               i18n: TranslatorRunner,
                               event_from_user: User,
                               **kwargs):
    start_data = dialog_manager.start_data

    projects = start_data[StDataConst.list_projects.value]
    preview_text = i18n.company.admin.list.projects()

    return {
        'preview_text': preview_text,
        'projects': projects,
        'btn_back': i18n.button.back()
    }


async def list_users_getter(dialog_manager: DialogManager,
                            i18n: TranslatorRunner,
                            event_from_user: User,
                            **kwargs):
    start_data = dialog_manager.start_data

    users = start_data[StDataConst.list_users.value]
    preview_text = i18n.company.admin.list.users()

    return {
        'preview_text': preview_text,
        'users': users,
        'btn_back': i18n.button.back()
    }
