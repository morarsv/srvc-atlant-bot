from typing import Optional
from pydantic import BaseModel, ConfigDict


class SRoles(BaseModel):
    role_id: Optional[int] = None
    role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class SCompanies(BaseModel):
    company_id: Optional[int] = None
    company: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class SProjects(BaseModel):
    project_id: Optional[int] = None
    title: Optional[str] = None
    company_id: Optional[int] = None
    user_login: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class SProjectUser(BaseModel):
    project_id: Optional[int] = None
    user_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
