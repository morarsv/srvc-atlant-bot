import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager

from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            DialogDataConstant as DgDataConst)

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def input_getter(dialog_manager: DialogManager,
                       i18n: TranslatorRunner,
                       event_from_user: User,
                       **kwargs):
    dialog_data = dialog_manager.dialog_data
    skip = None if dialog_data.get(DgDataConst.finished_key.value) else 1
    return {
        'input_title': i18n.input.project.title(),
        'input_description': i18n.input.project.description(),
        'btn_cancel': i18n.button.cancel(),
        'btn_skip': i18n.button.skip(),
        'skip': skip
    }


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data
    dialog_data = dialog_manager.dialog_data

    dialog_data[DgDataConst.finished_key.value] = True
    status_edit = start_data.get(StDataConst.status_edit.value, False)
    if status_edit:
        start_data[StDataConst.status_edit.value] = False
        widget_data[WgDataConst.status_edit_project.value] = True

        title = start_data[StDataConst.project_title.value]
        description = start_data[StDataConst.project_description.value]
        widget_data[WgDataConst.project_title.value] = title
        widget_data[WgDataConst.project_description.value] = description

    title = widget_data[WgDataConst.project_title.value]
    description = widget_data.get(WgDataConst.project_description.value, ' ')
    confirm = widget_data.get(WgDataConst.status_confirm.value, None)
    delete = widget_data.get(WgDataConst.status_edit_project.value, None)
    preview_text = i18n.project.info.about.project(
        title=title,
        description=description
    )
    preview_text = f'{preview_text}\n\n{i18n.description.button.confirm()}' if confirm else preview_text

    return {
        'preview_text': preview_text,
        'btn_edit_title': i18n.button.edit.title(),
        'btn_edit_description': i18n.button.edit.description(),
        'btn_confirm': i18n.button.confirm(),
        'btn_delete': i18n.button.delete.object(),
        'btn_cancel': i18n.button.cancel(),
        'delete': delete,
        'confirm': confirm
    }
