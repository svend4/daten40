# IFOS 71601-72000 — Synthetic Monitoring & User Journeys

**Slug:** `synthetic_monitoring_user_journeys`  
**Категория:** Observability & Reliability · **Приоритет:** P2 · **Версия:** 0.29.0

## 1) Идея блока (зачем)
Реальные пользователи (RUM) и серверные метрики (APM/Logs) показывают, что проблема уже случилась.  
**Synthetics** позволяют обнаружить сбой раньше: система сама «играет роль пользователя», регулярно проверяя критические сценарии
(логин, поиск, оформление, оплату) и ключевые API (поиск, каталог, оплата, биллинг).

Цели:
- раннее обнаружение деградаций
- измерение доступности/latency по регионам
- контроль критических бизнес-джорни end-to-end
- "канареечные" проверки после релиза/фичефлага

## 2) Что делает блок (от простого к сложному)

### Уровень A — Базовые синтетические проверки
1. **HTTP/API checks**: status code, latency, body match, schema smoke.
2. **DNS/TCP/TLS checks**: разрешение домена, рукопожатие TLS, сертификаты.
3. **Ping/ICMP (опционально)**: доступность сети (в приватных сетях часто выключено).

### Уровень B — Browser/UI checks
4. Headless browser шаги: открыть страницу → клик → ввод → ожидание.
5. Скриншоты при ошибке, HAR/trace, console errors.
6. Тайм-ауты и ретраи (с защитой от "flapping").

### Уровень C — User Journeys (end-to-end)
7. Модель джорни (с шагами, ассертами, метками критичности).
8. Прогоны из разных регионов / POP / ISP (если есть).
9. Разделение по окружениям: `prod`, `staging`, `preview`.

### Уровень D — Интеграция с SRE/AIOps
10. Генерация сигналов:
   - алерт по SLO/availability
   - событие “journey failed”
   - regression event (latency ↑ после релиза)
11. Обогащение сигналов:
   - связка с `service_id` (по endpoint → сервису)
   - связка с релизами/фичефлагами
   - ссылка на runbook/owner (из Service Catalog)

## 3) Что блок НЕ делает
- Не заменяет RUM (это «роботы», а не реальные пользователи).
- Не гарантирует отсутствие ложных срабатываний (сеть/провайдеры).
- Не исполняет remediation сам (это делает workflow runner / on-call).

## 4) Сущности

### SyntheticCheck
- `check_id`, `name`, `type`: `api|dns|tls|browser`
- `target_url` / `host`
- `schedule`: cron/interval
- `regions[]`
- `timeout_ms`, `retries`
- `assertions[]` (status/body/schema/selector)
- `tags[]`: `journey:checkout`, `tier:critical`
- `owner_team`, `service_id` (или выводится через mapping)

### Journey
- `journey_id`, `name`, `criticality`
- `steps[]`: список шагов (action/selector/value/assert/screenshot_on_fail)
- `success_criteria`: p95 latency, availability threshold
- `links`: runbook, dashboard

### SyntheticResult
- `check_id`, `run_id`, `timestamp`, `region`
- `status`: pass/fail
- `latency_ms`
- `error_type`, `error_message`
- `artifacts`: screenshot, har, trace_id

## 5) API (минимальный)
- `POST /synthetics/checks` (create/update)
- `GET /synthetics/checks`
- `POST /synthetics/run` (ручной прогон)
- `GET /synthetics/results?check_id=...`
- `POST /journeys` (каталог джорни)
- `GET /journeys`
- `GET /journeys/{id}/runs`

## 6) MVP-алгоритмы
- Дедуп алертов (одинаковая ошибка в течение N минут → один инцидент).
- Quorum по регионам: алерт только если fail в ≥K регионах.
- Стабилизация flapping: require consecutive failures.

## 7) Зависимости (вход/выход)
Входы:
- 70801-71200 Progressive Delivery (релизы/канареечки)
- 51201-51600 Feature Flags (канареечные джорни по включению флага)
- 70001-70400 Load testing (сценарии можно переиспользовать)

Выходы:
- в AIOps (72401-72800) как сигнал `synthetic_failure`
- в Incident Response (69201-69600) как триггер
- в Service Catalog (72801-73200) для ownership/маршрутизации
