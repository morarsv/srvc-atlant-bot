import logging
from aiogram.types import User
from aiogram_dialog import DialogManager
from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst
from fluentogram import TranslatorRunner
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    preview_text = i18n.atlant.admin.preview() + '\n\n' + i18n.atlant.admin.regenerate.dbt()
    return {
        'preview_text': preview_text,
        'btn_add_company': i18n.button.add.company(),
        'btn_add_user': i18n.button.add.user(),
        'btn_list_company': i18n.button.list.companies(),
        'btn_regenerate_dbt': i18n.button.regenerate.dbt(),
        'btn_back': i18n.button.back()
    }


async def add_user_getter(dialog_manager: DialogManager,
                          i18n: TranslatorRunner,
                          event_from_user: User,
                          **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    companies = widget_data[WgDataConst.companies.value]
    return {
        'preview_text': i18n.atlant.admin.add.user(),
        'companies': companies,
        'btn_back': i18n.button.back()
    }


async def list_company_getter(dialog_manager: DialogManager,
                              i18n: TranslatorRunner,
                              event_from_user: User,
                              **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    companies = widget_data[WgDataConst.companies.value]
    return {
        'preview_text': i18n.atlant.admin.list.companies(),
        'companies': companies,
        'btn_back': i18n.button.back()
    }


async def card_company_getter(dialog_manager: DialogManager,
                              i18n: TranslatorRunner,
                              event_from_user: User,
                              **kwargs):
    widget_data = dialog_manager.current_context().widget_data

    users = widget_data[WgDataConst.users.value]
    projects = widget_data[WgDataConst.projects.value]
    company_name = widget_data[WgDataConst.company_name.value]
    company_id = widget_data[WgDataConst.company_id.value]
    company_created = widget_data[WgDataConst.company_created.value]

    preview_text = i18n.atlant.admin.info.company(
        company_id=company_id,
        company_name=company_name,
        count_users=len(users),
        count_projects=len(projects),
        created_at=company_created
    ) + '\n\n' + i18n.atlant.admin.regenerate.yaml()

    return {
        'preview_text': preview_text,
        'btn_list_users': i18n.button.list.users(),
        'btn_list_projects': i18n.button.list.projects(),
        'btn_regenerate_yaml': i18n.button.regenerate.yaml(),
        'btn_back': i18n.button.back(),
        'users': users,
        'projects': projects
    }


async def list_users_getter(dialog_manager: DialogManager,
                            i18n: TranslatorRunner,
                            event_from_user: User,
                            **kwargs):
    widget_data = dialog_manager.current_context().widget_data

    users = widget_data[WgDataConst.users.value]
    company_name = widget_data[WgDataConst.company_name.value]

    preview_text = i18n.atlant.admin.company.list.users(company_name=company_name)

    return {
        'preview_text': preview_text,
        'btn_back': i18n.button.back(),
        'users': users
    }


async def list_projects_getter(dialog_manager: DialogManager,
                               i18n: TranslatorRunner,
                               event_from_user: User,
                               **kwargs):
    widget_data = dialog_manager.current_context().widget_data

    projects = widget_data[WgDataConst.projects.value]
    company_name = widget_data[WgDataConst.company_name.value]

    preview_text = i18n.atlant.admin.company.list.projects(company_name=company_name)

    return {
        'preview_text': preview_text,
        'btn_back': i18n.button.back(),
        'projects': projects
    }
