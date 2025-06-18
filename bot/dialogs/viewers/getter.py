import logging

from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (StartDataConstant as StDataConst,
                                            WidgetDataConstant as WgDataConst)

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    start_data = dialog_manager.start_data
    viewers = start_data[StDataConst.list_viewers.value]
    preview_text = f'{i18n.viewers.preview.viewers()}\n\n{i18n.viewers.description.list.viewers()}' if viewers else \
        i18n.viewers.preview.viewers()
    return {
        'preview_text': preview_text,
        'btn_list_viewers': i18n.button.list.viewers(),
        'btn_add_user': i18n.button.add.user(),
        'btn_back': i18n.button.back(),
        'viewers': viewers,
    }


async def list_viewers_getter(dialog_manager: DialogManager,
                              i18n: TranslatorRunner,
                              event_from_user: User,
                              **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    viewers = widget_data[WgDataConst.list_viewers.value]
    return {
        'preview_text': i18n.viewers.list.viewers(),
        'btn_back': i18n.button.back(),
        'viewers': viewers
    }


async def info_viewer_getter(dialog_manager: DialogManager,
                             i18n: TranslatorRunner,
                             event_from_user: User,
                             **kwargs):
    widget_data = dialog_manager.current_context().widget_data

    remove_project = widget_data[WgDataConst.viewer_connected_list_projects.value]
    set_project = widget_data[WgDataConst.viewer_available_list_projects.value]
    connected = widget_data[WgDataConst.viewer_connected_list_projects.value]
    available = widget_data[WgDataConst.viewer_available_list_projects.value]

    viewer_login = widget_data[WgDataConst.viewer_login.value]
    viewer_username = widget_data[WgDataConst.viewer_username.value]
    preview_text = i18n.viewers.info.viewer(
        full_name=viewer_username,
        login=viewer_login
    )
    preview_text = f'{preview_text}\n\n{i18n.viewers.description.connect.projects()}' if available else preview_text
    preview_text = f'{preview_text}\n\n{i18n.viewers.description.remove.projects()}' if connected else preview_text

    return {
        'preview_text': preview_text,
        'btn_delete_viewer': i18n.button.delete.object(),
        'btn_set_project': i18n.button.viewer.set.projects(),
        'btn_remove_project': i18n.button.viewer.remove.projects(),
        'btn_back': i18n.button.back(),
        'set_project': set_project,
        'remove_project': remove_project
    }


async def list_projects_getter(dialog_manager: DialogManager,
                               i18n: TranslatorRunner,
                               event_from_user: User,
                               **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    projects = widget_data[WgDataConst.list_projects.value]
    preview_text = i18n.viewers.settings.projects()

    selected = 1 if widget_data.get(WgDataConst.projects_id.value, None) else None
    return {
        'preview_text': preview_text,
        'btn_confirm': i18n.button.confirm(),
        'btn_back': i18n.button.back(),
        'selected': selected,
        'projects': projects,
    }
