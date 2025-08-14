import asyncio
import logging
from typing import TYPE_CHECKING
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from fluentogram import TranslatorRunner
from bot.database import query
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            StartDataConstant as StDataConst,
                                            PoolingConstant as poolConst)
from bot.lexicon.lexicon_ya import LEXICON_SYSTEM_ID, LEXICON_ATTRIBUTION
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from bot.services.yandex.utils import get_ya_goals, get_ya_counters
from bot.database.models import YandexAccesses, YaMetrikaCounters, Projects
from bot.state.dialog_state import YaMetrikaCountersEditAddSG, ProjectsSG
from bot.services.airflow.utils import create_connection_metrika
from bot.services.msvc.generator import func
from bot.utils.bot_func import bot_current_time, get_session_data, alert_msg_to_chat

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner
logger = logging.getLogger(__name__)

_chat_alert_id = LEXICON_TG_BOT['CHAT_ID_ACC_ALERTS']


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    widget_data[WgDataConst.status_edit_counter.value] = False
    await dialog_manager.switch_to(
        state=YaMetrikaCountersEditAddSG.PREVIEW,
        show_mode=ShowMode.EDIT
    )


async def btn_cancel(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_ecommerce_to_preview(callback: CallbackQuery,
                                   button: Button,
                                   dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    selected_ecommerce = widget_data[WgDataConst.selected_counter_ecommerce.value][0]
    widget_data[WgDataConst.counter_ecommerce.value] = int(selected_ecommerce)
    widget_data[WgDataConst.status_edit_counter.value] = True


async def btn_edit_counter(callback: CallbackQuery,
                           button: Button,
                           dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data
    widget_data = dialog_manager.current_context().widget_data

    counter_id = int(widget_data[WgDataConst.counter_id.value])
    project_id = start_data[StDataConst.project_id.value]
    ya_accesses: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_METRIKA']
    )

    counters = await get_ya_counters(
        oauth_token=ya_accesses.access_token,
        logger=logger
    )
    counters_id: list[int] = await query.get_ya_m_counters_id_by_p_id(p_id=project_id)
    if counters_id:
        counters_id.remove(counter_id)
        counters = [counter for counter in counters if counter[1] not in counters_id]

    start_data[StDataConst.list_counters.value] = counters
    widget_data[WgDataConst.selected_counter_id.value] = []
    widget_data[WgDataConst.status_edit_counter.value] = True

    await dialog_manager.switch_to(
        state=YaMetrikaCountersEditAddSG.COUNTERS,
        show_mode=ShowMode.EDIT
    )


async def btn_counter_to_attribution(callback: CallbackQuery,
                                     button: Button,
                                     dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data

    project_id = int(start_data[StDataConst.project_id.value])
    list_counters = start_data[StDataConst.list_counters.value]
    status_first = start_data.get(StDataConst.status_first.value, False)

    selected_counter_id = widget_data[WgDataConst.selected_counter_id.value][0]
    counter = next((counter for counter in list_counters if str(counter[1]) == selected_counter_id), None)
    counter_id = int(counter[1])
    widget_data[WgDataConst.counter_id.value] = counter_id
    counter_name = counter[0].split(':')[0]
    widget_data[WgDataConst.counter_name.value] = counter_name

    ya_accesses: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_METRIKA']
    )
    k_goals = await get_ya_goals(oauth_token=ya_accesses.access_token,
                                 counter_id=counter_id,
                                 logger=logger)
    widget_data[WgDataConst.list_k_goals.value] = k_goals

    widget_data[WgDataConst.status_edit_counter.value] = False
    widget_data[WgDataConst.selected_attribution.value] = []
    widget_data[WgDataConst.selected_minor_attribution.value] = []
    widget_data[WgDataConst.selected_counter_k_goals_id.value] = []
    widget_data[WgDataConst.selected_counter_m_goals_id.value] = []
    widget_data[WgDataConst.selected_counter_ecommerce.value] = []

    if status_first:
        attribution = [(v, k) for k, v in LEXICON_ATTRIBUTION.items()]
        widget_data[WgDataConst.list_attributions.value] = attribution
        widget_data[WgDataConst.counter_attribution.value] = []
        widget_data[WgDataConst.counter_minor_attribution.value] = []
        await dialog_manager.switch_to(show_mode=ShowMode.EDIT,
                                       state=YaMetrikaCountersEditAddSG.ATTRIBUTION)
    else:
        widget_data[WgDataConst.counter_attribution.value] = start_data[StDataConst.counter_attribution.value]
        widget_data[WgDataConst.counter_minor_attribution.value] = start_data[
            StDataConst.counter_minor_attribution.value]
        await dialog_manager.switch_to(state=YaMetrikaCountersEditAddSG.KEY_GOALS,
                                       show_mode=ShowMode.EDIT)


async def btn_attribution_to_minor_attribution(callback: CallbackQuery,
                                               button: Button,
                                               dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    selected_attribution = widget_data[WgDataConst.selected_attribution.value][0]
    attribution = [(v, k) for k, v in LEXICON_ATTRIBUTION.items() if k != selected_attribution]
    widget_data[WgDataConst.list_m_attributions.value] = attribution
    widget_data[WgDataConst.counter_attribution.value] = LEXICON_ATTRIBUTION.get(selected_attribution)


async def btn_minor_attribution_to_k_goals(callback: CallbackQuery,
                                           button: Button,
                                           dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data

    selected_minor_attribution = widget_data.get(WgDataConst.selected_minor_attribution.value, None)
    if selected_minor_attribution:
        selected_minor_attribution = selected_minor_attribution[0]
        widget_data[WgDataConst.counter_minor_attribution.value] = LEXICON_ATTRIBUTION.get(selected_minor_attribution)
    else:
        widget_data[WgDataConst.counter_minor_attribution.value] = 'None'


async def btn_k_goals_to_minor_goals(callback: CallbackQuery,
                                     button: Button,
                                     dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data

    k_goals_list = widget_data[WgDataConst.list_k_goals.value]
    selected_k_goals = widget_data[WgDataConst.selected_counter_k_goals_id.value]

    selected_k_goals_names = list(
        goal for goal in k_goals_list if str(goal[1]) in selected_k_goals
    )
    widget_data[WgDataConst.selected_counter_k_goals_names.value] = selected_k_goals_names
    k_goals = [goal[0] for goal in selected_k_goals_names]
    widget_data[WgDataConst.counter_k_goals.value] = '\n'.join(k_goals)

    m_goals_list = list(goals for goals in k_goals_list if str(goals[1]) not in selected_k_goals)
    widget_data[WgDataConst.list_m_goals.value] = m_goals_list

    await dialog_manager.next(show_mode=ShowMode.EDIT)


async def btn_back_from_k_goals(callback: CallbackQuery,
                                button: Button,
                                dialog_manager: DialogManager) -> None:
    start_data = dialog_manager.start_data

    status_first = start_data.get(StDataConst.status_first.value, False)
    if status_first:
        await dialog_manager.back(show_mode=ShowMode.EDIT)
    else:
        await dialog_manager.switch_to(state=YaMetrikaCountersEditAddSG.COUNTERS,
                                       show_mode=ShowMode.EDIT)


async def next_m_goals_to_ecommerce(callback: CallbackQuery,
                                    button: Button,
                                    dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    selected_m_goals = widget_data.get(WgDataConst.selected_counter_m_goals_id.value, None)
    if selected_m_goals:
        list_m_goals = widget_data[WgDataConst.list_m_goals.value]

        selected_m_goals_names = list(
            goal for goal in list_m_goals if str(goal[1]) in selected_m_goals
        )
        widget_data[WgDataConst.selected_counter_m_goals_names.value] = selected_m_goals_names

        m_goals = [goal[0] for goal in selected_m_goals_names]
        widget_data[WgDataConst.counter_m_goals.value] = '\n'.join(m_goals)
    else:
        widget_data[WgDataConst.counter_m_goals.value] = 'None'


async def btn_confirm(callback: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    start_data = dialog_manager.start_data
    middleware_data = dialog_manager.middleware_data
    status_first = start_data.get(StDataConst.status_first.value, False)
    status_old_object = widget_data.get(WgDataConst.status_old_obj.value, False)
    project_id = int(start_data[StDataConst.project_id.value])
    i18n: TranslatorRunner = middleware_data[poolConst.i18n.value]

    tg_id = int(callback.from_user.id)
    _, _, role_id, user_uuid, company_id, company_name = get_session_data(tg_id=tg_id,
                                                                          dialog_manager=dialog_manager)

    counter_id = widget_data[WgDataConst.counter_id.value]
    counter_name = widget_data[WgDataConst.counter_name.value]
    counter_attribution = widget_data[WgDataConst.counter_attribution.value]
    counter_minor_attribution = widget_data[WgDataConst.counter_minor_attribution.value] if \
        widget_data[WgDataConst.counter_minor_attribution.value] != 'None' else None

    selected_k_goals_names = widget_data[WgDataConst.selected_counter_k_goals_names.value]
    selected_k_goals_id = widget_data[WgDataConst.selected_counter_k_goals_id.value]
    k_goals_id = [int(goal) for goal in selected_k_goals_id]
    k_goals_names = [goal[0] for goal in selected_k_goals_names]

    selected_m_goals = widget_data.get(WgDataConst.selected_counter_m_goals_id.value, None)
    if selected_m_goals:
        selected_m_goals_names = widget_data[WgDataConst.selected_counter_m_goals_names.value]
        selected_m_goals_id = widget_data[WgDataConst.selected_counter_m_goals_id.value]
        m_goals_id = [int(goal) for goal in selected_m_goals_id]
        m_goals_names = [goal[0] for goal in selected_m_goals_names]
    else:
        m_goals_id = None
        m_goals_names = None

    counter_ecommerce = widget_data[WgDataConst.counter_ecommerce.value]

    ya_counter: YaMetrikaCounters = YaMetrikaCounters()
    ya_counter.project_id = project_id
    ya_counter.counter_name = counter_name
    ya_counter.counter_id = counter_id
    ya_counter.attribution = counter_attribution
    ya_counter.minor_attribution = counter_minor_attribution
    ya_counter.names_key_goals = k_goals_names
    ya_counter.names_minor_goals = m_goals_names
    ya_counter.key_goals = k_goals_id
    ya_counter.minor_goals = m_goals_id
    ya_counter.ecommerce = counter_ecommerce

    ya_accesses: YandexAccesses = await query.get_ya_accesses_by_project_and_system_id(
        p_id=project_id,
        s_id=LEXICON_SYSTEM_ID['YA_METRIKA']
    )
    project: Projects = await query.get_project_by_id(project_id=project_id)
    project_title: str = project.title
    start_date: str = str(project.created_at)
    time: str = await bot_current_time()

    await create_connection_metrika(logger=logger,
                                    project_title=project_title,
                                    metrika=ya_counter,
                                    access_token=ya_accesses.access_token,
                                    chat_id=LEXICON_TG_BOT['CHAT_ID_ERR_REPORT'],
                                    i18n=i18n,
                                    callback=callback,
                                    time=time)

    if status_first:
        await alert_msg_to_chat(chat_id=_chat_alert_id,
                                msg=i18n.alert.added.ya.metrika.counters(
                                    title=project_title,
                                    company=company_name,
                                    ya_counter=counter_name
                                ),
                                logger=logger)
        await query.add_ya_metrik_counter(ya_metrika_counter=ya_counter)
    elif status_old_object:
        metrika_counter_id = int(start_data[StDataConst.project_counter_id.value])
        await alert_msg_to_chat(chat_id=_chat_alert_id,
                                msg=i18n.alert.edited.ya.metrika.counters(
                                    title=project_title,
                                    company=company_name,
                                ),
                                logger=logger)
        await query.update_ya_metrika_counter(metrika_counter_id=metrika_counter_id,
                                              metrika=ya_counter)
    else:
        await alert_msg_to_chat(chat_id=_chat_alert_id,
                                msg=i18n.alert.added.ya.metrika.counters(
                                    title=project_title,
                                    company=company_name,
                                    ya_counter=counter_name
                                ),
                                logger=logger)
        await query.add_ya_metrik_counter(ya_metrika_counter=ya_counter)

    asyncio.create_task(func.generate_dag(logger=logger,
                                          project_title=project_title,
                                          project_id=project_id,
                                          company_name=company_name,
                                          start_date=start_date))
    asyncio.create_task(func.generate_dbt_metrika(
        logger=logger,
        company_id=company_id,
        company_name=company_name
    ))
    await dialog_manager.start(
        show_mode=ShowMode.EDIT,
        state=ProjectsSG.INFO_PROJECT,
        mode=StartMode.RESET_STACK,
        data={
            StDataConst.project_id.value: project_id
        }
    )
