import re
from collections.abc import Iterable
from html.parser import HTMLParser

from structure import HtmlTag

from collections import deque


class StopParsing(Exception):
    """
    Класс исключения для остановки парсинга html стрыницы
    """
    def __init__(self, *args, **kwargs):
        self.data = kwargs.pop('data', None)

    def __str__(self):
        return f'{self.__class__.__name__}, parsing is ending'


STARTEND_TAGS = {'img', 'link', 'meta', 'input', 'br'}


class HTMLParserWithRules(HTMLParser):

    def __init__(self, *, convert_charrefs=True, rules: Iterable[str]):
        if not rules:
            raise TypeError('arg rules must be Rules object')
        super().__init__(convert_charrefs=convert_charrefs)

        self.current_html_tag: HtmlTag | None = None

        self.content_tags: list[HtmlTag] = []
        self._name_tags: deque[str] = deque()
        self._pattern: re.Pattern = re.compile(
            r'|'.join(
                fr'^{tag}$' if
                tag != 'h' else
                fr'^{tag}\d*$' for
                tag in rules
            )
        )

    def feed(self, data: str) -> None:
        try:
            super().feed(data)
        except StopParsing:
            ...

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ...

    def handle_starttag(self, tag, attrs):
        if tag in STARTEND_TAGS:
            self.handle_startendtag(tag, attrs)
        else:
            if self._pattern.match(tag):
                name_tag = 'h' if tag[0] == 'h' else tag
                html_tag = HtmlTag(name=name_tag, content=[], parent=self.current_html_tag)
                if self.current_html_tag:
                    self.current_html_tag.content.append(html_tag)
                self.current_html_tag = html_tag

            self._name_tags.append(tag)

    def handle_endtag(self, tag):
        if tag in STARTEND_TAGS:
            self.handle_startendtag(tag, [])
        else:
            if self._pattern.match(tag):
                assert self.current_html_tag, 'Встретился закрывающий тэг, но self.current_html_tag пустой!'
                if not self.current_html_tag.parent:
                    self.content_tags.append(self.current_html_tag)
                self.current_html_tag = self.current_html_tag.parent

            last_open_tag = self._name_tags.pop()

            assert last_open_tag == tag, f'last_open_tag:{last_open_tag} != tag:{tag}'

            if not self._name_tags:
                raise StopParsing(data=self.content_tags)

    def handle_data(self, data):
        if self.current_html_tag:
            if self._pattern.match(self.current_html_tag.name):
                if not re.match(r'^[\s\n]*$', data):
                    self.current_html_tag.content.append(data)


def parse_html_with_rules(html: str, rules) -> list[HtmlTag]:
    parser = HTMLParserWithRules(rules=rules)
    parser.feed(html)
    content_tags: list[HtmlTag] = parser.content_tags
    return content_tags
