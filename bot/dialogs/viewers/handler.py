import asyncio
import logging
from uuid import UUID
from typing import Any, TYPE_CHECKING
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from bot.database.models import Users, Projects, ProjectUser
from bot.database import query
from bot.state.dialog_state import ViewersSG, ViewersAddUserSG, StartSG
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            PoolingConstant as poolConst)
from bot.services.web_reports.utils import (web_set_user_to_project,
                                            web_delete_viewer, web_remove_user_from_project)
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        show_mode=ShowMode.EDIT,
        mode=StartMode.RESET_STACK,
        state=StartSG.PREVIEW
    )


async def btn_add_user(callback: CallbackQuery,
                       button: Button,
                       dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data
    await dialog_manager.start(state=ViewersAddUserSG.INPUT_USERNAME,
                               mode=StartMode.NORMAL,
                               data={
                                   StDataConst.manager_uuid.value: start_data[StDataConst.manager_uuid.value],
                                   StDataConst.company_id.value: start_data[StDataConst.company_id.value]
                               })


async def btn_list_viewers(callback: CallbackQuery,
                           button: Button,
                           dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    user_id = start_data[StDataConst.manager_uuid.value]
    list_users: list[Users] = await query.get_viewers_by_manager_id(manager_id=UUID(user_id))
    users = [(user.full_name, user.login) for user in list_users]
    widget_data[WgDataConst.manager_uuid.value] = user_id
    widget_data[WgDataConst.list_viewers.value] = users
    await dialog_manager.switch_to(
        state=ViewersSG.LIST_VIEWERS,
        show_mode=ShowMode.EDIT
    )


async def btn_switch_to_viewer(callback: CallbackQuery,
                               widget: Any,
                               dialog_manager: DialogManager,
                               selected_item: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    login = selected_item
    manager_uuid: UUID = UUID(widget_data[WgDataConst.manager_uuid.value])
    viewer: Users = await query.get_user_by_login(login=login)

    connected_projects: list[Projects] = await query.get_list_projects_by_user_uuid(user_uuid=viewer.id)
    available_projects: list[Projects] = await query.get_available_projects_for_viewer(
        manager_uuid=manager_uuid,
        viewer_uuid=viewer.id,
    )
    connected_projects_list = [(project.title, project.id) for project in connected_projects]
    available_projects_list = [(project.title, project.id) for project in available_projects]

    widget_data[WgDataConst.viewer_connected_list_projects.value] = connected_projects_list
    widget_data[WgDataConst.viewer_available_list_projects.value] = available_projects_list
    widget_data[WgDataConst.viewer_uuid.value] = str(viewer.id)
    widget_data[WgDataConst.viewer_login.value] = viewer.login
    widget_data[WgDataConst.viewer_username.value] = viewer.full_name
    await dialog_manager.switch_to(state=ViewersSG.INFO_VIEWER,
                                   show_mode=ShowMode.EDIT)


async def btn_delete_viewer(callback: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    user_uuid = UUID(str(widget_data[WgDataConst.viewer_uuid.value]))
    await query.delete_viewer_by_id(user_id=user_uuid)
    await web_delete_viewer(
        logger=logger,
        user_id=str(user_uuid),
        callback=callback
    )
    login = [WgDataConst.viewer_login.value]
    list_viewers = widget_data[WgDataConst.list_viewers.value]
    list_viewers = [viewer for viewer in list_viewers if viewer[1] != login]
    widget_data[StDataConst.list_viewers.value] = list_viewers
    await dialog_manager.switch_to(
        state=ViewersSG.PREVIEW,
        show_mode=ShowMode.EDIT
    )


async def btn_set_project(callback: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.status_set_project.value] = True
    widget_data[WgDataConst.status_remove_project.value] = False
    widget_data[WgDataConst.list_projects.value] = widget_data[WgDataConst.viewer_available_list_projects.value]
    await dialog_manager.switch_to(state=ViewersSG.LIST_PROJECTS,
                                   show_mode=ShowMode.EDIT)


async def btn_remove_project(callback: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.status_set_project.value] = False
    widget_data[WgDataConst.status_remove_project.value] = True
    widget_data[WgDataConst.list_projects.value] = widget_data[WgDataConst.viewer_connected_list_projects.value]
    await dialog_manager.switch_to(state=ViewersSG.LIST_PROJECTS,
                                   show_mode=ShowMode.EDIT)


async def btn_confirm(callback: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    i18n: TranslatorRunner = middleware_data[poolConst.i18n.value]
    user_uuid = str(widget_data[WgDataConst.viewer_uuid.value])
    list_projects = widget_data[WgDataConst.projects_id.value]
    status_set = widget_data[WgDataConst.status_set_project.value]
    status_remove = widget_data[WgDataConst.status_remove_project.value]
    requests = []
    requests_web = []
    if status_set:
        for project_id in list_projects:
            project_user = ProjectUser()
            project_user.user_id = UUID(user_uuid)
            project_user.project_id = int(project_id)
            requests.append(query.set_user_to_project(project_user=project_user))
            requests_web.append(web_set_user_to_project(
                logger=logger,
                project_id=int(project_id),
                user_id=str(user_uuid),
                callback=callback
            ))
    if status_remove:
        for project_id in list_projects:
            requests.append(query.remove_user_from_project(project_id=int(project_id),
                                                           user_uuid=UUID(user_uuid)))
            requests_web.append(web_remove_user_from_project(
                logger=logger,
                project_id=int(project_id),
                user_id=user_uuid,
                callback=callback
            ))
    await asyncio.gather(*requests)
    await asyncio.gather(*requests_web)
    await callback.answer(i18n.successfully.updated())

    widget_data[WgDataConst.projects_id.value] = []

    login = widget_data[WgDataConst.viewer_login.value]
    manager_uuid: UUID = UUID(str(widget_data[WgDataConst.manager_uuid.value]))
    viewer: Users = await query.get_user_by_login(login=login)

    connected_projects: list[Projects] = await query.get_list_projects_by_user_uuid(user_uuid=viewer.id)
    available_projects: list[Projects] = await query.get_available_projects_for_viewer(
        manager_uuid=manager_uuid,
        viewer_uuid=viewer.id,
    )
    connected_projects_list = [(project.title, project.id) for project in connected_projects]
    available_projects_list = [(project.title, project.id) for project in available_projects]

    widget_data[WgDataConst.viewer_connected_list_projects.value] = connected_projects_list
    widget_data[WgDataConst.viewer_available_list_projects.value] = available_projects_list

    await dialog_manager.switch_to(state=ViewersSG.INFO_VIEWER,
                                   show_mode=ShowMode.EDIT)


async def back_from_projects(callback: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.projects_id.value] = []
