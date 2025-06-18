import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from bot.lexicon.lexicon_ya import LEXICON_ATTRIBUTION
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst)


if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    start_data = dialog_manager.start_data

    attribution = start_data[StDataConst.counter_attribution.value]
    minor_attribution = start_data[StDataConst.counter_minor_attribution.value] or '-'
    role_id = start_data[StDataConst.user_role_id.value]
    list_counters = start_data[StDataConst.ya_metrika_counters.value]

    preview_text = i18n.project.ya.metrika.counters.preview.manager(
        key_attribution=attribution,
        minor_attribution=minor_attribution
    )

    preview_text = preview_text if role_id != 4 else i18n.project.ya.metrika.counters.preview.viewer(
        key_attribution=attribution,
        minor_attribution=minor_attribution
    )
    access = 1 if role_id != 4 else None

    return {
        'preview_text': preview_text,
        'btn_add_metrika': i18n.button.add.ya.counters(),
        'btn_edit_attribution': i18n.button.edit.attribution(),
        'btn_back': i18n.button.back(),
        'list_counters': list_counters,
        'access': access
    }


async def key_attribution_getter(dialog_manager: DialogManager,
                                 i18n: TranslatorRunner,
                                 event_from_user: User,
                                 **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    attribution = widget_data[WgDataConst.list_attributions.value]
    selected = 1 if widget_data.get(WgDataConst.counter_attribution.value) else None
    return {
        'attribution': attribution,
        'attribution_text': i18n.project.ya.metrika.config.attribution(),
        'selected': selected,
        'btn_continue': i18n.button.next(),
        'btn_cancel': i18n.button.cancel()
    }


async def minor_attribution_getter(dialog_manager: DialogManager,
                                   i18n: TranslatorRunner,
                                   event_from_user: User,
                                   **kwargs):
    widget_data = dialog_manager.current_context().widget_data

    attribution = widget_data[WgDataConst.list_attributions.value]
    return {
        'attribution': attribution,
        'attribution_text': i18n.project.ya.metrika.config.m.attribution(),
        'btn_continue': i18n.button.next(),
        'btn_back': i18n.button.back()
    }


async def window_attribution_getter(dialog_manager: DialogManager,
                                    i18n: TranslatorRunner,
                                    event_from_user: User,
                                    **kwargs):
    widget_data = dialog_manager.current_context().widget_data

    attribution = widget_data[WgDataConst.counter_attribution.value]
    minor_attribution = widget_data.get(WgDataConst.counter_minor_attribution.value, None)

    minor_attribution = LEXICON_ATTRIBUTION.get(minor_attribution[0]) if minor_attribution else '-'
    preview_text = i18n.project.ya.metrika.counters.selected.attribution(
        key_attribution=attribution,
        minor_attribution=minor_attribution
    )
    return {
        'preview_text': preview_text,
        'btn_confirm': i18n.button.confirm(),
        'btn_cancel': i18n.button.cancel()
    }
