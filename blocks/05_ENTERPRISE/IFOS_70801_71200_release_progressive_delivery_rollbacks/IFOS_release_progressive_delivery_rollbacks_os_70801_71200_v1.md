# IFOS Block 70801–71200: Progressive Delivery, Rollbacks & Safe Releases
**Slug:** `release_progressive_delivery_rollbacks`  
**Category:** Delivery & Reliability  
**Priority:** P1  
**Status:** MVP + Later design (spec)

## 1. Зачем этот блок
Цель — выпускать изменения безопасно: маленькими порциями, с автоматическими проверками, с быстрым откатом и понятными правилами “когда можно выкатывать”, а когда — стоп.

Ключевой принцип IFOS: **релиз = управляемый эксперимент под контролем SLO/SLI**, а не “нажали Deploy и молимся”.

## 2. Понятия (простые определения)
- **Progressive delivery** — поэтапная доставка: 1% → 5% → 25% → 100% трафика/пользователей.
- **Canary** — маленькая “канарейка” аудитории для раннего обнаружения проблем.
- **Rollout / Rollback** — раскат/откат версии.
- **Release gate** — “ворота” с условиями: без выполнения условий релиз не идёт дальше.
- **Bake time** — время “выдержки” на этапе (например, 30 минут на 5%).
- **Guardrail metrics** — “охранные” метрики: ошибки, latency, saturation, crash rate, churn.

## 3. MVP (что делаем в первую очередь)
### 3.1 Release plan как объект данных
**ReleasePlan** (простая структура):
- `release_id`, `service/app`, `version`
- `strategy`: canary | blue_green | rolling | shadow
- `stages`: список этапов (% трафика / сегмент пользователей / длительность bake)
- `gates`: список условий, которые должны быть “зелёными”
- `rollback_policy`: правила отката (авто/ручной), пороги, кто может override
- `approvals`: кто утверждает релиз (RACI, роли)
- `audit`: журнал всех действий

### 3.2 Stage-based rollout engine
MVP-движок выполняет этапы:
1) включает фичефлаги / маршрутизацию (traffic split) на нужный сегмент
2) ждёт bake-time
3) проверяет gates (SLO/SLI + guardrails)
4) либо переходит на следующий этап, либо запускает rollback

### 3.3 Gate checks (минимальный набор)
- Error rate ↑ (например, 5xx / total) выше порога
- Latency p95/p99 выше порога
- Saturation (CPU/mem/queue depth) выше порога
- Crash rate / fatal exceptions выше порога
- SLO burn-rate (ускоренный расход error budget) выше порога

### 3.4 Rollback
В MVP делаем 2 режима:
- **Auto-rollback**: если gate красный N минут подряд
- **Manual rollback**: кнопка + причина + ссылка на инцидент/тикет

### 3.5 UI минимально
- Экран релиза: этапы, текущее состояние, таймер bake-time, “почему стоп”
- Кнопки: Pause / Resume / Rollback / Promote
- Ссылки: метрики/дашборды, лог/трейсы, сравнение версий

## 4. Later (расширение)
### 4.1 Политики релизов (Policy Engine)
Пример политик:
- “В пятницу после 16:00 — запрещено”
- “Без зелёного SLO 24h — запрещено”
- “Требуется 2 approvals для production”
- “Платёжные компоненты — только blue/green”

### 4.2 Авто-диагностика причины
При красном gate:
- собрать “дифф” между версиями (фичи, конфиг, миграции)
- подсветить top offenders (endpoint, region, cohort)
- предложить действие: rollback / pause / расширить bake-time

### 4.3 Multi-service coordinated releases
- оркестрация зависимостей
- безопасный порядок (backend → api → ui)
- контракты и совместимость

### 4.4 Shadow + Mirroring
- shadow traffic (без влияния на пользователей)
- сравнение ответов (diff) + latency

## 5. API (контуры)
### 5.1 Write API (минимум)
- `POST /releases` создать ReleasePlan
- `POST /releases/<built-in function id>/start`
- `POST /releases/<built-in function id>/pause`
- `POST /releases/<built-in function id>/promote` (следующий stage)
- `POST /releases/<built-in function id>/rollback`
- `GET /releases/<built-in function id>` состояние
- `GET /releases/<built-in function id>/events` аудит

### 5.2 Интеграции
- Feature flags / remote config
- Observability (metrics, logs, traces)
- CI/CD (pipeline triggers)
- Incident/ticketing

## 6. Данные и аудит
Храним:
- все stage transitions
- значения метрик на момент решения
- кто нажал кнопку и почему
- ссылки на тикеты/инциденты/PR

## 7. Минимальный “one-click” сценарий (пример)
**Сценарий:** релиз коннектора Make/WordPress
1) Создали ReleasePlan: 1% 20 мин → 5% 30 мин → 25% 60 мин → 100%
2) Запуск релиза
3) На 5% вырос 500 error rate и burn-rate → auto-pause
4) Система показывает: “рост ошибок в endpoint /oauth/callback”
5) Нажали rollback, релиз закрыт, тикет создан

## 8. Выходы (deliverables)
- ReleasePlan schema + events schema
- MVP UI wireflow
- Policy templates (пачка правил)
- Rollback cookbook

---
