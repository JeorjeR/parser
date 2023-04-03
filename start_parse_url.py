import re
import sys
from urllib.error import URLError
from urllib.request import urlopen
from structure import HtmlTag
from formatter import format_html
from output import write_content_to_file
from parser import parse_html_with_rules
from rules import Settings, get_rules_for_url


# TODO изменить название класса
class HtmlPage:
    def __init__(self, url: str):
        self.url = url

    @property
    def rules(self) -> Settings:
        return get_rules_for_url(self.url)

    @property
    def html(self) -> str:
        try:
            with urlopen(self.url, timeout=5) as response:
                charset = response.headers.get_content_charset()
                html: str = response.read().decode(charset)
                return html
        except URLError:
            sys.exit(f'\rНе удалось открыть указанную ссылку {self.url}')

    def get_content(self) -> str:
        article_start_index: int = get_article_start_index(self.html[:])

        tags_with_content: list[HtmlTag] = parse_html_with_rules(
            self.html[article_start_index:], self.rules.text_tag)

        content: str = format_html(tags_with_content, self.rules.formatter_rules)
        return content


def get_article_start_index(html: str) -> int:
    article_start_index: int = re.search(
        r'<article[^>]*>', html).start()
        # r'<article[^>]*>|<div[^>]+class="[^>"]+([Aa]rticle)[^>]+>', html).start()
    return article_start_index


def start_parse(url: str) -> str:
    page = HtmlPage(url)
    content = page.get_content()
    file_name: str = write_content_to_file(url, content, page.rules.current_directory)
    return file_name
