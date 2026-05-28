# Data Contract — variant_04 (Лондон, архив погоды)

## 1. Источник данных

| Параметр | Значение |
|----------|----------|
| **Название API** | Open-Meteo Archive API |
| **Endpoint** | https://archive-api.open-meteo.com/v1/archive |
| **Метод** | GET |
| **Таймаут** | 15 секунд |

## 2. Параметры запроса

| Параметр | Значение |
|----------|----------|
| latitude | 51.5072 |
| longitude | -0.1276 |
| timezone | Europe/London |
| start_date | 2024-01-01 |
| end_date | 2024-01-07 |
| hourly | temperature_2m, relative_humidity_2m, precipitation, wind_speed_10m |

## 3. Формат ответа

- **Тип:** JSON
- **Часовые данные:** time, temperature_2m, relative_humidity_2m, precipitation, wind_speed_10m

## 4. Обработка ошибок

- Таймаут (>15 сек) → ошибка
- HTTP 400 → неверные даты
- Не JSON → ошибка

## 5. Сохранение

- **Путь:** `data/raw/variant_04/`
- **Формат имени:** `{start_date}_{end_date}_{timestamp}.json`