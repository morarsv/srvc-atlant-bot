import logging

from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from bot.lexicon.constants.constant import (WidgetDataConstant as WgDataConst,
                                            PoolingConstant as poolConst)
from typing import TYPE_CHECKING
from fluentogram import TranslatorRunner
if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def _get_faq_title_by_role(role_id: int,
                                 i18n: TranslatorRunner) -> list[tuple[str, Any]]:
    if role_id == 2:
        faq = [(i18n.faq.how.create.project.title(), 1),
               (i18n.faq.what.next.after.project.title(), 2),
               (i18n.faq.how.add.extra.counter.title(), 3),
               (i18n.faq.how.connect.disconnect.direct.logins.title(), 4),
               (i18n.faq.what.are.viewers.title(), 5),
               (i18n.faq.how.work.viewers.title(), 6)]
        return faq
    if role_id in [1, 3]:
        faq = [(i18n.faq.how.create.project.title(), 1),
               (i18n.faq.what.next.after.project.title(), 2),
               (i18n.faq.how.add.extra.counter.title(), 3),
               (i18n.faq.how.connect.disconnect.direct.logins.title(), 4),
               (i18n.faq.what.are.viewers.title(), 5),
               (i18n.faq.how.work.viewers.title(), 6),
               (i18n.faq.what.are.management.profile.title(), 7),
               (i18n.faq.how.create.manager.title(), 8),
               (i18n.faq.how.give.withdraw.permission.title(), 9)]
        return faq
    if role_id == 4:
        return [(i18n.faq.where.see.project.report.title(), 10)]


async def _get_faq_text_by_id(text_id: int,
                              i18n: TranslatorRunner) -> str:
    text = {
        1: i18n.faq.how.create.project.text(),
        2: i18n.faq.what.next.after.project.text(),
        3: i18n.faq.how.add.extra.counter.text(),
        4: i18n.faq.how.connect.disconnect.direct.logins.text(),
        5: i18n.faq.what.are.viewers.text(),
        6: i18n.faq.how.work.viewers.text(),
        7: i18n.faq.what.are.management.profile.text(),
        8: i18n.faq.how.create.manager.text(),
        9: i18n.faq.how.give.withdraw.permission.text(),
        10: i18n.faq.where.see.project.report.text()
    }
    return text[text_id]


async def btn_switch_to_faq(
        callback: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        selected_item: str
) -> None:
    middleware_data = dialog_manager.middleware_data
    widget_data = dialog_manager.current_context().widget_data
    i18n: TranslatorRunner = middleware_data[poolConst.i18n.value]
    text_id = int(selected_item)
    faq = await _get_faq_text_by_id(text_id=text_id,
                                    i18n=i18n)
    widget_data[WgDataConst.faq.value] = faq
    await dialog_manager.next(show_mode=ShowMode.EDIT)
