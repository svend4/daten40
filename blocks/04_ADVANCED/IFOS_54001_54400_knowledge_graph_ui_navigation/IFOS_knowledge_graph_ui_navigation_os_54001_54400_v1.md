# IFOS 54001–54400 — Knowledge Graph UI & Navigation OS (визуальная карта зависимостей) (v1)
Цель: дать человеку **карту всей системы** (как “проводник + карта метро + IDE для зависимостей”):
- где используется этот блок (bundle/коннектор/шаг/документ)
- что сломается при изменении (impact analysis)
- какие зависимости нужны (dependency explorer)
- как быстро найти “первопричину” (root cause navigation)
- как собрать “витрину” и “пакет” из графа (curation)

Эта часть соединяет:
- **Knowledge Worker OS** (документы/карточки/проекты)
- **Runtime OS** (запуски, процессы)
- **Integration OS** (коннекторы)
- **Data OS** (сущности, контракты)
- **Security/Compliance** (политики)

Порядок: простое → среднее → сложное.

---

## 54001–54030 — Graph Model: что считаем узлами и рёбрами
### Узлы (Nodes)
- Workspace, Project
- Document, Card
- Bundle, Template, Connector
- Process, Step, Run, Incident
- EntityType, Dataset, SchemaContract
- Policy, ApprovalRule, Budget

### Рёбра (Edges)
- uses (использует)
- depends_on (зависит)
- produces (порождает данные)
- triggers (запускает)
- governed_by (регулируется политикой)
- approved_by (требует согласования)
- caused (причина/следствие)
Важно: граф версионируется: **node_version + edge_version**.

---

## 54031–54080 — Link Types Catalog: словарь связей
Связи должны быть стандартизированы (как “грамматика”):
- doc → describes → bundle
- process → uses → connector
- process_step → reads → dataset
- process_step → writes → dataset
- bundle → installs → connector
- policy → constrains → process
- run → produced → artifact
- incident → affects → process/run
Каждая связь включает:
- directed? (да/нет)
- strength (weak/strong)
- evidence (откуда связь: manifest, log, user link)
- confidence (0..1)

---

## 54081–54120 — Views: как человек видит граф (5 базовых режимов)
1) **Map View** (node-link diagram): “карта метро”
2) **List View** (таблица): сортировка/фильтры
3) **Matrix View** (adjacency heatmap): быстро видеть зависимости
4) **Timeline View** (изменения/версии): кто что менял
5) **Impact View** (что затронет изменение)

Каждый режим поддерживает:
- фильтры (по типу, риску, проекту)
- поиск
- “сохранить представление” (saved view)
Один клик = jump-to-cause (переход к первопричине).

---

## 54121–54160 — Dependency Explorer: “что нужно чтобы работало”
Функция:
- берём цель (например: “витрина сравнения”)
- строим дерево зависимостей:
  - bundles
  - connectors
  - policies
  - data contracts
  - budgets/quotas
Показываем:
- обязательные зависимости (hard)
- рекомендуемые (soft)
- конфликтующие (incompatible)
- недостающие (missing)
Кнопки:
- install missing
- request approval
- apply mapping
Это превращает настройку IFOS в “мастер установки”.

---

## 54161–54220 — Impact Analysis: “что сломается если поменять X”
Вход:
- объект (node_id) + proposed change (diff)
- контекст (workspace/project)
Выход:
- список затронутых объектов
- уровень риска (low/medium/high)
- какие run’ы и витрины пострадают
- какие политики нарушатся
- какие тесты нужно прогнать
Используется:
- перед публикацией bundle
- перед обновлением коннектора
- перед изменением схемы данных
UI делает понятное резюме:
“Изменение поля price затронет 3 процесса, 1 витрину, 2 маппинга”.

---

## 54221–54260 — Root Cause Navigation: “найти первопричину за 3 клика”
Сценарий:
- alert/incident → run → step → connector/dataset → policy/budget
- показать цепочку причин
- показать “первую ошибку” и “первую несовместимость”
Это снимает главную боль интеграций: “где сломалось?”.

---

## 54261–54310 — Graph Search: запросы по связям
Примеры запросов:
- “покажи всё, что зависит от connector.telegram”
- “покажи процессы с риском PII”
- “покажи все витрины, где используется entity Product”
- “покажи что изменилось за 7 дней”
Поддержка:
- простые фильтры (UI)
- расширенный язык (query DSL) для power users
Результаты можно “сохранить как View” и поделиться.

---

## 54311–54360 — UI Components: карточки, мини‑карта, инспектор
Компоненты:
- Graph MiniMap (обзор)
- Node Inspector (метаданные, версии, связи, кнопки действий)
- Edge Inspector (evidence/confidence)
- Diff Viewer (для impact analysis)
- Dependency Tree Panel
- “Explain” (простыми словами: что это и зачем)
UX правило:
- 3 уровня подробности: кратко → подробно → техподробности (как мы делали ранее).

---

## 54361–54390 — Performance & Scaling: чтобы не тормозило
Проблема: граф может быть 100k+ узлов.
Стратегия:
- подгрузка по области (lazy subgraph)
- кеш популярных views
- ограничение depth по умолчанию
- server-side query + pagination
Плюс:
- “сводные узлы” (collapse clusters)
- “группы” по проектам/домены

---

## 54391–54400 — Governance & Quality: правда vs выдумка
Источник связи:
- manifest (высокая уверенность)
- runtime logs (средняя/высокая)
- user link (средняя)
- AI inference (низкая, маркировать!)

Правило:
- AI‑связи всегда помечаются как “inferred” и требуют подтверждения,
  иначе мы получим ложную карту.
Это защищает систему от “галлюцинаций графа”.

---

## Итог
Knowledge Graph UI & Navigation OS делает IFOS “видимым”:
- зависимости понятны
- изменения безопасны
- причинно‑следственные цепочки быстры
- установка становится мастером
Без графа IFOS будет “набором деталей”, с графом — становится “операционной системой”.

---

## Что дальше
Следующий блок:
**54401–54800 — Document & Artifact Vault OS: хранилище артефактов, файлов, бинарей, дедуп, подписей, provenance**  
Скажете “Продолжение” — сделаю.
