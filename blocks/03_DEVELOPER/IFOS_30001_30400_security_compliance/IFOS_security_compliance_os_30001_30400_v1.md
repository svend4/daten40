# IFOS 30001–30400 — Security & Compliance OS (v1)
Цель: сделать “интернет‑функции” **безопасными**, чтобы “установка в 1 клик” не превращалась в вирус/утечку/хаос.

Порядок: от простого к среднему и далее к сложному.

---

## 30001–30040 — Secrets: секреты как ссылки (а не значения)
Принцип №1: **секреты не хардкодятся** в конфиге.
В конфиге хранится только `secret_ref`, а значение лежит в secret store.

SecretRef:
- имя (secretref.telegram.bot)
- назначение (Telegram bot token)
- политика доступа (кто может читать/менять)
- ротация (как часто менять)

Плюс: можно безопасно экспортировать/делиться пакетами/бандлами без утечки токенов.

---

## 30041–30090 — RBAC: роли и права
Role Based Access Control:
- Viewer: смотреть
- Operator: запускать/останавливать
- Editor: менять конфиги/витрины
- Admin: секреты, политики, подписи, публикация

RBAC применяется к:
- пакетам
- коннекторам
- витринам
- авто‑починке (autofix)
- публикации в marketplace

---

## 30091–30140 — Policies: политика как код
Policy определяет:
- какие домены/сети разрешены
- какие типы действий разрешены (install, run, export, webhook)
- лимиты (частота, объём данных, стоимость)
- требования approvals (например “high risk autofix требует Admin”)

Это “конституция” системы.

---

## 30141–30180 — Audit: журнал доверия (что кто сделал)
AuditEvent:
- actor (user/agent/service)
- action (install/run/update_secret/publish)
- object_ref (package/job/vitrine)
- ts
- result (ok/denied)
- diff (что изменилось)
- correlation ids (run_id, trace_id)

Если случилось “почему так вышло” — audit отвечает без эмоций.

---

## 30181–30220 — Package Signing: подписи пакетов
Пакет должен быть подписан:
- publisher_id
- signature
- hash всех файлов
- версия

Цель: защита от подмены.
Marketplace принимает только подписанные пакеты (или помечает “unverified”).

---

## 30221–30260 — Supply Chain Attestations: происхождение сборки
Attestation фиксирует:
- откуда код (repo commit)
- какая сборка (CI job id)
- какие зависимости (lockfile)
- скан уязвимостей (SBOM)

Это защита от “встроенного трояна” в цепочке зависимостей.

---

## 30261–30310 — Sandbox: безопасный запуск
SandboxProfile ограничивает:
- сеть (allowlist доменов)
- файловую систему (read-only / tmp)
- CPU/RAM/timeout
- запреты (no shell, no exec)
- изоляцию процессов

Сandbox нужен для:
- новых пакетов
- непроверенных коннекторов
- исполнения “скриптов” из marketplace

---

## 30311–30360 — Permission Requests: запросы разрешений как в Android
PermissionRequest:
- что просит пакет (network: api.telegram.org, read: drive, write: sheets)
- зачем (reason)
- срок (1 запуск / 24ч / постоянно)
- кто одобрил

Это делает “установку” прозрачной: пользователь видит, что реально будет происходить.

---

## 30361–30400 — Safe One‑Click Install: установка в 1 клик, но безопасно
Алгоритм “1 клик”:
1) verify signature
2) check attestation + SBOM
3) run policy engine (RBAC + org policy)
4) show permissions (what/why)
5) dry-run (проверка секретов/квот/эндпоинтов)
6) sandbox first run
7) enable + monitoring (alerts + health checks)

Результат: **скорость как у App Store**, но **контроль как у enterprise**.

---

## Мини‑архитектура Security & Compliance OS
SecretRef → RBAC → Policy Engine → Audit → Signing → Attestations → Sandbox → Permissions → Safe One‑Click Install

---

## Что дальше логически
Следующий блок (если скажете “Продолжение”):
**30401–30800 — Marketplace & Distribution OS**: каталог пакетов, рейтинги/отзывы, “витрины”, ценовые модели, dependency resolution, install/run lifecycle, версии и совместимость.
