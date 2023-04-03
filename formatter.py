import re
import sys
from collections import deque
from collections.abc import Iterable, Mapping
from rules import Settings
from structure import HtmlTag

PARAMETERS = frozenset([
    'template',
])

url_pattern = re.compile(
    r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b'
    r'(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$|'
    r'^[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&//=]*)$'
)


class FormatterHtmlContent:

    def __init__(self, html_tags: Iterable[HtmlTag], rules: Mapping, max_line_length: int):
        for tag_parameters in rules.values():
            if not set(tag_parameters.keys()).issubset(PARAMETERS):
                raise AttributeError(f'Неизвестный параметр')
        self.html_tags = html_tags
        self.tags_with_rules = rules
        self.current_line_length: int = 0
        self.max_line_length = max_line_length

    def _get_template(self, tag):
        tag_rule = self.tags_with_rules.get(tag.name, None)
        if tag_rule:
            return tag_rule.get('template', '{}')
        return '{}'

    def _content_to_template(self, tag, tag_content) -> str:
        try:
            tag_template: str = self._get_template(tag)
            return tag_template.format(tag_content)
        except AttributeError:
            sys.exit(f'Шаблон для тэга должен быть типа int: {tag_template}')

    def split_text_to_word_iter(self, text: str):
        line_buffer = deque()
        for match in re.finditer(r'\n|[^\s]+', text):
            word = match.group()
            if re.match(url_pattern, word):
                word = f'[{word}]'
            max_line_length = self.max_line_length - len(line_buffer)
            current_word_len = len(word)
            self.current_line_length += current_word_len + 1

            if word == '\n':
                self.current_line_length = 0
                continue
            if self.current_line_length > max_line_length:
                yield ' '.join(line_buffer)
                line_buffer.clear()
                line_buffer.append(word)
                self.current_line_length = len(word)
            else:
                line_buffer.append(word)

        yield ' '.join(line_buffer)

    def level_two(self, tag):
        if tag.content:
            content_buffer = []

            if self._get_template(tag).startswith('\n'):
                self.current_line_length = 0

            for element in tag.content:
                if isinstance(element, HtmlTag):
                    content_part = self.level_two(element)
                else:
                    content_part: str = '\n'.join(self.split_text_to_word_iter(element))
                content_buffer.append(content_part)

            if self._get_template(tag).endswith('\n'):
                self.current_line_length = 0

            tag_content = ' '.join(content_buffer)
            content = self._content_to_template(tag, tag_content)
            return content
        return ''

    def level_one(self):
        for tag in self.html_tags:
            yield self.level_two(tag)

    def get_text(self):
        return ''.join(self.level_one())


def format_html(tags: Iterable[HtmlTag], settings: Settings) -> str:
    result_content: str = FormatterHtmlContent(
        tags,
        settings.formatter_rules,
        settings.max_line_length,
    ).get_text()
    return result_content
