# Парсер html сайтов на Python с использованием стандартных библиотек
### Запуск программы
```commandline
    python src\parse_url.py [ссылка на страницу]
```
## Пояснение к настройкам
Настройки задаются в файле `src\settings.py`. Допустимые параметры можно посмотреть в<br>
`src\rules.py` в переменной `STANDARD_RULES`
```
# Пример файла settings.py
URL_RULES = {
    'ссылка':
        {
            'TEXT_TAGS': ('h', 'p'),
            'FORMATTING_RULES':
                {
                    'p': {
                        'template': '\n[ПАРАГРАФ]{}[ПАРАГРАФ]\n',
                    },
                    'h': {
                        'template': '\n[ЗАГОЛОВОК]{}[ЗАГОЛОВОК]\n',
                    },
                    'b': {
                        'template': '[ЖИРНЫЙ ШРИФТ]{}[ЖИРНЫЙ ШРИФТ]',
                    },
                    'li': {
                        'template': '\n{}',
                    },
                    'a': {
                        'template': '[ГИПЕРССЫЛКА]{}[ГИПЕРССЫЛКА]',
                    },
                },
            'MAX_LINE_LENGTH': 20,
        }
}
CURRENT_DIRECTORY = r'C:\Egor\projects\pythonProject\tensor\result'

MAX_LINE_LENGTH = 80
```

## Алгоритм решения задачи
>1. С помощью регулярных выражений программа находит блок html страницы,<br>
>внутри которого расположен текст статьи. Весь текст выше этого тега обрезается.<br>
>>Наиболее вероятно, что текст будет
>>расположен внутри тэга `<article>`. Если статьи внутри этого тега нет, то <br> 
>>скорее всего он расположен внутри `<div class=...article...>`, если и здесь нет успеха,<br>
>>то текст статьи может лежать в `<div class=...content...>`. Тэги имеют приоритет в<br>
>>соответствующем порядке (*от самого важного в порядке убывания важности*)<br>
>>`<article>, <div class=...article...>, <div class=...content...>`<br>

>2. Обрезанный html передается в парсер.
>>### Алгоритм работы парсера
>>**Для удобства обозначим переменные:**<br>
>>`text_tag` - тэги, внутри которых будем считать, что есть текст.<br>
>>`content_tags` - список, в который записываются экземпляры класса `HtmlTag`.<br>
>>`HtmlTag(name: имя тэга, content: контент внутри тэга, parent: родительский тэг).`<br>
>>`current_html_tag` - последний открытый тэг (**экземпляр класса `HtmlTag`**).<br>
>>>Если встретился **открывающий** тэг из `text_tags`<br>
>>>1. Создаем экземпляр HtmlTag. В качестве родителя назначаем `current_html_tag`<br>
>>>>Если `current_html_tag` непустой, то добавляем HtmlTag в конец списка `conten`* переменой<br>
>>>>`current_html_tag`.<br>
>>>
>>>Присваиваем переменной `current_html_tag` ссылку на созданный HtmlTag 
>>
>>>Если встретился **закрывающий** тэг из `text_tags`<br>
>>>>Если у `current_html_tag` нет родителя, то добавляем `current_html_tag`<br>
>>>>в конец списка `content_tags`
>>>
>>>Меняем ссылку текущего тэга на ссылку его родителя `current_html_tag = current_html_tag.parent`<br>
>>
>>>Если встретился **контент** внутри тэга из `text_tags`<br>
>>>Добавляем его в конец списка content переменной `current_html_tag`<br>
>>
>>Алгоритм ведет стэк встретившихся тэгов, как только стэк становится пустым - парсинг заканчивается.<br>

>3. Далее происходит итерация по списку `content_tags`<br>
>>Каждый элемент списка `content_tags` передается в функцию. Функция либо форматирует и записывает<br>
>>(*в случае если элемент является строкой*) элемент в переменную, которая накапливает в себе весь контент,
>>либо рекурсивно вызывает себя, передавая в качестве аргумента элемент - `HtmlTag`.


