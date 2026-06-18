# IFOS 60801–61200 — Office Suite UI OS (UI “как офисный пакет”) (v1)
Цель: сделать интерфейс IFOS понятным как “Office”: файлы, папки, документы, таблицы, макросы, презентации.
Проблема: даже хорошие модули бесполезны, если их нельзя быстро найти, понять и запустить.
Этот блок — детальная спецификация UI (на уровне “можно реализовать”).

Порядок: простое → среднее → сложное.

---

## 60801–60820 — Принцип: 5 приложений вместо хаоса
Внутри IFOS всегда доступны “5 офисных приложений”:
1) **Registry** (табличный каталог) — реестр сущностей, коннекторов, планов, цен, полей
2) **Blueprints** (документы) — описание процессов, витрин, пакетов
3) **Macros / Runner** (макросы) — запуск workflows и bundles
4) **Vitrines / Conference** (презентации) — сравнение, новости, отчёты
5) **Console** (панель) — мониторинг, ошибки, очереди, логи, метрики
Пользователь всегда понимает: “я сейчас в таблице / документе / макросе / презентации / консоли”.

---

## 60821–60850 — Информационная архитектура (IA)
Глобальные зоны:
- Left sidebar: Workspace / Projects / Apps / Recent
- Top bar: Search, Create (+), Share, Run, Notifications, Profile
- Main: Canvas (таблица/документ/витрина)
- Right pane: Inspector (properties, dependencies, quality gates, docs, security)
Объекты в workspace:
- Artefact (коннектор, макрос, схема)
- Bundle (пакет)
- Blueprint (документ)
- Vitrine (витрина)
- Dataset / Source (источник данных)
- Run (запуск/исполнение)

---

## 60851–60890 — Модель “файлы/папки/документы”
Ключ: всё выглядит как файловая система:
- “Новый…” → Blueprint / Registry Table / Vitrine / Macro
- “Сохранить как…” → versioned
- “Экспорт” → JSON/CSV/MD/HTML
- “Поделиться” → link + permissions
- “История версий” → diff/rollback
Каждый объект имеет:
- name, id, owner, tags, status
- versions
- dependencies (bundle graph)
- quality scorecard
Это позволяет “рационализацию” на практике: собрать “папку решений” под задачу.

---

## 60891–60930 — Карточки и витрины (Card system)
Единая карточка для всего:
- title + badges (trust tier, docs score, security)
- summary (3–4 строки)
- actions: Run / Install / Compare / Add to bundle
- metadata: cost, license, supported connectors
- preview: скрин/диаграмма/пример
Карточка = “ярлык функции” (как вы и описывали: слово в техническом словаре).

---

## 60931–60970 — Таблицы и гриды (Registry UI)
Registry = Excel‑стиль:
- columns, filters, group by, pivot‑like views
- inline editing
- formula cells для derived fields
- validation rules
- import/export CSV
- dedup suggestions (показывать похожие записи)
Супер‑функция: “Make.com scenarios as rows” — каждый сценарий как строка с полями качества.

---

## 60971–61010 — Редакторы (Blueprint/Macro/Vitrine)
Редакторы:
- Blueprint editor: структурный документ + блоки (sections)
- Macro editor: визуально или YAML/JSON DSL + тест‑раннер
- Vitrine builder: drag‑drop layout + data bindings
- Docs editor: auto docs + ручные правки
Все редакторы имеют:
- autosave
- validation
- “Run in sandbox”
- “Generate docs”
- “Create issue”

---

## 61011–61040 — Macro Runner (запуск в один клик)
Runner UI:
- pick bundle
- choose profile (env: dev/stage/prod)
- params form (generated from schema)
- dry-run option
- run logs + artifacts
- export report
Состояния: queued → running → succeeded/failed → needs attention.
“Needs attention” открывает подсказки и troubleshooting.

---

## 61041–61070 — Conference mode (презентация/новостная конференция)
Conference mode = “слайд‑лента”, но интерактивная:
- daily/weekly digest
- сравнение 3–5 вариантов
- “что изменилось” (diff)
- кнопки: open sources, reproduce, export
Это делает “новостную конференцию” отдельной функцией (как вы просили).

---

## 61071–61100 — Search & Filters (поиск как у профессиональных каталогов)
Поиск везде:
- global search по объектам
- faceted filters (license, trust tier, category, connector)
- “compare” режим: выбрать несколько → сравнение по метрикам
- saved searches (“умные папки”)
- ranking: сначала quality + trust, потом реклама (разделено)

---

## 61101–61130 — Hotkeys & power‑user режим
Принцип: всё делается с клавиатуры:
- Ctrl+K: command palette
- Ctrl+N: new
- Ctrl+P: open
- Ctrl+Enter: run
- Ctrl+Shift+F: global search
- Alt+1..5: переключение приложений (Registry/Blueprint/Macro/Vitrine/Console)
На мобильном — жесты и быстрые кнопки.

---

## 61131–61160 — Accessibility (a11y) и инвалидность
Требования:
- полнота клавиатурной навигации
- высокие контрасты
- озвучка и aria labels
- масштабирование 200%
- режим “простые шаги”
- режим “крупные кнопки”
- минимизация когнитивной нагрузки (guided mode)
Это критично для массового внедрения и социальной ценности.

---

## 61161–61180 — i18n (локализация) и “словарь терминов”
UI должен иметь:
- словарь терминов (artefact/bundle/macro) с примерами
- переключение RU/DE/EN
- локализация форматов дат/валют
- translation memory для docs
Плюс: glossary влияет на обучение (60401–60800).

---

## 61181–61200 — State sync, ошибки, onboarding
Состояние:
- offline-first (кэш)
- conflict resolution (как Google Docs)
- audit log (кто что менял)
Ошибки:
- понятные error cards
- кнопка “исправить”
- генерация issue в поддержку/maintainer
Onboarding:
- 3‑шаговый тур
- “первый успешный run” как цель

---

## Итог
Office Suite UI OS делает IFOS “пакетом приложений”, а не хаосом:
- единые карточки
- таблицы как Excel
- документы как Word
- макросы в один клик
- конференция как презентация
- консоль как панель управления

---

## Что дальше
Следующий блок:
**61201–61600 — Integration with Existing Ecosystems OS: WordPress/Make/n8n/Zapier/GitHub/Play Store каталогизация и импорт**  
Скажете “Продолжение” — сделаю.
