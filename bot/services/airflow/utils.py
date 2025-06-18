import logging
import httpx
import json
from fluentogram import TranslatorRunner
from aiogram.types import CallbackQuery
from typing import TYPE_CHECKING
from bot.database.models import YaMetrikaCounters
from bot.lexicon.constants.constant import WordConst as WConst
from bot.lexicon.lexicon_airflow import LEXICON_CONNECTION_TYPE, LEXICON_DATA, LEXICON_URL
from bot.lexicon.lexicon_ya import LEXICON_ATTRIBUTION_AIRFLOW

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner
from bot.utils.bot_func import (detect_language, err_msg_airflow_connection,
                                err_msg_airflow_start_dag, bot_start_end_airflow_dag)

_headers = {
    'Content-Type': 'application/json'
}


async def create_connection_direct(logger: logging,
                                   project_title: str,
                                   login: str,
                                   access_token: str,
                                   project_id: str,
                                   chat_id: str,
                                   i18n: TranslatorRunner,
                                   callback: CallbackQuery,
                                   time: str) -> None:
    connection = WConst.direct.value
    connection_id: str = await detect_language(f'{project_title}_{connection}_{login}')
    url = LEXICON_URL['AIRFLOW_URL'] + LEXICON_URL['API_CREATE_CONNECTION']
    username = LEXICON_DATA['USER']
    password = LEXICON_DATA['PASSWORD']

    data = {
        "connection_id": connection_id,
        "conn_type": LEXICON_CONNECTION_TYPE['EMAIL'],
        "description": f"Added from telegram bot. Date: {time}",
        "login": login,
        "password": access_token
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              headers=_headers,
                              json=data,
                              auth=httpx.BasicAuth(username=username, password=password))

        if r.status_code == 409:
            return
        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            msg = ('Something bad has happened.\n'
                   'For security reasons detailed information about the error is not logged.\n'
                   'You should check your webserver logs and retrieve details of this error.')
            err_text = msg if r.status_code == 500 else r.text
            await err_msg_airflow_connection(time=time,
                                             project_id=f'{project_title}-{project_id}',
                                             counter_login=login,
                                             chat_id=chat_id,
                                             i18n=i18n,
                                             callback=callback,
                                             code=str(r.status_code),
                                             err_text=err_text)


async def create_connection_metrika(logger: logging,
                                    project_title: str,
                                    metrika: YaMetrikaCounters,
                                    access_token: str,
                                    chat_id: str,
                                    i18n: TranslatorRunner,
                                    callback: CallbackQuery,
                                    time: str) -> None:
    connection = WConst.metrika.value
    counter_id = metrika.counter_id
    project_id = metrika.project_id
    key_goals = metrika.key_goals
    minor_goals = metrika.minor_goals if metrika.minor_goals else []
    ecom_flag = int(metrika.ecommerce)
    attribution = metrika.attribution
    minor_attribution = metrika.minor_attribution
    attributions = \
        [LEXICON_ATTRIBUTION_AIRFLOW[attribution],
         LEXICON_ATTRIBUTION_AIRFLOW[str(minor_attribution)]] \
        if minor_attribution else [LEXICON_ATTRIBUTION_AIRFLOW[attribution]]
    extra = {'key_goals': key_goals,
             'minor_goals': minor_goals,
             'ecom_flag': ecom_flag,
             'attribution': attributions}

    connection_id: str = await detect_language(f'{project_title}_{connection}_{counter_id}')
    url = LEXICON_URL['AIRFLOW_URL'] + LEXICON_URL['API_CREATE_CONNECTION']
    username = LEXICON_DATA['USER']
    password = LEXICON_DATA['PASSWORD']

    data = {
        "connection_id": connection_id,
        "conn_type": LEXICON_CONNECTION_TYPE['EMAIL'],
        "description": f"Added from telegram bot. Date: {time}",
        "login": str(counter_id),
        "password": access_token,
        "extra": json.dumps(extra)
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(url=url,
                              headers=_headers,
                              json=data,
                              auth=httpx.BasicAuth(username=username, password=password))

        logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
        if r.status_code == 409:
            url = LEXICON_URL['AIRFLOW_URL'] \
                  + LEXICON_URL['API_UPDATE_CONNECTION'].format(connection_id=connection_id)
            r = await client.patch(url=url,
                                   headers=_headers,
                                   json=data,
                                   auth=httpx.BasicAuth(username=username, password=password))

        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            msg = ('Something bad has happened.\n'
                   'For security reasons detailed information about the error is not logged.\n'
                   'You should check your webserver logs and retrieve details of this error.')
            err_text = msg if r.status_code == 500 else r.text
            await err_msg_airflow_connection(time=time,
                                             project_id=f'{project_title}-{project_id}',
                                             counter_login=counter_id,
                                             chat_id=chat_id,
                                             i18n=i18n,
                                             callback=callback,
                                             code=str(r.status_code),
                                             err_text=err_text)


async def set_active_dag(logger: logging,
                         company: str,
                         project_id: str,
                         company_id: str,
                         created_date: str,
                         i18n: TranslatorRunner,
                         callback: CallbackQuery
                         ) -> None:
    company = await detect_language(company)
    dag_id = f'{company}_{project_id}'
    url_start = LEXICON_URL['AIRFLOW_URL'] + LEXICON_URL['API_INFO_AND_START_DAG'].format(dag_id=dag_id)
    url_run = LEXICON_URL['AIRFLOW_URL'] + LEXICON_URL['API_RUN_DAG'].format(dag_id=dag_id)
    username = LEXICON_DATA['USER']
    password = LEXICON_DATA['PASSWORD']

    start, end = await bot_start_end_airflow_dag(created_date=created_date)

    data = {
        'is_paused': False
    }

    data_run = {
        'conf': {
            'start_date': start,
            'end_date': end
        }
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url=url_start,
                             auth=httpx.BasicAuth(username=username, password=password))

        if r.status_code != 200:
            logger.error(f'Status code: {r.status_code}\n'
                         f'Detail: {r.text}')
            await err_msg_airflow_start_dag(project_id=project_id,
                                            company_name=company_id,
                                            i18n=i18n,
                                            callback=callback,
                                            code=str(r.status_code),
                                            err_text=r.text)
        if r.status_code == 200:
            r = await client.patch(url=url_start,
                                   headers=_headers,
                                   json=data,
                                   auth=httpx.BasicAuth(username=username, password=password))
            if r.status_code == 200:
                logger.info(f'Successfully updated')

            if r.status_code == 409:
                logger.info(r.text)
            if r.status_code != 200:
                logger.error(f'Status code: {r.status_code}\n'
                             f'Detail: {r.text}')
                await err_msg_airflow_start_dag(project_id=project_id,
                                                company_name=company_id,
                                                i18n=i18n,
                                                callback=callback,
                                                code=str(r.status_code),
                                                err_text=r.text)

            r = await client.post(url=url_run,
                                  headers=_headers,
                                  json=data_run,
                                  auth=httpx.BasicAuth(username=username, password=password))
            if r.status_code == 200:
                logger.info(f'Successfully updated')
                return
            if r.status_code == 409:
                logger.info(r.text)
            if r.status_code != 200:
                logger.error(f'Status code: {r.status_code}\n'
                             f'Detail: {r.text}')
                await err_msg_airflow_start_dag(project_id=project_id,
                                                company_name=company_id,
                                                i18n=i18n,
                                                callback=callback,
                                                code=str(r.status_code),
                                                err_text=r.text)
