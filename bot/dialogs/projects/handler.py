import logging
from uuid import UUID
from typing import Any
from aiogram.types import User
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from bot.lexicon.lexicon_ya import LEXICON_SYSTEM_ID
from bot.services.yandex.utils import get_ya_counters
from bot.database import query
from bot.database.models import (Projects, YaDirectLogins,
                                 YaMetrikaCounters, YandexAccesses)
from bot.state.dialog_state import (StartSG, ProjectsSG, ProjectsEditAddSG, YaMetrikaCountersSG,
                                    YaMetrikaCountersEditAddSG, YaDirectLoginsSettingsSG, YaDirectLoginsAddSG)
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            PoolingConstant as poolConst)
from bot.support_models.models import SupportSessionUser

logger = logging.getLogger(__name__)


async def get_list_projects(dialog_manager: DialogManager,
                            event_from_user: User) -> list[tuple[str, int]]:
    middleware_data = dialog_manager.middleware_data
    tg_id = int(event_from_user.id)

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    user: SupportSessionUser = online_users.get(tg_id)
    user_uuid: UUID = user['user_uuid']

    list_projects: list[Projects] = await query.get_list_projects_by_user_uuid(user_uuid=user_uuid)
    projects = [(p.title, p.id) for p in list_projects]
    return projects


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        show_mode=ShowMode.EDIT,
        mode=StartMode.RESET_STACK,
        state=StartSG.PREVIEW
    )


async def btn_add_project(callback: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data

    user_uuid = start_data[StDataConst.user_uuid.value]
    await dialog_manager.start(
        state=ProjectsEditAddSG.INPUT_TITLE,
        show_mode=ShowMode.EDIT,
        mode=StartMode.NORMAL,
        data={
            StDataConst.user_uuid.value: user_uuid
        }
    )


async def btn_update_list_project(callback: CallbackQuery,
                                  button: Button,
                                  dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data

    user_uuid = UUID(start_data[StDataConst.user_uuid.value])
    list_projects: list[Projects] = await query.get_list_projects_by_user_uuid(user_uuid=user_uuid)
    projects = [(p.title, p.id) for p in list_projects]
    start_data[StDataConst.list_projects.value] = projects


async def btn_switch_to_project(callback: CallbackQuery,
                                widget: Any,
                                dialog_manager: DialogManager,
                                selected_item: str) -> None:
    project_id = int(selected_item)
    widget_data = dialog_manager.current_context().widget_data

    widget_data[WgDataConst.project_id.value] = project_id

    await dialog_manager.switch_to(
        state=ProjectsSG.INFO_PROJECT,
        show_mode=ShowMode.EDIT
    )


async def switch_to_service(callback: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    project_id = int(widget_data.get(WgDataConst.project_id.value,
                                     start_data.get(StDataConst.project_id.value)))
    ya_access_metrika: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_METRIKA']
    )
    ya_access_direct: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_DIRECT']
    )

    access_metrika = True if ya_access_metrika else False
    access_direct = True if ya_access_direct else False
    widget_data[WgDataConst.ya_access_metrika.value] = access_metrika
    widget_data[WgDataConst.ya_access_direct.value] = access_direct


async def update_project_data(dialog_manager: DialogManager):
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data
    project_id = widget_data.get(WgDataConst.project_id.value,
                                 start_data.get(StDataConst.project_id.value))
    project: Projects = await query.get_project_by_id(project_id=project_id)
    list_counters: list[str] = await query.get_ya_m_counters_names_by_p_id(p_id=project_id)
    list_logins: list[str] = await query.get_ya_active_d_logins_names_by_p_id(p_id=project_id)
    url_link = await query.get_report_project(project_id=project.id)
    counters = ', '.join(list_counters or []) or None
    logins = ', '.join(list_logins or []) or None

    widget_data[WgDataConst.project_id.value] = project_id
    widget_data[WgDataConst.project_title.value] = project.title
    widget_data[WgDataConst.project_description.value] = project.description
    widget_data[WgDataConst.project_connected_counters.value] = counters
    widget_data[WgDataConst.project_connected_logins.value] = logins

    return project_id, project.title, project.description, counters, logins, url_link


async def btn_settings_ya_logins(callback: CallbackQuery,
                                 button: Button,
                                 dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    project_id = widget_data[WgDataConst.project_id.value]
    all_logins: list[YaDirectLogins] = await query.get_ya_direct_logins_by_project_id(p_id=project_id)

    active_list_logins = [(login.direct_login, login.id) for login in all_logins if login.active]
    inactive_list_logins = [(login.direct_login, login.id) for login in all_logins if not login.active]

    activated_logins: list[str] = [login.direct_login for login in all_logins if login.active]
    deactivated_logins: list[str] = [login.direct_login for login in all_logins if not login.active]
    activated_logins_names = ', '.join(activated_logins or []) or None
    deactivated_logins_names = ', '.join(deactivated_logins or []) or None

    await dialog_manager.start(
        state=YaDirectLoginsSettingsSG.PREVIEW,
        mode=StartMode.NORMAL,
        show_mode=ShowMode.EDIT,
        data={
            StDataConst.project_id.value: project_id,
            StDataConst.ya_direct_activated_logins.value: activated_logins_names,
            StDataConst.ya_direct_deactivated_logins.value: deactivated_logins_names,
            StDataConst.project_ya_list_active_logins.value: active_list_logins,
            StDataConst.project_ya_list_inactive_logins.value: inactive_list_logins
        }
    )


async def btn_settings_ya_counters(callback: CallbackQuery,
                                   button: Button,
                                   dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    role_id = start_data[StDataConst.user_role_id.value]
    project_id = widget_data[WgDataConst.project_id.value]
    project_title = widget_data[WgDataConst.project_title.value]
    list_counters: list[YaMetrikaCounters] = await query.get_ya_m_list_counters_by_p_id(project_id=project_id)
    counter: YaMetrikaCounters = list_counters[0]
    counters = [(f'{c.counter_name}: {c.counter_id}', str(c.id)) for c in list_counters]
    await dialog_manager.start(
        state=YaMetrikaCountersSG.PREVIEW,
        mode=StartMode.NORMAL,
        show_mode=ShowMode.EDIT,
        data={
            StDataConst.counter_attribution.value: counter.attribution,
            StDataConst.counter_minor_attribution.value: counter.minor_attribution,
            StDataConst.user_role_id.value: role_id,
            StDataConst.project_id.value: project_id,
            StDataConst.project_title.value: project_title,
            StDataConst.ya_metrika_counters.value: counters
        }
    )


async def btn_edit_project(callback: CallbackQuery,
                           button: Button,
                           dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data

    project_id = widget_data[WgDataConst.project_id.value]
    project_title = widget_data[WgDataConst.project_title.value]
    project_description = widget_data[WgDataConst.project_description.value]

    await dialog_manager.start(
        state=ProjectsEditAddSG.PREVIEW,
        show_mode=ShowMode.EDIT,
        mode=StartMode.NORMAL,
        data={
            StDataConst.status_edit.value: True,
            StDataConst.project_id.value: project_id,
            StDataConst.project_title.value: project_title,
            StDataConst.project_description.value: project_description
        }
    )


async def btn_update_status(callback: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    project_id = widget_data.get(WgDataConst.project_id.value,
                                 start_data.get(StDataConst.project_id.value))

    ya_access_metrika: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_METRIKA']
    )
    ya_access_direct: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_DIRECT']
    )

    access_metrika = True if ya_access_metrika else False
    access_direct = True if ya_access_direct else False
    widget_data[WgDataConst.ya_access_metrika.value] = access_metrika
    widget_data[WgDataConst.ya_access_direct.value] = access_direct
    await dialog_manager.switch_to(
        state=ProjectsSG.ADD_SERVICE,
        show_mode=ShowMode.EDIT
    )


async def btn_add_ya_logins(callback: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data
    project_id = widget_data.get(WgDataConst.project_id.value,
                                 start_data.get(StDataConst.project_id.value, ''))
    await dialog_manager.start(
        state=YaDirectLoginsAddSG.PREVIEW,
        show_mode=ShowMode.EDIT,
        mode=StartMode.NORMAL,
        data={
            StDataConst.project_id.value: project_id
        }
    )


async def btn_add_ya_counters(callback: CallbackQuery,
                              button: Button,
                              dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    project_title = widget_data.get(WgDataConst.project_title.value,
                                    start_data.get(StDataConst.project_title.value, ''))
    project_id = widget_data.get(WgDataConst.project_id.value,
                                 start_data.get(StDataConst.project_id.value, ''))
    list_counters: list[YaMetrikaCounters] = await query.get_ya_m_list_counters_by_p_id(project_id=project_id)

    role_id = start_data[StDataConst.user_role_id.value]

    if list_counters:
        counter: YaMetrikaCounters = list_counters[0]
        counters = [(f'{c.counter_name}: {c.counter_id}', str(c.id)) for c in list_counters]
        await dialog_manager.start(
            state=YaMetrikaCountersSG.PREVIEW,
            show_mode=ShowMode.EDIT,
            mode=StartMode.NORMAL,
            data={
                StDataConst.user_role_id.value: role_id,
                StDataConst.counter_attribution.value: counter.attribution,
                StDataConst.counter_minor_attribution.value: counter.minor_attribution,
                StDataConst.project_id.value: project_id,
                StDataConst.project_title.value: project_title,
                StDataConst.ya_metrika_counters.value: counters
            }
        )
    else:
        ya_accesses: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
            p_id=project_id,
            s_id=LEXICON_SYSTEM_ID['YA_METRIKA']
        )
        counters = await get_ya_counters(
            oauth_token=ya_accesses.access_token,
            logger=logger
        )
        await dialog_manager.start(
            state=YaMetrikaCountersEditAddSG.COUNTERS,
            show_mode=ShowMode.EDIT,
            mode=StartMode.NORMAL,
            data={
                StDataConst.user_role_id.value: role_id,
                StDataConst.status_first.value: True,
                StDataConst.project_title.value: project_title,
                StDataConst.project_id.value: project_id,
                StDataConst.list_counters.value: counters
            }
        )


async def btn_ya_metrika_access(callback: CallbackQuery,
                                button: Button,
                                dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.selected_metrika.value] = True

    await dialog_manager.switch_to(state=ProjectsSG.YA_ACCESS,
                                   show_mode=ShowMode.EDIT)


async def btn_ya_direct_access(callback: CallbackQuery,
                               button: Button,
                               dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.selected_metrika.value] = False

    await dialog_manager.switch_to(state=ProjectsSG.YA_ACCESS,
                                   show_mode=ShowMode.EDIT)

