# IFOS 33201–33600 — Data Quality & Dedup OS (v1)
Цель: превратить “дикое поле интернета” в **учтённую, нормализованную и не-дублирующуюся** базу функций.
Без этого Registry превращается в мусор:
- одинаковые плагины/сценарии под разными именами,
- разные версии и форки,
- битые ссылки,
- неполные карточки,
- конфликтующие свойства.

Data Quality OS отвечает за:
- импорт из источников (GitHub/WordPress/Make/App stores/каталоги),
- нормализацию и унификацию полей,
- создание канонических (CanonicalItem) карточек,
- дедупликацию (fingerprints + similarity),
- merge/conflict resolution,
- “source of truth” (какой источник доверительнее),
- качество (DQ score) и аудит изменений.

Порядок: простое → среднее → сложное.

---

## 33201–33230 — DQSource и RawItem: “как есть”
### DQSource
Описание источника импорта:
- тип: github_repo, wp_directory, make_templates, app_store, custom_feed
- режим: full scan / incremental
- доверие/приоритет (используется в TruthPolicy)

### RawItem
Не трогаем оригинал: сохраняем “как есть” + ссылки/метаданные.
Это важно для:
- повторной нормализации по новым правилам,
- доказательства происхождения,
- восстановления после ошибок нормализации.

---

## 33231–33280 — Normalization: привести к одному языку полей
Normalization — это набор правил (NormalizeRule):
- привести названия (title casing, убрать мусорные слова),
- унифицировать категории/теги,
- сопоставить auth/inputs/outputs,
- выделить “capabilities”,
- вытащить зависимости (deps) и ограничения (constraints),
- распознать “тип артефакта” (wp plugin / make scenario / docker image / npm pkg).

Результат: CanonicalItem (каноническая карточка).

---

## 33281–33340 — Fingerprints: быстрые “отпечатки” для дедупа
Чтобы искать “то же самое”, нужны отпечатки:
- url_fingerprint (нормализованный URL)
- code_fingerprint (repo+path+hash)
- name_fingerprint (очищенное название + vendor)
- capability_fingerprint (набор возможностей)
- io_fingerprint (inputs/outputs схема)

Fingerprint нужен для:
- поиска кандидатов на дедуп,
- ускорения сравнения (сначала cheap checks, потом deep similarity).

---

## 33341–33410 — DedupCandidate: кандидаты на совпадение
DedupCandidate — это пара (A,B) + score + объяснение:
- score 0..1
- evidence: какие fingerprints совпали, какие поля похожи
- recommendation: merge / keep separate / needs review

Стратегия:
- 0.95+ автослияние (по строгим правилам)
- 0.75–0.95 в очередь на review
- <0.75 оставляем как разные

---

## 33411–33490 — Merge & Conflict: как объединять без потерь
### MergeProposal
Предлагает объединение:
- кто “главный” (primary)
- что переносим (fields)
- что остаётся как alias/redirect
- что конфликтует

### Conflict
Типы конфликтов:
- разные авторы/лицензии
- разные цены/планы
- разные capabilities (несовместимо)
- разные источники и версии

### MergeDecision
Результат решения (auto или human):
- merged / rejected / deferred
- audit trail: кто решил и почему
- последствия: redirects, aliases, update references

---

## 33491–33540 — TruthPolicy: “какому источнику верить”
TruthPolicy задаёт приоритеты:
- официальный каталог (wp.org) > сторонний список
- repo владельца > форк
- подписанные артефакты > неподписанные
- свежий релиз > древний архив

TruthPolicy используется при merge:
- если 2 источника дают разные поля, выбираем по приоритетам
- сохраняем attribution (откуда взято).

---

## 33541–33580 — Attribution и DQ Score
### Attribution
Каждое поле в CanonicalItem можно сопровождать:
- source_id
- raw_ref
- retrieved_at
- confidence

### DQScore
Оценка качества карточки:
- completeness (есть ли минимальные поля)
- freshness (давность обновления)
- trust (надежность источников)
- installability (есть ли recipe)
- docs_quality (наличие/структура документации)

Эта оценка влияет на:
- ранжирование в поиске,
- попадание в “витрины”,
- автослияние.

---

## 33581–33600 — Import Jobs: конвейеры импорта
ImportJob описывает:
- источник
- стратегию (full/incremental)
- стадия: fetch → parse → normalize → dedup → merge → publish
- статистику (сколько новых/обновлённых/дубликатов)
- “quarantine” для подозрительных записей

---

## Что дальше
Следующий блок:
**33601–34000 — Search, Ranking & Vitrines OS** (поиск, фасеты, ранжирование, персонализация, витрины “лучшие решения”, “проверенные”, “готовые к 1‑клику”).  
Скажете “Продолжение” — сделаю.
