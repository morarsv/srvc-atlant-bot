from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class PathToDirectory:
    log_err: str


@dataclass
class DatabaseConfig:
    url: str


@dataclass
class APIGenerator:
    url: str
    yaml: str
    sql: str


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
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        nats=NatsConfig(servers=env.list('NATS_SERVERS')),
        database=DatabaseConfig(url=env('SQLALCHEMY_URL')),
        paths=PathToDirectory(log_err=env('LOG_ERR')),
        msvc_generator=APIGenerator(url=env('MSVC_GENERATOR_URL'),
                                    yaml=env('MSVC_GENERATOR_YAML'),
                                    sql=env('MSVC_GENERATOR_SQL'))
    )
