# IFOS 33601–34000 — Search, Ranking & Vitrines OS (v1)
Цель: превратить Registry + Marketplace в **понятный “каталог решений”**, где:
- поиск находит *то, что нужно* (и не показывает мусор),
- ранжирование поднимает “лучшие” (качество/доверие/готовность к 1‑клику),
- витрины дают готовые подборки (по задачам, отраслям, уровню риска),
- персонализация учитывает контекст (Android vs сервер, novice vs pro),
- обратная связь улучшает качество (клики, установки, успех запуска, отзывы).

Порядок: простое → среднее → сложное.

---

## 33601–33630 — Минимальный поиск: Query → Hits
### SearchQuery
Запрос включает:
- text (строка)
- filters (facet filters: kind, category, capability, price, risk, platform)
- sort (relevance / dq_score / popularity / freshness / price)
- paging (offset/limit)
- user_context (платформа, регион, язык, уровень доступа)

### SearchResponse
Ответ:
- hits (SearchHit) с explain (почему показано)
- facets (доступные фильтры)
- suggestions (поправки запроса: “возможно вы имели в виду…”)

**Важно:** мы ищем не “страницы”, а **функции/пакеты/витрины**, то есть “сделай X”.

---

## 33631–33690 — Индексация: IndexDocument и IndexConfig
### IndexDocument
Единый индексный документ для item/bundle/vitrine:
- title/description
- capabilities
- inputs/outputs (сжатая схема)
- artifacts (тип, ref, версия)
- deps (зависимости)
- quality_signals (DQ score, trust, installability, health)
- popularity (установки/успехи/время)

### IndexConfig
- какие поля индексируем полнотекстом
- какие поля — фасеты
- какие веса (title>description>tags)
- языковые настройки (ru/de/en), stemming, stopwords

---

## 33691–33740 — Facets: фильтры как “панель управления”
FacetDefinition описывает фильтры:
- kind (wp_plugin/make_scenario/container/api…)
- category (маркетинг/финансы/документы…)
- capability (send_email, scrape_web, generate_pdf…)
- platform (android/local/docker/k8s)
- risk (low/medium/high) — из policies/provenance
- “1‑click ready” (есть рецепт установки + run profile)

Фасеты — ключ к “управлению хаосом”.

---

## 33741–33810 — RankingProfile: как выбрать “лучшее”
Ранжирование обычно = сумма сигналов:
- text relevance (BM25/вектор/гибрид)
- dq_score.overall
- trust / provenance (подпись, официальный источник)
- installability (есть installer recipe)
- runtime health (успешные прогоны)
- popularity (installs, retention)
- freshness (recent update)
- price fit (если фильтр по бюджету)

RankingProfile задаёт веса и правила “boost/penalty”.

---

## 33811–33860 — Query Rewrite + Synonyms + Boost Rules
Чтобы люди находили, даже если называют по-разному:
- SynonymDictionary: “интегромат=make”, “письмо=email”, “телега=telegram”
- QueryRewriteRule: исправления, расширения, нормализация слов
- BoostRule: поднимать “проверенные” и “готовые к 1‑клику”, скрывать “битые”.

---

## 33861–33910 — Витрины: готовые подборки “как в магазине”
Vitrine — это curated/auto‑generated коллекция:
- “Автоматизация офиса 2.0: топ‑набор”
- “WordPress: must‑have плагины”
- “Make: лучшие сценарии для новичка”
- “Android‑локально: работает без сервера”
- “Безопасные решения (strict policy)”.

VitrineItem хранит:
- ссылку на canonical_id
- позицию/причину (reason)
- требования (requires: docker, k8s, android)
- уровень “one‑click readiness”.

---

## 33911–33960 — Персонализация: профиль пользователя/организации
PersonalizationProfile учитывает:
- платформу (android vs server)
- предпочтения (open‑source, self‑hosted)
- ограничения (нет docker / нет root / только EU data)
- роли (novice/pro/dev/admin)
- историю (что ставил, что запускалось успешно)

Персонализация **не должна ломать** базовый поиск: она лишь переставляет и уточняет.

---

## 33961–33990 — Обратная связь и обучение
FeedbackEvent:
- impression (показ)
- click
- install
- run_success / run_fail (самый ценный сигнал)
- rating/review
- report_issue (битая ссылка/вредонос)

Из feedback строим:
- popularity и success_rate
- “quality_signals” для ранжирования
- автоматические предупреждения (если success_rate падает).

---

## 33991–34000 — A/B тесты ранжирования и витрин
ABTest:
- варианты RankingProfile (A,B,C…)
- измерения: CTR, install_rate, run_success_rate, time_to_value
- guardrails: безопасность/стоимость/жалобы
- постепенный rollout

---

## Что дальше
Следующий блок:
**34001–34400 — Enterprise & Governance OS** (мульти‑тенант, роли, орг‑политики, каталоги компании, approval flows, аудит, комплаенс, лицензирование внутри организации).  
Скажете “Продолжение” — сделаю.
