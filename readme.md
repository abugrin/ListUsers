Сохраняет ID, email, Имя и Фамилию всех пользователей организации Яндекс 360 в формате CSV

Необходимо в папку со скриптом положить файл ```.env``` содержащий

```
TOKEN =   # Токен доступа к API Яндекс 360, должен иметь права directory:read_users
ORG_ID =  # Organization ID.
PER_PAGE = 50  # Количество пользователей получаемых одним запросом. Рекомендуется 50 - 100
```

Создание токена: https://yandex.ru/dev/api360/doc/concepts/access.html


Установить зависимости
```pip install -r requirements.txt```

Запустить скрипт
```python listusers.py```

Пользователи будут импортированы в файл users.csv