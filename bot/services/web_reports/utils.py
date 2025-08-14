import logging
import httpx

from urllib.parse import urljoin
from aiogram.types import CallbackQuery
from bot.database.models import Companies, Users, Projects
from bot.services.web_reports.models import SCompanies, SProjects
from bot.lexicon.lexicon_web import LEXICON_API_WEB_ATLANT, LEXICON_API_DATA, LEXICON_WEB_ATLANT_REPORTS
from bot.utils.bot_func import err_msg_api_atlant_web
from bot.utils.bot_func import bot_current_time
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from bot.database import query

_headers = {
    'Content-Type': 'application/json'
}

_username: str = LEXICON_API_DATA['USER']
_password: str = LEXICON_API_DATA['PASSWORD']

_chat_id = LEXICON_TG_BOT['CHAT_ID_ERR_REPORT']


async def web_add_company(logger: logging,
                          company_name: str,
                          callback: CallbackQuery
                          ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_ADD_COMPANY'])
    company: Companies = await query.get_company_by_name(name=company_name)
    c: SCompanies = SCompanies.model_validate(company)
    c.company_id = company.id
    data = c.model_dump()
    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              headers=_headers,
                              json=data,
                              auth=httpx.BasicAuth(
                                  username=_username,
                                  password=_password)
                              )

        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'Company ID: {company.id}\n'
                         f'Company Name: {company.company}\n'
                         f'Method: web_add_company')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)


async def web_add_user(logger: logging,
                       user_login: str,
                       callback: CallbackQuery
                       ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_ADD_USER'])
    user: Users = await query.get_user_by_login(login=user_login)
    data = {
        "user_id": str(user.id),
        "full_name": user.full_name,
        "company_id": user.company_id,
        "role_id": user.role_id,
        "login": user.login,
        "password": user.password
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              headers=_headers,
                              json=data,
                              auth=httpx.BasicAuth(
                                  username=_username,
                                  password=_password)
                              )
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'User ID: {user.id}\n'
                         f'Username: {user.full_name}\n'
                         f'Login: {user.login}\n'
                         f'Company ID: {user.company_id}\n'
                         f'Role ID: {user.role_id}\n'
                         f'Method: web_add_user')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)


async def web_update_user(logger: logging,
                          login: str,
                          callback: CallbackQuery
                          ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_UPDATE_USER'])
    user: Users = await query.get_user_by_login(login=login)

    data = {
        'user_id': str(user.id),
        'full_name': user.full_name,
        'login': login,
        'password': user.password
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              headers=_headers,
                              json=data,
                              auth=httpx.BasicAuth(
                                  username=_username,
                                  password=_password)
                              )
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'Username: {user.full_name}\n'
                         f'Login: {login}\n'
                         f'Method: web_update_user')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)


async def web_delete_manager(logger: logging,
                             user_id: str,
                             callback: CallbackQuery
                             ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_DELETE_MANAGER'].format(user_id=user_id))
    async with httpx.AsyncClient() as client:
        r = await client.delete(url=url,
                                headers=_headers,
                                auth=httpx.BasicAuth(
                                    username=_username,
                                    password=_password)
                                )
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'User ID: {user_id}\n'
                         f'Method: web_delete_manager')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)


async def web_delete_viewer(logger: logging,
                            user_id: str,
                            callback: CallbackQuery
                            ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_DELETE_VIEWER'].format(user_id=user_id))
    async with httpx.AsyncClient() as client:
        r = await client.delete(url=url,
                                headers=_headers,
                                auth=httpx.BasicAuth(
                                    username=_username,
                                    password=_password)
                                )
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'User ID: {user_id}\n'
                         f'Role: viewer\n'
                         f'Method: web_delete_viewer')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)


async def web_add_project(logger: logging,
                          user_id: str,
                          project: Projects,
                          callback: CallbackQuery
                          ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_ADD_PROJECT'].format(user_id=user_id))
    p: SProjects = SProjects.model_validate(project)
    p.project_id = project.id
    data = p.model_dump()
    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              headers=_headers,
                              json=data,
                              auth=httpx.BasicAuth(
                                  username=_username,
                                  password=_password
                              ))
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'User ID: {user_id}\n'
                         f'Project ID: {p.project_id}\n'
                         f'Title: {p.title}\n'
                         f'Method: web_add_project')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)


async def web_update_project(logger: logging,
                             project_id: int,
                             project_title: str,
                             callback: CallbackQuery
                             ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_UPDATE_PROJECT'])
    data = {
        "project_id": project_id,
        "title": project_title
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              headers=_headers,
                              json=data,
                              auth=httpx.BasicAuth(
                                  username=_username,
                                  password=_password
                              ))
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'Project ID: {project_id}\n'
                         f'Title: {project_title}\n'
                         f'Method: web_update_project')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)


async def web_set_user_to_project(logger: logging,
                                  project_id: int,
                                  user_id: str,
                                  callback: CallbackQuery
                                  ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_SET_USER_TO_PROJECT'].format(user_id=user_id))
    data = {
        "project_id": project_id
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              headers=_headers,
                              json=data,
                              auth=httpx.BasicAuth(
                                  username=_username,
                                  password=_password
                              ))
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'Error\n'
                         f'User ID: {user_id}\n'
                         f'Project ID: {project_id}\n'
                         f'Method: web_set_user_to_project')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)


async def web_remove_user_from_project(logger: logging,
                                       project_id: int,
                                       user_id: str,
                                       callback: CallbackQuery
                                       ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_REMOVE_USER_FROM_PROJECT'])
    data = {
        "project": {
            "project_id": project_id
        },
        "user": {
            "user_id": user_id
        }
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              headers=_headers,
                              json=data,
                              auth=httpx.BasicAuth(
                                  username=_username,
                                  password=_password
                              ))
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'Error\n'
                         f'User ID: {user_id}\n'
                         f'Project ID: {project_id}\n'
                         f'Method: web_remove_user_from_project')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)


async def web_delete_project(logger: logging,
                             project_id: int,
                             callback: CallbackQuery
                             ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_DELETE_PROJECT'].format(project_id=project_id))

    async with httpx.AsyncClient() as client:
        r = await client.delete(url=url,
                                headers=_headers,
                                auth=httpx.BasicAuth(
                                    username=_username,
                                    password=_password
                                ))
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'{r.text}\n'
                         f'Project ID: {project_id}\n'
                         f'Method: web_delete_project')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)


async def web_logout_from_sessions(logger: logging,
                                   user_uuid: str,
                                   login: str,
                                   callback: CallbackQuery
                                   ) -> None:
    time: str = await bot_current_time()
    url: str = urljoin(LEXICON_API_WEB_ATLANT['ATLANT_API_URL'],
                       LEXICON_API_WEB_ATLANT['ATLANT_API_LOGOUT_FROM_SESSIONS'])
    data = {
        "user_id": user_uuid,
        "login": login
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              headers=_headers,
                              json=data,
                              auth=httpx.BasicAuth(
                                  username=_username,
                                  password=_password
                              ))
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            text: str = (f'{r.text}\n'
                         f'Method: web_logout_from_sessions')
            await err_msg_api_atlant_web(time=time,
                                         chat_id=_chat_id,
                                         code=str(r.status_code),
                                         err_text=text)
            raise Exception


def get_company_report(company_id: int) -> str:
    url = urljoin(LEXICON_WEB_ATLANT_REPORTS['ADDRESS_REPORT'],
                  LEXICON_WEB_ATLANT_REPORTS['COMPANY_REPORT'].format(id=company_id))
    return url


def get_project_report(project_id: int) -> str:
    url = urljoin(LEXICON_WEB_ATLANT_REPORTS['ADDRESS_REPORT'],
                  LEXICON_WEB_ATLANT_REPORTS['PROJECT_REPORT'].format(id=project_id))
    return url


def get_list_reports() -> str:
    url = urljoin(LEXICON_WEB_ATLANT_REPORTS['ADDRESS_REPORT'],
                  LEXICON_WEB_ATLANT_REPORTS['LIST_REPORT'])
    return url
