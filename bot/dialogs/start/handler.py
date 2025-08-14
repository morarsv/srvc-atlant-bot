import logging
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from bot.state.dialog_state import AtlantAdministrationSG, ProjectsSG, ViewersSG, CompanyAdminSG
from bot.database.models import Users, Projects
from bot.utils.bot_func import get_session_data
from bot.database import query
from bot.lexicon.constants.constant import (StartDataConstant as StDataConst,
                                            WidgetDataConstant as WDataConst)


logger = logging.getLogger(__name__)


async def btn_to_atlant_administrator(callback: CallbackQuery,
                                      button: Button,
                                      dialog_manager: DialogManager) -> None:
    await dialog_manager.start(show_mode=ShowMode.EDIT,
                               state=AtlantAdministrationSG.PREVIEW,
                               mode=StartMode.NORMAL)


async def btn_to_administrator(callback: CallbackQuery,
                               button: Button,
                               dialog_manager: DialogManager) -> None:
    tg_id = int(callback.from_user.id)
    _, _, _, _, company_id, _ = get_session_data(
        tg_id=tg_id,
        dialog_manager=dialog_manager
    )
    list_projects: list[Projects] = await query.get_projects_by_company(company_id=company_id)
    list_users: list[Users] = await query.get_active_users_by_company_id(company_id=company_id)

    projects: list[tuple[str, int]] = [(project.title, project.id) for project in list_projects]
    users: list[tuple[str, str]] = [(user.full_name, user.login) for user in list_users]

    await dialog_manager.start(
        state=CompanyAdminSG.PREVIEW,
        show_mode=ShowMode.EDIT,
        mode=StartMode.RESET_STACK,
        data={
            StDataConst.list_projects.value: projects,
            StDataConst.list_users.value: users
        }
    )


async def btn_to_project(callback: CallbackQuery,
                         button: Button,
                         dialog_manager: DialogManager) -> None:
    tg_id = int(callback.from_user.id)

    _, _, role_id, user_uuid, _, _ = get_session_data(
        tg_id=tg_id,
        dialog_manager=dialog_manager
    )

    await dialog_manager.start(
        show_mode=ShowMode.EDIT,
        state=ProjectsSG.PREVIEW,
        mode=StartMode.NORMAL,
        data={
            StDataConst.user_uuid.value: str(user_uuid),
            StDataConst.user_role_id.value: role_id
        }
    )


async def btn_to_viewers(callback: CallbackQuery,
                         button: Button,
                         dialog_manager: DialogManager) -> None:
    tg_id = int(callback.from_user.id)

    _, _, _, user_uuid, company_id, _ = get_session_data(
        tg_id=tg_id,
        dialog_manager=dialog_manager
    )
    list_users: list[Users] = await query.get_viewers_by_manager_id(manager_id=user_uuid)
    users = [(user.full_name, user.login) for user in list_users]
    await dialog_manager.start(
        state=ViewersSG.PREVIEW,
        show_mode=ShowMode.EDIT,
        mode=StartMode.RESET_STACK,
        data={
            StDataConst.list_viewers.value: users,
            StDataConst.manager_uuid.value: str(user_uuid),
            StDataConst.company_id.value: company_id
        }
    )


async def get_company_report(company_id: int) -> str:
    url = await query.get_report_company(company_id=company_id)
    return url


async def check_attention_project(dialog_manager: DialogManager) -> bool:
    widget_data = dialog_manager.current_context().widget_data
    tg_id = int(dialog_manager.event.from_user.id)
    _, _, _, user_uuid, _, _ = get_session_data(
        tg_id=tg_id,
        dialog_manager=dialog_manager
    )
    list_projects: list[int] = await query.get_projects_ids_by_user_without_direct(user_uuid=user_uuid)
    widget_data[WDataConst.projects_id.value] = list_projects
    return True if list_projects else False


async def attention_project(dialog_manager: DialogManager) -> str:
    widget_data = dialog_manager.current_context().widget_data
    projects_ids = widget_data[WDataConst.projects_id.value]
    projects_title: list[str] = await query.get_projects_title_by_ids(ids=projects_ids)
    return ','.join(projects_title)
