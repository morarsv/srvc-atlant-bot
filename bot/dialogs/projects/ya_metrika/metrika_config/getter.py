import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            WordConst as WConst)

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def counters_getter(dialog_manager: DialogManager,
                          i18n: TranslatorRunner,
                          event_from_user: User,
                          **kwargs):
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    counters = start_data[StDataConst.list_counters.value]

    if counters:
        status_edit_counter = widget_data.get(WgDataConst.status_edit_counter.value, False)

        preview_text = i18n.project.ya.metrika.config.counters.full()

        edit = 1 if status_edit_counter else None
        selected = 1 if widget_data.get(WgDataConst.selected_counter_id.value, False) else None
        edit = None if selected else edit

        preview_text = f'{preview_text}\n\n{i18n.project.ya.metrika.config.edit.notice.counter()}' if edit else \
            preview_text

    else:
        preview_text = i18n.project.ya.metrika.config.counters.empty()
        edit = None
        selected = None

    return {
        'preview_text': preview_text,
        'btn_continue': i18n.button.next(),
        'btn_back': i18n.button.back(),
        'btn_cancel': i18n.button.cancel(),
        'counters': counters,
        'selected': selected,
        'edit': edit
    }


async def attribution_getter(dialog_manager: DialogManager,
                             i18n: TranslatorRunner,
                             event_from_user: User,
                             **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    attribution = widget_data[WgDataConst.list_attributions.value]
    selected = 1 if widget_data.get(WgDataConst.selected_attribution.value) else None
    return {
        'attribution': attribution,
        'attribution_text': i18n.project.ya.metrika.config.attribution(),
        'selected': selected,
        'btn_continue': i18n.button.next(),
        'btn_back': i18n.button.back()
    }


async def minor_attribution_getter(dialog_manager: DialogManager,
                                   i18n: TranslatorRunner,
                                   event_from_user: User,
                                   **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    attribution = widget_data[WgDataConst.list_m_attributions.value]
    return {
        'attribution': attribution,
        'attribution_text': i18n.project.ya.metrika.config.m.attribution(),
        'btn_continue': i18n.button.next(),
        'btn_back': i18n.button.back()
    }


async def k_goals_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    k_goals = widget_data.get(WgDataConst.list_k_goals.value, None)
    k_goals_text = i18n.project.ya.metrika.key.goals.full() if k_goals else i18n.project.ya.metrika.key.goals.empty()
    selected = widget_data.get(WgDataConst.selected_counter_k_goals_id.value, None)
    return {
        'k_goals_text': k_goals_text,
        'k_goals': k_goals,
        'btn_continue': i18n.button.next(),
        'btn_back': i18n.button.back(),
        'selected': selected
    }


async def m_goals_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    m_goals = widget_data.get(WgDataConst.list_m_goals.value, None)
    m_goals_text = i18n.project.ya.metrika.minor.goals.full() if m_goals else \
        i18n.project.ya.metrika.minor.goals.empty()

    return {
        'm_goals_text': m_goals_text,
        'm_goals': m_goals,
        'btn_continue': i18n.button.next(),
        'btn_back': i18n.button.back(),
    }


async def ecommerce_getter(dialog_manager: DialogManager,
                           i18n: TranslatorRunner,
                           event_from_user: User,
                           **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    ecommerce = [(WConst.yes.value, 1), (WConst.no.value, 0)]
    ecommerce_text = i18n.project.ya.metrika.ecommerce()
    selected = widget_data.get(WgDataConst.selected_counter_ecommerce.value, None)
    return {
        'ecommerce_text': ecommerce_text,
        'ecommerce': ecommerce,
        'btn_continue': i18n.button.next(),
        'btn_back': i18n.button.back(),
        'selected': selected
    }


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    role_id = start_data[StDataConst.user_role_id.value]
    project_title = start_data[StDataConst.project_title.value]
    status_old_obj = start_data.get(StDataConst.status_old_obj.value, False)
    if status_old_obj:
        start_data[StDataConst.status_old_obj.value] = False
        widget_data[WgDataConst.status_old_obj.value] = True
        counter_id = start_data[StDataConst.counter_id.value]
        counter_name = start_data[StDataConst.counter_name.value]
        counter_attribution = start_data[StDataConst.counter_attribution.value]
        counter_minor_attribution = start_data[StDataConst.counter_minor_attribution.value]
        counter_k_goals = start_data[StDataConst.counter_k_goals.value]
        counter_m_goals = start_data[StDataConst.counter_m_goals.value]
        counter_ecommerce = start_data[StDataConst.counter_ecommerce.value]

        widget_data[WgDataConst.counter_id.value] = counter_id
        widget_data[WgDataConst.counter_name.value] = counter_name
        widget_data[WgDataConst.counter_attribution.value] = counter_attribution
        widget_data[WgDataConst.counter_minor_attribution.value] = counter_minor_attribution
        widget_data[WgDataConst.counter_k_goals.value] = counter_k_goals
        widget_data[WgDataConst.counter_m_goals.value] = counter_m_goals
        widget_data[WgDataConst.counter_ecommerce.value] = counter_ecommerce

    counter_id = widget_data[WgDataConst.counter_id.value]
    counter_name = widget_data[WgDataConst.counter_name.value]
    counter_attribution = widget_data[WgDataConst.counter_attribution.value]
    counter_minor_attribution = widget_data[WgDataConst.counter_minor_attribution.value] if \
        widget_data[WgDataConst.counter_minor_attribution.value] != 'None' else '-'
    counter_k_goals = widget_data[WgDataConst.counter_k_goals.value]
    counter_m_goals = widget_data[WgDataConst.counter_m_goals.value] if \
        widget_data[WgDataConst.counter_m_goals.value] != 'None' else '-'
    counter_ecommerce = widget_data[WgDataConst.counter_ecommerce.value]

    counter_ecommerce = WConst.yes.value if counter_ecommerce == 1 else WConst.no.value
    preview_text = i18n.project.ya.metrika.counters.info.counter(
        project_title=project_title,
        attribution=counter_attribution,
        minor_attribution=counter_minor_attribution,
        counter=counter_name,
        counter_id=counter_id,
        k_goals=counter_k_goals,
        m_goals=counter_m_goals,
        ecommerce=counter_ecommerce
    )
    access = 1 if role_id != 4 else None
    edited = 1 if widget_data.get(WgDataConst.status_edit_counter.value, False) else None
    return {
        'preview_text': preview_text,
        'btn_confirm': i18n.button.confirm(),
        'btn_cancel': i18n.button.cancel(),
        'btn_edit_counter': i18n.button.edit.counter(),
        'access': access,
        'edited': edited
    }
