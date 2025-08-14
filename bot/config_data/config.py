from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    service_token: str
    alerts_token: str


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class PathToDirectory:
    log_err: str
    dir_yml: str


@dataclass
class DatabaseConfig:
    url: str


@dataclass
class APIGenerator:
    login: str
    password: str
    url: str
    yaml: str
    reg_yaml: str
    reg_sql: str
    sql_company: str
    sql_project: str
    sql_direct: str
    sql_metrika: str
    comment_add: str
    comment_edit: str


@dataclass
class Config:
    tg_bot: TgBot
    nats: NatsConfig
    database: DatabaseConfig
    paths: PathToDirectory
    msvc_generator: APIGenerator


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(service_token=env('BOT_TOKEN'),
                     alerts_token=env('BOT_ALERT_TOKEN')),
        nats=NatsConfig(servers=env.list('NATS_SERVERS')),
        database=DatabaseConfig(url=env('SQLALCHEMY_URL')),
        paths=PathToDirectory(log_err=env('LOG_ERR'),
                              dir_yml=env('DIR_YML')),
        msvc_generator=APIGenerator(login=env('ATLANT_API_LOGIN'),
                                    password=env('ATLANT_API_PASSWORD'),
                                    url=env('MSVC_GENERATOR_URL'),
                                    yaml=env('MSVC_GENERATOR_API_YAML'),
                                    reg_yaml=env('MSVC_GENERATOR_API_REG_YAML'),
                                    reg_sql=env('MSVC_GENERATOR_API_REG_SQL'),
                                    sql_company=env('MSVC_GENERATOR_API_SQL_COMPANY'),
                                    sql_project=env('MSVC_GENERATOR_API_SQL_PROJECT'),
                                    sql_direct=env('MSVC_GENERATOR_API_SQL_DIRECT'),
                                    sql_metrika=env('MSVC_GENERATOR_API_SQL_METRIKA'),
                                    comment_add=env('MSVC_GENERATOR_API_COMMENT_ADD'),
                                    comment_edit=env('MSVC_GENERATOR_API_COMMENT_EDIT')
                                    )
    )
