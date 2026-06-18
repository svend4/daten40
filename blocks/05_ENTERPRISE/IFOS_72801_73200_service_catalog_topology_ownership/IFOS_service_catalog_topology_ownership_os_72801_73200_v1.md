# IFOS Block 72801–73200 — Service Catalog, Topology Graph & Ownership (Owner Routing)

## 1) Зачем нужен блок
Интернет и корпоративные экосистемы «богаты функциями», но бедны **связями и ответственностью**: есть тысячи коннекторов, приложений, плагинов, сценариев — но часто непонятно:
- какой «сервис» реально существует (что именно он делает);
- кто за него отвечает (владелец, команда, дежурный);
- от чего он зависит и что сломается вслед за ним (топология/граф);
- где инструкции (runbook), какие SLO/SLI, какие алерты и KPI;
- кому автоматически назначать тикет/инцидент и как эскалировать.

Этот блок закрывает системную дыру «**кто отвечает за что**» и даёт топологию для AIOps/корреляций, ранжирования, компилятора решений и *one-click bundles*.

## 2) Что входит в блок (Scope)
### 2.1 Service Catalog (каталог сервисов)
Для каждого сервиса хранится:
- идентификатор и название
- описание «что делает» (capabilities)
- домен/продукт/линия бизнеса
- критичность (Tier 0–4), класс данных, влияние (impact)
- владелец: команда / конкретная роль (Service Owner, Tech Lead, SRE, Security)
- каналы связи: Slack/Teams/Email, on-call расписание
- ссылки: репозиторий, документация, runbook, dashboard, SLO, алерты
- окружения: prod/stage/dev, регионы

### 2.2 Topology Graph (граф зависимостей)
Типы узлов:
- service, database, queue, topic, api, job, third-party, cloud-resource
Типы связей:
- depends_on / calls / publishes_to / consumes_from / stores_in / authenticates_via
Каждая связь имеет:
- направление, тип, важность, latency/timeout, версия контракта, owner

### 2.3 Ownership & Owner-Routing (маршрутизация ответственности)
Правила назначения:
- инциденты, алерты, тикеты, задачи качества данных, задачи безопасности
- кто первичный ответственный (owner), кто резерв, кто эскалация
- эскалационные политики: SLA на реакцию, ступени, часы работы/дежурства
- правила «какой сигнал куда»: severity×tier×домен×регион×фича-флаг×релиз

## 3) Что блок НЕ делает (out of scope)
- Не заменяет систему мониторинга (метрики/логи/трейсы) — лишь связывает её с сервисами.
- Не заменяет тикет-систему — лишь маршрутизирует и синхронизирует.
- Не хранит секреты (это Credential Vault блок) — хранит только ссылки/политики доступа.
- Не «магически» строит топологию полностью автоматически: поддерживает импорт + частичную автодетекцию.

## 4) Пользовательские сценарии (User Stories)
1. **Инцидент**: «Падает API оплаты в регионе EU» → система находит сервис, tier, owner, on-call, зависимости, открывает тикет и запускает runbook.
2. **Дежурный**: получает алерт и сразу видит: сервис, последних релизов, связанные SLO, upstream/downstream.
3. **Аналитик качества**: находит, какие пайплайны и витрины зависят от датасета, и кому назначать задачу.
4. **Планировщик решений**: по намерению пользователя («подключить CRM→Email→Sheets») выбирает сервисы/коннекторы и предлагает проверенные связки.
5. **Безопасность**: список сервисов, работающих с PII, и владельцы; контроль согласований.

## 5) Минимальная модель данных (MVP)
### 5.1 Entity: Service
- service_id (slug)
- name
- description
- tier (0..4)
- domain
- owner_team_id
- oncall_policy_id
- runbook_url
- docs_url
- repo_url
- dashboards[] (urls)
- slo_refs[] (ids)
- tags[] (e.g., payments, eu, b2b)

### 5.2 Entity: Team
- team_id
- name
- contacts (email, chat)
- escalation_chain[] (team_id/user_id)
- timezone
- working_hours

### 5.3 Entity: TopologyEdge
- edge_id
- from_type/from_id
- to_type/to_id
- relation (calls/depends_on/reads/writes/queues)
- criticality (low/med/high)
- contract_version
- notes

### 5.4 Entity: RoutingRule
- rule_id
- signal_type (incident/alert/ticket/data_quality/security)
- match (tier, domain, region, severity, tags)
- assign_to (team_id, queue_id, oncall_policy_id)
- escalate_to (policy)
- auto_actions (create_ticket, page_oncall, runbook_link)

## 6) API (черновик)
- GET /catalog/services?query=&tier=&domain=&tag=
- GET /catalog/services/{service_id}
- POST /catalog/services (RBAC: admin/service-owner)
- GET /topology/graph?scope=service:{id}&depth=2
- POST /topology/edges (bulk import)
- GET /ownership/routes/resolve?signal=alert&service_id=...&severity=...
- POST /incidents/{id}/route (назначить по правилам + sync в тикетинг)

## 7) UI (витрины)
- **Service Page**: карточка сервиса + SLO + алерты + runbook + владельцы + граф зависимостей.
- **Topology Explorer**: интерактивная карта зависимостей (фильтры: tier, домен, region).
- **Owner Dashboard**: «что на мне» (инциденты, тикеты, просрочки SLO, change-планы).
- **Routing Simulator**: тест правил (почему сигнал попал именно сюда).

## 8) Импорт / синхронизация
Источники:
- репозитории (README/ каталоги runbooks)
- monitoring (labels: service=, team=)
- kubernetes (service discovery)
- CI/CD (pipeline→service mapping)
- тикетинг (queues/owners)
Поддержка:
- bulk CSV/JSON
- webhook/cron синхронизация
- дедупликация (совпадение по slug/URL/labels)

## 9) Seed-данные (пример)
См. файлы:
- IFOS_service_catalog_seed_72801_73200_v1.csv
- IFOS_topology_edges_seed_72801_73200_v1.csv

## 10) Критерии готовности (Definition of Done)
- Есть каталог сервисов, поиск и карточка сервиса.
- Есть граф зависимостей и просмотр цепочек upstream/downstream.
- Есть owner-routing и симулятор правил.
- Интеграция с инцидентами/тикетами: «назначение» + ссылки на runbook/SLO.
