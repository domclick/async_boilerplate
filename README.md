# async_boilerplate

[![License: MIT](https://img.shields.io/badge/licence-MIT-orange)](https://github.com/domclick/async_boilerplate/blob/master/LICENSE.md)
![](https://img.shields.io/badge/python-3.8-blue)

Пример асинхронного веб-сервера на Sanic.

Статья на Habr - https://habr.com/ru/company/domclick/blog/531254/

Основной функционал:
- Веб сервер
- Работа с очередями rabbitMQ
- Запуск периодических заданий


## Установка
Для работы необходим Python версии 3.8

Зависимости ставятся командой `pip install -r requirements.txt`

## Команды для запуска
Для локального запуска необходимо поднять бд и rabbitMQ командой `docker-compose up` и прогнать миграции командой `alembic upgrade head`

Веб-сервер — `python manage.py run`

Консьюмеры — `python manage.py consume`

Кроны — `python manage.py schedule`


## Author
- [Semin Ivan](https://github.com/iasemin) (Author)

## Contributor Notice

We are always open for contributions. Feel free to submit an issue
or a PR. However, when submitting a PR we will ask you to sign
our [CLA (Contributor License Agreement)][cla-text] to confirm that you
have the rights to submit your contributions and to give us the rights
to actually use them.

When submitting a PR our special bot will ask you to review and to sign
our [CLA][cla-text]. This will happen only once for all our GitHub repositories.

## License

Copyright Ⓒ 2020 ["Sberbank Real Estate Center" Limited Liability Company](https://domclick.ru/).

[MIT License](./LICENSE.md)