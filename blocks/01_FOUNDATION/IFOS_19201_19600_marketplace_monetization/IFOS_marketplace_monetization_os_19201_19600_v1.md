# IFOS 19201–19600 — Marketplace & Monetization‑OS: витрины, цены, лицензии, биллинг, ревшэр, промо‑пакеты, “установка как сервис”, рейтинг (rating vs evidence) (v1)

Ваш тезис: **не изобретать новое, а рационализировать и компилировать готовое**.  
Тогда рынок должен уметь:
1) быстро **находить** модуль/кластер,  
2) гарантировать **качество** (см. блок 18801–19200),  
3) прозрачно **монетизировать** (цена/лицензия/выплаты),  
4) делать **установку/обновление** “одной кнопкой”.

Marketplace & Monetization‑OS — это “коммерческий слой” Internet Function OS.

Ниже — от простого к сложному.

---

## 19201–19250 — Витрина как продукт (простое)

### 19201) Marketplace listing = “обложка” ассета
Листинг — не маркетинговый текст, а **структурированный объект**:
- что это (категория/теги/совместимость)
- что делает (capabilities)
- как поставить (install profile + requirements)
- доказательства качества (quality_score + SLO + smoke/synthetic)
- цена/планы
- лицензия
- поддержка/контакты
- политика безопасности

### 19220) “Витрина‑кластер” (bundle showcase)
Для пользователя важны **кластеры**, а не “плагины по одному”:
- News Digest Cluster
- Travel Comparison Cluster
- WordPress Publishing Cluster
- CRM‑light Cluster (Make + Sheets + Telegram)

Витрина должна показывать:
- “что входит” (компоненты)
- “что будет на выходе” (output contracts)
- “сколько минут до первой пользы” (TTFS)

---

## 19251–19310 — Pricing & Entitlements (среднее)

### 19251) Pricing plan как объект
План содержит:
- тип: free / one‑time / subscription / usage
- цена + валюта
- ограничения: runs/day, connectors count, retention days
- что включено (features)
- пробный период
- политика возвратов

### 19280) Entitlement: “что разрешено именно этому клиенту”
Entitlement хранит:
- subject (tenant/user)
- purchased plan
- границы (limits)
- срок действия
- признак grace period (если платёж задержан)

Это критично, чтобы “одна кнопка” не превращалась в хаос доступа.

---

## 19311–19400 — Billing + Ledger (сложно, но обязательно)

### 19311) Billing event
События биллинга должны быть атомарными:
- purchase_created
- payment_succeeded / failed
- usage_reported
- refund_issued
- chargeback
- payout_scheduled

### 19340) Ledger (учётная книга) — источник истины
Зачем ledger:
- прозрачность расчётов
- аудит
- исправление ошибок (replay событий)
- честный ревшэр для издателей

**Принцип:** UI может ошибаться, ledger — нет.

---

## 19401–19470 — Revenue share & Payouts (очень сложно)

### 19401) Revshare policy
Ревшэр должен быть объектом:
- базовый процент
- промо‑кампании (временные исключения)
- “кто платит комиссии” (платформа/издатель/клиент)
- минимальный порог выплат
- удержания/резервы (на возвраты)

### 19430) Payout
Выплата включает:
- период расчёта
- список ledger entries
- итог
- удержания
- статус (scheduled/paid/failed)

---

## 19471–19530 — Reputation: rating vs evidence (сложнее)

### 19471) Разделяем 3 сигнала
- **rating**: субъективное мнение
- **evidence_score**: факты (runs/tests/SLO)
- **quality_score**: агрегированный скоринг (см. 18801–19200)

Marketplace показывает все 3, чтобы:
- убрать накрутку,
- дать честное сравнение,
- стимулировать авторов делать smoke/synthetic.

### 19510) Reviews как “структурные отзывы”
Не “нравится/не нравится”, а:
- какой use case
- какой stack (Make/n8n/WP)
- какие проблемы
- какой TTFS
- что улучшить

---

## 19531–19600 — Install/Update as a Service (самое сложное)

### 19531) Install Transaction = одна операция с rollback
Установка должна быть транзакцией:
- precheck (токены/requirements)
- resolve deps (bundles)
- apply (install/config)
- verify (smoke test)
- commit / rollback
- evidence record

### 19570) Update flow: canary + gates
Обновление идёт по гейтам:
- smoke PASS
- SLO без регрессии
- synthetic PASS (>=N)
- canary rollout
- full rollout

### 19590) “One‑click restore”
Если сломалось — откатить на прошлую версию:
- restore config snapshot
- rollback dependencies
- rerun smoke
- record incident draft (если нужно)

---

## Что лежит в пакете
- JSON Schemas: listing, pricing, license, entitlement, purchase, billing event, ledger entry, revshare, payout, promo pack, reputation summary, install transaction
- Specs: listing, pricing/entitlements, billing/ledger, reviews/reputation, install/update flow
- OpenAPI: marketplace/monetization API (MVP)
- Examples: “News Digest Cluster” как платный bundle
- Python skeletons: marketplace service, entitlement checker, billing ledger, payout calculator, reputation engine, review moderation
