import sys
from dataclasses import dataclass, field
from pathlib import PurePath
from types import MappingProxyType

import settings

URL_RULES: dict | None
FORMATTING_RULES: dict | None

STANDARD_RULES = dict(
    CUTTER_TAGS=frozenset({'article'}),
    TEXT_TAGS=frozenset({'p', 'h', 'b', 'li', 'i', 'a'}),
    IGNORE_TAGS=frozenset({}),
    CURRENT_DIRECTORY=PurePath(__file__).parent,
    MAX_LINE_LENGTH=80,
    URL_RULES={},
    FORMATTING_RULES={
        'p': {
            'template': '\n{}\n',
        },
        'h': {
            'template': '\n{}\n',
        },
        'b': {
            'template': ' {} ',
        },
        'li': {
            'template': '\n{}',
        },
        'a': {
            'template': '{}',
        },

    }
)


settings_vars = vars(globals().get('settings', None))
USER_SETTINGS = {
    key: value for key, value in
    settings_vars.items() if not
    (key.startswith('__') or key.startswith('_'))
}


unsupported_settings = set(USER_SETTINGS).difference(STANDARD_RULES)
if unsupported_settings:
    sys.exit(f'В файле настроек недопустимые параметры {unsupported_settings}')


def get_parameter(param_name: str):
    param_value = USER_SETTINGS.get(param_name, None)
    if not param_value:
        param_value = STANDARD_RULES.get(param_name)
    else:
        try:
            param_value_correct_type = type(STANDARD_RULES.get(param_name))
            if not isinstance(param_value, param_value_correct_type):
                param_value = param_value_correct_type(param_value)
        except TypeError as ex:
            sys.exit(f'Неверно задан параметр {param_name} - {ex}')
    return param_value


FORMATTING_RULES: MappingProxyType = MappingProxyType(get_parameter('FORMATTING_RULES'))


@dataclass(frozen=True, slots=True)
class Settings:
    cutter_tag: frozenset = get_parameter('CUTTER_TAGS')
    text_tag: frozenset = get_parameter('TEXT_TAGS')
    ignore_tag: frozenset = get_parameter('IGNORE_TAGS')
    formatter_rules: MappingProxyType = field(default_factory=lambda: FORMATTING_RULES)
    current_directory: str = get_parameter('CURRENT_DIRECTORY')
    max_line_length: int = get_parameter('MAX_LINE_LENGTH')


def get_standard_rules():
    return Settings()


def get_rules_for_url(url: str) -> Settings:
    # TODO не надо по конкретной ссылке искать в словаре, нужно обрезать ссылку до домена и искать по нему в словаре
    url_rules = get_parameter('URL_RULES')
    if url_rules:
        return url_rules.get(url, get_standard_rules())
    return get_standard_rules()




