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

    project_title = start_data[StDataConst.project_title.value]
    project_description = start_data[StDataConst.project_description.value]
    managers = start_data[StDataConst.project_managers.value]
    ya_direct_logins = start_data[StDataConst.project_ya_direct_logins.value]
    ya_metrika_counters = start_data[StDataConst.project_ya_metrika_counters.value]
    available_managers = start_data[StDataConst.available_managers.value]
    connected_managers = start_data[StDataConst.connected_managers.value]

    ya_logins = 1 if ya_direct_logins != 'None' else None
    ya_counters = 1 if ya_metrika_counters != 'None' else None
    available_managers = 1 if available_managers != 'None' else None
    connected_managers = 1 if connected_managers != 'None' else None
    list_managers = managers if managers != 'None' else '-'

    preview_text = i18n.company.admin.info.project(
        title=project_title,
        description=project_description,
        list_managers=list_managers
    )
    preview_text = f'{preview_text}\n\n{i18n.company.admin.info.ya.logins(logins=ya_direct_logins)}' if \
        ya_logins else preview_text
    preview_text = f'{preview_text}\n\n{i18n.company.admin.info.ya.counters(counters=ya_metrika_counters)}' if \
        ya_counters else preview_text
    preview_text = f'{preview_text}\n\n{i18n.company.admin.description.button.set.manager()}' if \
        available_managers else preview_text
    preview_text = f'{preview_text}\n\n{i18n.company.admin.description.button.remove.manager()}' if \
        connected_managers else preview_text
    return {
        'preview_text': preview_text,
        'btn_ya_list_counters': i18n.button.list.ya.counters(),
        'btn_set_managers': i18n.button.set.manager(),
        'btn_remove_managers': i18n.button.remove.manager(),
        'btn_back': i18n.button.back(),
        'connected_managers': connected_managers,
        'available_managers': available_managers,
        'ya_counters': ya_counters
    }


async def list_ya_counters_getter(dialog_manager: DialogManager,
                                  i18n: TranslatorRunner,
                                  event_from_user: User,
                                  **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    counters = widget_data[WgDataConst.project_list_counters.value]
    preview_text = i18n.project.list.metrika()
    return {
        'preview_text': preview_text,
        'btn_back': i18n.button.back(),
        'counters': counters
    }


async def ya_counter_getter(dialog_manager: DialogManager,
                            i18n: TranslatorRunner,
                            event_from_user: User,
                            **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    project_title = start_data[StDataConst.project_title.value]
    attribution = widget_data[WgDataConst.counter_attribution.value]
    minor_attribution = widget_data[WgDataConst.counter_minor_attribution.value]
    counter_name = widget_data[WgDataConst.counter_name.value]
    counter_id = widget_data[WgDataConst.counter_id.value]
    k_goals_names = widget_data[WgDataConst.counter_k_goals.value]
    m_goals_names = widget_data[WgDataConst.counter_m_goals.value]
    ecommerce = widget_data[WgDataConst.counter_ecommerce.value]

    preview_text = i18n.project.ya.metrika.counters.info.counter(
        project_title=project_title,
        attribution=attribution,
        minor_attribution=minor_attribution,
        counter=counter_name,
        counter_id=counter_id,
        k_goals=k_goals_names,
        m_goals=m_goals_names,
        ecommerce=ecommerce
    )
    return {
        'preview_text': preview_text,
        'btn_back': i18n.button.back()
    }


async def list_available_managers_getter(dialog_manager: DialogManager,
                                         i18n: TranslatorRunner,
                                         event_from_user: User,
                                         **kwargs):
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    preview_text = i18n.company.admin.set.managers()
    managers = start_data[StDataConst.available_managers.value]
    selected = widget_data.get(WgDataConst.selected_manager_set_to_project.value, None)

    return {
        'preview_text': preview_text,
        'btn_confirm': i18n.button.confirm(),
        'btn_back': i18n.button.back(),
        'managers': managers,
        'selected': selected
    }


async def list_connected_managers_getter(dialog_manager: DialogManager,
                                         i18n: TranslatorRunner,
                                         event_from_user: User,
                                         **kwargs):
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    preview_text = i18n.company.admin.remove.managers()
    managers = start_data[StDataConst.connected_managers.value]
    selected = widget_data.get(WgDataConst.selected_manager_remove_from_project.value, None)

    return {
        'preview_text': preview_text,
        'btn_confirm': i18n.button.confirm(),
        'btn_back': i18n.button.back(),
        'managers': managers,
        'selected': selected
    }
