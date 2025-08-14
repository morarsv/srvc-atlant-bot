import logging
from _operator import itemgetter
from aiogram_dialog.widgets.kbd import (Button, Column, ScrollingGroup, Select,
                                        Multiselect, Back, Next, SwitchTo, Row)
from aiogram_dialog.widgets.text import Format
from aiogram_dialog import Dialog, Window
from bot.state.dialog_state import YaMetrikaCountersSG
from bot.dialogs.projects.ya_metrika.handler import (btn_switch_to_counter, btn_add_metrika,
                                                     btn_edit_attribution, btn_back, btn_confirm,
                                                     selected_attribution)
from bot.dialogs.projects.ya_metrika.getter import (key_attribution_getter, preview_getter,
                                                    minor_attribution_getter, window_attribution_getter)
from bot.lexicon.constants.constant import WidgetDataConstant as WgDataConst
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware


logger = logging.getLogger(__name__)

preview_window = Window(
    Format(
        text='{preview_text}'
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='list_counters',
                item_id_getter=itemgetter(1),
                on_click=btn_switch_to_counter
            )
        ),
        width=1,
        height=5,
        id='scroll'
    ),
    Row(
        Button(
            text=Format(
                text='{btn_add_metrika}'
            ),
            id='btn_add_metrika',
            on_click=btn_add_metrika
        ),
        Button(
            text=Format(
                text='{btn_edit_attribution}'
            ),
            id='btn_edit_attribution',
            on_click=btn_edit_attribution,
        ),
        when='access'
    ),
    Button(
        text=Format(
            text='{btn_back}'
        ),
        id='btn_exit',
        on_click=btn_back
    ),
    getter=preview_getter,
    state=YaMetrikaCountersSG.PREVIEW

)

key_attribution_window = Window(
    Format(
        text='{attribution_text}',
    ),
    ScrollingGroup(
        Column(
            Multiselect(
                checked_text=Format('✅ {item[0]}'),
                unchecked_text=Format('❎ {item[0]}'),
                id=WgDataConst.counter_attribution.value,
                min_selected=0,
                max_selected=1,
                item_id_getter=itemgetter(1),
                items="attribution",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager_k',
    ),
    Next(
        text=Format(
            text='{btn_continue}'
        ),
        on_click=selected_attribution,
        when='selected',
    ),
    Back(
        text=Format(
            text='{btn_cancel}'
        ),
    ),
    getter=key_attribution_getter,
    state=YaMetrikaCountersSG.KEY_ATTRIBUTION
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
                id=WgDataConst.counter_minor_attribution.value,
                min_selected=0,
                max_selected=1,
                item_id_getter=itemgetter(1),
                items="attribution",
            ),
        ),
        width=1,
        height=5,
        id='scroll_with_pager_m',
    ),
    Next(
        text=Format(text='{btn_continue}'),
        when='selected',
    ),
    getter=minor_attribution_getter,
    state=YaMetrikaCountersSG.MINOR_ATTRIBUTION

)

attribution_window = Window(
    Format(
        text='{preview_text}'
    ),
    Button(
        text=Format(
            text='{btn_confirm}'
        ),
        id='btn_confirm',
        on_click=btn_confirm
    ),
    SwitchTo(
        text=Format(
            text='{btn_cancel}'
        ),
        id='b_cancel',
        state=YaMetrikaCountersSG.PREVIEW,
    ),
    getter=window_attribution_getter,
    state=YaMetrikaCountersSG.ATTRIBUTION
)

ya_metrika_list_counters_dialog = Dialog(
    preview_window, key_attribution_window, minor_attribution_window, attribution_window
)

ya_metrika_list_counters_dialog.callback_query.middleware(AuthorizationMiddleware())
ya_metrika_list_counters_dialog.message.middleware(AuthorizationMiddleware())
ya_metrika_list_counters_dialog.message.middleware(MessageMonitorMiddleware())
