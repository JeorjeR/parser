import re
import sys
from http.client import HTTPException
from urllib.error import URLError
from urllib.request import urlopen
from structure import HtmlTag
from formatter import format_html
from output import write_content_to_file
from parser import parse_html_with_rules
from rules import Settings, get_rules_for_url


class HtmlPage:
    """
    Класс html страницы, знает ссылку, html код, правила для парсинга страницы
    """
    def __init__(self, url: str):
        self.url = url

    @property
    def rules(self) -> Settings:
        return get_rules_for_url(self.url)

    @property
    def html(self) -> str:
        try:
            with urlopen(self.url, timeout=8) as response:
                charset = response.headers.get_content_charset()
                html: str = response.read().decode(charset)
                return html
        except (URLError, HTTPException, TimeoutError, ValueError) as ex:
            sys.exit(f'\rНе удалось открыть указанную ссылку {self.url}\n{ex}')

    def get_content(self) -> str:
        """
        Возвращает отформатированную статью со страницы
        """
        article_start_index: int = self.get_article_start_index()
        h = self.html[article_start_index:]
        tags_with_content: list[HtmlTag] = parse_html_with_rules(
            self.html[article_start_index:], self.rules.text_tags)

        content: str = format_html(tags_with_content, self.rules)
        return content

    def get_article_start_index(self) -> int:
        """
        Вычисляет индекс тэга, внутри которого лежит статья
        """
        content_pattern = self.rules.cutter_tag
        start_tag_iter = re.finditer(fr'{content_pattern}', self.html)
        content_start_index = None
        article_start_index = None
        for tag in start_tag_iter:
            try:
                if article := tag.group('article'):
                    article = article.lower()
                if content := tag.group('content'):
                    content = content.lower()

                if tag.group('start'):
                    return tag.start()
                elif article == 'article':
                    if not article_start_index:
                        article_start_index = tag.start()
                elif content == 'content':
                    if not content_start_index:
                        content_start_index = tag.start()
            except IndexError:
                return tag.start()

        if article_start_index:
            return article_start_index
        elif content_start_index:
            return content_start_index
        else:
            sys.exit('Не получилось найти контент на данной странице, '
                     'возможно неверно задан параметр CUTTER_TAG')


def start_parse(url: str) -> str:
    page = HtmlPage(url)
    content = page.get_content()
    file_name: str = write_content_to_file(url, content, page.rules.current_directory)
    return file_name
