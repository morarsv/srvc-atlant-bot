import logging
import httpx
from aiogram.types import CallbackQuery
from bot.config_data.config import Config, load_config
from bot.lexicon.lexicon_tg import LEXICON_TG_BOT
from bot.utils.bot_func import alert_msg_to_chat
from bot.utils.bot_func import bot_current_time

configuration: Config = load_config()

_username: str = configuration.msvc_generator.login
_password: str = configuration.msvc_generator.password
_chat_id = LEXICON_TG_BOT['CHAT_ID_ERR_REPORT']


async def generate_dag(logger: logging,
                       project_title: str,
                       project_id: int,
                       company_name: str,
                       start_date: str
                       ) -> None:
    url = configuration.msvc_generator.url + configuration.msvc_generator.yaml
    data = {
        "project_title": project_title,
        "project_id": project_id,
        "company_name": company_name,
        "start_date": start_date,
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url,
                                  json=data,
                                  auth=httpx.BasicAuth(username=_username,
                                                       password=_password)
                                  )

            if r.status_code == 409:
                return
            if r.status_code != 200:
                logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
                time = await bot_current_time()
                msg = ('Something bad has happened.\n'
                       'For security reasons detailed information about the error is not logged.\n'
                       'You should check your webserver logs and retrieve details of this error.')
                err_text = msg if r.status_code >= 500 else r.text
                await alert_msg_to_chat(
                    chat_id=_chat_id,
                    msg=f'TIME: {time}\n\n'
                        f'STATUS CODE: {r.status_code}\n\n'
                        f'ERROR MESSAGE: {err_text}',
                    logger=logger
                )
    except Exception as e:
        logger.error(f"Exception in generate_dag: {e}")


async def regenerate_dag(logger: logging,
                         company_id: int,
                         company_name: str
                         ) -> None:
    url = configuration.msvc_generator.url + configuration.msvc_generator.reg_yaml
    data = {
        "company_id": company_id,
        "company_name": company_name
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url=url,
                                  json=data,
                                  auth=httpx.BasicAuth(username=_username,
                                                       password=_password)
                                  )

            if r.status_code == 409:
                return
            if r.status_code != 200:
                logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
                time = await bot_current_time()
                msg = ('Something bad has happened.\n'
                       'For security reasons detailed information about the error is not logged.\n'
                       'You should check your webserver logs and retrieve details of this error.')
                err_text = msg if r.status_code >= 500 else r.text
                await alert_msg_to_chat(
                    chat_id=_chat_id,
                    msg=f'TIME: {time}\n\n'
                        f'STATUS CODE: {r.status_code}\n\n'
                        f'ERROR MESSAGE: {err_text}',
                    logger=logger
                )
    except Exception as e:
        logger.error(f"Exception in regenerate_dag: {e}")


async def regenerate_dbt(logger: logging
                         ) -> None:
    url = configuration.msvc_generator.url + configuration.msvc_generator.reg_sql
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(url=url,
                                  auth=httpx.BasicAuth(username=_username,
                                                       password=_password)
                                  )

            if r.status_code == 409:
                return
            if r.status_code != 200:
                logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
                time = await bot_current_time()
                msg = ('Something bad has happened.\n'
                       'For security reasons detailed information about the error is not logged.\n'
                       'You should check your webserver logs and retrieve details of this error.')
                err_text = msg if r.status_code >= 500 else r.text
                await alert_msg_to_chat(
                    chat_id=_chat_id,
                    msg=f'TIME: {time}\n\n'
                        f'CMD: dbt regenerate\n\n'
                        f'STATUS CODE: {r.status_code}\n\n'
                        f'ERROR MESSAGE: {err_text}',
                    logger=logger
                )
    except Exception as e:
        logger.error(f"Exception in regenerate_dbt: {e}")


async def generate_dbt_company(logger: logging,
                               company_id: int,
                               company_name: str
                               ) -> None:
    url = configuration.msvc_generator.url + configuration.msvc_generator.sql_company
    data = {
        "company_id": company_id,
        "company_name": company_name
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url,
                                  json=data,
                                  auth=httpx.BasicAuth(username=_username,
                                                       password=_password)
                                  )

            if r.status_code == 409:
                return
            if r.status_code != 200:
                logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
                time = await bot_current_time()
                msg = ('Something bad has happened.\n'
                       'For security reasons detailed information about the error is not logged.\n'
                       'You should check your webserver logs and retrieve details of this error.')
                err_text = msg if r.status_code >= 500 else r.text
                await alert_msg_to_chat(
                    chat_id=_chat_id,
                    msg=f'TIME: {time}\n\n'
                        f'CMD: dbt company\n\n'
                        f'STATUS CODE: {r.status_code}\n\n'
                        f'ERROR MESSAGE: {err_text}',
                    logger=logger
                )
    except Exception as e:
        logger.error(f"Exception in generate_dbt_company: {e}")


async def generate_dbt_project(logger: logging,
                               company_id: int,
                               company_name: str
                               ) -> None:
    url = configuration.msvc_generator.url + configuration.msvc_generator.sql_project
    data = {
        "company_id": company_id,
        "company_name": company_name
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url,
                                  json=data,
                                  auth=httpx.BasicAuth(username=_username,
                                                       password=_password)
                                  )

            if r.status_code == 409:
                return
            if r.status_code != 200:
                logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
                time = await bot_current_time()
                msg = ('Something bad has happened.\n'
                       'For security reasons detailed information about the error is not logged.\n'
                       'You should check your webserver logs and retrieve details of this error.')
                err_text = msg if r.status_code >= 500 else r.text
                await alert_msg_to_chat(
                    chat_id=_chat_id,
                    msg=f'TIME: {time}\n\n'
                        f'CMD: dbt project\n\n'
                        f'STATUS CODE: {r.status_code}\n\n'
                        f'ERROR MESSAGE: {err_text}',
                    logger=logger
                )
    except Exception as e:
        logger.error(f"Exception in generate_dbt_project: {e}")


async def generate_dbt_direct(logger: logging,
                              company_id: int,
                              company_name: str
                              ) -> None:
    url = configuration.msvc_generator.url + configuration.msvc_generator.sql_direct
    data = {
        "company_id": company_id,
        "company_name": company_name
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url,
                                  json=data,
                                  auth=httpx.BasicAuth(username=_username,
                                                       password=_password)
                                  )

            if r.status_code == 409:
                return
            if r.status_code != 200:
                logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
                time = await bot_current_time()
                msg = ('Something bad has happened.\n'
                       'For security reasons detailed information about the error is not logged.\n'
                       'You should check your webserver logs and retrieve details of this error.')
                err_text = msg if r.status_code >= 500 else r.text
                await alert_msg_to_chat(
                    chat_id=_chat_id,
                    msg=f'TIME: {time}\n\n'
                        f'CMD: dbt direct\n\n'
                        f'STATUS CODE: {r.status_code}\n\n'
                        f'ERROR MESSAGE: {err_text}',
                    logger=logger
                )
    except Exception as e:
        logger.error(f"Exception in generate_dbt_direct: {e}")


async def generate_dbt_metrika(logger: logging,
                               company_id: int,
                               company_name: str,
                               ) -> None:
    url = configuration.msvc_generator.url + configuration.msvc_generator.sql_metrika
    data = {
        "company_id": company_id,
        "company_name": company_name
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url,
                                  json=data,
                                  auth=httpx.BasicAuth(username=_username,
                                                       password=_password)
                                  )

            if r.status_code == 409:
                return
            if r.status_code != 200:
                logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
                time = await bot_current_time()
                msg = ('Something bad has happened.\n'
                       'For security reasons detailed information about the error is not logged.\n'
                       'You should check your webserver logs and retrieve details of this error.')
                err_text = msg if r.status_code >= 500 else r.text
                await alert_msg_to_chat(
                    chat_id=_chat_id,
                    msg=f'TIME: {time}\n\n'
                        f'CMD: dbt metrika\n\n'
                        f'STATUS CODE: {r.status_code}\n\n'
                        f'ERROR MESSAGE: {err_text}',
                    logger=logger
                )
    except Exception as e:
        logger.error(f"Exception in generate_dbt_metrika: {e}")


async def edit_comment(logger: logging,
                       comment_id: int
                       ) -> None:
    url = configuration.msvc_generator.url + configuration.msvc_generator.comment_edit
    data = {
        'comment_id': comment_id
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url,
                                  json=data,
                                  auth=httpx.BasicAuth(username=_username,
                                                       password=_password)
                                  )

            if r.status_code == 409:
                return
            if r.status_code != 200:
                logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
                time = await bot_current_time()
                msg = ('Something bad has happened.\n'
                       'For security reasons detailed information about the error is not logged.\n'
                       'You should check your webserver logs and retrieve details of this error.')
                err_text = msg if r.status_code >= 500 else r.text
                await alert_msg_to_chat(
                    chat_id=_chat_id,
                    msg=f'TIME: {time}\n\n'
                        f'CMD: Edit Comment\n\n'
                        f'STATUS CODE: {r.status_code}\n\n'
                        f'ERROR MESSAGE: {err_text}',
                    logger=logger
                )
    except Exception as e:
        logger.error(f"Exception in edit_comment: {e}")


async def add_comment(logger: logging,
                      comment_id: int
                      ) -> None:
    url = configuration.msvc_generator.url + configuration.msvc_generator.comment_add
    data = {
        'comment_id': comment_id
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(url=url,
                                  json=data,
                                  auth=httpx.BasicAuth(username=_username,
                                                       password=_password)
                                  )

            if r.status_code == 409:
                return
            if r.status_code != 200:
                logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
                time = await bot_current_time()
                msg = ('Something bad has happened.\n'
                       'For security reasons detailed information about the error is not logged.\n'
                       'You should check your webserver logs and retrieve details of this error.')
                err_text = msg if r.status_code >= 500 else r.text
                await alert_msg_to_chat(
                    chat_id=_chat_id,
                    msg=f'TIME: {time}\n\n' 
                        f'CMD: Add Comment\n\n'
                        f'STATUS CODE: {r.status_code}\n\n'
                        f'ERROR MESSAGE: {err_text}',
                    logger=logger
                )
    except Exception as e:
        logger.error(f"Exception in add_comment: {e}")
