import logging
from typing import Any, TYPE_CHECKING
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from bot.state.dialog_state import (CompanyAdminProjectsSG,
                                    CompanyAdminAddEditUserSG, StartSG)
from bot.database.models import Users, Projects
from bot.database import query
from bot.lexicon.constants.constant import (PoolingConstant as poolConst,
                                            StartDataConstant as StDataConst)
from bot.support_models.models import SupportSessionUser
from bot.services.web_reports.utils import web_logout_from_sessions
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


logger = logging.getLogger(__name__)


async def btn_add_user(callback: CallbackQuery,
                       button: Button,
                       dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        state=CompanyAdminAddEditUserSG.INPUT_USERNAME,
        mode=StartMode.NORMAL,
        show_mode=ShowMode.EDIT
    )


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        state=StartSG.PREVIEW,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT
    )


async def btn_logout_frm_sessions(callback: CallbackQuery,
                                  button: Button,
                                  dialog_manager: DialogManager) -> None:
    middleware_data = dialog_manager.middleware_data
    tg_id = int(callback.from_user.id)
    i18n: TranslatorRunner = middleware_data[poolConst.i18n.value]
    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    user: SupportSessionUser = online_users.get(tg_id)
    user_uuid = user.get('user_uuid')
    login = user.get('login')
    try:
        await web_logout_from_sessions(
            logger=logger,
            user_uuid=str(user_uuid),
            login=login,
            callback=callback
        )
    except:
        await callback.answer(text=i18n.unsuccessfully.updated())
    else:
        await callback.answer(text=i18n.successfully.updated())


async def btn_switch_to_user(callback: CallbackQuery,
                             widget: Any,
                             dialog_manager: DialogManager,
                             selected_item: str) -> None:
    user_login = selected_item

    user: Users = await query.get_user_by_login(login=user_login)

    username = user.full_name
    role_id = user.role_id
    role = user.role.role
    login = user.login
    company_id = user.company_id
    password = user.password
    user_uuid = str(user.id)

    await dialog_manager.start(
        state=CompanyAdminAddEditUserSG.PREVIEW,
        mode=StartMode.NORMAL,
        show_mode=ShowMode.EDIT,
        data={
            StDataConst.user_edit.value: True,
            StDataConst.username.value: username,
            StDataConst.user_uuid.value: user_uuid,
            StDataConst.user_role.value: role,
            StDataConst.user_login.value: login,
            StDataConst.company_id.value: company_id,
            StDataConst.user_role_id.value: role_id,
            StDataConst.user_password.value: password
        }
    )


async def btn_switch_to_project(callback: CallbackQuery,
                                widget: Any,
                                dialog_manager: DialogManager,
                                selected_item: str) -> None:
    middleware_data = dialog_manager.middleware_data
    tg_id = int(callback.from_user.id)
    project_id = int(selected_item)

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    user: SupportSessionUser = online_users.get(tg_id)
    company_id: int = int(user.get('company_id'))
    project: Projects = await query.get_project_by_id(project_id=project_id)

    list_counters: list[str] = await query.get_ya_m_counters_names_by_p_id(p_id=project_id)
    list_logins: list[str] = await query.get_ya_d_logins_names_by_p_id(p_id=project_id)
    list_connected_managers: list[Users] = await query.get_list_managers_by_p_id(project_id=project_id)
    list_available_managers: list[Users] = await query.get_available_managers_by_p_id(project_id=project_id,
                                                                                      company_id=company_id)

    available_managers = [(manager.full_name, manager.login) for manager in list_available_managers] if \
        list_available_managers else 'None'
    connected_managers = [(manager.full_name, manager.login) for manager in list_connected_managers] if \
        list_connected_managers else 'None'
    managers_list = [manager[0] for manager in connected_managers] if list_connected_managers else None

    ya_counters = ', '.join(list_counters) if list_counters else 'None'
    ya_logins = ', '.join(list_logins) if list_logins else 'None'
    managers = ', '.join(managers_list) if list_connected_managers else 'None'

    await dialog_manager.start(
        state=CompanyAdminProjectsSG.PREVIEW,
        show_mode=ShowMode.EDIT,
        mode=StartMode.NORMAL,
        data={
            StDataConst.project_id.value: project_id,
            StDataConst.project_title.value: project.title,
            StDataConst.project_description.value: project.description,
            StDataConst.project_ya_direct_logins.value: ya_logins,
            StDataConst.project_ya_metrika_counters.value: ya_counters,
            StDataConst.project_managers.value: managers,
            StDataConst.available_managers.value: available_managers,
            StDataConst.connected_managers.value: connected_managers
        }
    )
