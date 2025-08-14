import logging

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput
from bot.database import query
from bot.lexicon.constants.constant import (StartDataConstant as StDataConst,
                                            PoolingConstant as poolConst,
                                            DialogDataConstant as dDataConst)
from bot.database.models import Users
from bot.support_models.models import SupportSessionUser
from bot.state.dialog_state import AuthorizationSG, StartSG
from bot.utils.bot_func import clean_text
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

logger = logging.getLogger(__name__)


async def btn_logout(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager) -> None:
    middleware_data = dialog_manager.middleware_data
    start_data = dialog_manager.start_data

    start_data[StDataConst.authorized.value] = False
    start_data[StDataConst.unauthorized.value] = True

    online_users = middleware_data[poolConst.online_users.value]
    tg_id = int(callback.from_user.id)

    try:
        await query.logout_user(tg_id=tg_id)
    except:
        logger.exception(f'Check login handler(btn_logout)\n'
                         f'Logout exception from ORM')
    try:
        online_users.pop(tg_id)
    except:
        logger.exception(f'Logout! Not online user with key')

    middleware_data[poolConst.online_users.value] = online_users

    await dialog_manager.switch_to(state=AuthorizationSG.PREVIEW,
                                   show_mode=ShowMode.EDIT)


async def success_input_login(message: Message,
                              widget: ManagedTextInput,
                              dialog_manager: DialogManager,
                              text: str) -> None:
    await dialog_manager.next(show_mode=ShowMode.EDIT)
    await message.delete()


async def success_input_password(message: Message,
                                 widget: ManagedTextInput,
                                 dialog_manager: DialogManager,
                                 text: str) -> None:
    widget_data = dialog_manager.current_context().widget_data
    middleware_data = dialog_manager.middleware_data

    online_users: dict[int, SupportSessionUser] = middleware_data[poolConst.online_users.value]
    tg_id = int(message.from_user.id)
    try:
        await message.delete()
    except AttributeError as e:
        logger.error(f'Error deleting message: {e}')
    login: str = widget_data.get(dDataConst.input_login.value)
    password: str = widget_data.get(dDataConst.input_password.value)

    login = clean_text(login)
    password = clean_text(password)

    user: Users = await query.get_user_by_login(
        login=login.lower()
    )

    if user is None:
        await dialog_manager.start(state=AuthorizationSG.FAIL,
                                   show_mode=ShowMode.EDIT)
        return

    db_psw: str = user.password
    ph: PasswordHasher = PasswordHasher()

    try:
        ph.verify(db_psw, password)
    except LookupError as e:
        logger.error(f'Error verifying. Wrong password. Exception: {e}')
        await dialog_manager.start(state=AuthorizationSG.FAIL,
                                   show_mode=ShowMode.EDIT)
        return
    except VerifyMismatchError as e:
        logger.error(f'Error verifying. Wrong password. Exception: {e}')
        await dialog_manager.start(state=AuthorizationSG.FAIL,
                                   show_mode=ShowMode.EDIT)
        return

    login = user.login
    username = user.full_name
    try:
        await query.login_user(
            login=login,
            tg_id=tg_id
        )
    except Exception as e:
        logger.error(f'Check login handler(success_input_password)\n'
                     f'Login exception from ORM: {e}')

    online_users[tg_id] = SupportSessionUser(
        username=user.full_name,
        login=user.login,
        role_id=user.role_id,
        user_uuid=user.id,
        company_id=user.company_id,
        company_name=user.company.company
    )
    middleware_data[poolConst.online_users.value] = online_users
    await dialog_manager.start(state=StartSG.PREVIEW,
                               mode=StartMode.RESET_STACK,
                               data={
                                   StDataConst.username.value: username,
                                   StDataConst.user_role_id.value: user.role_id,
                               },
                               show_mode=ShowMode.EDIT)
