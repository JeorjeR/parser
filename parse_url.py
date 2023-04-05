import itertools
import sys
from threading import Event, Thread

from html_initialization import start_parse

url = sys.argv[1]


def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle('.'*idx for idx in range(15)):
        status = f'\r{msg} {char}'
        print(status, end='', flush=True)
        if done.wait(.1):
            break
        blanks = ' ' * len(status)
        print(f'\r{blanks}\r', end='')


def supervisor(url_):
    done = Event()
    spinner = Thread(target=spin, args=('Processing', done))
    spinner.start()
    try:
        file_name = start_parse(url_)
    finally:
        done.set()
    return file_name


def main(url_):
    file_name = supervisor(url_)
    print('\rФайл со статьей успешно создан по пути', f'{file_name}', sep=' ')


ERROR_MESSAGE = '\rПрограмма преждевременно завершила работу '


if __name__ == '__main__':
    try:
        if not url:
            sys.exit('Ссылка не была передана в программу')
        main(url)
    except KeyboardInterrupt:
        print(ERROR_MESSAGE, file=sys.stderr)
    except AssertionError as ex:
        print(ERROR_MESSAGE, ex, sep='\nСкорее всего html страница некорректно обработалась парсером\n', file=sys.stderr)
    except:
        print(ERROR_MESSAGE, file=sys.stderr)
        raise
