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
6. ## Week 4 — Mart (Группировки и агрегаты)

### Что сделано
- normalized-данные (почасовые) агрегированы в дневную витрину
- добавлен `city_id = 'GB_LON'` (из конфига variant_04.yml)
- использован справочник `configs/cities.csv` (содержит city_id, city_name, country_code)
- выполнен `LEFT JOIN` по `city_id`
- проверено отсутствие many‑to‑many (число строк не изменилось)
- рассчитаны KPI согласно варианту

### Гранулярность
Одна строка = один день (для Лондона)

### KPI витрины
- `avg_temp_c` – средняя температура за день, °C
- `max_temp_c` – максимальная температура за день, °C
- `total_precip_mm` – сумма осадков за день, мм
- `rainy_hours` – количество часов с осадками > 0
- `max_wind_kmh` – максимальная скорость ветра за день, км/ч

*(дополнительно: топ‑5 дней по ветру – как пример использования витрины)*

### Результат
Витрина сохраняется в: `data/mart/variant_04/mart_daily_YYYY-MM-DD_HH-MM-SS.csv`

### Итог
Собран полный pipeline:  
`raw JSON (Open‑Meteo Archive)` → `normalized CSV (почасовой)` → `mart CSV (суточный)`

### Схема витрины (mart)

| Поле | Тип | Описание |
|------|-----|-----------|
| date | object (date) | Дата (UTC) |
| avg_temp_c | float64 | Средняя температура за день, °C |
| max_temp_c | float64 | Максимальная температура за день, °C |
| total_precip_mm | float64 | Сумма осадков, мм |
| rainy_hours | int64 | Количество часов с осадками > 0 |
| max_wind_kmh | float64 | Максимальная скорость ветра, км/ч |
| city_id | object | Код города (GB_LON) |
| city_name | object | Название города (Лондон) |
| country_code | object | Код страны (GB) |