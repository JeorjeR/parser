import itertools
import sys
from threading import Event, Thread

from start_parse_url import start_parse

# url = sys.argv[1]


# url = 'https://lenta.ru/news/2023/03/30/nizhepoyasa/'
# url = 'https://habr.com/ru/post/721788/'
# url = 'https://www.gazeta.ru/politics/news/2023/03/30/20098033.shtml'
# url = 'https://www.gazeta.ru/comments/column/kolesnikov/14779778.shtml'
# url = 'https://www.rbc.ru/business/31/03/2023/6425abb79a79477297e32c03?from=from_main_2'
url = 'https://habr.com/ru/company/rshb/blog/726690/'


# TODO !!!! обработать ошибку если не нашли начало блока article иначе вылетает nontype hasnt stert()


# TODO в целом все сделано, но необходимо решить следующе вопросы
#   1. Как определять с какого тэга начинать читать контент, то есть в файле настроек дать возможность ввести название
#       тега и его класс допустим, потом парсер как то должен найти этот тег


def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle('.'*idx for idx in range(15)):
        status = f'\r{msg} {char}'
        print(status, end='', flush=True)
        if done.wait(.1):
            break
        blanks = ' ' * len(status)
        print(f'\r{blanks}\r', end='')


def supervisor():
    done = Event()
    spinner = Thread(target=spin, args=('Processing', done))
    spinner.start()
    try:
        file_name = start_parse(url)
    finally:
        done.set()
    return file_name


def main():
    file_name = supervisor()
    print('\rФайл со статьей успешно создан по пути', f'{file_name}', sep=' ')


ERROR_MESSAGE = '\rПрограмма преждевременно завершила работу '


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(ERROR_MESSAGE, file=sys.stderr)
    except:
        print(ERROR_MESSAGE, file=sys.stderr)
        raise