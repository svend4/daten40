# IFOS 20801–21200 — Marketplace Economics & Feedback‑OS: отзывы, сравнение, trust‑signals из эксплуатации, анти‑накрутка, цены/лицензии/партнёрки, “quality ladder”, витрины, рекомендации (v1)

Суть вашей идеи про “дикое поле интернета”:
- решений много,
- но **нет вертикали качества**, нет понятных витрин и нет “шкалы доверия”,
- отзывы либо отсутствуют, либо не сопоставимы, либо легко накручиваются,
- сравнение — в голове пользователя, а не в системе.

Marketplace Economics & Feedback‑OS делает “рынок функций” управляемым:
1) единые **отзывы/оценки** и агрегаты,
2) **сравнение** ассетов и “пакетов функций”,
3) **рекомендации** по задачам (intent‑based),
4) экономику: **цены, лицензии, партнёрки**,
5) **анти‑накрутка** и доказательные trust signals,
6) “quality ladder” — лестницу зрелости ассета,
7) витрины‑подборки (curations/portfolios),
8) A/B эксперименты (улучшение выдачи без гадания).

Ниже — от простого к сложному.

---

## 20801–20860 — Отзывы и оценки (простое)

### 20801) Review = атом обратной связи
Review обязателен быть структурированным:
- subject_id (что оценили)
- context (где использовали: локально/облако, размер потока)
- outcome (что получилось: success/partial/fail)
- pros/cons
- evidence refs (лог‑фрагменты без секретов, скриншоты, артефакты)
- moderation status

### 20830) Rating aggregate
Система хранит агрегат:
- mean / median
- distribution (1..5)
- confidence (чем больше реальных запусков, тем выше)
- decay (старые отзывы имеют меньший вес)
- verified_usage_ratio (сколько отзывов подтверждено реальными jobs)

---

## 20861–20930 — Сравнение (среднее)

### 20861) Comparison engine
Сравнение — это “таблица решений”:
- capabilities coverage
- стоимость (tokens/время/деньги)
- сложность настройки (1..5)
- trust score
- ограничения (permissions, регионы, тарифы)
- “операционные риски” (инциденты, fail‑rate)

### 20900) Compare bundles vs single assets
Пользователи хотят сравнивать не “плагин”, а “решение под задачу”:
- “News digest cluster” vs “News conference cluster”
- “Travel comparison portal blueprint” vs “affiliate travel plugin”

---

## 20931–21010 — Рекомендации (среднее → сложное)

### 20931) Intent‑based recommendation
Вход: intent + контекст пользователя (безопасно)
Выход: топ‑N с объяснениями:
- почему подходит (capabilities)
- какой риск (trust, incidents)
- какая цена (estimated cost)

### 20970) Cold start
Когда нет отзывов:
- weight on scans + smoke + SLO + publisher reputation
- “sandbox verified” бейдж
- “new but verified” категория

---

## 21011–21080 — Экономика: цены/лицензии/партнёрки (сложно)

### 21011) Pricing plans
Планы бывают:
- free / community
- subscription
- usage‑based (per job / per 1k items / per token)
- enterprise (контракт)

### 21040) Licenses
Лицензия — не “бумага”, а машиночитаемая политика:
- allowed uses
- redistribution
- attribution
- commercial use
- data restrictions

### 21060) Affiliate programs
Партнёрки встроены:
- tracking_id
- payout rules
- cookie window
- allowed traffic types
- compliance (anti‑fraud)

---

## 21081–21140 — Анти‑накрутка и trust signals (очень важно)

### 21081) Anti‑fraud signals
Сигналы:
- review velocity spikes
- same fingerprint reviewers
- low verified usage
- IP/device clustering
- identical review text
- publisher self‑review

### 21110) Verified usage
Review может иметь “verified” только если:
- есть job_id с реальным запуском
- smoke PASS хотя бы раз
- runtime logs подтверждают outcome (без секретов)

---

## 21141–21200 — Quality ladder, витрины и A/B (самое сложное)

### 21141) Quality ladder (лестница зрелости)
Уровни (пример):
- L0 Draft (нет smoke, нет scans)
- L1 Sandbox‑verified (smoke PASS)
- L2 Safe (scans PASS, signed, SBOM)
- L3 Reliable (SLO ok, incidents low)
- L4 Proven (many verified reviews)
- L5 Curated (в витрине/портфеле)

### 21170) Vitrines & portfolios
Витрина — это “подборка”:
- “Top 20 for news aggregation”
- “Starter kits for SMEs”
- “Make.com migration packs”
Портфель = набор витрин + стандарты.

### 21185) A/B experiments
Чтобы улучшать рекомендации:
- гипотеза
- метрики успеха (conversion, retention, success jobs)
- guardrails (не ухудшить безопасность/качество)

---

## Что лежит в пакете
- JSON Schemas: review, rating aggregate, comparison result, recommendation, pricing plan, license, affiliate program, anti-fraud signals, quality ladder, vitrines/portfolios, A/B experiment
- Specs: feedback/reviews, comparison engine, recommendations, pricing/licensing/affiliates, anti-fraud, quality ladder, vitrines/curations, A/B experiments
- OpenAPI: Marketplace Feedback API (MVP)
- Examples: “News Digest Cluster” (reviews+aggregates+comparison+recommendations+pricing+affiliate+anti-fraud+quality ladder+vitrine)
- Python skeletons: review moderation/scoring, comparison engine, recommendation ranker, pricing rules, anti-fraud detector
