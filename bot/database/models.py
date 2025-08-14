from typing import List
from dataclasses import dataclass

from sqlalchemy import BigInteger, String, Uuid, func, text, DateTime, Integer, ForeignKey, Boolean, ARRAY, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from bot.config_data.config import Config, load_config
from datetime import datetime
from uuid import UUID

config: Config = load_config()

engine = create_async_engine(url=config.database.url, pool_size=10, max_overflow=20, pool_timeout=30, )
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    tg_id = mapped_column(BigInteger, unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(300), nullable=True)
    company_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey('companies.id', ondelete='CASCADE'),
                                            nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.id'), nullable=False)
    login: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("(NOW() AT TIME ZONE 'UTC' + interval '7 hour')"))
    role: Mapped['Roles'] = relationship(back_populates='users', lazy='joined')
    company: Mapped['Companies'] = relationship(back_populates='users', lazy='joined')
    projects: Mapped[List['Projects']] = relationship(back_populates='user',
                                                      lazy='selectin',
                                                      cascade='delete')


class Roles(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(unique=True, nullable=True)
    users: Mapped[List['Users']] = relationship(back_populates='role', cascade='delete', lazy='selectin')


class Companies(Base):
    __tablename__ = 'companies'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    report: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(), )
    users: Mapped[List['Users']] = relationship(back_populates='company',
                                                lazy='selectin',
                                                cascade='delete')
    projects: Mapped[List['Projects']] = relationship(back_populates='company',
                                                      lazy='selectin',
                                                      cascade='delete')


@dataclass
class Projects(Base):
    __tablename__ = 'projects'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(String(4096), nullable=False)
    company_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey('companies.id', ondelete='CASCADE'),
                                            nullable=False)
    user_login: Mapped[str] = mapped_column(String(120),
                                            ForeignKey('users.login', ondelete='CASCADE'),
                                            nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("(NOW() AT TIME ZONE 'UTC' + interval '7 hour')"))
    company: Mapped['Companies'] = relationship(back_populates='projects', lazy='joined')
    user: Mapped['Users'] = relationship(back_populates='projects', lazy='joined')
    yandex_accesses: Mapped[List['YandexAccesses']] = relationship(back_populates='project',
                                                                   lazy='selectin',
                                                                   cascade='delete')
    yandex_direct_logins: Mapped[List['YaDirectLogins']] = relationship(back_populates='project',
                                                                        lazy='selectin',
                                                                        cascade='delete')
    yandex_metrika_counters: Mapped[List['YaMetrikaCounters']] = relationship(back_populates='project',
                                                                              lazy='selectin',
                                                                              cascade='delete')
    report: Mapped[List['ProjectReport']] = relationship(back_populates='project',
                                                         lazy='selectin',
                                                         cascade='delete')


class ProjectReport(Base):
    __tablename__ = 'project_report'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey('projects.id', ondelete='CASCADE'),
                                            nullable=False)
    report_url: Mapped[str] = mapped_column(String(500), nullable=True)
    project: Mapped['Projects'] = relationship(back_populates='report', lazy='joined')


class ConnectedSystems(Base):
    __tablename__ = 'connected_systems'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    system: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    yandex_accesses: Mapped[List['YandexAccesses']] = relationship(back_populates='system',
                                                                   lazy='selectin',
                                                                   cascade='delete')


@dataclass
class YandexAccesses(Base):
    __tablename__ = 'yandex_accesses'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    system_id: Mapped[int] = mapped_column(Integer,
                                           ForeignKey('connected_systems.id', ondelete='CASCADE'),
                                           nullable=False)
    project_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey('projects.id', ondelete='CASCADE'),
                                            nullable=False)
    access_token: Mapped[str] = mapped_column(String(300), nullable=False)
    expires_in: Mapped[int] = mapped_column(Integer, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(400), nullable=False)
    token_type: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("(NOW() AT TIME ZONE 'UTC' + interval '7 hour')"))
    system: Mapped['ConnectedSystems'] = relationship(back_populates='yandex_accesses', lazy='joined')
    project: Mapped['Projects'] = relationship(back_populates='yandex_accesses', lazy='joined')


@dataclass
class YaDirectLogins(Base):
    __tablename__ = 'yandex_direct_logins'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey('projects.id', ondelete='CASCADE'),
                                            nullable=False)
    direct_login: Mapped['str'] = mapped_column(String(500), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("(NOW() AT TIME ZONE 'UTC' + interval '7 hour')"))
    project: Mapped['Projects'] = relationship(back_populates='yandex_direct_logins', lazy='joined')


@dataclass
class YaMetrikaCounters(Base):
    __tablename__ = 'yandex_metrika_counters'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey('projects.id', ondelete='CASCADE'),
                                            nullable=False)
    counter_name: Mapped[str] = mapped_column(String(500), nullable=False)
    counter_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    attribution: Mapped[str] = mapped_column(String(500), nullable=False)
    minor_attribution: Mapped[str] = mapped_column(String(500), nullable=True)
    names_key_goals: Mapped[List[str]] = mapped_column(ARRAY(String(1000)), nullable=False)
    names_minor_goals: Mapped[List[str]] = mapped_column(ARRAY(String(1000)), nullable=True)
    key_goals: Mapped[List[int]] = mapped_column(ARRAY(BigInteger), nullable=False)
    minor_goals: Mapped[List[int]] = mapped_column(ARRAY(BigInteger), nullable=True)
    ecommerce: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("(NOW() AT TIME ZONE 'UTC' + interval '7 hour')"))
    project: Mapped['Projects'] = relationship(back_populates='yandex_metrika_counters', lazy='joined')


@dataclass
class ProjectUser(Base):
    __tablename__ = 'project_user'
    project_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey('projects.id', ondelete='CASCADE'),
                                            nullable=False,
                                            primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid,
                                          ForeignKey('users.id', ondelete='CASCADE'),
                                          nullable=False,
                                          primary_key=True)


@dataclass
class ProjectComment(Base):
    __tablename__ = 'project_comment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey('projects.id', ondelete='CASCADE'),
                                            nullable=False)
    project_title: Mapped[str] = mapped_column(String(500),
                                               nullable=False)
    comment: Mapped[str] = mapped_column(String(1024), nullable=True)
    specified_date: Mapped[Date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("(NOW() AT TIME ZONE 'UTC' + interval '7 hour')"))


@dataclass
class ManagerViewer(Base):
    __tablename__ = 'manager_viewer'
    manager_id: Mapped[UUID] = mapped_column(Uuid,
                                             ForeignKey('users.id', ondelete='CASCADE'),
                                             nullable=False,
                                             primary_key=True)
    viewer_id: Mapped[UUID] = mapped_column(Uuid,
                                            ForeignKey('users.id', ondelete='CASCADE'),
                                            nullable=False,
                                            primary_key=True)


async def async_database_run():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
