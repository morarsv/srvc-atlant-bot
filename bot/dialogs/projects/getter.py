import logging
from aiogram.types import User
from aiogram_dialog import DialogManager, ShowMode
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst)
from fluentogram import TranslatorRunner
from typing import TYPE_CHECKING
from bot.services.web_reports.utils import get_project_report
from bot.services.yandex.utils import get_url_ya_access
from bot.lexicon.lexicon_ya import LEXICON_SYSTEM_ID, LEXICON_URL
from bot.dialogs.projects.handler import update_project_data, get_list_projects

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    start_data = dialog_manager.start_data

    projects = await get_list_projects(
        dialog_manager=dialog_manager,
        event_from_user=event_from_user
    )
    role_id = start_data[StDataConst.user_role_id.value]

    try:
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    except AttributeError as e:
        dialog_manager.show_mode = ShowMode.SEND
        logger.error(f'Error deleting message: {e}')
    if role_id != 4:
        access = 1
        preview_text = i18n.project.preview.manager()
    else:
        access = None
        preview_text = i18n.project.preview.viewer.fill() if projects else i18n.project.preview.viewer.empty()

    return {
        'preview_text': preview_text,
        'btn_list_projects': i18n.button.list.projects(),
        'btn_add_project': i18n.button.add.project(),
        'btn_back': i18n.button.back(),
        'projects': projects,
        'access': access
    }


async def list_projects_getter(dialog_manager: DialogManager,
                               i18n: TranslatorRunner,
                               event_from_user: User,
                               **kwargs):
    projects = await get_list_projects(
        dialog_manager=dialog_manager,
        event_from_user=event_from_user
    )

    preview_text = i18n.project.list.projects()
    return {
        'preview_text': preview_text,
        'btn_back': i18n.button.back(),
        'projects': projects,
    }


async def info_project_getter(dialog_manager: DialogManager,
                              i18n: TranslatorRunner,
                              event_from_user: User,
                              **kwargs):
    start_data = dialog_manager.start_data
    try:
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    except AttributeError as e:
        dialog_manager.show_mode = ShowMode.SEND
        logger.error(f'Error deleting message: {e}')
    role_id = start_data[StDataConst.user_role_id.value]

    project_id, project_title, project_description, ya_counters, ya_logins, url_link = await update_project_data(
        dialog_manager=dialog_manager
    )

    project_url = get_project_report(project_id=project_id)

    preview_text = i18n.project.info.about.project(
        title=project_title,
        description=project_description
    )

    if ya_counters:
        preview_text = (f'{preview_text}\n'
                        f'\n{i18n.project.info.ya.counters(counters=ya_counters)}')
    if ya_logins:
        preview_text = (f'{preview_text}\n'
                        f'\n{i18n.project.info.ya.logins(logins=ya_logins)}')

    logins = 1 if ya_logins else None
    access, logins = (1, logins) if role_id != 4 else (None, None)
    return {
        'preview_text': preview_text,
        'btn_get_url_report': i18n.button.url.report(),
        'btn_report_project': i18n.button.report.project(),
        'btn_settings_ya_logins': i18n.button.settings.logins(),
        'btn_list_ya_counters': i18n.button.list.ya.counters(),
        'btn_add_service': i18n.button.add.service(),
        'btn_edit': i18n.button.edit.object(),
        'btn_back': i18n.button.back(),
        'project_url_link': url_link,
        'report_url': project_url,
        'counters': ya_counters,
        'logins': logins,
        'access': access
    }


async def add_service_getter(dialog_manager: DialogManager,
                             i18n: TranslatorRunner,
                             event_from_user: User,
                             **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data
    try:
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    except AttributeError as e:
        dialog_manager.show_mode = ShowMode.SEND
        logger.error(f'Error deleting message: {e}')
    preview_text = i18n.project.add.services.project()

    access_direct = widget_data.get(WgDataConst.ya_access_direct.value,
                                    start_data.get(StDataConst.ya_access_direct.value))
    access_metrika = widget_data.get(WgDataConst.ya_access_metrika.value,
                                     start_data.get(StDataConst.ya_access_metrika.value))
    counters = widget_data.get(WgDataConst.project_connected_counters.value, None)

    metrika_in = 1 if access_metrika else None
    direct_in = 1 if access_direct else None

    project_id = widget_data.get(WgDataConst.project_id.value,
                                 start_data.get(StDataConst.project_id.value))
    ya_direct_url = get_url_ya_access(p_id=project_id,
                                      system_id=LEXICON_SYSTEM_ID['YA_DIRECT'],
                                      scope=LEXICON_URL['SCOPE_DIRECT'])
    ya_metrika_url = get_url_ya_access(p_id=project_id,
                                       system_id=LEXICON_SYSTEM_ID['YA_METRIKA'],
                                       scope=LEXICON_URL['SCOPE_METRIKA'])

    btn_add_ya_counters = i18n.button.list.ya.counters() if counters else i18n.button.add.ya.counters()
    return {
        'preview_text': preview_text,
        'btn_update_status': i18n.button.update.status(),
        'btn_add_ya_logins': i18n.button.add.ya.logins(),
        'btn_add_ya_counters': btn_add_ya_counters,
        'btn_ya_direct_access': i18n.button.ya.access.direct(),
        'btn_ya_metrika_access': i18n.button.ya.access.metrika(),
        'btn_back': i18n.button.back(),
        'metrika_in': metrika_in,
        'direct_in': direct_in,
        'ya_direct_url': ya_direct_url,
        'ya_metrika_url': ya_metrika_url
    }


async def ya_access_getter(dialog_manager: DialogManager,
                           i18n: TranslatorRunner,
                           event_from_user: User,
                           **kwargs):
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    project_id = widget_data.get(WgDataConst.project_id.value,
                                 start_data.get(StDataConst.project_id.value))
    ya_direct_url = get_url_ya_access(p_id=project_id,
                                      system_id=LEXICON_SYSTEM_ID['YA_DIRECT'],
                                      scope=LEXICON_URL['SCOPE_DIRECT'])
    ya_metrika_url = get_url_ya_access(p_id=project_id,
                                       system_id=LEXICON_SYSTEM_ID['YA_METRIKA'],
                                       scope=LEXICON_URL['SCOPE_METRIKA'])

    link = ya_metrika_url if widget_data[WgDataConst.selected_metrika.value] else ya_direct_url

    logger.info(f'Link authorize: {link}')
    return {
        'preview_text': i18n.project.ya.access(),
        'btn_open_browser': i18n.button.ya.access.open.web.browser(),
        'btn_open_tg_web': i18n.button.ya.access.open.tg.web(),
        'btn_back': i18n.button.back(),
        'link': link
    }
