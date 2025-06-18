import re


def check_format_login(text: str) -> str:
    pattern = r'^[a-zA-Z0-9]{4,20}$'
    if re.match(pattern, text):
        return text
    raise ValueError


def check_format_password(text: str) -> str | None:
    if text is None:
        return text
    pattern = r"^(?=.*[a-z])(?=.*\d)[a-zA-Z\d]{8,20}$"
    if re.match(pattern, text):
        return text
    raise ValueError


def check_format_company(text: str) -> str:
    pattern = r'^(?=.*[A-Za-zА-Яа-я\d])[\dA-Za-zА-Яа-я\W]{3,150}$'
    if re.match(pattern, text):
        return text
    raise ValueError


def check_format_title(text: str) -> str | None:
    if text is None:
        return text
    pattern = r"^(?=.*[A-Za-zА-Яа-я\d])[\dA-Za-zА-Яа-я\W]{3,}$"
    if re.match(pattern, text):
        return text
    raise ValueError


def check_format_list_logins(text: str) -> str | None:
    if text is None:
        return text
    pattern = r"^(?=.*[A-Za-zА-Яа-я\d])[\dA-Za-zА-Яа-я,\W]{2,}$"
    if re.match(pattern, text):
        return text
    raise ValueError
