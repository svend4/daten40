# IFOS 32001–32400 — Knowledge Registry OS (v1)
Идея: “интернет — это миллиард функций, но они не собраны в систему”.  
**Knowledge Registry OS** превращает плагины, сценарии (Make/n8n), API, приложения, шаблоны и готовые куски кода в **единый словарь**:
- у каждого “кирпичика” есть карточка (что делает),
- место в таксономии (где он в “периодической таблице” функций),
- совместимость (с чем работает),
- зависимости (что нужно для запуска),
- витрина (готовые “пакеты одной кнопкой”),
- рейтинг/отзывы,
- trust/репутация и лицензии,
- нормальная “установка” и “запуск” (Install→Run).

Порядок: простое → среднее → сложное.

---

## 32001–32030 — Минимальная карточка “Функции” (RegistryItem)
Любой объект (plugin/app/scenario/api/template) становится **RegistryItem**:
- `id`, `name`, `kind` (plugin/app/scenario/api/template)
- `summary` (1–2 предложения)
- `inputs/outputs` (чтобы люди и машины понимали)
- `capabilities` (что умеет: send_email, parse_pdf, scrape_site…)
- `install_recipe` (как установить/запустить)
- `dependencies` (что нужно)
- `license_policy`
- `maintainer`, `source_url`, `docs_url`
- `quality` (статусы: draft/stable/deprecated)

Принцип: **одно действие = одна функция = один узел словаря**.

---

## 32031–32070 — Таксономия: “периодическая таблица функций”
Чтобы не тонуть в миллионах карточек, нужна **иерархия**:
- Domain (например: Docs, Messaging, Payments, Travel, CRM, Monitoring)
- Category (например: Parse/Generate/Sync/Notify)
- Capability (конкретная функция: “extract_pdf_text”, “send_telegram_message”)
- Variant (реализация: “Telegram Bot API”, “Slack webhook”, “Gmail API”)

TaxonomyNode хранит:
- `path` (Docs/Parse/PDF)
- `synonyms` (поисковые слова)
- `examples` (где применяется)
- `constraints` (например: “нужен OAuth”)

---

## 32071–32110 — Теги и “словарь синонимов”
Одна и та же штука может называться по‑разному:
- “интеграция”, “автоматизация”, “workflow”, “pipeline”
- “обновить записи” vs “sync”

Поэтому:
- Tag = плоские метки (быстро фильтровать)
- Synonyms = словарь связей (чтобы поиск находил правильное)

---

## 32111–32160 — Рейтинги/Отзывы: почему людям не хватает “витрин”
Проблема сейчас:
- много плагинов/сценариев, но нет ясности “какой лучший”,
- отзывы разбросаны, часто фейковые или бесполезные,
- нет связки “отзыв → версия → окружение → доказательства”.

RatingReview должен включать:
- оценка (звёзды/баллы) + текст
- версия объекта и окружение (WordPress 6.x, Make, n8n, Node 20…)
- подтверждение использования (квитанция установки/запуска, лог успеха)
- теги отзыва (performance, UX, bugs, docs)

---

## 32161–32210 — Trust Score: репутация, анти‑мусор, анти‑фейк
TrustSignal собирает “сигналы доверия”:
- maintainer verified (подтверждённый автор)
- signed builds (подпись артефактов)
- vulnerability history (CVEs/инциденты)
- popularity (установки/звёзды) — но не единственный критерий
- review quality (подтверждённые отзывы)
- doc completeness (наличие quickstart, примеров, API)
- support responsiveness (SLA ответов)

TrustScore = агрегат:
- baseline по источнику
- бонус/штраф по сигналам
- штраф за подозрительные паттерны (накрутка)

---

## 32211–32260 — Совместимость: “работает ли у меня?”
CompatibilityMatrix отвечает:
- поддерживаемые ОС/рантаймы (linux/windows/android?)
- версии платформ (WP, Make, n8n, Node, Python)
- ограничения (нужен сервер, нужен ключ API, платный тариф)
- I/O совместимость (форматы, auth схемы)

Это позволяет строить:
- фильтры “только работает на Android”,
- “только open-source/self-hosted”,
- “без платных ключей”.

---

## 32261–32310 — Dependency Graph: “что нужно, чтобы работало”
Каждый объект имеет dependencies:
- runtime (python/node/docker)
- services (redis/postgres)
- credentials (oauth, api_key)
- other registry items

DependencyGraph нужен чтобы:
- автоматически собрать “пакет”,
- проверить совместимость,
- предложить альтернативы (“если нет Docker — вот вариант без Docker”).

---

## 32311–32360 — One‑Click Install / Run: рецепт + оркестрация
InstallRecipe описывает:
- что скачать (artifact_url)
- как проверить хеш
- как установить (docker compose / pip / wp plugin install)
- как настроить (env vars, secrets)
- как запустить и сделать health check
- как откатить (uninstall/rollback)

Цель: **кнопка “установить и запустить”**, как “макрос в Excel”, но для интернета.

---

## 32361–32390 — Витрины (Vitrines): кластеры “лучшее из лучшего”
Витрина = curated bundle для задачи:
- “автоматизация офиса 2.0”
- “агрегатор новостей + сравнение + отзывы”
- “портал сравнения страховок/путешествий”

Vitrine включает:
- подборку registry items
- dependency graph
- готовые конфиги
- demo dataset
- инструкцию “start here”
- benchmark (скорость/стоимость)

---

## 32391–32400 — Модерация, лицензии, правила качества
Чтобы Registry не превратился в свалку:
- ModerationDecision (approve/reject/quarantine)
- LicensePolicy (MIT/GPL/Commercial/Proprietary, ограничения использования)
- Quality levels (draft/stable/deprecated)
- “Security bar” (минимальные требования к безопасности)

---

## Мини‑архитектура Knowledge Registry OS
Ingest (из GitHub/Make/WP) → Normalize → Taxonomy classify → Reviews/Trust → Compatibility → Dependency resolve → Package/Vitrine → One‑click install/run → Monitoring feedback → Reconcile versions

---

## Что дальше
Следующий блок:
**32401–32800 — Marketplace & Billing OS** (подписки, лицензии, платёжные планы, trial, usage‑based, revenue share, “маркетплейс как AppStore для сценариев/плагинов”).  
Скажете “Продолжение” — сделаю.
