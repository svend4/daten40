# IFOS 68401–68800: Supply-chain Monitoring & Auto-Remediation OS (SBOM/CVE/Alerts/Rebuild)
Дата: 2026-01-02  
Версия: v1

## 0) Зачем этот блок
Предыдущий блок **Reproducible Builds & Signing** (manifest/build recipe/SBOM/provenance/подписи/verification policy) отвечает на вопрос: *«Можно ли доверять тому, что я устанавливаю?»*  

Этот блок отвечает на следующий вопрос, без которого "one‑click bundles" превращаются в риск:

**«Что делать, когда завтра найдут уязвимость (CVE) в зависимости/пакете/коннекторе — кого затронуло, кого уведомить, что заблокировать, что пересобрать и как доказать, что исправлено?»**

То есть: **не разовая проверка**, а *непрерывный контур* мониторинга поставки (supply chain): SBOM → сопоставление с advisory/CVE → оценка риска → алерты → авто‑действия (block/quarantine/rebuild/patch) → аудит/отчёт.

---

## 1) Объекты и термины (главные сущности)
### 1.1 Advisory / CVE / Bulletin
*Сигнал риска* из внешнего мира:
- CVE и записи NVD / CNA
- security advisories (GitHub, vendor advisories, OSV и др.)
- бюллетени (CERT, вендор‑порталы)

**Advisory** в IFOS нормализуется до единого формата (см. JSON Schema `IFOS_advisory_schema_v1.json`).

### 1.2 SBOM
Список компонентов/зависимостей конкретного пакета/бандла/сборки (из прошлого блока).  
SBOM — "карта того, что внутри".

### 1.3 Scan Result
Результат процедуры сопоставления SBOM ↔ advisory:
- найденные совпадения (match)
- степень уверенности (confidence)
- правила исключений (suppression)
- итоговый риск и рекомендации

### 1.4 Affected Graph
Граф "кто затронут":
- Package → Version → Dependency tree
- Bundle → Installed instance → Tenant/Org/Project
- Runtime job history (где исполнялось)

### 1.5 Alert & Notification
Стандартизированные оповещения:
- кому (владельцу пакета, пользователям, enterprise‑админам)
- куда (email/webhook/Slack/Telegram/ServiceNow/Jira)
- с каким приоритетом и дедлайном
- с подтверждением получения (ack)

### 1.6 Remediation Plan
План действий:
- блокировка установки/запуска
- карантин (ограничение сети/доступов)
- rebuild пакета/бандла
- bump dependency / patch
- rollout/проверки

### 1.7 Auto‑Actions (политики автоматизации)
Набор политик: "если риск ≥ X и эксплуатируемость высокая → сделать Y".

---

## 2) Основной конвейер (Pipeline) — от простого к сложному
### Уровень 1: Минимальный (ручной)
1. Импорт advisory/CVE (по расписанию или вручную)
2. Скан SBOM выбранного пакета
3. Создание алерта владельцу пакета
4. Ручной выпуск patched‑версии

**Что даёт:** уже уменьшает хаос и даёт "единую правду" по уязвимостям внутри IFOS.

### Уровень 2: Командный (полу‑авто)
1. Автоскан всех опубликованных пакетов по расписанию
2. Автосопоставление SBOM ↔ advisory
3. Создание тикета (Jira/GitHub Issues) + уведомления пользователям
4. Политика запрета установки/обновления при Critical
5. Проверка patched‑версии (smoke tests) и публикация

**Что даёт:** marketplace начинает "сам себя защищать".

### Уровень 3: Enterprise (авто‑ремедиация и аудит)
1. Multi‑source ingestion (NVD/OSV/GHSA/vendor feeds) + дедупликация
2. Учет контекста эксплуатации: internet‑facing? есть ли exploit? EPSS? runtime signals?
3. Автоматические действия:
   - block install / quarantine runtime
   - forced upgrade
   - emergency rebuild + re‑sign + publish receipt
4. Рассылка и подтверждение (ack) + SLA дедлайны
5. Полный аудит: кто был затронут, когда исправлено, кем подтверждено

**Что даёт:** "операционная безопасность" как сервис.

---

## 3) Политики риска (Risk Policy)
Риск = не только CVSS. В IFOS используем композицию факторов:

- **Severity**: критичность (CVSS v3/v4), вендор‑оценка
- **Exploitability**: наличие PoC/эксплойта, EPSS (если доступно)
- **Exposure**: где используется компонент (public API, server‑side, client‑side)
- **Reachability**: достижимость уязвимого кода по данным (если есть)
- **Prevalence**: сколько инсталляций/тенантов/бандлов затронуто
- **Compensating controls**: sandbox/ограничения прав/изоляция
- **Confidence**: уверенность матчинга (SBOM→advisory)

Политика задаётся в `vuln_policy` (см. `IFOS_vuln_policy_schema_v1.json` + seed CSV).

---

## 4) Стратегии действий (Remediation Strategies)
### 4.1 Block / Gate
- запрет установки пакета
- запрет публикации в public канал
- запрет запуска workflow (если пакет — критическая часть раннера)

### 4.2 Quarantine
- ограничения сети (deny egress)
- ограничение секретов/доступов
- снижение квот

### 4.3 Patch / Upgrade
- bump зависимости
- backport patch (если upstream не выпускает)
- замена компонента

### 4.4 Rebuild / Re-sign / Republish
- сборка по build recipe
- генерация нового SBOM + provenance
- подпись + publish receipt
- forced rollout для инсталляций (если включено)

### 4.5 Compensating controls
- включить WAF rule / rate limit
- отключить опасную функцию
- feature flag

---

## 5) Интерфейсы (Control Plane API)
См. файл `IFOS_supply_chain_monitoring_control_plane_api_v1.yaml`:
- Ingest advisory
- Trigger scan (package/bundle/tenant/channel)
- Get scan results + affected graph
- Create/ack/close alerts
- Create remediation plan + execute actions
- Query compliance report (audit)

---

## 6) Минимальные артефакты, которые должны появиться в системе
- `Advisory` (normalized)
- `ScanResult`
- `AffectedGraph` (или ссылочный набор affected entities)
- `Alert`
- `RemediationPlan`
- `ExecutionReceipt` (ссылка на факт выполнения действий)
- `ComplianceReport` (для аудита)

---

## 7) Пример сценариев (коротко)
### Сценарий A: Critical CVE в популярной библиотеке
1) приходит advisory  
2) совпало в SBOM у 120 пакетов  
3) policy: Critical + exploit confirmed → block installs в public  
4) владельцам пакетов созданы тикеты + уведомления  
5) авто‑rebuild для тех пакетов, где patch = bump dependency без breaking changes  
6) публикация и forced upgrade в enterprise‑тенантах

### Сценарий B: False positive
1) advisory совпал по имени, но версия не уязвима  
2) confidence низкая → требует ручного подтверждения  
3) добавляется suppression rule (с TTL и обоснованием)  
4) следующие сканы не тревожат

---

## 8) Definition of Done (готовность блока)
- ingestion минимум из 2 источников (например GHSA + OSV)
- скан SBOM + матчинги + риск‑оценка
- алерты + подтверждение получения
- политики auto‑block/quarantine
- rebuild→re‑sign→republish (связь с прошлым блоком)
- отчёт “кто затронут / когда исправлено”
