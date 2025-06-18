import logging

from operator import itemgetter
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, ScrollingGroup, Column, Select
from aiogram_dialog.widgets.text import Format
from bot.dialogs.faq.handler import btn_switch_to_faq
from bot.dialogs.faq.getter import main_getter, faq_getter
from bot.state.dialog_state import FaqSG
from bot.middlewares.authorization_monitor import AuthorizationMiddleware
from bot.middlewares.message_monitor import MessageMonitorMiddleware

logger = logging.getLogger(__name__)

preview_window = Window(
    Format(
        text='{preview_text}',
    ),
    ScrollingGroup(
        Column(
            Select(
                text=Format(text='{item[0]}'),
                id='id',
                items='faq',
                item_id_getter=itemgetter(1),
                on_click=btn_switch_to_faq
            )
        ),
        width=1,
        height=5,
        id='scroll'
    ),
    getter=main_getter,
    state=FaqSG.MAIN,
)

text_window = Window(
    Format(
        text='{faq}'
    ),
    Back(
        text=Format(
            text='{btn_back}'
        )
    ),
    getter=faq_getter,
    state=FaqSG.TEXT
)


faq_dialog = Dialog(
    preview_window, text_window
)

faq_dialog.message.middleware(AuthorizationMiddleware())
faq_dialog.message.middleware(MessageMonitorMiddleware())
faq_dialog.callback_query.middleware(AuthorizationMiddleware())
