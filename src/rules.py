import sys
from dataclasses import dataclass, field
from pathlib import PurePath
from types import MappingProxyType

import settings

URL_RULES: dict | None
FORMATTING_RULES: dict | None
STANDARD_CUTTER_REGEX = (
    r'(<(div)[^<]*(class|id)="[^"]*((?P<article>[Aa]rticle)|'
    r'(?P<content>[Cc]ontent))[^>]*>)|(<(?P<start>article)[^>]*>)'
)


STANDARD_RULES = dict(
    CUTTER_TAG=STANDARD_CUTTER_REGEX,
    TEXT_TAGS=frozenset({'p', 'h', 'b', 'li', 'i', 'a'}),
    CURRENT_DIRECTORY=PurePath(__file__).parent,
    MAX_LINE_LENGTH=80,
    URL_RULES=MappingProxyType({}),
    FORMATTING_RULES=MappingProxyType({
        'p': {
            'template': '\n{}\n',
        },
        'h': {
            'template': '\n{}\n',
        },
        'b': {
            'template': '{}',
        },
        'li': {
            'template': '\n{}',
        },
        'a': {
            'template': '{}',
        },
    })
)


settings_vars = vars(globals().get('settings', None))
USER_SETTINGS = {
    key: value for key, value in
    settings_vars.items() if not
    (key.startswith('__') or key.startswith('_'))
}


def check_settings(standard_settings, other_settings):
    unsupported_settings = set(other_settings).difference(standard_settings)
    if unsupported_settings:
        sys.exit(f'В файле настроек недопустимые параметры {unsupported_settings}')


check_settings(STANDARD_RULES, USER_SETTINGS)


def get_parameter(standard_settings, other_settings, param_name: str) -> tuple:
    param_value = other_settings.get(param_name, None)
    if not param_value:
        param_value = standard_settings.get(param_name)
    else:
        try:
            param_value_correct_type = type(standard_settings.get(param_name))
            if not isinstance(param_value, param_value_correct_type):
                param_value = param_value_correct_type(param_value)
        except (TypeError, ValueError) as ex:
            sys.exit(f'Неверно задан параметр {param_name}\n{ex}')
    return param_name, param_value


def create_settings(standard_settings, other_settings) -> dict:
    check_settings(standard_settings, other_settings)
    settings_ = dict(get_parameter(standard_settings, other_settings, name) for name in standard_settings)
    return settings_


SETTINGS = create_settings(STANDARD_RULES, USER_SETTINGS)


@dataclass(frozen=True, slots=True)
class Settings:
    cutter_tag: frozenset = SETTINGS['CUTTER_TAG']  # Тэг, который содержит статью
    text_tags: frozenset = SETTINGS['TEXT_TAGS']  # Тэги, из которых буде тбраться контент
    formatting_rules: dict = field(default_factory=lambda: SETTINGS['FORMATTING_RULES'])  # Шаблоны для тэгов
    current_directory: str = SETTINGS['CURRENT_DIRECTORY']  # Директория, в которую записываются результаты
    max_line_length: int = SETTINGS['MAX_LINE_LENGTH']  # Максимальная длина строки


def get_rules():
    return Settings()


def get_rules_for_url(url: str) -> Settings:
    url_rules: dict = SETTINGS['URL_RULES']
    if rules := url_rules.get(url, None):
        if not isinstance(rules, dict):
            sys.exit(f'Неверно задан параметр URL_RULES')
        settings_: dict = create_settings(SETTINGS, rules)
        settings_.pop('URL_RULES')
        return Settings(**{name.lower(): value for name, value in settings_.items()})
    return Settings()
