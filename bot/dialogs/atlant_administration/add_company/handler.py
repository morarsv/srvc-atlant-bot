import asyncio
import logging

from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from bot.database.models import Companies
from bot.database import query
from bot.services.web_reports.utils import web_add_company
from bot.services.msvc.generator import func
from bot.state.dialog_state import AtlantAdministrationAddCompanySG, AtlantAdministrationEditAddUserSG
from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import (StartDataConstant as StDataConst,
                                            WidgetDataConstant as WgDataConst,
                                            PoolingConstant as poolDataConst)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def err_format_company(message: Message,
                             widget: ManagedTextInput,
                             dialog_manager: DialogManager,
                             error: ValueError):
    await dialog_manager.switch_to(state=AtlantAdministrationAddCompanySG.INPUT_COMPANY,
                                   show_mode=ShowMode.EDIT)
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')


async def next_or_end_company(message: Message,
                              widget: ManagedTextInput,
                              dialog_manager: DialogManager,
                              text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    company_name = text
    company: Companies = await query.get_company_by_name(name=company_name)
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')

    if company is not None:
        widget_data[WgDataConst.err_uniq_company.value] = True
        await dialog_manager.switch_to(state=AtlantAdministrationAddCompanySG.INPUT_COMPANY,
                                       show_mode=ShowMode.EDIT)
    else:
        widget_data[WgDataConst.company_name.value] = company_name
        widget_data[WgDataConst.err_uniq_company.value] = False
        await dialog_manager.next(show_mode=ShowMode.EDIT)


async def btn_confirm(callback: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    i18n: TranslatorRunner = middleware_data[poolDataConst.i18n.value]
    company_name = widget_data[WgDataConst.company_name.value]

    company: Companies = Companies()
    company.company = company_name

    await query.create_company(company=company)
    company: Companies = await query.get_company_by_name(name=company_name)
    asyncio.create_task(func.generate_dbt_company(
        logger=logger,
        company_id=company.id,
        company_name=company_name
    ))
    await web_add_company(
        logger=logger,
        company_name=company_name,
        callback=callback
    )
    await callback.answer(i18n.successfully.created())
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def btn_back(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager) -> None:
    await dialog_manager.done(show_mode=ShowMode.EDIT)


async def add_user_from_company(callback: CallbackQuery,
                                button: Button,
                                dialog_manager: DialogManager) -> None:
    widget_data = dialog_manager.current_context().widget_data
    company_name = widget_data[WgDataConst.company_name.value]
    await dialog_manager.start(
        mode=StartMode.NORMAL,
        show_mode=ShowMode.EDIT,
        state=AtlantAdministrationEditAddUserSG.INPUT_USERNAME,
        data={
            StDataConst.company_name.value: company_name,
            StDataConst.status.value: StDataConst.new_company.value
        })
