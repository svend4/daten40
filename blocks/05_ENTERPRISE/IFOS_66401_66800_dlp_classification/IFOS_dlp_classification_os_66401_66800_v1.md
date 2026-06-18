# IFOS 66401–66800 — DLP Deep & Data Classification OS (v1)
Цель: превратить “дикий интернет” (миллионы интеграций) в управляемую систему, где **данные имеют тип/класс**,
а любая передача данных наружу подчиняется правилам: *что можно*, *куда можно*, *в каком виде*, *с каким логом/receipt*.

Этот блок связывает три слоя:
- **Data OS** (типы сущностей/активов)
- **Gateway/Egress Control** (маршруты наружу)
- **Forensics** (доказательства/кейсы)

Главные идеи:
1) **Единая таксономия данных** (DataClass + DataLabel)
2) **Сканирование и классификация** (scanners + signals)
3) **DLP-политики** (rules → policies → policy packs)
4) **Data Contracts**: что коннектор/процесс *имеет право* читать/писать/передавать
5) **Редакция/обезличивание** (redaction profiles)
6) **Transfer Decision**: стандартизированное решение “ALLOW / TRANSFORM / DENY” с объяснимостью

Порядок: **простое → среднее → сложное**.

---

## 66401–66440 — Простое: минимальная таксономия данных
### DataClass (класс данных)
Минимальный набор (можно расширять):
- PUBLIC — публичные данные
- INTERNAL — внутренние (не для внешней публикации)
- CONFIDENTIAL — конфиденциальные
- PII — персональные данные
- FINANCIAL — финансы/платёжные данные
- HEALTH — медицинские данные
- SECRETS — токены/ключи/пароли
- IP — интеллектуальная собственность (код, модели, чертежи)

### DataLabel (ярлыки)
Ярлыки уточняют контекст:
- REGION:EU, REGION:DE, REGION:US
- CUSTOMER:*, TENANT:*
- SOURCE:CRM, SOURCE:HR, SOURCE:Docs
- PURPOSE:Support, PURPOSE:Billing, PURPOSE:Analytics
- RETENTION:90D/365D/7Y
- EXPORT:Allowed/Restricted

Правило: **класс = риск**, ярлык = контекст.

---

## 66441–66510 — Базовое: сканирование и классификация
### Scanner
Сканер — модуль, который анализирует контент (payload, файлы, таблицы):
- regex/heuristics (email, IBAN, passport)
- dictionary (ключевые слова)
- ML classifier (опционально)
- структурный анализ (CSV/JSON keys)
- secret detectors (JWT, API keys patterns)
- OCR — только если нужно (дорого/рисково)

### ClassificationResult
Выход:
- detected_classes: [PII, FINANCIAL]
- labels: [REGION:EU, PURPOSE:Billing]
- confidence
- evidence: какие правила сработали (без раскрытия секретов)
- redaction_suggestions

Важно: результат **не должен** содержать сырой секретный контент.

---

## 66511–66600 — Среднее: DLP rules → DLP policies
### DlpRule
Правило вида:
- IF (class=PII AND region=EU AND dest not in allowlist) THEN DENY
- IF (class=SECRETS) THEN DENY + open incident
- IF (class=CONFIDENTIAL AND purpose=Support) THEN TRANSFORM (mask) + ALLOW

### DlpPolicy
Политика собирает набор правил и режим:
- mode: monitor_only / enforce
- sampling: 0..1 (сколько payload можно инспектировать)
- redaction_profile: строгий/сбалансированный
- escalation: какой тип инцидента открыть

Плюс:
- версионирование
- dry-run перед enforce
- “justification” (почему правило существует)

---

## 66601–66670 — Среднее+: редация и обезличивание
### RedactionProfile
Определяет, как трансформировать данные:
- mask_email (a***@b.com)
- mask_iban (DE** **** **** **** 1234)
- hash_id (sha256 + salt)
- tokenize (vault tokens)
- remove_fields (удалить ключи JSON)
- aggregate (вместо списка → count/sum)

Важно:
- редация должна быть **детерминированной** (для аналитики) либо **недетерминированной** (для приватности) — явно задаётся.
- редация фиксируется в **TransferDecision** и в receipts/логах.

---

## 66671–66740 — Сложное: Data Contracts (контракты данных)
Контракт отвечает на вопрос: **кто** (workflow/connector/role) может:
- READ какие классы данных (и откуда)
- WRITE куда
- TRANSFER наружу (какие домены/маршруты)
- TRANSFORM каким профилем
- RETAIN сколько и где хранить

Контракт:
- scope (tenant, env, workflow)
- allowed_data_classes + required_labels
- allowed_destinations (routes/allowlists)
- required_controls (sandbox, receipts, encryption)
- audit requirements

Контракт становится “документом истины” для проверки коннекторов и процессов.

---

## 66741–66800 — Decision Engine: единое решение на каждый outbound
### TransferDecision
На каждый outbound запрос/пакет:
- decision: ALLOW / TRANSFORM / DENY
- policy_id + rule_id
- classified: detected classes/labels
- applied_redaction_profile (если TRANSFORM)
- receipts_required (true/false)
- reason_code + human_reason
- correlation ids (tenant/workflow/connector/route)

Это связывает DLP, Gateway и Forensics:
- Gateway исполняет решение
- Forensics использует decision + receipts как доказательство
- Аналитика видит статистику нарушений/срабатываний

---

## Что дальше
Следующий блок:
**66801–67200 — Secure Data Sharing & Synthetic Data OS**  
(шэринг данных между командами/тенантами, песочницы, синтетические наборы для тестов, “demo datasets”, безопасные примеры и test keys).
