import logging
from _operator import itemgetter
from aiogram_dialog.widgets.kbd import (Button, Column, ScrollingGroup,
                                        Multiselect, Back, Next)
from aiogram_dialog.widgets.text import Format
from aiogram_dialog import Dialog, Window
from bot.state.dialog_state import YaMetrikaCountersEditAddSG
from bot.dialogs.projects.ya_metrika.metrika_config.handler import (btn_counter_to_attribution, btn_confirm,
                                                                    btn_attribution_to_minor_attribution,
                                                                    btn_cancel, btn_ecommerce_to_preview,
                                                                    btn_minor_attribution_to_k_goals,
                                                                    btn_k_goals_to_minor_goals, btn_back,
                                                                    btn_back_from_k_goals, btn_edit_counter,
                                                                    next_m_goals_to_ecommerce)
from bot.dialogs.projects.ya_metrika.metrika_config.getter import (counters_getter, attribution_getter,
                                                                   k_goals_getter, m_goals_getter,
                                                                   ecommerce_getter, preview_getter,
                                                                   minor_attribution_getter)
from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware

logger = logging.getLogger(__name__)

counters_window = Window(
    Format(
        text='{preview_text}',
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.selected_counter_id.value,
                max_selected=1,
                item_id_getter=itemgetter(1),
                items="counters",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager_counters',
        when='counters'
    ),
    Button(
        text=Format('{btn_continue}'),
        id='btn_continue',
        on_click=btn_counter_to_attribution,
        when='selected'
    ),
    Button(
        text=Format(text='{btn_back}'),
        id='b_back',
        on_click=btn_back,
        when='edit'
    ),
    Button(
        text=Format(text='{btn_cancel}'),
        id='btn_cancel',
        on_click=btn_cancel
    ),
    getter=counters_getter,
    state=YaMetrikaCountersEditAddSG.COUNTERS

)

attribution_window = Window(
    Format(
        text='{attribution_text}',
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.selected_attribution.value,
                min_selected=0,
                max_selected=1,
                item_id_getter=itemgetter(1),
                items="attribution",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager0',
    ),
    Next(
        text=Format(text='{btn_continue}'),
        when='selected',
        on_click=btn_attribution_to_minor_attribution
    ),
    Back(
        text=Format(text='{btn_back}'),
    ),
    getter=attribution_getter,
    state=YaMetrikaCountersEditAddSG.ATTRIBUTION
)

minor_attribution_window = Window(
    Format(
        text='{attribution_text}',
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.selected_minor_attribution.value,
                min_selected=0,
                max_selected=1,
                item_id_getter=itemgetter(1),
                items="attribution",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager6',
    ),
    Next(
        text=Format(text='{btn_continue}'),
        id='btn_minor_attribution',
        on_click=btn_minor_attribution_to_k_goals
    ),
    Back(
        text=Format(text='{btn_back}'),
    ),
    getter=minor_attribution_getter,
    state=YaMetrikaCountersEditAddSG.MINOR_ATTRIBUTION
)

k_goals_window = Window(
    Format(
        text='{k_goals_text}',
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.selected_counter_k_goals_id.value,
                min_selected=0,
                max_selected=3,
                item_id_getter=itemgetter(1),
                when='k_goals',
                items="k_goals",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager1',
        when='k_goals'
    ),
    Button(
        text=Format('{btn_continue}'),
        id='btn_continue',
        on_click=btn_k_goals_to_minor_goals,
        when='selected'
    ),
    Button(
        text=Format(text='{btn_back}'),
        id='btn_back_k_goals',
        on_click=btn_back_from_k_goals,
    ),
    getter=k_goals_getter,
    state=YaMetrikaCountersEditAddSG.KEY_GOALS
)

m_goals_window = Window(
    Format(
        text='{m_goals_text}',
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.selected_counter_m_goals_id.value,
                max_selected=3,
                item_id_getter=itemgetter(1),
                when="m_goals",
                items="m_goals",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager2',
        when='m_goals'
    ),
    Next(
        text=Format('{btn_continue}'),
        on_click=next_m_goals_to_ecommerce
    ),
    Back(
        text=Format(text='{btn_back}'),
    ),
    getter=m_goals_getter,
    state=YaMetrikaCountersEditAddSG.MINOR_GOALS
)

ecommerce_window = Window(
    Format(
        text='{ecommerce_text}',
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.selected_counter_ecommerce.value,
                min_selected=0,
                max_selected=1,
                item_id_getter=itemgetter(1),
                items="ecommerce",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager3',
    ),
    Next(
        text=Format('{btn_continue}'),
        id='btn_ecommerce_to_preview',
        on_click=btn_ecommerce_to_preview,
        when='selected'
    ),
    Back(
        text=Format(text='{btn_back}'),
    ),
    getter=ecommerce_getter,
    state=YaMetrikaCountersEditAddSG.ECOMMERCE
)

preview_window = Window(
    Format(
        text='{preview_text}'
    ),
    Button(
        text=Format(
            text='{btn_edit_counter}'
        ),
        id='btn_edit_counter',
        on_click=btn_edit_counter,
        when='access'
    ),
    Button(
        text=Format(
            text='{btn_confirm}'
        ),
        id='btn_confirm',
        on_click=btn_confirm,
        when='edited'
    ),
    Button(
        text=Format(
            text='{btn_cancel}',
        ),
        id='btn_cancel',
        on_click=btn_cancel
    ),
    getter=preview_getter,
    state=YaMetrikaCountersEditAddSG.PREVIEW

)
ya_metrika_config_counter_dialog = Dialog(
    counters_window, attribution_window, minor_attribution_window, k_goals_window, m_goals_window,
    ecommerce_window, preview_window
)

ya_metrika_config_counter_dialog.callback_query.middleware(AuthorizationMiddleware())
ya_metrika_config_counter_dialog.message.middleware(AuthorizationMiddleware())
ya_metrika_config_counter_dialog.message.middleware(MessageMonitorMiddleware())
