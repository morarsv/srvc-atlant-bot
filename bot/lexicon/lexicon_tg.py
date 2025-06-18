from environs import Env

env = Env()
env.read_env()

LEXICON_TG_BOT: dict[str, str] = {
    'CHAT_ID': env.str('CHAT_ID'),
    'CHAT_ID_ERR_REPORT': env.str('CHAT_ID_ERR_REPORT'),
    'CHAT_ID_ACC_ALERTS': env.str('CHAT_ID_ACC_ALERTS')
}

LEXICON_TEMPLATE: dict[str, str] = {
    'REPORT': env.str('TEMPLATE_REPORT')
}
