import asyncio
import logging
from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button

from bot.database import query
from bot.database.models import Projects, Users, Companies
from bot.state.dialog_state import (AtlantAdministrationAddCompanySG, AtlantAdministrationEditAddUserSG,
                                    AtlantAdministrationProjectSG, AtlantAdministrationUserSG,
                                    AtlantAdministrationSG)
from bot.services.msvc.generator import func
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            WordConst as WConst)

logger = logging.getLogger(__name__)


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_add_company(callback: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager) -> None:
    await dialog_manager.start(mode=StartMode.NORMAL,
                               show_mode=ShowMode.EDIT,
                               state=AtlantAdministrationAddCompanySG.INPUT_COMPANY)


async def btn_regenerate_dbt(callback: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager) -> None:
    asyncio.create_task(func.regenerate_dbt(
        logger=logger
    ))


async def btn_add_user(callback: CallbackQuery,
                       button: Button,
                       dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data

    companies_list: list[Companies] = await query.get_all_companies()
    companies = [(c.company, c.id) for c in companies_list]
    widget_data[WgDataConst.companies.value] = companies
    await dialog_manager.switch_to(state=AtlantAdministrationSG.ADD_USER,
                                   show_mode=ShowMode.EDIT)


async def btn_list_companies(callback: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data

    companies_list: list[Companies] = await query.get_all_companies()
    companies = [(c.company, c.id) for c in companies_list]
    widget_data[WgDataConst.companies.value] = companies
    await dialog_manager.switch_to(state=AtlantAdministrationSG.LIST_COMPANIES,
                                   show_mode=ShowMode.EDIT)


async def btn_add_user_for_company(callback: CallbackQuery,
                                   widget: Any,
                                   dialog_manager: DialogManager,
                                   selected_item: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    companies = widget_data[WgDataConst.companies.value]
    company_id = int(selected_item)
    company_name = next(name for name, id_ in companies if id_ == company_id)

    await dialog_manager.start(mode=StartMode.NORMAL,
                               show_mode=ShowMode.EDIT,
                               state=AtlantAdministrationEditAddUserSG.INPUT_USERNAME,
                               data={
                                   StDataConst.company_name.value: company_name,
                                   StDataConst.company_id.value: company_id,
                                   StDataConst.status.value: StDataConst.old_company.value
                               })


async def btn_switch_to_company(callback: CallbackQuery,
                                widget: Any,
                                dialog_manager: DialogManager,
                                selected_item: str) -> None:
    widget_data = dialog_manager.current_context().widget_data

    company_id = int(selected_item)
    company: Companies = await query.get_company_by_id(c_id=company_id)
    company_name = company.company

    users_list: list[Users] = await query.get_users_by_company_id(company_id=company_id)
    projects_list: list[Projects] = await query.get_projects_by_company(company_id=company_id)

    users = [(u.full_name, u.login) for u in users_list]
    projects = [(p.title, p.id) for p in projects_list]

    widget_data[WgDataConst.users.value] = users
    widget_data[WgDataConst.projects.value] = projects
    widget_data[WgDataConst.company_name.value] = company_name
    widget_data[WgDataConst.company_id.value] = company_id
    widget_data[WgDataConst.company_created.value] = str(company.created_at)[:10]

    await dialog_manager.switch_to(state=AtlantAdministrationSG.CARD_COMPANY,
                                   show_mode=ShowMode.EDIT)


async def btn_regenerate_yaml(callback: CallbackQuery,
                              button: Button,
                              dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    company_name = widget_data[WgDataConst.company_name.value]
    company_id = widget_data[WgDataConst.company_id.value]
    asyncio.create_task(func.regenerate_dag(
        logger=logger,
        company_id=company_id,
        company_name=company_name
    ))


async def btn_switch_to_user(callback: CallbackQuery,
                             widget: Any,
                             dialog_manager: DialogManager,
                             selected_item: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    user_login = selected_item
    company_name = widget_data[WgDataConst.company_name.value]

    user: Users = await query.get_user_by_login(login=user_login)
    projects_list: list[Projects] = await query.get_list_projects_by_user_uuid(user_uuid=user.id)

    username = user.full_name
    user_password = user.password
    user_projects = ', '.join(p.title for p in projects_list) if projects_list else WConst.missing.value
    user_role = user.role.role
    user_status = WConst.activated.value if user.active else WConst.deactivated.value
    user_created = str(user.created_at)[:10]
    await dialog_manager.start(
        state=AtlantAdministrationUserSG.PREVIEW,
        mode=StartMode.NORMAL,
        show_mode=ShowMode.EDIT,
        data={
            StDataConst.company_name.value: company_name,
            StDataConst.username.value: username,
            StDataConst.user_projects.value: user_projects,
            StDataConst.user_role.value: user_role,
            StDataConst.user_status.value: user_status,
            StDataConst.user_password.value: user_password,
            StDataConst.user_login.value: user_login,
            StDataConst.user_created.value: user_created
        }
    )


async def btn_switch_to_project(callback: CallbackQuery,
                                widget: Any,
                                dialog_manager: DialogManager,
                                selected_item: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    project_id = int(selected_item)
    company_name = widget_data[WgDataConst.company_id.value]

    project: Projects = await query.get_project_by_id(project_id=project_id)
    managers_list: list[Users] = await query.get_list_managers_by_p_id(project_id=project_id)

    list_counters: list[str] = await query.get_ya_m_counters_names_by_p_id(p_id=project_id)
    list_logins: list[str] = await query.get_ya_d_logins_names_by_p_id(p_id=project_id)

    ya_counters = ', '.join(list_counters) if list_counters else 'None'
    ya_logins = ', '.join(list_logins) if list_logins else 'None'

    project_title = project.title
    project_description = project.description
    project_created = str(project.created_at)[:10]
    project_author = project.user.full_name
    project_managers = ', '.join(m.full_name for m in managers_list)

    await dialog_manager.start(
        state=AtlantAdministrationProjectSG.PREVIEW,
        mode=StartMode.NORMAL,
        show_mode=ShowMode.EDIT,
        data={
            StDataConst.project_id.value: project.id,
            StDataConst.project_title.value: project_title,
            StDataConst.project_description.value: project_description,
            StDataConst.project_ya_direct_logins.value: ya_logins,
            StDataConst.project_ya_metrika_counters.value: ya_counters,
            StDataConst.company_name.value: company_name,
            StDataConst.project_author.value: project_author,
            StDataConst.project_created.value: project_created,
            StDataConst.project_managers.value: project_managers,
        }
    )
