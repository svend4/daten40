# IFOS — Incident Response & Postmortems (#69201–69600)
**Slug:** `incident_response_postmortems`  
**Категория:** Observability & Reliability  
**Версия:** v1 (0.1.0)  
**Роль блока:** превратить «алерты и хаос» в управляемый процесс: декларация инцидента → устранение → коммуникации → постмортем → действия → знания.

---

## 1) Зачем этот блок нужен (идея и исходная боль)
Интернет и корпоративный софт сегодня — это море готовых компонентов (SaaS, плагины, интеграции, Make/n8n сценарии, open‑source).  
Но когда что-то ломается:
- непонятно **кто главный** (Incident Commander), где «war room», где чек-лист;
- теряется **контекст** (какие изменения были, какие алерты, что уже пробовали);
- коммуникации идут вразнобой (внутри команды одно, пользователям другое);
- после восстановления **знание не фиксируется** (повторяем те же ошибки).

Этот блок добавляет «операционную дисциплину» как продукт: инциденты — это **объекты**, с **таймлайном**, **ролью**, **уровнем серьёзности**, **влиянием**, **решением**, **постмортемом** и **action items**, которые реально выполняются.

---

## 2) Область ответственности (что делает / не делает)
### Делает
1. **Создание и ведение инцидента**: статус, роли, ссылки на алерты/дашборды/тикеты, таймлайн, решения.
2. **Эскалация и управление**: severity, on‑call, вызов владельцев сервисов, переключение на IC.
3. **Коммуникации**: внутренний канал + клиентские обновления (шаблоны, частота, контроль качества).
4. **Постмортем**: стандартный формат, причинно‑следственный анализ, проверка гипотез, артефакты.
5. **Действия (Action Items)**: задачи, владельцы, сроки, контроль выполнения, связь с релизами.
6. **Уроки и знания**: автоматическая упаковка в Knowledge Vault/KB (RAG), обновление runbooks.
7. **Метрики надёжности**: MTTA/MTTR, повторяемость причин, «токсичные» сервисы, эффективность алертов.

### Не делает (границы)
- не заменяет Observability (логи/метрики/трейсы) — **использует** её;
- не заменяет Ticketing/Case Mgmt — **интегрируется** с ним;
- не строит полноценный CMDB/ITSM «как ServiceNow» — только необходимые сущности;
- не является самостоятельным PagerDuty — подключается к on‑call системам.

---

## 3) Модель данных (сущности)
### 3.1 Основные сущности
- **Incident**: `id`, `title`, `status`, `severity`, `started_at`, `declared_at`, `mitigated_at`, `resolved_at`, `customer_impact`, `services`, `owners`, `tags`, `links[]`.
- **IncidentRoleAssignment**: `incident_id`, `role` (IC/Comms/Ops/SME/Scribe), `user_id`, `from`, `to`.
- **IncidentTimelineEvent**: `time`, `type` (alert/change/action/decision/comms), `text`, `author`, `refs[]`.
- **Postmortem**: `incident_id`, `summary`, `impact`, `root_causes[]`, `contributing_factors[]`, `what_worked`, `what_failed`, `detection_gaps`, `followups[]`, `attachments[]`.
- **ActionItem**: `id`, `incident_id`, `title`, `owner`, `due_date`, `status`, `verification`, `linked_ticket`.
- **CustomerUpdate**: `incident_id`, `audience`, `time`, `message`, `channel` (statuspage/email/inapp), `approved_by`.

### 3.2 Вспомогательные сущности
- **Service/Component** (лёгкий каталог): `service_id`, `name`, `tier`, `owner_team`, `slo_ref`.
- **OnCallPolicy**: `service_id`, `provider` (PagerDuty/Opsgenie), `schedule_ref`, `escalation_path`.
- **ChangeEvent**: деплой/конфиг/фича‑флаг, связанный с инцидентом.

---

## 4) Severity модель (простой, но жёсткий стандарт)
Рекомендуемая 4‑уровневая модель:
- **SEV1**: массовая недоступность/потеря данных/безопасность, критический бизнес‑ущерб → немедленная эскалация.
- **SEV2**: сильная деградация ключевых функций, затрагивает значимую долю пользователей.
- **SEV3**: частичная деградация/неосновной сервис, workaround возможен.
- **SEV4**: локальная ошибка/единичные обращения, анализ без «war room».

Правила:
- severity задаётся **при декларации** и пересматривается с фиксацией в таймлайне;
- severity определяет: роли, частоту апдейтов, обязательность постмортема, набор уведомлений.

---

## 5) Процесс (end‑to‑end), от простого к среднему
### Шаг 1. Детектирование
Источники:
- алерты (Observability & SRE),
- тикеты/обращения (Case Mgmt),
- автоматические проверки/мониторы.

Автодействия:
- если алерт соответствует SLO burn / критичности → предлагается «Declare Incident».

### Шаг 2. Декларация инцидента
Создаётся Incident, задаются:
- краткий заголовок (что сломалось + где),
- SEV,
- затронутые сервисы,
- первичный owner/IC,
- стартовый таймлайн (ссылки на дашборды, релизы, фича‑флаги).

### Шаг 3. War room (оперативная работа)
Авто‑создание «комнаты»:
- чат‑канал (Slack/Teams/Telegram),
- видеозвонок (опционально),
- доска действий,
- pinned: текущий статус, гипотезы, владельцы, next update time.

### Шаг 4. Митигирование
- фиксация решений/действий в таймлайне (scribe),
- запуск runbooks,
- создание action items в процессе (в т.ч. «проверить X», «откатить Y»).

### Шаг 5. Коммуникации
- внутренние апдейты по таймеру (например, каждые 15–30 мин для SEV1),
- внешние апдейты: статус‑страница / e‑mail / in‑app (с шаблонами, approvals).

### Шаг 6. Резолв и закрытие
- фиксируется момент «mitigated» и «resolved»,
- собираются ссылки на артефакты: графики, логи, PR, тикеты, изменения.

### Шаг 7. Постмортем (обязателен для SEV1–SEV2)
Шаблон постмортема:
- Summary (1–2 абзаца)
- Impact (кто/что/сколько/как долго)
- Detection (как заметили / почему поздно)
- Timeline (ключевые события)
- Root causes / Contributing factors
- What worked / What failed
- Action items (prevent / detect / mitigate)
- Follow-up verification (как убедимся, что исправили)

### Шаг 8. Выполнение действий и обучение
- action items попадают в backlog/владельцам,
- проверка выполнения (SRE/owner),
- runbooks и витрины обновляются,
- инцидент превращается в «кейс знаний» (KB / RAG).

---

## 6) API (минимум для интеграций)
### 6.1 Incident API
- `POST /incidents` — создать
- `PATCH /incidents/<built-in function id>` — обновить статус, severity, impact, сервисы
- `POST /incidents/<built-in function id>/roles` — назначить роли
- `POST /incidents/<built-in function id>/timeline` — добавить событие
- `POST /incidents/<built-in function id>/links` — прикрепить дашборды/алерты/тикеты/релизы
- `POST /incidents/<built-in function id>/customer-updates` — опубликовать/запланировать апдейт
- `POST /incidents/<built-in function id>/postmortem` — создать/обновить постмортем
- `POST /incidents/<built-in function id>/action-items` — завести action item
- `GET /incidents?status=open&sev=SEV1` — фильтры для UI/дашбордов

### 6.2 Webhooks
- `incident.declared`, `incident.updated`, `incident.mitigated`, `incident.resolved`
- `postmortem.published`
- `action_item.overdue`

---

## 7) Автоматизация (как «рационализация» превращается в продукт)
Ключ: **не изобретать новый велосипед**, а заставить уже существующие системы работать как единое целое.

Примеры автомакросов:
1. **Auto‑Declare from SLO burn**: если burn_rate > X → создать incident + добавить дашборд + уведомить on‑call.
2. **ChatOps bootstrap**: создать канал/тред, закрепить шаблон статуса, назначить IC.
3. **Timeline capture**: при каждом деплое/конфиг‑изменении рядом с инцидентом — событие в таймлайне.
4. **Customer update drafts**: генерация безопасного текста апдейта из фактов (без утечек).
5. **Postmortem generator**: собрать таймлайн + артефакты + превратить в черновик постмортема.
6. **Action item enforcement**: если postmortem опубликован, но нет action items — блокировать закрытие.
7. **Knowledge packaging**: инцидент → статья в KB + обновление runbook.

---

## 8) UI/UX (минимальный «офисный» интерфейс)
Экран **Incident Room**:
- шапка: SEV, статус, таймер, next update time
- роли: IC/Comms/Ops/Scribe
- вкладки: Timeline / Actions / Evidence / Comms / Postmortem
- быстрые кнопки: “Declare”, “Mitigate”, “Resolve”, “Create Update”, “Start Postmortem”

Экран **Postmortem Editor**:
- шаблон + подсказки (поля обязательности по SEV)
- список action items (owner+due)
- кнопка “Publish to Knowledge Vault”

---

## 9) Метрики (что измерять)
- **MTTA** (mean time to acknowledge)
- **MTTR** (mean time to resolve)
- **Incidents per service**
- **Repeat rate** (повторяемость root cause)
- **Alert quality**: false positives / noise
- **Action item completion rate**
- **Customer impact minutes**

---

## 10) Безопасность и комплаенс
- RBAC: кто может объявлять SEV1, кто публикует внешний апдейт
- аудит всех изменений
- redaction/маскирование секретов и персональных данных
- ретеншн: инциденты и постмортемы — отдельные политики хранения
- экспорт для юридических/регуляторных запросов (только согласованные поля)

---

## 11) MVP‑разрез (что сделать первым)
**MVP‑0 (самое простое):**
- Incident entity + статус + severity
- ручной таймлайн и roles
- связка с тикетингом (create ticket)
- базовый postmortem шаблон

**MVP‑1 (среднее):**
- автодекларация из алертов
- коммуникации шаблонами + approvals
- action items контроль и отчётность

**MVP‑2 (продвинуто):**
- генерация постмортема из артефактов
- knowledge packaging + обучение runbooks
- аналитика надёжности по сервисам/тенантам

---

## 12) Что дальше (следующий блок)
Следующий логичный блок: **Resilience / Chaos / GameDays (69601–70000)** — плановые упражнения, хаос‑тестирование, проверки DR‑планов, автоматизированная оценка готовности.

