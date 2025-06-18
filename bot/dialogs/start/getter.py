import logging

from typing import TYPE_CHECKING
from aiogram.types import User
from aiogram_dialog import DialogManager, ShowMode
from fluentogram import TranslatorRunner
from bot.services.web_reports.utils import get_list_reports
from bot.support_models.models import SupportSessionUser

from bot.lexicon.constants.constant import PoolingConstant as poolConst


if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def preview_getter(dialog_manager: DialogManager,
                         i18n: TranslatorRunner,
                         event_from_user: User,
                         **kwargs):
    try:
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    except AttributeError as e:
        dialog_manager.show_mode = ShowMode.SEND
        logger.error(f'Error deleting message: {e}')

    middleware_data = dialog_manager.middleware_data
    tg_id = int(event_from_user.id)

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]

    user: SupportSessionUser = online_users.get(tg_id)
    username: str = user['username']
    role_id: int = user['role_id']

    report_url = get_list_reports()

    atlant_administrator, administrator, manager, viewer, report = None, None, None, None, None
    description_start = None

    if role_id == 3:
        atlant_administrator, administrator, manager, report, viewer = 1, 1, 1, 1, 1
        description_start = i18n.start.preview.admin()
    elif role_id == 1:
        administrator, manager, report, viewer = 1, 1, 1, 1
        description_start = i18n.start.preview.admin()
    elif role_id == 2:
        manager, viewer = 1, 1
        description_start = i18n.start.preview.manager()
    elif role_id == 4:
        description_start = i18n.start.preview.viewer()

    return {
        'hello_user': i18n.start.preview.hello(username=username),
        'description_start': description_start,
        'btn_to_administrator': i18n.button.to.administrator(),
        'btn_to_project': i18n.button.to.project(),
        'btn_to_atlant_administrator': i18n.button.to.atlant.administrator(),
        'btn_to_viewers': i18n.button.to.viewers(),
        'btn_report_company': i18n.button.report.company(),
        'report_url': report_url,
        'atlant_administrator': atlant_administrator,
        'administrator': administrator,
        'manager': manager,
        'viewer': viewer,
        'report': report
    }
