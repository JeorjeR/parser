import re
import sys
from pathlib import PurePath, Path
from urllib.parse import ParseResult, urlparse


class OutputContent:
    def __init__(self, url, content, current_directory=None):
        self.url = url
        self.content = content
        self.current_directory = current_directory

    @property
    def file_name(self):
        parse_url: ParseResult = urlparse(self.url)
        file_name = ''.join(parse_url[1:3])
        file_name = file_name[:-1] if file_name.endswith(r'/', -1) else file_name
        pure_path = PurePath(file_name)
        if suffixes := pure_path.suffixes:
            file_name = re.sub(r''.join(suffixes), '.txt', file_name)
        else:
            file_name += '.txt'
        if self.current_directory:
            try:
                file_name = PurePath(self.current_directory).joinpath(PurePath(file_name))
            except TypeError:
                sys.exit(f'Параметр CURRENT_DIRECTORY должен быть str, bytes или os.PathLike.'
                         f' Был передан {self.current_directory}')
        return file_name

    def _create_dirs_if_not_exists(self):
        pure_path = PurePath(self.file_name)
        path = Path(str(pure_path.parent))
        path.mkdir(parents=True, exist_ok=True)

    def output_content(self):
        self._create_dirs_if_not_exists()
        with open(self.file_name, 'w+', encoding='WINDOWS-1251', errors='replace', newline='') as file:
            file.write(self.content)
            return self.file_name


def write_content_to_file(url: str, content, current_directory: str) -> str:
    file_name: str = OutputContent(url, content, current_directory).output_content()
    return file_name
