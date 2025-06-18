from sqlalchemy import select, func, update, insert, delete as alchemy_delete
from bot.database.models import (async_session, Users, Companies, Projects, ProjectUser, ProjectReport,
                                 YandexAccesses, YaDirectLogins, YaMetrikaCounters, ManagerViewer)
from uuid import UUID


# Профили и юзеры
async def update_tg_id(login: str, tg_id: int | None) -> None:
    async with async_session() as session:
        stmt = select(Users).where(login == Users.login)
        result = await session.execute(stmt)
        user = result.scalar()
        user.tg_id = tg_id
        await session.commit()


async def logout_user(tg_id: int) -> None:
    async with async_session() as session:
        stmt = (update(Users).
                where(Users.tg_id == tg_id).
                values(tg_id=None))
        await session.execute(stmt)
        await session.commit()


async def login_user(login: str, tg_id: int) -> None:
    async with async_session() as session:
        stmt = (update(Users).
                where(Users.login == login).
                values(tg_id=tg_id))
        await session.execute(stmt)
        await session.commit()


async def update_atlant_user_by_login(login: str, full_name: str, password: str) -> None:
    async with async_session() as session:
        stmt = (update(Users).
                where(Users.login == login).
                values(full_name=full_name,
                       password=password
                       ))
        await session.execute(stmt)
        await session.commit()


async def update_other_user_by_login(login: str, full_name: str, password: str) -> None:
    async with async_session() as session:
        stmt = (update(Users).
                where(Users.login == login).
                values(full_name=full_name,
                       tg_id=None,
                       password=password
                       ))
        await session.execute(stmt)
        await session.commit()


async def add_user(user: Users) -> None:
    async with async_session() as session:
        session.add(user)
        await session.commit()


async def deactivate_user_by_login(login: str, user_uuid: UUID) -> None:
    async with async_session() as session:
        stmt = (update(Users).
                where(login == Users.login).
                values(
                    active=False,
                    tg_id=None)
                )
        await session.execute(stmt)
        stmt = (alchemy_delete(ProjectUser).
                where(ProjectUser.user_id == user_uuid))
        await session.execute(stmt)
        await session.commit()


async def get_user_by_login(login: str) -> Users | None:
    async with async_session() as session:
        return await session.scalar(select(Users).where(login == Users.login))


async def get_user_by_tg_id(tg_id: int) -> Users | None:
    async with async_session() as session:
        return await session.scalar(select(Users).where(tg_id == Users.tg_id, Users.active))


async def get_active_users_by_company_id(company_id: int) -> list[Users] | None:
    async with async_session() as session:
        return await session.scalars(select(Users)
                                     .where(company_id == Users.company_id,
                                            Users.active)
                                     .order_by(Users.full_name.asc()))


async def get_users_by_company_id(company_id: int) -> list[Users]:
    async with async_session() as session:
        stmt = (select(Users).
                where(Users.company_id == company_id).
                order_by(Users.full_name.asc()))
        result = await session.scalars(stmt)
        return result.all()


async def get_list_users_uuid_by_logins(list_logins: list[str]) -> list[UUID]:
    async with async_session() as session:
        stmt = (select(Users.id).where(Users.login.in_(list_logins)))
        result = await session.scalars(stmt)
        return result.all()


async def get_managers_by_company_id(company_id: int) -> list[Users] | None:
    async with async_session() as session:
        return await session.scalars(select(Users)
                                     .where(company_id == Users.company_id, Users.role_id.in_([2, 4]),
                                            Users.active)
                                     .order_by(Users.full_name.asc()))


async def get_viewers_by_manager_id(manager_id: UUID) -> list[Users] | None:
    async with async_session() as session:
        stmt = (
            select(Users)
            .where(
                Users.active,
                Users.id.in_(
                    select(ManagerViewer.viewer_id).where(manager_id == ManagerViewer.manager_id)
                )
            )
        )
        result = await session.scalars(stmt)
        return result.all()


async def delete_viewer_by_id(user_id: UUID) -> None:
    async with async_session() as session:
        stmt = (alchemy_delete(Users).where(Users.id == user_id))
        await session.execute(stmt)
        await session.commit()


async def add_viewer(manager_id: UUID, user: Users) -> None:
    async with async_session() as session:
        session.add(user)
        await session.flush()
        viewer_manager = ManagerViewer()
        viewer_manager.manager_id = manager_id
        viewer_manager.viewer_id = user.id
        session.add(viewer_manager)
        await session.commit()


async def get_active_user_by_id(user_id: UUID) -> Users:
    async with async_session() as session:
        return await session.scalar(select(Users).where(user_id == Users.id, Users.active))


async def get_user_by_id(user_id: UUID) -> Users:
    async with async_session() as session:
        return await session.scalar(select(Users).where(user_id == Users.id))


async def get_logins() -> list[str]:
    async with async_session() as session:
        result = await session.scalars(select(Users.login))
        return result.all()


# Companies
async def create_company(company: Companies) -> None:
    async with async_session() as session:
        session.add(company)
        await session.commit()


async def add_company_and_user(company: Companies, user: Users) -> None:
    async with async_session() as session:
        session.add(company)
        await session.flush()
        c_id = await session.scalar(
            select(Companies.id).where((str(company.company).lower() == func.lower(Companies.company))))
        user.company_id = c_id
        session.add(user)
        await session.commit()


async def get_all_companies() -> list[Companies]:
    async with async_session() as session:
        result = await session.scalars(select(Companies).order_by(Companies.company.asc()))
        return result.all()


async def get_companies_names() -> list[str]:
    async with async_session() as session:
        result = await session.scalars(select(Companies.company))
        return result.all()


async def get_company_by_id(c_id: int) -> Companies:
    async with async_session() as session:
        return await session.scalar(select(Companies).where(c_id == Companies.id))


async def get_company_by_name(name: str) -> Companies:
    async with async_session() as session:
        return await session.scalar(select(Companies).where(Companies.company == name))


# Проекты
async def add_project_and_report_and_set_manager(project: Projects, user_id: UUID) -> None:
    async with async_session() as session:
        session.add(project)
        await session.flush()
        project_user = ProjectUser()
        project_report = ProjectReport()
        project_report.project_id = project.id
        project_user.project_id = project.id
        project_user.user_id = user_id
        session.add(project_user)
        session.add(project_report)
        await session.commit()


async def set_manager_to_project(project_id: int, user_uuid: UUID) -> None:
    async with async_session() as session:
        project_user = ProjectUser()
        project_user.project_id = project_id
        project_user.user_id = user_uuid
        session.add(project_user)
        await session.commit()


async def get_project_by_title_description_and_user_login(title: str,
                                                          description: str,
                                                          user_login: str) -> Projects:
    async with async_session() as session:
        stmt = (select(Projects).
                where(Projects.title == title,
                      Projects.description == description,
                      Projects.user_login == user_login))
        result = await session.scalar(stmt)
        return result


async def get_project_by_title(title: str,
                               login: str) -> Projects:
    async with (async_session() as session):
        stmt = (select(Projects).
                where(Projects.title == title, Projects.user_login == login).
                order_by(Projects.created_at.asc()).
                limit(1))
        result = await session.scalars(stmt)
        return result.first()


async def delete_project_by_id(p_id: int) -> None:
    async with async_session() as session:
        project: Projects = await session.scalar(select(Projects).where(p_id == Projects.id))
        await session.delete(project)
        await session.commit()


async def get_project_by_id(project_id: int) -> Projects:
    async with async_session() as session:
        return await session.scalar(select(Projects).where(project_id == Projects.id))


async def get_projects_by_company(company_id: int) -> list[Projects]:
    async with async_session() as session:
        stmt = (select(Projects).
                where(Projects.company_id == company_id).
                order_by(Projects.title))
        result = await session.scalars(stmt)
        return result.all()


async def update_project_by_id(p_id: int, title: str, description: str) -> None:
    async with async_session() as session:
        stmt = (update(Projects).
        where(Projects.id == p_id).
        values(
            title=title,
            description=description
        ))
        await session.execute(stmt)
        await session.commit()


# Yandex Accesses
async def set_yandex_accesses(ya: YandexAccesses) -> None:
    async with async_session() as session:
        stmt = select(YandexAccesses).where(ya.project_id == YandexAccesses.project_id,
                                            ya.system_id == YandexAccesses.system_id)
        result = await session.execute(stmt)
        yandex_accesses = result.scalar()
        if yandex_accesses is not None:
            await session.delete(yandex_accesses)
        session.add(ya)
        await session.commit()


async def get_ya_accesses_by_project_and_system_id(p_id: int, s_id: int) -> YandexAccesses | None:
    async with async_session() as session:
        return await session.scalar(select(YandexAccesses).where(
            p_id == YandexAccesses.project_id, s_id == YandexAccesses.system_id))


# Yandex Direct Logins
async def add_ya_direct_logins(direct_login: YaDirectLogins) -> None:
    async with async_session() as session:
        stmt = select(YaDirectLogins).where(
            YaDirectLogins.direct_login == direct_login.direct_login,
            YaDirectLogins.project_id == direct_login.project_id
        )
        result = await session.execute(stmt)
        direct = result.scalar()

        if direct:
            direct.active = True
        else:
            session.add(direct_login)

        await session.commit()


async def set_ya_direct_login_status(l_id: int, status: bool) -> None:
    async with async_session() as session:
        stmt = select(YaDirectLogins).where(l_id == YaDirectLogins.id)
        result = await session.execute(stmt)
        login: YaDirectLogins = result.scalar()
        login.active = status
        await session.commit()


async def get_ya_direct_active_logins_by_p_id(p_id: int) -> list[YaDirectLogins]:
    async with async_session() as session:
        result = await session.scalars(select(YaDirectLogins).where(p_id == YaDirectLogins.project_id,
                                                                    YaDirectLogins.active))
        return result.all()


async def get_ya_direct_inactive_logins_by_p_id(p_id: int) -> list[YaDirectLogins]:
    async with async_session() as session:
        result = await session.scalars(select(YaDirectLogins).where(p_id == YaDirectLogins.project_id,
                                                                    YaDirectLogins.active == False))
        return result.all()


async def get_ya_direct_logins_by_project_id(p_id: int) -> list[YaDirectLogins]:
    async with async_session() as session:
        result = await session.scalars(select(YaDirectLogins).where(p_id == YaDirectLogins.project_id))
        return result.all()


# Yandex Metrika Counters
async def add_ya_metrik_counter(ya_metrika_counter: YaMetrikaCounters) -> None:
    async with async_session() as session:
        session.add(ya_metrika_counter)
        await session.commit()


async def update_ya_metrika_counter(metrika_counter_id: int, metrika: YaMetrikaCounters) -> None:
    async with async_session() as session:
        stmt = (
            update(YaMetrikaCounters).
            where(YaMetrikaCounters.id == metrika_counter_id).
            values(counter_name=metrika.counter_name,
                   counter_id=metrika.counter_id,
                   names_key_goals=metrika.names_key_goals,
                   names_minor_goals=metrika.names_minor_goals,
                   key_goals=metrika.key_goals,
                   minor_goals=metrika.minor_goals,
                   ecommerce=metrika.ecommerce)
        )
        await session.execute(stmt)
        await session.commit()


async def set_ya_metrik_attribution(p_id: int,
                                    attribution: str,
                                    minor_attribution: str) -> None:
    async with async_session() as session:
        stmt = (
            update(YaMetrikaCounters).
            where(YaMetrikaCounters.project_id == p_id).
            values(attribution=attribution, minor_attribution=minor_attribution)
        )
        await session.execute(stmt)
        await session.commit()


async def get_ya_m_list_counters_by_p_id(project_id: int) -> list[YaMetrikaCounters]:
    async with async_session() as session:
        result = await session.scalars(select(YaMetrikaCounters).where(
            YaMetrikaCounters.project_id == project_id
        ))
        return result.all()


async def get_ya_m_counter_by_id(counter_id: int) -> YaMetrikaCounters | None:
    async with async_session() as session:
        return await session.scalar(select(YaMetrikaCounters).
                                    where(counter_id == YaMetrikaCounters.id))


async def get_ya_metrik_counter_by_p_id(p_id: int) -> YaMetrikaCounters | None:
    async with async_session() as session:
        return await session.scalar(select(YaMetrikaCounters).
                                    where(p_id == YaMetrikaCounters.project_id))


async def get_ya_m_counters_id_by_p_id(p_id: int) -> list[int]:
    async with async_session() as session:
        stmt = (select(YaMetrikaCounters.counter_id).where(YaMetrikaCounters.project_id == p_id))
        result = await session.scalars(stmt)
        return result.all()


async def get_ya_m_counters_names_by_p_id(p_id: int) -> list[str]:
    async with async_session() as session:
        stmt = (select(YaMetrikaCounters.counter_name).where(YaMetrikaCounters.project_id == p_id))
        result = await session.scalars(stmt)
        return result.all()


async def get_ya_d_logins_names_by_p_id(p_id: int) -> list[str]:
    async with async_session() as session:
        stmt = (select(YaDirectLogins.direct_login).where(YaDirectLogins.project_id == p_id))
        result = await session.scalars(stmt)
        return result.all()


async def get_ya_active_d_logins_names_by_p_id(p_id: int) -> list[str]:
    async with async_session() as session:
        stmt = (select(YaDirectLogins.direct_login).where(YaDirectLogins.project_id == p_id,
                                                          YaDirectLogins.active))
        result = await session.scalars(stmt)
        return result.all()


# Project User
async def set_user_to_project(project_user: ProjectUser) -> None:
    async with async_session() as session:
        session.add(project_user)
        await session.commit()


async def get_managers_by_p_id(p_id: int) -> list[ProjectUser]:
    async with async_session() as session:
        result = await session.scalars(select(ProjectUser).where(p_id == ProjectUser.project_id))
        return result.all()


async def get_list_managers_by_p_id(project_id: int) -> list[Users]:
    async with async_session() as session:
        stmt = (select(Users).where(
            Users.role_id != 4,
            Users.id.in_(
                select(ProjectUser.user_id).where(ProjectUser.project_id == project_id)
        )))
        result = await session.scalars(stmt)
        return result.all()


async def get_available_managers_by_p_id(project_id: int, company_id: int) -> list[Users]:
    async with async_session() as session:
        stmt = (select(Users).
                where(Users.company_id == company_id, Users.active, Users.role_id != 4, ~Users.id.in_(
                    select(ProjectUser.user_id).where(ProjectUser.project_id == project_id)
        )))
        result = await session.scalars(stmt)
        return result.all()


async def remove_user_from_project(project_id: int, user_uuid: UUID) -> None:
    async with async_session() as session:
        project_user: ProjectUser = await session.scalar(select(ProjectUser).
                                                         where(project_id == ProjectUser.project_id,
                                                               user_uuid == ProjectUser.user_id))
        await session.delete(project_user)
        await session.commit()


async def remove_project_by_u_id(u_id: UUID) -> None:
    async with async_session() as session:
        project_users = await session.scalars(select(ProjectUser).
                                              where(u_id == ProjectUser.user_id))
        for project_user in project_users:
            await session.delete(project_user)
        await session.commit()


async def get_list_projects_by_user_uuid(user_uuid: UUID) -> list[Projects]:
    async with async_session() as session:
        stmt = select(Projects).where(Projects.id.in_(
            select(ProjectUser.project_id).where(user_uuid == ProjectUser.user_id)
        ))
        result = await session.scalars(stmt)
        return result.all()


async def get_available_projects_for_viewer(manager_uuid: UUID, viewer_uuid: UUID) -> list[Projects]:
    async with async_session() as session:
        stmt = (
            select(Projects)
            .where(Projects.id.in_(
                select(ProjectUser.project_id).where(~ProjectUser.project_id.in_(
                    select(ProjectUser.project_id).where(ProjectUser.user_id == viewer_uuid)),
                                                     ProjectUser.user_id == manager_uuid)
            ))
        )
        result = await session.scalars(stmt)
        return result.all()


async def get_report_project(project_id: int) -> str:
    async with async_session() as session:
        return await session.scalar(select(ProjectReport.report_url).where(ProjectReport.project_id == project_id))
