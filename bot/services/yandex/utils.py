import logging
import httpx
from bot.lexicon.lexicon_ya import LEXICON_URL


def get_url_ya_access(p_id: int,
                      system_id: int,
                      scope: str) -> str:
    client_id = LEXICON_URL['CLIENT_ID']
    redirect_uri = LEXICON_URL['REDIRECT_URI']
    base_url = LEXICON_URL['BASEURL']
    auth_uri = LEXICON_URL['AUTH_WITH_CODE'].format(client_id=client_id,
                                                    redirect_uri=redirect_uri,
                                                    state=('{}_{}'.format(p_id, system_id))
                                                    )
    return base_url + auth_uri + scope


async def get_ya_advertiser_clients_logins(oauth_token: str,
                                           logger: logging) -> list[dict]:
    url = LEXICON_URL['DIRECT_API_URL_ADVERTISER_CLIENTS']
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Accept-Language": "ru",
        "Content-Type": "application/json"
    }
    json = {
        "method": "get",
        "params": {
            "FieldNames": ['ClientId', 'Login']
        }
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, json=json)

        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            return []

        try:
            response_json = r.json()
        except ValueError:
            logger.exception(f'Ошибка при декодировании JSON: {r.text}')
            return []

        if 'error' in response_json:
            error_code = response_json['error'].get('error_code', 'Неизвестный код ошибки')
            error_detail = response_json['error'].get('error_detail', 'Подробности ошибки отсутствуют')
            error_string = response_json['error'].get('error_string', 'Ошибка')
            request_id = response_json['error'].get('request_id', 'Нет ID запроса')
            logger.error(f"Ошибка {error_code}: {error_string}. Подробности: {error_detail}. ID запроса: {request_id}")

            return ['Error', {'code': error_code,
                              'detail': error_detail}]
    result = response_json['result']['Clients']
    return result


async def check_ya_representative_clients_logins(oauth_token: str,
                                                 login: str,
                                                 logger: logging) -> dict:
    url = LEXICON_URL['DIRECT_API_URL_ADVERTISER_CLIENTS']
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Client-Login": login,
        "Accept-Language": "ru",
        "Content-Type": "application/json"
    }
    json = {
        "method": "get",
        "params": {
            "FieldNames": ['ClientId', 'Login']
        }
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, json=json)

        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            return {login: False}

        try:
            response_json = r.json()
        except ValueError:
            logger.exception(f'Ошибка при декодировании JSON: {r.text}')
            return {login: False}
        logger.info(r.json())
    return {login: True} if 'result' in response_json else {login: False}


async def get_ya_agency_clients_logins(oauth_token: str,
                                       logger: logging) -> list[dict]:
    url = LEXICON_URL['DIRECT_API_URL_AGENCY_CLIENTS']
    headers = {
        "Authorization": f"Bearer {oauth_token}",
        "Accept-Language": "ru",
        "Content-Type": "application/json"
    }
    json = {
        "method": "get",
        "params": {
            "SelectionCriteria": {},
            "FieldNames": ['ClientId', 'Login']
        }
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, json=json)

        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            return []

        try:
            response_json = r.json()
        except ValueError:
            logger.exception(f'Ошибка при декодировании JSON: {r.text}')
            return []

        if 'error' in response_json:
            error_code = response_json['error'].get('error_code', 'Неизвестный код ошибки')
            error_detail = response_json['error'].get('error_detail', 'Подробности ошибки отсутствуют')
            error_string = response_json['error'].get('error_string', 'Ошибка')
            request_id = response_json['error'].get('request_id', 'Нет ID запроса')
            logger.error(f"Ошибка {error_code}: {error_string}. Подробности: {error_detail}. ID запроса: {request_id}")

            return ['Error', {'code': error_code,
                              'detail': error_detail}]

    result = response_json['result']['Clients']
    return result


async def get_ya_counters(oauth_token: str,
                          logger: logging) -> list[tuple]:
    url = LEXICON_URL['METRIKA_API_COUNTERS']
    headers = {
        'GET': '/management/v1/counters HTTP/1.1',
        'Host': 'api-metrika.yandex.net',
        'Authorization': f'OAuth {oauth_token}',
        'Content-Type': 'application/x-yametrika+json'
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            return []

        try:
            response_json = r.json()['counters']
        except ValueError:
            logger.exception(f'Ошибка при декодировании JSON: {r.text}')
            return []

    result = [(f'{c['name']}: {c['id']}', c['id']) for c in response_json]

    return result


async def get_ya_counter_info(oauth_token: str,
                              counter: int,
                              logger: logging) -> str:
    url = LEXICON_URL['METRIKA_API_GET_COUNTER'].format(counter=counter)
    headers = {
        'GET': '/management/v1/counters HTTP/1.1',
        'Host': 'api-metrika.yandex.net',
        'Authorization': f'OAuth {oauth_token}',
        'Content-Type': 'application/x-yametrika+json'
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            return ''

        try:
            response_json = r.json()
        except ValueError:
            logger.exception(f'Ошибка при декодировании JSON: {r.text}')
            return ''

    return response_json['counter']['name']


async def get_ya_goals(oauth_token: str,
                       counter_id: int,
                       logger: logging) -> list[tuple]:
    url = LEXICON_URL['METRIKA_API_GOALS'].format(counter_id=counter_id)
    headers = {
        'GET': '/management/v1/counters HTTP/1.1',
        'Host': 'api-metrika.yandex.net',
        'Authorization': f'OAuth {oauth_token}',
        'Content-Type': 'application/x-yametrika+json'
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)

        if r.status_code != 200:
            logger.error(f"Ошибка: {r.status_code}, Тело ответа: {r.text}")
            return []

        try:
            response_json = r.json()['goals']
        except ValueError:
            logger.exception(f'Ошибка при декодировании JSON: {r.text}')
            return []

    result = [(f'{c['id']}:{c['name']}', c['id']) for c in response_json]

    return sorted(result, key=lambda x: x[0].split(':')[1])
