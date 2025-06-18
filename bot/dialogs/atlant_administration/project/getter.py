import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager

from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst)

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    start_data = dialog_manager.start_data

    project_id = start_data[StDataConst.project_id.value]
    project_title = start_data[StDataConst.project_title.value]

    company_name = start_data[StDataConst.company_name.value]
    project_author = start_data[StDataConst.project_author.value]
    project_created = start_data[StDataConst.project_created.value]
    project_managers = start_data[StDataConst.project_managers.value]
    project_description = start_data[StDataConst.project_description.value]

    ya_logins = start_data[StDataConst.project_ya_direct_logins.value]
    ya_counters = start_data[StDataConst.project_ya_metrika_counters.value]

    ya_counters, counters = (ya_counters, 1) if ya_counters != 'None' else ('-', None)
    ya_logins = ya_logins if ya_logins != 'None' else '-'

    preview_text = i18n.atlant.admin.info.project(
        project_id=project_id,
        project_title=project_title,
        project_description=project_description,
        ya_logins=ya_logins,
        ya_counters=ya_counters,
        company_name=company_name,
        author=project_author,
        created_at=project_created,
        managers=project_managers
    )

    return {
        'preview_text': preview_text,
        'btn_counters_list': i18n.button.list.ya.counters(),
        'btn_back': i18n.button.back(),
        'counters': counters
    }


async def list_counters_getter(dialog_manager: DialogManager,
                               i18n: TranslatorRunner,
                               event_from_user: User,
                               **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    project_ya_counters_list = widget_data[WgDataConst.project_list_counters.value]
    preview_text = i18n.project.list.metrika()
    return {
        'preview_text': preview_text,
        'counters': project_ya_counters_list,
        'btn_back': i18n.button.back()
    }


async def counter_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    project_title = start_data[StDataConst.project_title.value]
    attribution = widget_data[WgDataConst.counter_attribution.value]
    minor_attribution = widget_data[WgDataConst.counter_minor_attribution.value]
    counter_name = widget_data[WgDataConst.counter_name.value]
    counter_id = widget_data[WgDataConst.counter_id.value]
    k_goals = widget_data[WgDataConst.counter_k_goals.value]
    m_goals = widget_data[WgDataConst.counter_m_goals.value]
    ecommerce = widget_data[WgDataConst.counter_ecommerce.value]

    preview_text = i18n.atlant.admin.info.counter(
        project_title=project_title,
        attribution=attribution,
        minor_attribution=minor_attribution,
        counter=counter_name,
        counter_id=counter_id,
        k_goals=k_goals,
        m_goals=m_goals,
        ecommerce=ecommerce
    )

    return {
        'preview_text': preview_text,
        'btn_back': i18n.button.back()
    }
