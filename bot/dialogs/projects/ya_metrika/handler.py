import logging

from typing import TYPE_CHECKING, Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner
from bot.database import query
from bot.services.yandex.utils import get_ya_counters
from bot.database.models import YandexAccesses, Projects, YaMetrikaCounters
from bot.lexicon.lexicon_ya import LEXICON_SYSTEM_ID, LEXICON_ATTRIBUTION
from bot.state.dialog_state import YaMetrikaCountersEditAddSG, YaMetrikaCountersSG
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            PoolingConstant as poolConst)
from bot.services.airflow.dags_generator.dag_func import generate_dag
from bot.services.airflow.utils import set_active_dag
from bot.utils.bot_func import alert_msg_to_chat
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)

_chat_alert_id = LEXICON_TG_BOT['CHAT_ID_ACC_ALERTS']


async def btn_switch_to_counter(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        selected_item: str) -> None:
    start_data = dialog_manager.start_data

    role_id = start_data[StDataConst.user_role_id.value]
    project_id = start_data[StDataConst.project_id.value]
    project_title = start_data[StDataConst.project_title.value]
    counter_id = int(selected_item)

    list_counters: list[YaMetrikaCounters] = await query.get_ya_m_list_counters_by_p_id(project_id=project_id)
    counters = [(f'{c.counter_name}:{c.counter_id}', c.id) for c in list_counters]
    start_data[StDataConst.ya_metrika_counters.value] = counters

    counter: YaMetrikaCounters = await query.get_ya_m_counter_by_id(counter_id=counter_id)
    m_attribution = counter.minor_attribution or 'None'
    k_goals_names = '\n'.join(counter.names_key_goals)
    names_minor_goals = counter.names_minor_goals
    m_goals_names = ('\n'.join(names_minor_goals)) if counter.names_minor_goals else 'None'
    await dialog_manager.start(state=YaMetrikaCountersEditAddSG.PREVIEW,
                               show_mode=ShowMode.EDIT,
                               mode=StartMode.NORMAL,
                               data={
                                   StDataConst.status_old_obj.value: True,
                                   StDataConst.user_role_id.value: role_id,
                                   StDataConst.project_id.value: project_id,
                                   StDataConst.project_counter_id.value: counter.id,
                                   StDataConst.project_title.value: project_title,
                                   StDataConst.counter_attribution.value: counter.attribution,
                                   StDataConst.counter_minor_attribution.value: m_attribution,
                                   StDataConst.counter_name.value: counter.counter_name,
                                   StDataConst.counter_id.value: counter.counter_id,
                                   StDataConst.counter_k_goals.value: k_goals_names,
                                   StDataConst.counter_m_goals.value: m_goals_names,
                                   StDataConst.counter_ecommerce.value: counter.ecommerce
                               })


async def btn_edit_attribution(callback: CallbackQuery,
                               button: Button,
                               dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data

    attribution = [(v, k) for k, v in LEXICON_ATTRIBUTION.items()]
    widget_data[WgDataConst.list_attributions.value] = attribution
    widget_data[WgDataConst.counter_attribution.value] = []
    widget_data[WgDataConst.counter_minor_attribution.value] = []
    await dialog_manager.switch_to(
        state=YaMetrikaCountersSG.KEY_ATTRIBUTION,
        show_mode=ShowMode.EDIT
    )


async def btn_add_metrika(callback: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data

    project_id = start_data[StDataConst.project_id.value]
    project_title = start_data[StDataConst.project_title.value]
    counters = start_data[StDataConst.ya_metrika_counters.value]
    role_id = start_data[StDataConst.user_role_id.value]
    attribution = start_data[StDataConst.counter_attribution.value]
    minor_attribution = start_data[StDataConst.counter_minor_attribution.value] or 'None'

    ya_accesses: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_METRIKA']
    )
    list_counters = await get_ya_counters(
        oauth_token=ya_accesses.access_token,
        logger=logger
    )
    counters = [counter[0] for counter in counters]
    list_counters = [counter for counter in list_counters if counter[0] not in counters]
    await dialog_manager.start(
        state=YaMetrikaCountersEditAddSG.COUNTERS,
        show_mode=ShowMode.EDIT,
        mode=StartMode.NORMAL,
        data={
            StDataConst.user_role_id.value: role_id,
            StDataConst.counter_attribution.value: attribution,
            StDataConst.counter_minor_attribution.value: minor_attribution,
            StDataConst.project_title.value: project_title,
            StDataConst.project_id.value: project_id,
            StDataConst.list_counters.value: list_counters
        }
    )


async def selected_attribution(callback: CallbackQuery,
                               button: Button,
                               dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    selected = widget_data[WgDataConst.counter_attribution.value][0]
    attribution = [(v, k) for k, v in LEXICON_ATTRIBUTION.items() if k != selected]
    widget_data[WgDataConst.counter_attribution.value] = LEXICON_ATTRIBUTION.get(selected)
    widget_data[WgDataConst.list_attributions.value] = attribution


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_confirm(callback: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data
    middleware_data = dialog_manager.middleware_data

    i18n: TranslatorRunner = middleware_data[poolConst.i18n.value]

    project_id = start_data[StDataConst.project_id.value]
    attribution = widget_data[WgDataConst.counter_attribution.value]
    minor_attribution = widget_data.get(WgDataConst.counter_minor_attribution.value, None)

    minor_attribution = LEXICON_ATTRIBUTION.get(minor_attribution[0]) if minor_attribution else None
    start_data[StDataConst.counter_attribution.value] = attribution
    start_data[StDataConst.counter_minor_attribution.value] = minor_attribution
    try:
        await query.set_ya_metrik_attribution(
            p_id=project_id,
            attribution=attribution,
            minor_attribution=minor_attribution
        )
        await callback.answer(i18n.successfully.added())
    except Exception as e:
        await callback.answer(i18n.unsuccessfully.updated())
        logger.error(f'Error with database: {e}')
    project: Projects = await query.get_project_by_id(project_id=project_id)
    title = project.title
    company_name = project.company.company
    start_date: str = str(project.created_at)
    try:
        await generate_dag(logger=logger,
                           project_title=title,
                           project_id=project_id,
                           company_name=company_name,
                           start_date=start_date,
                           callback=callback)
    except Exception as e:
        logger.exception(f"Ошибка при генерации дага на стророне микросервиса: {e}")
    await set_active_dag(
        logger=logger,
        company=company_name,
        project_id=str(project_id),
        company_id=str(project.company_id),
        created_date=start_date,
        i18n=i18n,
        callback=callback
    )
    widget_data[WgDataConst.counter_attribution.value] = []
    widget_data[WgDataConst.counter_minor_attribution.value] = []
    await alert_msg_to_chat(chat_id=_chat_alert_id,
                            callback=callback,
                            msg=i18n.alert.edited.ya.metrika.counter.attr(
                                title=title,
                                company=company_name
                            ),
                            logger=logger)
    await dialog_manager.switch_to(
        state=YaMetrikaCountersSG.PREVIEW,
        show_mode=ShowMode.EDIT
    )
