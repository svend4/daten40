# IFOS 29601–30000 — Data Quality & Knowledge OS (v1)
Цель: из “дикого интернета” получить **понятные, чистые, проверяемые данные**, чтобы:
- функции/плагины/сценарии можно было **сравнивать**, **находить**, **комбинировать**;
- новости/каталоги не были шумом (дубликаты, спам, мусор);
- система могла объяснять: **почему этот результат** и **почему этому можно доверять**;
- всё было **версионировано**, чтобы “вчера” и “сегодня” сравнивались честно.

Порядок: от простого к среднему и далее к сложному.

---

## 29601–29640 — Raw Records: сырьё как есть
RawRecord — “как пришло”:
- source_id (откуда)
- fetched_at
- payload (html/json/text)
- content_hash
- headers/meta

Нельзя “улучшать” данные без сохранения сырья — иначе теряется проверяемость.

---

## 29641–29690 — Normalization: приводим к общему виду
NormalizedRecord — единая структура:
- title, summary, url, author, published_at
- entities (если нашли)
- language, region
- canonical_id (после дедупа)

Нормализация — это “Excel‑таблица” для хаоса: одинаковые колонки для разных источников.

---

## 29691–29740 — Taxonomy: словарь категорий и тегов (грамматика интернета)
Taxonomy определяет:
- категории (например: News, Marketplace, Automation, Security)
- теги (rss, telegram, wordpress, hosting, pricing)
- синонимы и алиасы (make.com ~ integromat)
- правила вложенности (дерево/граф)

Это основа навигации и витрин.

---

## 29741–29790 — Tagging Rules: автоматическая разметка
TaggingRule:
- условие (regex, ключевые слова, entity match)
- тег/категория
- confidence
- override policy (ручная правка сильнее автоматики)

Теги должны быть воспроизводимы: “почему поставили этот тег”.

---

## 29791–29830 — Dedupe Clusters: убираем дубликаты
DedupeCluster:
- canonical record
- duplicates list
- similarity score
- причина совпадения (url/canonical, title+date, embedding)

Дедуп нужен не только в новостях — и в плагинах, и в сценариях, и в карточках.

---

## 29831–29870 — Entity Resolution: кто есть кто
Entity:
- product, company, person, library, service
EntityLink:
- “Google Cloud Run” == “Cloud Run” (alias)
- “Make” == “Integromat” (historical rename)
- “WordPress plugin X” связан с “Company Y”

Entity resolution делает возможным сравнение: иначе одно и то же выглядит разным.

---

## 29871–29920 — Provenance & Trust: откуда взялось и насколько надёжно
Provenance:
- источник, дата, способ получения
- цепочка трансформаций (raw → normalized → deduped → ranked)
TrustScore:
- репутация источника
- свежесть (recency)
- согласованность с другими источниками
- признаки SEO‑спама/перепечатки

Важно: доверие — это не “истина”, а оценка риска ошибки.

---

## 29921–29960 — Explanation: “почему этот результат”
Explanation объект:
- какие факторы влияли (score breakdown)
- какие правила сработали (tagging rule ids)
- какие источники подтверждают
- какие альтернативы были рядом

Это ключ к “анти‑рекламе” и честной витрине/сравнению.

---

## 29961–30000 — Versioned Datasets: версии данных как Git
DatasetVersion:
- dataset_id (например: marketplace_listings)
- version (semver или дата)
- diff summary (что изменилось)
- snapshot refs (файлы/коллекции)
- migration steps

Версии позволяют:
- сравнить “вчера/сегодня”
- откатить ошибки
- репродуцировать отчёты и сравнения

---

## Мини‑архитектура Data Quality & Knowledge OS
1) RawRecord → 2) NormalizedRecord → 3) Taxonomy → 4) TaggingRules  
5) Dedupe → 6) Entities/Links → 7) Provenance/Trust → 8) Explanation → 9) Versioned Datasets

---

## Что дальше логически
Следующий блок (если скажете “Продолжение”):
**30001–30400 — Security & Compliance OS**: секреты, доступы, политики, audit, sandbox, supply-chain, подписи пакетов, “безопасная установка одной кнопкой”.
