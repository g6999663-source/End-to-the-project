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
- ## 7. Normalized слой (после очистки)

**Зерно таблицы:** одна строка = один час (одна временная точка архива)

| Поле | Тип | Nullable | Описание |
|------|-----|----------|-----------|
| datetime_utc | datetime64[ns] | No | Временная метка (UTC) |
| temp_c | float64 | No | Температура воздуха на высоте 2 м, °C |
| rel_humidity_percent | float64 | No | Относительная влажность, % |
| precip_mm | float64 | No | Осадки, мм |
| wind_kmh | float64 | No | Скорость ветра на высоте 10 м, км/ч |
| city | object (str) | No | Название города (London) |
| variant_id | object (str) | No | Идентификатор варианта (04) |

**Выполненные шаги очистки:**
1. Преобразование `timestamp` из строки в тип `datetime`.
2. Заполнение пропусков в `precipitation` нулями (если были).
3. Удаление дубликатов строк (если были).
4. Переименование колонок для удобства.
5. Проверка диапазонов значений (выбросы не обнаружены).