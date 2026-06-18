# IFOS — Operating Model: Roles, Teams, RACI, SLAs (Human+AI org design) (Блок 68001–68400)

Версия: v1 · Пакет: `IFOS_68001_68400_operating_model_roles_teams_raci_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок

IFOS — не просто софт, а **операционная система функций**.
Чтобы она реально работала, нужен **Operating Model**:
- кто отвечает за registry, mapping, качество, безопасность,
- как принимаются изменения,
- как работают SLA/инциденты,
- как встроены AI‑агенты (аналитик/менеджер/архитектор).

Этот блок переводит IFOS из «папки документов» в **работающую организацию**.

## 1) Принцип: Human+AI команда

Роли делятся на:
- **Human owners** (несут юридическую и финальную ответственность)
- **AI assistants** (ускоряют: поиск, предложения, черновики)
- **AI controllers** (авто‑проверки, policy checks, drift alerts)

## 2) Базовые домены работ (teams)

1) Registry & Ontology
2) Connectors & SDK
3) Marketplace & Curation
4) Trust & Safety (модерация)
5) Security & Privacy
6) Runtime & Reliability
7) UX & Templates (витрины, офис‑UI)
8) Data Quality & Provenance
9) Enterprise / Sales / Support

## 3) Роли (каталог)

- **Product Owner (IFOS Core)**: roadmap, приоритеты
- **Registry Curator**: добавление/правка записей
- **Ontology Steward**: тезаурус, связи capabilities
- **Connector Engineer**: коннекторы, тест‑харнесс
- **QA / Verification**: evidence, smoke tests
- **Trust & Safety Moderator**: политики контента
- **Security Engineer**: секреты, ключи, доступ
- **Privacy/Compliance Officer**: GDPR, retention
- **SRE/Operations**: инциденты, аптайм
- **Support/Case Manager**: тикеты, disputes
- **Docs/Knowledge Engineer**: пакеты, документация
- **AI Copilot Manager**: promptpacks, guardrails
- **Data Steward**: дедуп, lineage, quality

## 4) RACI матрицы (ключевые процессы)

### 4.1 Добавление нового коннектора в Marketplace
- R: Connector Engineer
- A: Marketplace Owner
- C: Security, Privacy, Trust&Safety
- I: Product Owner, Support

### 4.2 Обновление capability mapping
- R: Registry Curator
- A: Ontology Steward
- C: QA/Verification, Connector Engineer
- I: UX Team

### 4.3 Реакция на drift (сломался API)
- R: SRE + QA
- A: Connector Owner
- C: Support, Marketplace
- I: Product Owner

### 4.4 Инцидент по приватности
- R: Security Engineer
- A: Privacy Officer
- C: Legal, Product
- I: Customers (по процедуре)

## 5) SLA / SLO / OLA (пример)

- **SLO uptime**: 99.5% (P0 runtime)
- **SLA support**: ответ ≤ 24h (paid), ≤ 72h (free)
- **OLA** между командами: Security review ≤ 3 рабочих дня
- **Drift fix**: critical connectors ≤ 48h

## 6) Change management (как меняется система)

1) Proposal (issue/PR)
2) Auto checks (policy, schema, tests)
3) Human review (RACI)
4) Staging (demo env)
5) Release workflow (publishing)
6) Post‑release monitoring (observability)

## 7) Где тут AI‑агенты (3‑уровневая модель)

### Operational agents
- автоклассификация
- извлечение функций из README/OpenAPI
- дедуп/нормализация

### Tactical agent (AI‑manager)
- приоритизация тикетов
- рекомендации альтернатив
- поиск root cause по инцидентам

### Strategic agent (AI‑architect/mentor)
- проверка целостности архитектуры
- поиск дыр и предложения новых блоков
- сценарное планирование roadmap

## 8) Дыры/что ещё нужно

- Нужна модель KPI/OKR по доменам.
- Нужна система прав доступа (RBAC) в UI и API.
- Нужны playbooks для инцидентов и коммуникации.

## 9) Зависимости

### Hard deps
- 34001–34400 `enterprise_governance_os`
- 36001–36400 `enterprise_identity_access_os`
- 42801–43200 `case_management_ticketing_os`
- 46001–46400 `publishing_release_workflow_os`
- 34801–35200 `observability_reliability_os`

### Optional deps
- 55201–55600 `compliance_policy_engine_os`
- 59601–60000 `enterprise_rollouts_change_control_os`
