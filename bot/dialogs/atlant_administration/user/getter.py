import logging
from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager

from fluentogram import TranslatorRunner
from bot.lexicon.constants.constant import StartDataConstant as StDataConst

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    start_data = dialog_manager.start_data

    company_name = start_data[StDataConst.company_name.value]
    username = start_data[StDataConst.username.value]
    user_projects = start_data[StDataConst.user_projects.value]
    user_role = start_data[StDataConst.user_role.value]
    user_status = start_data[StDataConst.user_status.value]
    user_created = start_data[StDataConst.user_created.value]

    preview_text = i18n.atlant.admin.info.user(
        username=username,
        company_name=company_name,
        count_projects=user_projects,
        role=user_role,
        status=user_status,
        creates_at=user_created
    )

    return {
        'preview_text': preview_text,
        'btn_edit': i18n.button.edit.object(),
        'btn_back': i18n.button.back()
    }
