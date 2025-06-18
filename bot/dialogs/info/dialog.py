import logging
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from bot.state.dialog_state import InfoSG
from bot.middlewares.message_monitor import MessageMonitorMiddleware
from bot.dialogs.info.getter import preview_getter

logger = logging.getLogger(__name__)

info_dialog = Dialog(
    Window(
        Format(
            text='{preview_text}'
        ),
        state=InfoSG.PREVIEW,
        getter=preview_getter,
    ),
)

info_dialog.message.middleware(MessageMonitorMiddleware())
