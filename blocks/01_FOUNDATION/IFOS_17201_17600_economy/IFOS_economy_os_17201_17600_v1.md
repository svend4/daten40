# IFOS 17201–17600 — Economy‑OS: рейтинги/отзывы с доказательностью (evidence), биллинг, метрики маркетплейса, “прославление” лучших модулей и анти‑накрутка (v1)

То, что вы описали (“почему нет рекламы, славы, отзывов, вертикали качества?”) — не культурная проблема, а **отсутствие технического слоя**.
Economy‑OS добавляет слой экономической и репутационной логики поверх Registry‑OS + Governance‑OS + Execution‑OS + Knowledge‑OS.

Цель:
- **видимость** лучших компонентов (как “лучшие плагины”/“топ сценарии”)
- **понятные отзывы** (с контекстом и доказательностью)
- **честный рейтинг** (не только “звёзды”, а “звёзды × evidence”)
- **оплата и мотивация** (цены, usage, биллинг, revenue share)
- **анти‑накрутка** (фрод сигнал + модерация + санкции)

Ниже — по порядку, от простого к сложному.

---

## 17201–17260 — Базовые объекты: рейтинг, отзыв, evidence score (простое)

### 17201) Rating (агрегат)
Rating — агрегированная оценка ассета (function/recipe/bundle/plugin):
- средняя оценка
- количество отзывов
- распределение по звёздам
- доверительный интервал
- **evidence‑weighted score** (главное отличие)

### 17202) Review (отзыв как “структурированный протокол”)
Review включает:
- оценка (1..5)
- текст
- контекст (какой target: Make/n8n/WP/native, какой план установки)
- подтверждение использования (run references)
- заявленные проблемы/ошибки (ошибка 401, 429, schema mismatch)
- “что ожидал / что получил”

### 17203) Evidence Score
Evidence‑Score — коэффициент доверия к отзыву/рейтингу:
- подтверждённый запуск (Run PASS/WARN/FAIL)
- наличие smoke tests
- стабильность (N успешных запусков)
- наличие плейбуков/доков
- отсутствие фрод‑сигналов

Итог: **звёзды без evidence почти не влияют**, а verified usage влияет сильно.

---

## 17261–17340 — Pricing и Usage: как считать ценность (среднее)

### 17261) Pricing Plan
Нужно различать:
- free (open source/бесплатно)
- subscription (за время)
- usage‑based (за runs/шаги/байты/сообщения)
- revenue share (процент с продаж/лидов)

### 17262) Usage Record (metering)
Usage фиксируется автоматически из Execution‑OS:
- run duration, steps, network bytes
- calls to paid APIs (если есть)
- storage writes
- “premium features” flags

### 17263) Billing Invoice
Invoice строится из usage record + pricing plan:
- line items
- taxes (опционально позже)
- disputes link (в Governance‑OS)
- evidence link (почему начислили)

---

## 17341–17420 — Marketplace Metrics: метрики качества, понятности, скорости внедрения

### 17341) Метрики ассета
- install success rate
- time-to-first-success
- failure rate by error class
- documentation completeness (doc card score)
- tutorial coverage
- playbook coverage
- user retention (повторные запуски jobs)

### 17342) “Почему это лучше” — не маркетинг, а trace
Economy‑OS хранит **recommendation trace**:
- какие кандидаты сравнивались
- почему выбрали этот
- какие evidence/метрики влияли

Это превращает “рекламу” в объяснимый рейтинг.

---

## 17421–17510 — Promotion engine: “прославление” хороших модулей (высокий уровень)

### 17421) Promotion Rule
Правила видимости:
- поднять в выдаче, если evidence_score > X и install_success_rate > Y
- понизить, если фрод сигнал или много disputes
- выделить “editor’s pick” только при L2+ evidence

### 17422) Leaderboards
Панели “лучшее за неделю/месяц”:
- best stability
- fastest install
- best docs
- best value (price/quality)
- most reused in clusters

Важно: leaderboard строится *не по лайкам*, а по реальным эксплуатационным данным.

---

## 17511–17600 — Anti‑fraud: защита рейтингов и экономики (самое сложное)

### 17511) Типовые атаки
- накрутка отзывов (боты)
- “review bombing” конкурентов
- подмена run evidence
- аффилированные аккаунты
- “слив” промокодов для накрутки

### 17512) Anti‑fraud signals
- подозрительная плотность отзывов во времени
- много отзывов без verified usage
- повторяющиеся тексты/паттерны
- корреляции аккаунтов/тенантов
- несоответствие run logs заявлению в отзыве

### 17513) Связь с Governance‑OS
Anti‑fraud → санкции/апелляции:
- временная заморозка рейтинга
- скрытие отзывов
- требование доказательности (run refs)
- appeal workflow

---

## Приложения (в этом пакете)
- JSON Schemas: rating, review, evidence score, pricing plan, usage record, invoice, revenue share, antifraud signals, promotion rules, leaderboard
- Specs: ranking+evidence, reviews+reputation, billing+metering, market metrics, promotion visibility, anti-fraud
- OpenAPI: Economy API (MVP)
- Examples: rating/review/evidence/usage/invoice/revenue share/promo/leaderboard/antifraud signal
- Python skeletons: metering engine, ranking engine, invoice generator, promotion engine, antifraud engine
