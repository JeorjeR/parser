import itertools
import sys
from threading import Event, Thread

from start_parse_url import start_parse

# url = argv[1]
# url = 'https://lenta.ru/news/2023/03/30/nizhepoyasa/'
# url = 'https://habr.com/ru/post/721788/'
# url = 'https://www.gazeta.ru/politics/news/2023/03/30/20098033.shtml'
url = 'https://www.gazeta.ru/comments/column/kolesnikov/14779778.shtml'
# url = 'https://www.rbc.ru/business/31/03/2023/6425abb79a79477297e32c03?from=from_main_2'

# TODO накинуть кода для того чтобы можно было узнать информацию о программе и тд, короче как консольную утилиту сделать
#   также засунуть в асинхронность чтобы пока программа работает в консоль выводилась загрузка

# TODO в целом все сделано, но необходимо решить следующе вопросы
#   1. Как определять с какого тэга начинать читать контент, то есть в файле настроек дать возможность ввести название
#       тега и его класс допустим, потом парсер как то должен найти этот тег
#   2. Обработать ошибочные ситуации в программе, неверные данные в настройках, плохая url, в общем все что зависит от
#        ввода пользователем

# TODO текущие недочеты
#   1. В тексте пропал все запятые из-за неверного регулярного выражения
#   2. Из-за того что ключ словаря просто h  на самом деле тэги то h{цифра} то шаблон для тэгов не работает
#   3. Снос строки считается в рамках одной текстовой конструкции а не в рамках всего текста


def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.1):
            break
        blanks = ' ' * len(status)
        print(f'\r{blanks}\r', end='')


def supervisor():
    done = Event()
    spinner = Thread(target=spin, args=('Processing....', done))
    spinner.start()
    try:
        file_name = start_parse(url)
    finally:
        done.set()
    return file_name


def main():
    file_name = supervisor()
    print('\rФайл со статьей успешно создан по пути', f'{file_name}', sep=' ')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\rПрограмма преждевременно завершила работу', file=sys.stderr)
    except:
        print('\rПрограмма преждевременно завершила работу', file=sys.stderr)
        raise
