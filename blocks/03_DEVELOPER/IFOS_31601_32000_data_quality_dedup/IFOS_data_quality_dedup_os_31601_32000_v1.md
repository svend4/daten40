# IFOS 31601–32000 — Data Quality & Dedup OS (v1)
Цель: интернет остаётся “диким полем”, потому что данные **грязные, разрозненные и дублируются**.
Эта ОС делает 3 вещи:
1) **Нормализация**: привести разные источники к каноническому виду.
2) **Качество**: измерять/улучшать качество, ставить “quality gates”.
3) **Дедуп/идентичность**: понять, что “это одно и то же”, и хранить правду как версии фактов с доказательствами.

Порядок: от простого → к среднему → к сложному.

---

## 31601–31630 — Проблема “всё одинаковое, но по-разному написано”
Типовые боли:
- один и тот же объект (товар/услуга/новость) описан 50 способами;
- разные URL ведут на одно и то же;
- даты/валюты/единицы измерения в разных форматах;
- названия компаний/людей/городов пишутся по-разному (транслит/сокращения);
- тексты перепостов и агрегаторов создают тысячи дублей.

Если это не решать, Registry/Marketplace превращается в “мусорный каталог”.

---

## 31631–31680 — Минимальная модель данных: Source → Record → NormalizedRecord
**SourceProfile** описывает источник: домен, формат, доверие, частота, правила извлечения.

**Raw Record** — как пришло (RSS item, JSON API, HTML snippet).

**NormalizedRecord** — как надо хранить “внутри”:
- `canonical_title`
- `canonical_url` (нормализованный)
- `published_at` (ISO)
- `content_text` (чистый текст)
- `language`
- `tags`
- `entities` (пока простые извлечения/словарь)
- `fingerprints` (для дедупа)
- `provenance` (откуда взяли)

---

## 31681–31720 — Нормализация (простая → средняя)
Простые операции (обязательные):
- trim/whitespace
- lowercase (для ключей/сравнения)
- URL canonicalization (убрать UTM, нормализовать протокол/хост/слеши)
- дата в ISO 8601
- валюта/числа/единицы измерения (EUR, kg, m²)
- очистка HTML → текст

Средние операции:
- language detection
- transliteration/collation keys
- “title cleanup” (убрать мусор типа “Breaking:”)
- нормализация брендов/моделей по словарю

---

## 31721–31770 — Quality Gates: “не пускаем мусор дальше”
QualityGateRule = правило + уровень + действие:
- **reject**: не принимать
- **quarantine**: принять в карантин (ручной/автоматический разбор)
- **accept_with_flags**: принять, но пометить

Примеры правил:
- пустой title → reject
- домен не из allowlist → quarantine
- слишком короткий текст (< 80 символов) → accept_with_flags
- подозрительный redirect chain → quarantine

Метрики качества:
- completeness (заполненность)
- validity (валидность форматов)
- uniqueness (уникальность)
- freshness (свежесть)
- consistency (согласованность)

---

## 31771–31830 — Fingerprints: “быстрый ключ похожести”
Fingerprints бывают:
- **exact**: sha256(canonical_url)
- **near-dup text**: simhash/minhash (упрощённо на прототипе)
- **title+date**: hash(clean_title + day(published_at))
- **content signature**: top-k tokens hash

Дедуп на объёмах делается в 2 шага:
1) быстрые кандидаты (по fingerprints)
2) точное решение (сравнение текста/полей)

---

## 31831–31890 — Dedupe: кандидаты → решение → действия
Процесс дедупа:
1) **candidate generation**: найти возможные дубли по fingerprints
2) **scoring**: посчитать схожесть (title/text/date/url)
3) **decision**:
   - `same` (дубль)
   - `different` (не дубль)
   - `unsure` (нужен человек/политика)
4) **merge policy**: как объединять поля (какой источник “главнее”)

Результат: `DedupeDecision` с причинами и сигналами.

---

## 31891–31940 — Identity Resolution: сущности и связи
Дедуп решает “одна запись”, identity решает “одна сущность”:
- Компания: “Deutsche Telekom”, “Telekom”, “DTAG”
- Продукт: “iPhone 15 Pro Max”, “Apple iPhone 15PM”

Entity модель:
- `entity_id`
- `type` (org/person/product/location/service)
- `names` (варианты)
- `external_ids` (wikidata, VAT, app_id)
- `features` (домены, телефоны, адреса)
- `links` (EntityLink: same_as / related_to / owned_by)

---

## 31941–31980 — Версии фактов: “правда меняется”
Важно хранить не только текущее состояние, но и историю:
- “цена была X, стала Y”
- “условия сервиса изменились”

Fact + FactVersion:
- Fact = “утверждение” (predicate+subject)
- FactVersion = значение + время + источник + confidence + evidence

---

## 31981–32000 — Provenance & Evidence: доказательства источников
Каждая запись должна знать:
- откуда взяли (source_url, fetched_at, extractor_version)
- чем подтверждено (snippet/HTML hash/скриншот hash)
- степень доверия (source trust + эвристики)

---

## Мини‑архитектура Data Quality & Dedup OS
Ingest → Normalize → Quality Gates → Fingerprint → Candidate Gen → Dedupe Decision → Entity Resolution → Fact Versioning → Provenance/Evidence → Reconciliation Jobs

---

## Что дальше
Следующий блок (если скажете “Продолжение”):
**32001–32400 — Knowledge Registry OS**: словарь функций/плагинов/сценариев как “периодическая таблица” интернета: таксономия, ранжирование, отзывы, trust, витрины, лицензии, совместимость, dependency graph.
