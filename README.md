## Содержание
- Описание приложения <br/>
- Структура приложения <br/>
- Используемые библиотеки <br/>

## Описание клиента
Api-клиент, реализации api-клиента для сервиса микроблога <br/>
(ссылка) <br/>

## Структура api-клиента

- "/api/users/me" - GET: получение данных о авторизированном юзере<br/>
- "/api/users/<int:id>" - GET: получение данных о юзере<br/>
- "/api/users/<int:id>/follow" - POST/DELETE: добавление/удаление пользователя<br/>
- "/api/tweets" - GET/POST: получение/добавление постов<br/>
- "/api/tweets/<int:id>" - DELETE: удаление постов<br/>
- "/api/medias" - POST: добавление медиа<br/>
- "/api/tweets/<int:id>/likes" - POST: добавление/удаление лайков<br/>

## Используемые сторонние библиотеки
<table align="center">
    <tr>
        <td align="center">Package</td>
        <td align="center">Version</td>
    </tr>
    <tr>
        <td align="center">flask</td>
        <td align="center">2.2.2</td>
    </tr>
    <tr>
        <td align="center">SQLAlchemy</td>
        <td align="center">2.0.19</td>
    </tr>
    <tr>
        <td align="center">psycopg2-binary</td>
        <td align="center">2.9.6</td>
    </tr>
    <tr>
        <td align="center">Flask-RESTful</td>
        <td align="center">0.3.9</td>
    </tr>
    <tr>
        <td align="center">flasgger</td>
        <td align="center">0.9.7.1</td>
    </tr>
</table>
