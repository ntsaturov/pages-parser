# pages-parser
Manager of page-parser tasks

#### Solution description

```
Описание задачи в папке docs -> "task_description.pdf".
Решение:
Инициализируем 2 отдельных модуля - FastApi с двумя эндпоинтами (get-task-by-id и parse-page - для создания задачи) и в отдельном потоке TaskScheduler (thread-pool из n воркеров) для выполнения задач.
Принцип работы сервиса достаточно прост:
1. Создаем задачу через parse_page отправля url post-запросом;
2. Задача на парсинг попадает в очередь со статусом "0" - created;
3. Далее TaskScheduler берет из базы задачи и переводит их в статус "10" - in progress. 
P.S.: Для предотвращения гонок или одновременного выполнения одной и той же задачи из разных потоков или инстансев, берем задачи из базы следующим запросом 
"update tasks as b set status = 10 from (select * from tasks where status=0 order by creation_timestamp for update skip locked) as a where b.id = a.id  returning b.*;" 
блокируя выбранные записи на уровне таблицы с помощью "for update skip locked".
4. Далее парсим url из каждой задачи, получаем данные со страницы и переводим каждую из задач в статус 20 (если все прошло удачно), либо в статус 21 (если задача завершилась с ошибкой).
```

<img src="https://github.com/ntsaturov/pages-parser/blob/main/docs/schema.png" width="700" height="450">

#### Structure of DB table
```
id character varying(255) - UUID
execution_timestamp timestamp without time zone - время выполнения задачи
creation_timestamp timestamp without time zone - время создания задачи
status integer - статус задачи (0 - created, 10 - in progress, 20 - successfully finished, 21 - finished with error)
url character varying(500) - url-path
data text - результат выполнения задачи 
```

Примеры запросов:

##### 1. Создание задачи:
<br> Endpoint: /api/tasks/parse_page
<br>Method: Post
<br>Request:
```
{
  "url": "https://example.com"
}
```

Response:
```
{
    "execution_timestamp": null,
    "creation_timestamp": "2023-06-29T19:35:03.298296",
    "url": "https://example.com",
    "id": "823010f9-b43e-48bd-aaf2-69d55b17b9a3",
    "status": 0,
    "data": null
}
```

##### 2. Просмотр статуса задачи и результата:
<br>Endpoint: /api/tasks/957d326d-b9f9-4b05-ab13-1f3bdd136d6f
<br>Method: GET

Response:
```
{
    "id": "957d326d-b9f9-4b05-ab13-1f3bdd136d6f",
    "execution_timestamp": "2023-06-29T20:08:52.584707",
    "status": 20,
    "data": "{'tags': {'html': 1, 'head': 1, 'meta': 1, 'link': 1, 'title': 1, 'style': 1, 'script': 1, 'body': 1, 'input': 1, 'label': 1, 'div': 1, 'a': 1, 'aside': 1, 'button': 1, 'svg': 1, 'path': 1, 'header': 1, 'nav': 1, 'img': 1, 'span': 1, 'form': 1, 'ol': 1, 'main': 1, 'ul': 1, 'li': 1, 'article': 1, 'h1': 1, 'p': 1, 'strong': 1, 'em': 1, 'h2': 1, 'pre': 1, 'code': 1, 'dl': 1, 'dt': 1, 'dd': 1, 'footer': 1}, 'scripts': ['https://example.com/latest//flarelytics/client.js', 'https://example.com/latest/assets/javascripts/bundle.51d95adb.min.js', 'https://example.com/latest/extra/redirects.js']}",
    "creation_timestamp": "2023-06-29T20:08:51.584707",
    "url": "https://example.com"
}
```

#### Build and run docker-compose
```
    make run_app
```

#### Stop docker-compose
```
    make stop_app
```

#### Run project local without docker-compose
```
    poetry install
    poetry shell
    ./scripts/create-db-container.sh
    uvicorn run:app --reload
```
