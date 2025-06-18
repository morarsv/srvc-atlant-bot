from environs import Env

env = Env()
env.read_env()

LEXICON_SYSTEM_ID: dict[str, int] = {
    'YA_DIRECT': env.int('YA_DIRECT'),
    'YA_METRIKA': env.int('YA_METRIKA')
}

LEXICON_URL: dict[str, str] = {
    'CLIENT_ID': env.str('CLIENT_ID'),
    'CLIENT_SECRET': env.str('CLIENT_SECRET'),
    'DIRECT_API_URL_ADVERTISER_CLIENTS': env.str('DIRECT_API_URL_ADVERTISER_CLIENTS'),
    'DIRECT_API_URL_AGENCY_CLIENTS': env.str('DIRECT_API_URL_AGENCY_CLIENTS'),
    'METRIKA_API_COUNTERS': env.str('METRIKA_API_COUNTERS'),
    'METRIKA_API_GOALS': env.str('METRIKA_API_GOALS'),
    'REDIRECT_URI': env.str('REDIRECT_URI'),
    'BASEURL': env.str('BASEURL'),
    'AUTH_WITH_CODE': env.str('AUTH_WITH_CODE'),
    'AUTH_WITHOUT_CODE': env.str('AUTH_WITHOUT_CODE'),
    'METRIKA_API_GET_COUNTER': env.str('METRIKA_API_GET_COUNTER'),
    'SCOPE_METRIKA': '&scope=metrika:read',
    'SCOPE_DIRECT': '&scope=direct:api'
}

LEXICON_ATTRIBUTION: dict[str, str] = {
    'AUTOMATICALLY': 'Автоматическая',
    'LAST_SIGNIFICANT_TRANSITION': 'Последний значимый переход',
    'LAST_CLICK_FROM_DIRECT': 'Первый переход из Директа',
    'FIRST_TRANSITION': 'Первый переход',
    'LAST_TRANSITION': 'Последний переход',

}

LEXICON_ATTRIBUTION_AIRFLOW: dict[str, str] = {
    'Автоматическая': 'automatic',
    'Последний значимый переход': 'lastsign',
    'Первый переход из Директа': 'last_yandex_direct_click',
    'Первый переход': 'first',
    'Последний переход': 'last'
}
