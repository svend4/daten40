# IFOS 65601–66000 — API Gateway & Egress Control OS (v1)
Цель: сделать **центральный “шлюз наружу”** для всего IFOS, чтобы интернет перестал быть “дикой степью”.
Gateway/Egress Control OS отвечает за:
- единый путь наружу (outbound) для Sandbox/Runtime/Agents
- политики: allowlist/denylist, DNS/IP правила, порты, протоколы
- защита от SSRF/сканирования/утечек (DLP, квоты, аномалии)
- шифрование и доверие: TLS policies, mTLS, pinning (где возможно)
- аудит и доказательства: неизменяемые логи, “egress receipts”
- enterprise change control: заявки/approval на новые домены

Порядок: **простое → среднее → сложное**.

---

## 65601–65620 — Простое: зачем нужен единый шлюз
Если дать коннекторам прямой интернет:
- они могут сходить куда угодно (утечка данных/секретов),
- могут “случайно” сделать сканирование сети,
- сложно расследовать инциденты,
- сложно повторить эксперимент (неясно, какие вызовы и куда).

Поэтому правило:
> **Sandbox НЕ имеет прямого outbound. Всё только через Gateway.**

---

## 65621–65670 — Базовые сущности
### GatewayRoute
Маршрут “кто и как ходит наружу”:
- source: runtime/sandbox/service
- destination: домен/endpoint group
- policy stack: egress rule + tls policy + inspection profile + dlp policy
- quotas/rate limits
- logging mode (metadata-only vs full headers vs sampled body hashes)

### EgressRule
- allowlist доменов/портов
- запрет IP literal и private ranges
- запрет metadata endpoints (169.254.169.254 и аналоги)
- ограничения по методам (GET/POST)
- лимит размера request/response

### EgressSession
Короткий пропуск на outbound (как “lease”, только для сети):
- TTL (например 5–15 минут)
- connector_id/workflow_id/tenant_id
- связан с attestation sandbox run

---

## 65671–65725 — Среднее: DNS, домены, IP и защита от SSRF
Gateway делает проверки:
- DNS resolve только через контролируемый resolver
- блок private IP ranges (RFC1918, link-local)
- блок IP literal (когда в URL указан IP)
- optional: разрешение только определённых ASN/гео для некоторых провайдеров

Практика:
- policy “deny by default”
- добавление домена = через ticket/approval (enterprise режим)

---

## 65726–65785 — TLS policies: доверие к каналу
**TLSPolicy** может включать:
- min TLS version (1.2/1.3)
- запрет слабых шифров
- требование SNI
- certificate validation strict
- (опционально) pinning/CA allowlist для критичных партнёров
- mTLS для корпоративных API

Важно: gateway не всегда “расшифровывает” трафик. В базовом режиме он контролирует **куда** и **сколько**.

---

## 65786–65835 — Inspection profiles: что проверять в запросах
**InspectionProfile** определяет глубину контроля:
- L0: metadata only (домен/порт/размер/частота)
- L1: headers + content-type + body hash sampling
- L2: structured inspection для JSON (схемы, поля)
- L3: proxy mode (полная проверка), только если разрешено enterprise policy

Почти всегда достаточно L0–L1 + DLP на структурированных данных, чтобы резко снизить риск утечки.

---

## 65836–65895 — DLP: защита от утечек данных
**DLPPolicy**:
- классификация данных: public / internal / confidential / pii
- правила: запрещать/маскировать/требовать approval
- детекторы: email/iban/credit card, ключи, токены, паспорта, адреса
- “redaction”: вырезать чувствительные поля из логов (и иногда из outbound, если proxy-mode)

DLP применяется:
- на payload (если инспекция разрешена)
- на headers (например Authorization не логировать)
- на логи (всегда)

---

## 65896–65935 — Квоты и экономия: “сколько можно ходить”
Gateway вводит:
- per-tenant budgets (requests/day, MB/day)
- per-connector budgets
- per-destination budgets (чтобы не получить бан)
- circuit breaker (ошибки → пауза)

Это связывается с Pricing/Quotas OS:
- “free tier” — малые лимиты
- enterprise — расширенные, с approval и отчётностью

---

## 65936–65970 — Аномалии и сигналы атак
**AnomalyRule** выявляет:
- неожиданные домены
- всплеск трафика
- частые deny
- смена географии резолва
- “beaconing” (периодические малые запросы)

Реакции:
- auto-block route
- quarantine connector version
- revoke egress sessions
- создать incident ticket

---

## 65971–66000 — Сложное: receipts, неизменяемые логи и “доказательство вызова”
Gateway пишет **OutboundRequestLog**:
- кто (tenant, workflow, connector, sandbox run)
- куда (domain, path hash)
- когда (ts)
- сколько (bytes, duration)
- решение policy (allow/deny, rule_id)
- “receipt” = хэш записи + подпись gateway

Это позволяет:
- воспроизводить процессы,
- доказывать compliance,
- быстро расследовать инциденты.

---

## Что дальше
Следующий блок:
**66001–66400 — Data Exfiltration Detection & Forensics OS**  
(глубже про корреляцию логов, расследования, граф инцидентов, контекстная реконструкция, отчёты).
