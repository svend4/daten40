# IFOS — In‑App Guidance, Tours & Contextual Help (Блок 50401–50800)

Версия: v1 · Пакет: `IFOS_50401_50800_in_app_guidance_help_os_pack.zip` · Дата: 2026-01-02

## 0) Идея (зачем нужен блок)

Wizards (49601–50000) помогают пройти первый путь «поставить и запустить». Но дальше пользователи застревают:
- где находится нужная функция в интерфейсе
- что означает ошибка/предупреждение
- какой следующий «правильный шаг»
- где документация именно для *этого* объекта (коннектор/макрос/витрина)

Этот блок делает IFOS похожим на зрелую офисную систему:
**подсказки, туры, контекстная справка, объяснение ошибок, поисковая помощь**.

## 1) Что делает (функции)

1) **Contextual Help** — справка на уровне экрана/виджета/поля формы.
2) **Interactive Tours** — краткие туры (onboarding) по ключевым сценариям.
3) **Explain‑this Error** — разбор ошибок: что случилось + вероятная причина + шаги исправления.
4) **Help Search** — поиск по статьям/FAQ/инструкциям (минимум: индекс по ключевым словам).
5) **Inline Docs Binding** — привязка документации к объектам registry (connector/macro/bundle/vitrine).
6) **Guidance Rules** — правила подсказок в зависимости от состояния (missing creds, failed preflight, quota, policy block).
7) **Feedback loop** — быстрый вопрос «помогло?» + отправка контекстного фидбэка.

## 2) Что НЕ делает (границы)

- Не заменяет курсы/сертификацию (56801–57200).
- Не делает полноценный knowledge-base с RAG (37201–37600) — это отдельный слой.
- Не хранит секреты и не исполняет макросы (использует другие блоки).

## 3) MVP (простое → среднее)

### Шаг 3.1 — Help Article (минимальная статья)

Сущность `help_article`:
- `article_id` (slug)
- `title`
- `summary`
- `body_md`
- `tags[]`
- `related_subjects[]` (ссылки на registry ids)
- `locale` (ru/de/en)

### Шаг 3.2 — Context Help Binding

Сущность `help_binding`:
- `binding_id`
- `ui_context` (route/screen/widget/field)
- `subject_type` (connector|macro|bundle|vitrine|policy)
- `subject_id`
- `article_id`
- `trigger` (hover|click|error|empty_state)

### Шаг 3.3 — Guided Tour Definition

Сущность `tour_definition`:
- `tour_id`
- `display_name`
- `entry_route`
- `steps[]` (selector + message + next_condition)
- `use_case_tag` (news|compare|automation|knowledge)

MVP: 3 тура: Console, Marketplace install, Reviews.

### Шаг 3.4 — Explain‑this Error

Сущность `error_explainer_rule`:
- `rule_id`
- `match` (код/фраза/тип)
- `cause`
- `fix_steps[]`
- `related_articles[]`

MVP: правила для типовых ошибок:
- missing credentials
- quota exceeded
- policy blocked
- connector timeout

### Шаг 3.5 — Help Search (индекс)

MVP поиск: простой inverted-index по словам/тэгам.
Эндпоинт: `GET /help/search?q=...` → список статей.

### Шаг 3.6 — Feedback (помогло/не помогло)

Сущность `help_feedback`:
- `feedback_id`
- `article_id` или `tour_id`
- `helpful` (true/false)
- `comment` (optional)
- `context` (route, subject_id, error_code)

## 4) Средний уровень: state-driven подсказки

1) **Empty states**: если нет коннектора/ключей/данных — показать кнопку «исправить».
2) **Health banners**: если runtime деградирует — подсказка о статусе и временном обходе.
3) **Policy hints**: если контент заблокирован модерацией — объяснить причину и путь апелляции.
4) **Adaptive shortcuts**: подсказки горячих клавиш/команд в зависимости от роли.

## 5) Ближе к сложному: персонализация и обучение в процессе работы

- персональные рекомендации статей/туров по телеметрии действий
- A/B эксперименты текстов подсказок
- генерация статей из bundle manifest + автосвязка с объектами

## 6) API (минимум)

- `GET  /help/articles/{article_id}`
- `GET  /help/search?q=`
- `GET  /help/bindings?route=`
- `GET  /tours` (каталог)
- `POST /tours/{tour_id}/start`
- `POST /help/feedback`
- `POST /errors/explain` (error payload → explanation)

## 7) Зависимости

### Hard deps
- 38801–39200 `app_shell_navigation` (контекст route/screen)
- 50001–50400 `ui_os_office_style` (единый UX-компонентный стиль)

### Optional deps
- 53201–53600 `ui_console_os` (встраивание подсказок в консоль)
- 56001–56400 `analytics_insights_os` (персонализация подсказок)
- 58401–58800 `knowledge_packaging_documentation_os` (шаблоны документации)
- 48401–48800 `trust_safety_moderation` (подсказки апелляций/ограничений)

## 8) Чек‑лист

- [ ] Help articles (CRUD)
- [ ] Bindings (route/widget/field)
- [ ] Tours (3 базовых)
- [ ] Error explainer rules (минимум 4)
- [ ] Search
- [ ] Feedback
