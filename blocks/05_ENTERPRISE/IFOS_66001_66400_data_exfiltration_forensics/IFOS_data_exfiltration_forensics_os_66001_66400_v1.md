# IFOS 66001–66400 — Data Exfiltration Detection & Forensics OS (v1)
Задача: когда “интернет-ОС” начинает исполнять тысячи интеграций и коннекторов, нужна не только безопасность,
но и **форензика**: быстро понять *что произошло*, *что утекло*, *через какой коннектор/маршрут*, *какие были доказательства*,
и *как закрыть дыру без остановки всей системы*.

Этот блок дополняет:
- Sandbox/Attestation OS (65201–65600)
- Gateway/Egress Control OS (65601–66000)

И вводит 4 главных продукта:
1) **Сигналы и алерты** (exfil detection)
2) **Кейс-менеджмент** (incident cases)
3) **Корреляция и реконструкция** (граф событий)
4) **Доказательства и отчёты** (chain-of-custody, receipts, forensic reports)

Порядок: **простое → среднее → сложное**.

---

## 66001–66030 — Простое: “что считать утечкой”
Утечка = не только “слили базу”. В IFOS это часто выглядит так:
- внезапно вырос outbound трафик у одного workflow/коннектора
- появился новый домен назначения
- выросло число deny/blocked событий (кто-то пытается пробить политики)
- DLP стал находить PII/секреты в outbound payload
- “beaconing”: маленькие запросы каждые N секунд
- последовательность запросов похожа на “экспорт” (страницы 1..N, батчи)

Минимальная цель: **фиксировать событие**, связать с workflow/tenant и поднять сигнал.

---

## 66031–66110 — Базовые события и единый формат логов
### IncidentEvent (универсальное событие)
Источник:
- gateway outbound logs (allow/deny + receipts)
- sandbox attestation events
- secrets vault events (rotation, access)
- runtime errors (всплеск 4xx/5xx)
- identity events (вход нового ключа/пользователя)

Событие должно иметь:
- correlation ids: tenant_id, workflow_id, connector_id, route_id, sandbox_run_id
- timestamps: event_ts + ingest_ts
- severity + category (exfil, auth, policy, anomaly)
- minimal “payload” (без секретов)

**Главное правило:** логи пишутся так, чтобы их можно было использовать как доказательство:
- неизменяемость (append-only)
- receipts/подписи на критичных событиях
- строгая маскировка секретов

---

## 66111–66185 — Среднее: детекторы (signals) и правила (alert rules)
### Detector
“Датчик” — это функция/модуль, который вычисляет сигнал:
- EGRESS_MB_PER_MINUTE
- NEW_DOMAIN_SEEN
- DLP_MATCH_COUNT
- DENY_SPIKE
- TOKEN_LEAK_PATTERN
- BEACONING_SCORE

### AlertRule
Правило:
- какой сигнал
- порог/окно
- фильтры (tenant, connector, route)
- реакция (notify, quarantine, revoke sessions, block route)

Механика:
- Rules должны быть версионированы
- “dry-run” режим (record_only) перед включением block действий
- каждое правило должно ссылаться на policy justification (почему так)

---

## 66186–66245 — Среднее+: кейс-менеджмент (incident cases)
Case = “папка расследования”:
- статус: opened → triage → investigating → contained → resolved → postmortem
- владелец (on-call / security / ops)
- список связанных событий (event_ids)
- список доказательств (evidence items)
- решения containment (что блокировали/отозвали/поменяли)
- ссылки на отчёты и задачи

Важно: **сохранять контекст** (кто принял решение, когда, почему).

---

## 66246–66315 — Сложное: корреляция и граф реконструкции
### CorrelationGraph
Граф соединяет:
- identity → token/secret → connector version → sandbox run → gateway route → outbound destinations
- добавляет временную линию и причинные связи

Преимущества:
- быстро увидеть “цепочку утечки”
- быстро определить radius (что ещё могло пострадать)
- формировать “для суда/аудита” понятный отчёт

Практика:
- вершины: Actor, Credential, Connector, Workflow, Route, Destination, Dataset, Event
- рёбра: USED, ISSUED, DEPLOYED, CALLED, EXFILTRATED_TO, BLOCKED_BY, ROTATED

---

## 66316–66375 — Доказательства: chain-of-custody и receipts
**EvidenceItem** — любой артефакт, который подтверждает факт:
- receipt bundle (набор подписанных gateway receipts)
- экспорт логов (с хэшем)
- конфиги policy/route на момент события
- attestation отчёт sandbox run
- снимок версии коннектора/хэши

**Chain-of-custody**:
- кто извлёк доказательство
- когда
- откуда
- какой хэш
- где хранится (WORM storage / immutable bucket)

Это превращает “лог” в “доказательство”.

---

## 66376–66400 — Автоматизированные отчёты и postmortem
**ForensicReport**:
- кратко: что произошло
- timeline
- root cause
- impact (какие данные/системы)
- containment действия
- remediation план
- “controls to add” (какие правила/политики усилить)

Авто-генерация:
- собрать события по case_id
- построить граф
- вставить receipts и ссылки на evidence
- сформировать executive summary + технический annex

---

## Что дальше
Следующий блок:
**66401–66800 — Data Loss Prevention (DLP) Deep & Classification OS**  
(единая классификация данных, контракты, маркеры, политики хранения/передачи и “правила мира” для всех коннекторов).
