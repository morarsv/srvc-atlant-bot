import logging

from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager, ShowMode
from fluentogram import TranslatorRunner
from bot.services.web_reports.utils import get_list_reports
from bot.utils.bot_func import get_session_data
from bot.dialogs.start.handler import check_attention_project, attention_project, get_company_report

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    try:
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    except AttributeError as e:
        dialog_manager.show_mode = ShowMode.SEND
        logger.error(f'Error deleting message: {e}')

    tg_id = int(event_from_user.id)
    username, _, role_id, _, company_id, _ = get_session_data(
        tg_id=tg_id,
        dialog_manager=dialog_manager
    )

    attention: bool = await check_attention_project(dialog_manager=dialog_manager)
    attention_projects = 1 if attention else None
    (atlant_administrator, administrator, manager, viewer, report,
     description_start) = None, None, None, None, None, None

    if role_id == 3:
        atlant_administrator, administrator, manager, report, viewer = 1, 1, 1, 1, 1
        description_start = i18n.start.preview.admin()
    elif role_id == 1:
        administrator, manager, report, viewer = 1, 1, 1, 1
        description_start = i18n.start.preview.admin()
    elif role_id == 2:
        manager, viewer = 1, 1
        description_start = i18n.start.preview.manager()
    elif role_id == 4:
        description_start = i18n.start.preview.viewer()

    if role_id != 4 and attention_projects:
        description_start = f'{description_start}\n\n{i18n.start.project.attention()}' \
            if attention_projects else description_start
    else:
        attention_projects = None

    return {
        'hello_user': i18n.start.preview.hello(username=username),
        'description_start': description_start,
        'btn_to_administrator': i18n.button.to.administrator(),
        'btn_to_project': i18n.button.to.project(),
        'btn_to_atlant_administrator': i18n.button.to.atlant.administrator(),
        'btn_to_viewers': i18n.button.to.viewers(),
        'btn_report_company': i18n.button.report.company(),
        'btn_attention': i18n.button.attention(),
        'attention_project': attention_projects,
        'atlant_administrator': atlant_administrator,
        'administrator': administrator,
        'manager': manager,
        'viewer': viewer,
        'report': report,
    }


async def attention_project_getter(dialog_manager: DialogManager,
                                   i18n: TranslatorRunner,
                                   event_from_user: User,
                                   **kwargs):
    dialog_manager.show_mode = ShowMode.EDIT
    titles = await attention_project(dialog_manager=dialog_manager)
    return {
        'preview_text': i18n.start.project.problem(projects=titles),
        'btn_back': i18n.button.back()
    }


async def company_report_getter(dialog_manager: DialogManager,
                                i18n: TranslatorRunner,
                                event_from_user: User,
                                **kwargs):
    tg_id = int(event_from_user.id)
    _, _, _, _, company_id, _ = get_session_data(
        tg_id=tg_id,
        dialog_manager=dialog_manager
    )
    web_url = get_list_reports()
    link_url = await get_company_report(company_id=company_id)
    return {
        'preview_text': i18n.start.company.report(),
        'btn_web_url': i18n.button.report.web.url(),
        'btn_link_url': i18n.button.report.link.url(),
        'web_url': web_url,
        'link_url': link_url,
        'btn_back': i18n.button.back()
    }
