# IFOS 61601–62000 — Enterprise Connectors & Credential Vault OS (v1)
Цель: закрыть “узкое горлышко” интеграций (API‑ключи, OAuth, сертификаты, тестовые окружения), чтобы IFOS реально работал как “B2B‑операционная система интернета”, а не как набор разрозненных скриптов.

Порядок: **простое → среднее → сложное**.

---

## 61601–61630 — Базовое: зачем Vault
Vault = системная подсистема IFOS, которая:
- безопасно хранит секреты (API keys, OAuth tokens, passwords, certificates)
- выдаёт секреты только по политике (policy)
- инжектит в рантайме (runner/connector) без утечки в UI/логи/экспорт
- ведёт аудит (кто/когда/зачем использовал)
- поддерживает dev/stage/prod/sandbox профили

**Правило №1:** секреты не попадают в bundle/export; в логах — только редактированные (redacted) значения.

---

## 61631–61680 — Модель секретов (Secret Model)
Секрет — это объект метаданных + зашифрованное значение:
- `secret_id`, `name`, `kind` (api_key/oauth_token/password/certificate/token_map)
- `scope`: workspace/project/env
- `connector_id` (опционально) — привязка к коннектору
- `tags`: sandbox/prod/shared/rotatable/compromised
- `expires_at` + TTL
- `storage`: envelope encryption (DEK+KEK), KMS key id

Поддерживаемые формы:
- single value (API key)
- map (client_id + client_secret + extra)
- blob (PEM/CRT)
- oauth refresh token + metadata

---

## 61681–61720 — Среды и профили (Env Profiles)
Env Profile задаёт “контекст запуска”:
- env: dev / stage / prod / sandbox
- region: eu / us / onprem
- network: egress allowlist
- logging: redaction + уровень
- policy pack: набор правил для секретов/раннеров

Каждый run выбирает profile → Vault понимает, какие секреты допустимы.

---

## 61721–61770 — Test keys & Sandbox creds (учебные ключи)
Чтобы снизить порог входа (и решить вопрос “где взять тестовые ключи/данные”):
- каталог официальных sandbox/test окружений провайдеров
- mock endpoints (локальные эмуляторы API)
- shared demo tenants (ограничены квотами)
- авто‑reset (например раз в сутки) для учебных ключей
- кнопка **“Use sandbox credentials”** в мастере установки bundle

Идея: пользователь нажимает 1–2 кнопки и сразу запускает демо без кредитки/договора.

---

## 61771–61820 — Требования коннектора к ключам (Credential Requirements)
Каждый connector обязан описать:
- тип auth: api_key / oauth2 / basic / mTLS / custom
- список полей (какие секретные, какие нет)
- где получить (doc link)
- scopes/permissions
- какие env поддерживает (sandbox/prod)
- health check (тестовый запрос)

Это превращает хаос интеграций в “унифицированные драйверы/словарь функций”.

---

## 61821–61860 — Политики (Policies): кто что может
Policy engine решает:
- кто может создавать/использовать/ротировать/отзывать секреты
- можно ли использовать prod‑секрет в dev/sandbox (обычно НЕТ)
- можно ли делиться секретом внутри workspace
- запрет экспорта секретов (always true)
- можно ли bundle требовать секреты класса “prod”

Policy packs версионируются и могут быть отраслевыми (финансы/медицина/гос).

---

## 61861–61910 — Ротация, отзыв, TTL, “компрометация”
Минимальный enterprise‑набор:
- TTL/expiry
- manual revoke
- scheduled rotation
- auto‑rotation (если провайдер позволяет)
- пометка `compromised` → блокировать run’ы и требовать замену
- “break‑glass” доступ: аварийный режим с усиленным аудитом

---

## 61911–61940 — Аудит (Audit events)
Audit event фиксирует:
- actor (user/service)
- secret_id
- action (create/use/rotate/revoke/deny)
- timestamp
- decision (allowed/denied)
- context (run_id, connector_id)
- policy snapshot hash

Отдельный журнал безопасности, не смешивается с обычными логами.

---

## 61941–61970 — Шифрование и KMS/HSM (SaaS и on‑prem)
Архитектура:
- envelope encryption (DEK шифрует секрет, KEK защищает DEK)
- KEK хранится в KMS (cloud) или HSM/on‑prem
- BYOK (bring your own key) для крупных компаний
- sealed backups + key rotation

Это позволяет IFOS работать как:
- SaaS
- self‑hosted (сервер/контейнер/мини‑кластер)
- “локальный офисный узел” (без облака)

---

## 61971–61990 — Runtime injection (Broker): секреты только в памяти
Секреты выдаются через брокер:
1) runner запрашивает `secret_ref` (без значения)
2) vault проверяет policy → выдаёт ephemeral token
3) connector получает секрет через secure channel
4) секрет живёт только в памяти процесса
5) redaction автоматически чистит вывод/логи

Это защищает от утечек через экспорт, скриншоты и “случайно залили на GitHub”.

---

## 61991–62000 — UI путь: “одна кнопка”
Правильный UX:
1) Install bundle
2) Wizard: выбрать env = sandbox/dev
3) “Use sandbox creds” → авто‑подстановка
4) Run test → health checks
5) Затем “Switch to prod” → добавить prod secrets
6) Включить rotation policy

Итог: интеграции становятся массово применимыми, а не “для технарей”.

---

## Что дальше
Следующий блок:
**62001–62400 — Sandbox, Mocking & Test Data OS** (генерация тестовых данных, mock‑серверы, запись/реплей, fixtures, demo‑тенанты).  
Напишите “Продолжение” — сделаю.
