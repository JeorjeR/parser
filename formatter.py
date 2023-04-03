import re
import sys
from collections import deque
from collections.abc import Iterable, Mapping

from structure import HtmlTag

PARAMETERS = frozenset([
    'template',
    'max_line_length',
])

# TODO проверить на валидность параметры введенные пользователем

# TODO нужен перенос по словам текста


class FormatterHtmlContent:

    def __init__(self, html_tags: Iterable[HtmlTag], rules: Mapping):
        for tag_parameters in rules.values():
            if not set(tag_parameters.keys()).issubset(PARAMETERS):
                raise AttributeError(f'Неизвестный параметр')
        self.html_tags = html_tags
        self.tags_with_rules = rules
        self.current_line_length: int = 0

    def content_to_template(self, tag, tag_content) -> str:
        tag_rule = self.tags_with_rules.get(tag.name, None)
        if tag_rule:
            try:
                tag_template: str = tag_rule.get('template', '{}')
                return tag_template.format(tag_content)
            except AttributeError:
                sys.exit(f'Шаблон для тэга должен быть типа int: {tag_template}')
        return tag_content

    def split_text_to_word_iter(self, text: str, max_line_length: int):
        line_buffer = deque()
        last_word_end_index = 0
        for match in re.finditer(r'\b[^\s\b]+\b', text):
            if self.current_line_length > max_line_length:
                yield ' '.join(line_buffer)
                line_buffer.clear()
                line_buffer.append(word := match.group())
                self.current_line_length = len(word)
            else:
                end_word_index = match.end()
                self.current_line_length += end_word_index - last_word_end_index
                line_buffer.append(match.group())
                last_word_end_index = end_word_index
        yield ' '.join(line_buffer)
        self.current_line_length = 0

    def level_two(self, tag):
        content_buffer = []
        for element in tag.content:
            if isinstance(element, HtmlTag):
                content_part = self.level_two(element)
            else:
                content_part: str = '\n'.join(self.split_text_to_word_iter(element, 80))
            content_buffer.append(content_part)
        tag_content = ' '.join(content_buffer)
        content = self.content_to_template(tag, tag_content)
        return content

    def level_one(self):
        for tag in self.html_tags:
            yield self.level_two(tag)

    def get_text(self):
        return ''.join(self.level_one())


def format_html(tags: Iterable[HtmlTag], rules: Mapping) -> str:
    result_content: str = FormatterHtmlContent(tags, rules).get_text()
    return result_content

# def outer(self, content):
#     for element in content:
#         def inner():
#             nonlocal content
#             if isinstance(element, HtmlTag):
#                 content = element.content
#                 return ''
#             else:
#                 return '\n'.join(self.split_text_to_word_iter(element, 80))
#         yield inner
