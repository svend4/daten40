# IFOS 43601–44000 — Content Import & Normalization OS (v1)
Цель: перестать “искать новое” и начать **массово рационализировать существующее**.
Для этого IFOS должен уметь:
- забирать контент из источников (web, APIs, docs, repos)
- извлекать данные (extract)
- приводить к единой форме (normalize)
- маппить в реестр схем (schema registry)
- обогащать (enrich), переводить, классифицировать
- скрывать персональные данные (PII redaction)
- обеспечивать качество (QA), карантин, дедупликацию

Порядок: простое → среднее → сложное.

---

## 43601–43640 — IngestSource: источник данных
**IngestSource** — описание откуда берём данные:
- тип: rss, website, api, github, gdrive, pdf, appstore
- auth (если нужно): oauth/key/cookie
- частота (schedule)
- правила robots/terms
- ограничения (rate limits, allowed domains)

Если источник не описан как объект — его нельзя повторяемо обрабатывать.

---

## 43641–43710 — FetchJob: загрузка и снимки (snapshots)
**FetchJob**:
- что загрузили (url/ref)
- когда (timestamp)
- checksum/etag
- статус (ok/error/retry)
- хранение (raw storage ref)

Это превращает интернет в “версионируемый архив”.

---

## 43711–43770 — Extractors: извлечение структуры
**Extractor** — модуль, который знает, как вытащить смысл из сырого:
- html → article/product/review
- github repo → readme, manifests, licenses, code stats
- pdf → text blocks + metadata
- api json → objects

Extractor выдаёт **RawItem** (полуструктурированный объект).

---

## 43771–43830 — RawItem → NormalizedItem: нормализация
**RawItem**: как получилось у парсера.
**NormalizedItem**: как должно быть в IFOS:
- единые поля: title, summary, body, links, timestamps, locale, entities
- нормализация валют/единиц/дат
- стандартная таксономия категорий

Цель: любые источники → одинаковый формат.

---

## 43831–43880 — Mapping Rules: привязка к Schema Registry
Чтобы данные стали “официальными”, нужно сопоставить их схеме:
- выбираем schema_id (например: ifos.review)
- применяем MappingRule (field mapping)
- валидируем (см. прошлый блок 43201–43600)

Так интернет превращается в “базу знаний” и “рынок функций”.

---

## 43881–43930 — Enrichment: обогащение, перевод, классификация
**EnrichmentJob**:
- language detection + перевод (если нужно)
- entity extraction (компании, продукты, версии)
- topic clustering (кластеры)
- quality signals (длина, источники, дубликаты)

Это ваш “двигатель рационализации”: не новое, а лучшее понимание старого.

---

## 43931–43960 — PII Redaction: приватность и безопасность
**PII Redaction Job**:
- обнаружение PII (emails, телефоны, адреса, токены)
- маскирование/удаление
- правила по регионам (GDPR)
- доказуемость (логируем что и как скрывали)

Без этого нельзя строить B2B и enterprise решения.

---

## 43961–43990 — Dedup & Quarantine: качество и карантин
**DedupKey**:
- hash нормализованного контента (title+body+source)
- fuzzy key (для похожих дубликатов)
**QuarantineItem**:
- почему в карантине (validation errors, low confidence)
- что нужно исправить (suggested fix)
- кто отвечает (owner/team)

Это помогает “не захлебнуться” в миллионах данных.

---

## 43991–44000 — Ingest Manifest: упаковка импорта
**IngestManifest** — пакет импорта:
- source → fetch jobs → raw items → normalized items
- mapping rules
- QA результаты
- ссылки на registry export

Это позволяет переносить данные между окружениями и повторять обработку.

---

## Итог
Этот блок делает IFOS “машиной рационализации”:
- интернет превращается в версионируемый архив (fetch jobs)
- extract/normalize/mapping → данные становятся совместимыми
- enrichment → кластеры и смысл
- privacy + QA → готово для продукта

---

## Что дальше
Следующий блок:
**44001–44400 — Searchable Knowledge Vault OS** (индексация, embeddings, полнотекст, faceting, query planner, citations, exports).  
Скажете “Продолжение” — сделаю.
