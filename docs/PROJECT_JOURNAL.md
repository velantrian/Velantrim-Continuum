# 📓 Журнал Velantrim Continuum

Краткая история проекта. Для продолжения работы откройте [рабочую тетрадь](WORKBOOK.md). Текущий допуск к экспериментам указан в [project-state.json](../project-state.json).

## Что сделано

| Дата | Результат | Подтверждение |
| --- | --- | --- |
| 2026-11-26 | Pilot Safety вошёл в `main`. Исправлены учёт неопределённого исхода, конкурентное резервирование и допуск повторной попытки при ошибках журнала. CI на merge-коммите прошёл 3/3. | [PR #68](https://github.com/velantrian/Velantrim-Continuum/pull/68) · [Коммит](https://github.com/velantrian/Velantrim-Continuum/commit/7c5d1e89705d37cfb9f8546f1de76527d08e2ace) |
| 2026-10-18–26 | Добавлен Capture-адаптер OpenRouter и обработка неопределённых исходов и осиротевших попыток. | [PR #63](https://github.com/velantrian/Velantrim-Continuum/pull/63) · [PR #66](https://github.com/velantrian/Velantrim-Continuum/pull/66) · [PR #67](https://github.com/velantrian/Velantrim-Continuum/pull/67) |
| 2026-08-24 | Владелец разрешил подготовку ограниченного Pilot на F1-P-A. Допуск к запуску требует отдельного решения. | [PR #34](https://github.com/velantrian/Velantrim-Continuum/pull/34) |
| 2026-08-22 | Утверждённые человеком Gold и Oracle внесены в репозиторий. | [PR #28](https://github.com/velantrian/Velantrim-Continuum/pull/28) |
| 2026-08-15 | Заложена исследовательская основа Experiment 0. | [PR #1](https://github.com/velantrian/Velantrim-Continuum/pull/1) |

## Что дальше

Подтвердить точную конфигурацию F1-P-A, включая модель, настройки, доступ и бюджет, затем пройти этапы допуска. На момент записи от 26 ноября Pilot имеет статус `NOT_AUTHORIZED`. Подробности и критерии готовности находятся в [рабочей тетради](WORKBOOK.md).

## Рабочие ссылки

- [Трекер задач GitHub Issues](https://github.com/velantrian/Velantrim-Continuum/issues) — ссылки на работу в репозитории. Ссылку на отдельную рабочую доску предстоит уточнить.
- [Исследовательская страница проекта в Notion](https://app.notion.com/p/3bcac84d054781ebb7b3cbd281bdcdc6).
- [Исторический реестр аудита и будущих работ](ai/AUDIT_AND_FUTURE_WORK.md) — ранние контрольные точки и исследовательские вопросы.

Добавляйте запись, когда появляется подтверждённый результат или принятое решение. Укажите дату, итог и ссылку на PR, коммит либо решение владельца. Для журналируемых экспериментов указывайте, был ли результат получен в синтетической проверке, Pilot или Evidence.
