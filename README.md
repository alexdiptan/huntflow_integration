# Сервис интеграции с Huntflow
Сервис принимает вебхуки по кандидатам и вакансиям. 
 - При добавлении вакансии, происходит поиск кандидатов, по полю position. Если значение position кандидата 
и вновь созданной вакансии совпадают, первый найденный кандидат добавляется на начальный статус вакансии.
 - При переводе кандидата на статус hired кандидату добавляется метка "нанят". Если такой метки нет в 
организации, то она добавляется.

## Установка
### Выполнить последовательно команды:

1. Клонировать репозиторий и перейти в директорию
```
git clone https://github.com/alexdiptan/huntflow_integration.git
cd huntflow_integration
```
2. Создать виртуальное окружение и активировать его:
```
python3 -m venv my_env
source my_env/bin/activate
```
3. Установить зависимости:
```
pip install -r requirements.txt
```

## Настройка переменных окружения
Ожидается, что переменные окружения будут храниться в файле `.env`, который расположен в директории `config/`. 
Пример заполненного файла находится `config/.env_template`

Для начала, нужно переименовать файл: 
```
mv config/.env_template config/.env
```
### Описание незаполненных переменных окружения
- `HF_API_TOKEN` - токен полученный в интерфейсе Хантфлоу
- `ORG_ID` - id организации.
- `START_VACANCY_STATUS_ID` - id статуса вакансии "Новые". На этот статус будет попадать кандидат, который будет
автоматически назначен на вакансию при совпадении поля position.
- `HIRED_STATUS_ID` - id статуса вакансии с типом "hired". Обычно такой тип имеет статус "Офер принят".

## Запуск приложения
Для запуска приложения нужно выполнить команду:
```
python main.py
```

## Дополнительные настройки в Хантфлоу
После запуска приложения, вебхуки принимаются на порту 8000. Вебхуки по вакансиям и кандидатам доступны 
на эндпоинтах `/vacancy` и `/applicant` соответственно. Адрес для вебхуков нужно указать в интерфейсе Хантфлоу.
