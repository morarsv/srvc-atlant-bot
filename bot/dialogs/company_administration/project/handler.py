import logging
import asyncio
from uuid import UUID
from typing import Any, TYPE_CHECKING
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from bot.state.dialog_state import CompanyAdminProjectsSG
from fluentogram import TranslatorRunner
from bot.database.models import Users, YaMetrikaCounters
from bot.database import query
from bot.lexicon.constants.constant import (PoolingConstant as poolConst,
                                            StartDataConstant as StDataConst,
                                            WidgetDataConstant as WgDataConst,
                                            WordConst as WConst)
from bot.services.web_reports.utils import web_set_user_to_project, web_remove_user_from_project
from bot.support_models.models import SupportSessionUser

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def update_start_data(dialog_manager: DialogManager,
                            callback: CallbackQuery,
                            project_id: int) -> None:
    middleware_data = dialog_manager.middleware_data
    start_data = dialog_manager.start_data
    tg_id = int(callback.from_user.id)

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    user: SupportSessionUser = online_users.get(tg_id)
    company_id: int = int(user.get('company_id'))

    list_connected_managers: list[Users] = await query.get_list_managers_by_p_id(project_id=project_id)
    list_available_managers: list[Users] = await query.get_available_managers_by_p_id(project_id=project_id,
                                                                                      company_id=company_id)

    available_managers = [(manager.full_name, manager.login) for manager in list_available_managers] if \
        list_available_managers else 'None'
    connected_managers = [(manager.full_name, manager.login) for manager in list_connected_managers] if \
        list_connected_managers else 'None'
    managers_list = [manager[0] for manager in connected_managers] if list_connected_managers else None

    managers = ', '.join(managers_list) if list_connected_managers else 'None'

    start_data[StDataConst.available_managers.value] = available_managers
    start_data[StDataConst.connected_managers.value] = connected_managers
    start_data[StDataConst.project_managers.value] = managers


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_ya_list_counters(callback: CallbackQuery,
                               button: Button,
                               dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data
    project_id = int(start_data[StDataConst.project_id.value])

    list_counters: list[YaMetrikaCounters] = await query.get_ya_m_list_counters_by_p_id(project_id=project_id)
    counters = [(f'{c.counter_name}:{c.counter_id}', c.id) for c in list_counters]
    widget_data[WgDataConst.project_list_counters.value] = counters
    await dialog_manager.switch_to(
        show_mode=ShowMode.EDIT,
        state=CompanyAdminProjectsSG.LIST_YA_COUNTERS
    )


async def btn_switch_to_ya_counter(callback: CallbackQuery,
                                   widget: Any,
                                   dialog_manager: DialogManager,
                                   selected_item: str, ) -> None:
    widget_data = dialog_manager.current_context().widget_data
    selected_counter = int(selected_item)

    counter: YaMetrikaCounters = await query.get_ya_m_counter_by_id(counter_id=selected_counter)

    names_minor_goals = counter.names_minor_goals
    m_goals_names = ('\n'.join(names_minor_goals)) if counter.names_minor_goals else '-'
    k_goals_names = '\n'.join(counter.names_key_goals)

    widget_data[WgDataConst.counter_attribution.value] = counter.attribution
    widget_data[WgDataConst.counter_minor_attribution.value] = counter.minor_attribution or '-'
    widget_data[WgDataConst.counter_name.value] = counter.counter_name
    widget_data[WgDataConst.counter_id.value] = counter.counter_id
    widget_data[WgDataConst.counter_k_goals.value] = k_goals_names
    widget_data[WgDataConst.counter_m_goals.value] = m_goals_names
    widget_data[WgDataConst.counter_ecommerce.value] = WConst.yes.value if counter.ecommerce == 1 else WConst.no.value

    await dialog_manager.switch_to(state=CompanyAdminProjectsSG.YA_COUNTER,
                                   show_mode=ShowMode.EDIT)


async def btn_back_from_managers(callback: CallbackQuery,
                                 button: Button,
                                 dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data

    widget_data[WgDataConst.selected_manager_set_to_project.value] = []
    widget_data[WgDataConst.selected_manager_remove_from_project.value] = []


async def btn_confirm_set(callback: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    project_id = int(start_data[StDataConst.project_id.value])

    i18n: TranslatorRunner = dialog_manager.middleware_data[poolConst.i18n.value]
    list_logins = widget_data[WgDataConst.selected_manager_set_to_project.value]
    list_users: list[UUID] = await query.get_list_users_uuid_by_logins(list_logins=list_logins)

    requests = [query.set_manager_to_project(project_id=project_id,
                                             user_uuid=user_uuid) for user_uuid in list_users]
    await asyncio.gather(*requests)

    requests_web = [web_set_user_to_project(
        logger=logger,
        project_id=project_id,
        user_id=str(user_uuid),
        callback=callback
    ) for user_uuid in list_users]
    await asyncio.gather(*requests_web)
    widget_data[WgDataConst.selected_manager_set_to_project.value] = []
    await update_start_data(
        dialog_manager=dialog_manager,
        callback=callback,
        project_id=project_id
    )
    await callback.answer(text=i18n.successfully.updated())
    await dialog_manager.switch_to(state=CompanyAdminProjectsSG.PREVIEW,
                                   show_mode=ShowMode.EDIT)


async def btn_confirm_remove(callback: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    project_id = int(start_data[StDataConst.project_id.value])

    i18n: TranslatorRunner = dialog_manager.middleware_data[poolConst.i18n.value]
    list_logins = widget_data[WgDataConst.selected_manager_remove_from_project.value]
    list_users: list[UUID] = await query.get_list_users_uuid_by_logins(list_logins=list_logins)

    requests = [query.remove_user_from_project(project_id=project_id,
                                               user_uuid=user_uuid) for user_uuid in list_users]
    await asyncio.gather(*requests)
    requests_web = [web_remove_user_from_project(
        logger=logger,
        project_id=project_id,
        user_id=str(user_uuid),
        callback=callback
    ) for user_uuid in list_users]

    await asyncio.gather(*requests_web)
    widget_data[WgDataConst.selected_manager_remove_from_project.value] = []
    await update_start_data(
        dialog_manager=dialog_manager,
        callback=callback,
        project_id=project_id
    )
    await callback.answer(text=i18n.successfully.updated())
    await dialog_manager.switch_to(state=CompanyAdminProjectsSG.PREVIEW,
                                   show_mode=ShowMode.EDIT)
