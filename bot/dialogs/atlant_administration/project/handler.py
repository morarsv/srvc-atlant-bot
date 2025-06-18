import logging
from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from bot.database import query
from bot.database.models import YaMetrikaCounters
from bot.state.dialog_state import AtlantAdministrationProjectSG
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            WordConst as WConst,
                                            StartDataConstant as StDataConst)

logger = logging.getLogger(__name__)


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_switch_to_counter(callback: CallbackQuery,
                                widget: Any,
                                dialog_manager: DialogManager,
                                selected_item: str) -> None:
    widget_data = dialog_manager.current_context().widget_data

    selected_counter = int(selected_item)
    counter: YaMetrikaCounters = await query.get_ya_m_counter_by_id(counter_id=selected_counter)

    k_goals = ', '.join(k for k in counter.names_key_goals)
    m_goals = ', '.join(counter.names_minor_goals or []) or '-'
    ecommerce = WConst.yes.value if counter.ecommerce == 1 else WConst.no.value

    widget_data[WgDataConst.counter_attribution.value] = counter.attribution
    widget_data[WgDataConst.counter_minor_attribution.value] = counter.minor_attribution or '-'
    widget_data[WgDataConst.counter_name.value] = counter.counter_name
    widget_data[WgDataConst.counter_id.value] = counter.counter_id
    widget_data[WgDataConst.counter_k_goals.value] = k_goals
    widget_data[WgDataConst.counter_m_goals.value] = m_goals
    widget_data[WgDataConst.counter_ecommerce.value] = ecommerce

    await dialog_manager.switch_to(state=AtlantAdministrationProjectSG.COUNTER,
                                   show_mode=ShowMode.EDIT)


async def btn_counters_list(callback: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    project_id = int(start_data[StDataConst.project_id.value])

    list_counters: list[YaMetrikaCounters] = await query.get_ya_m_list_counters_by_p_id(project_id=project_id)
    counters = [(f'{c.counter_name}:{c.counter_id}', c.id) for c in list_counters]
    widget_data[WgDataConst.project_list_counters.value] = counters
    await dialog_manager.switch_to(state=AtlantAdministrationProjectSG.LIST_COUNTRIES, show_mode=ShowMode.EDIT)