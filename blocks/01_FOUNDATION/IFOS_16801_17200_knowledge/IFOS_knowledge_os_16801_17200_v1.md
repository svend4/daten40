# IFOS 16801–17200 — Knowledge‑OS: авто‑документация, авто‑учебник, skill graphs, диагностика и “макросы для всего интернета” (v1)

Если Execution‑OS (16401–16800) отвечает “как запустить”, то Knowledge‑OS отвечает:
- **как понять**, что это за компонент/рецепт
- **как научиться** пользоваться (как в Excel “макросы”, но для любых функций)
- **как диагностировать**, почему не работает
- **как собрать кластер**, если пользователь просит “хочу как check24 / idealo / дайджест новостей / дропшиппинг”

Ниже — по порядку, от простого к сложному.

---

## 16801–16840 — Документация как исполняемый объект (простое)

### 16801) Doc Card вместо “README где попало”
Doc Card = минимальная карточка, которую может понять и человек, и машина:
- что делает
- входы/выходы
- ограничения (лимиты, регионы, цены)
- примеры “до/после”
- типовые ошибки + как исправить
- уровень доказательности (evidence hooks)

### 16802) Авто‑генерация Doc Card
Источники для генерации:
- capability contract (что обещает)
- install plan (как ставится)
- run records (что реально происходит)
- failure logs (что ломается)
- governance flags (риски)

Результат: **единый стиль документации** как у “Word/Excel”, но для любой функции.

---

## 16841–16920 — Tutorial Modules: авто‑учебник и “путь освоения” (среднее)

### 16841) Tutorial Module
Небольшой модуль обучения:
- цель (“настроить Telegram‑дайджест”)
- prerequisites (аккаунт, токены, доступы)
- шаги (1..N)
- контрольные точки (expected output)
- типовые ошибки (и быстрые фиксы)
- mini‑quiz (опционально)

### 16842) Learning Path
Learning Path = цепочка tutorial modules от простого к сложному:
- L0: включить готовый bundle
- L1: поменять источник данных (RSS/API)
- L2: добавить фильтры и сравнение
- L3: собрать “кластер” (несколько jobs + витрина + рейтинги)

---

## 16921–17010 — Skill Graphs: “грамматика интернета” (сложнее)

### 16921) Почему нужен skill graph
Make/WP/n8n имеют тысячи возможностей, но без “карты навыков”:
- не видно, что учить дальше
- не видно зависимости (OAuth → rate limits → retries)
- нет структуры “как макросы”

Skill Graph = граф:
- skill nodes (умение/операция)
- prerequisites edges
- mapped-to functions/recipes/bundles
- difficulty, estimated time, evidence

### 16922) Пример навыков
- “Настроить OAuth”
- “Сделать дедупликацию”
- “Сделать мониторинг ошибок”
- “Сделать безопасное хранение секретов”
- “Сделать витрину сравнения”

---

## 17011–17110 — Диагностика и Troubleshooting OS (сложное)

### 17011) Проблема “не работает”
Обычно это одно из:
- секрет/ключ неверный или истёк
- лимит API или блокировка региона
- неправильная схема данных (field mismatch)
- не совпала версия модуля/плагина
- sandbox policy запретила side effect
- webhook не доходит
- timeouts / concurrency

### 17012) Diagnostics Report
Knowledge‑OS создаёт отчёт на основе:
- run record + logs
- sandbox policy decisions
- contract expectations (что “должно быть”)
- known issues базы (community fixes)
- evidence court (если был fail)

Отчёт выдаёт:
- root cause hypotheses (с вероятностями)
- быстрые действия (1–3 пункта)
- “глубокие” действия (для инженера)
- ссылку на tutorial module “как исправить навсегда”

### 17013) Troubleshooting Playbook
Playbook — дерево решений:
- симптом → проверки → решения → предотвращение
Это можно автоматически пополнять из реальных инцидентов.

---

## 17111–17200 — Knowledge Packs: переносимость знаний + “встроенный мозг” (самый высокий уровень)

### 17111) Knowledge Pack Manifest
Pack = переносимый пакет знаний для bundle/кластера:
- docs (doc cards)
- tutorials (learning path)
- skill graph subset
- troubleshooting playbooks
- known issues + fixes
- policy advice (безопасность, секреты)

### 17112) “Почему нет рекламы и отзывов” — технический ответ
Потому что нет слоя Knowledge‑OS:
- нет стандартизированной карточки
- нет доказательности и контекста отзывов
- нет навыковой карты
- нет playbooks “как починить”
- нет пакетируемой витрины знаний

Knowledge‑OS делает **видимость и понятность**: “почему этот модуль лучший”, “как его ставить”, “как дебажить”, “как учиться дальше”.

---

## Приложения (в этом пакете)
- JSON Schemas: doc card, tutorial module, skill graph, diagnostics report, troubleshooting playbook, glossary entry, knowledge pack manifest, recommendation trace
- Specs: auto documentation, skill graph, diagnostics/troubleshooting, learning paths, KB ingest/RAG
- OpenAPI: Knowledge API (MVP)
- Examples: doc card + tutorial + skill graph + diagnostics report + playbook + knowledge pack + recommendation trace
- Python skeletons: doc generator, skill graph builder, diagnostics engine, KB ingest pipeline, CLI stub
