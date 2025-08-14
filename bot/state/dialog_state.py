from aiogram.fsm.state import State, StatesGroup


class AuthorizationSG(StatesGroup):
    PREVIEW = State()
    INPUT_LOGIN = State()
    INPUT_PASSWORD = State()
    FAIL = State()


class StartSG(StatesGroup):
    PREVIEW = State()
    ATTENTION_PROJECT = State()
    COMPANY_REPORT = State()


class AtlantAdministrationSG(StatesGroup):
    PREVIEW = State()
    ADD_USER = State()
    LIST_COMPANIES = State()
    CARD_COMPANY = State()
    LIST_USERS = State()
    LIST_PROJECTS = State()


class AtlantAdministrationAddCompanySG(StatesGroup):
    PREVIEW = State()
    INPUT_COMPANY = State()


class AtlantAdministrationEditAddUserSG(StatesGroup):
    PREVIEW = State()
    INPUT_USERNAME = State()
    INPUT_LOGIN = State()
    INPUT_PASSWORD = State()


class AtlantAdministrationUserSG(StatesGroup):
    PREVIEW = State()


class AtlantAdministrationProjectSG(StatesGroup):
    PREVIEW = State()
    LIST_COUNTRIES = State()
    COUNTER = State()


class MainSG(StatesGroup):
    MAIN = State()


class HelpSG(StatesGroup):
    MAIN = State()
    REQUEST = State()


class FaqSG(StatesGroup):
    MAIN = State()
    TEXT = State()


class ProjectsSG(StatesGroup):
    PREVIEW = State()
    LIST_PROJECTS = State()
    INFO_PROJECT = State()
    ADD_SERVICE = State()
    YA_ACCESS = State()
    REPORT = State()


class ProjectsEditAddSG(StatesGroup):
    PREVIEW = State()
    INPUT_TITLE = State()
    INPUT_DESCRIPTION = State()


class ProjectCommentSG(StatesGroup):
    PREVIEW = State()
    INPUT_TEXT = State()
    INPUT_DATE = State()
    INFO = State()


class YaMetrikaCountersSG(StatesGroup):
    PREVIEW = State()
    KEY_ATTRIBUTION = State()
    MINOR_ATTRIBUTION = State()
    ATTRIBUTION = State()


class YaMetrikaCountersEditAddSG(StatesGroup):
    COUNTERS = State()
    ATTRIBUTION = State()
    MINOR_ATTRIBUTION = State()
    KEY_GOALS = State()
    MINOR_GOALS = State()
    ECOMMERCE = State()
    PREVIEW = State()


class YaDirectLoginsSettingsSG(StatesGroup):
    PREVIEW = State()
    ACTIVATE = State()
    DEACTIVATE = State()


class YaDirectLoginsAddSG(StatesGroup):
    PREVIEW = State()
    AGENCY = State()
    REPRESENTATIVE = State()
    ADVERTISER = State()


class YaDirectLoginsAddAgencySG(StatesGroup):
    PREVIEW = State()


class YaDirectLoginsAddAdvertiserSG(StatesGroup):
    PREVIEW = State()


class YaDirectLoginsAddRepresentativeSG(StatesGroup):
    PREVIEW = State()
    INPUT_LOGINS = State()
    LIST_LOGINS = State()


class ViewersSG(StatesGroup):
    PREVIEW = State()
    LIST_VIEWERS = State()
    INFO_VIEWER = State()
    LIST_PROJECTS = State()


class ViewersAddUserSG(StatesGroup):
    PREVIEW = State()
    INPUT_USERNAME = State()
    INPUT_LOGIN = State()
    INPUT_PASSWORD = State()


class CompanyAdminSG(StatesGroup):
    PREVIEW = State()
    LIST_USERS = State()
    LIST_PROJECTS = State()


class CompanyAdminAddEditUserSG(StatesGroup):
    INPUT_USERNAME = State()
    INPUT_LOGIN = State()
    INPUT_PASSWORD = State()
    PREVIEW = State()


class CompanyAdminProjectsSG(StatesGroup):
    PREVIEW = State()
    LIST_YA_COUNTERS = State()
    LIST_AVAILABLE_MANAGERS = State()
    LIST_CONNECTED_MANAGERS = State()
    YA_COUNTER = State()


class ConnectUserSG(StatesGroup):
    PREVIEW = State()
    INPUT_USERNAME = State()
    INPUT_COMPANY = State()
    APPLICATION_FORM = State()


class InfoSG(StatesGroup):
    PREVIEW = State()
