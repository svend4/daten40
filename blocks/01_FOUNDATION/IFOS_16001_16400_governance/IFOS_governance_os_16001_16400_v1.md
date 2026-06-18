# IFOS 16001–16400 — Governance‑OS: evidence courts, арбитраж/споры, лицензии/права, анти‑фрод отзывов, и “конституция” реестра (v1)

Этот блок завершает архитектуру “Internet Function OS” как **управляемого пространства**, а не дикого поля.
Он отвечает на вопросы:
- почему нет “вертикали качества”
- почему нет честных отзывов и сравнимых рейтингов
- почему плагины/рецепты не “владеют ответственностью”
- как решать конфликты и ошибки без хаоса
- как публиковать и переиспользовать артефакты законно (IP/licensing)

Ниже — по порядку: от простого к сложному.

---

## 16001–16040 — Публикация = контракт ответственности (простое)

### 16001) Любой листинг должен иметь “паспорт публикации”
Минимум:
- кто издатель
- какая лицензия
- какие ограничения/риски (flags)
- какой уровень доказательности (evidence L0–L3)
- как выглядит процесс поддержки (support channels)

### 16002) Почему это критично
Без этого отзывы бессмысленны:
- люди сравнивают разные версии, разные режимы, разные условия
- “не работает” ≠ “плохо” (может не тот ключ, лимиты, регион)

Решение: **все отзывы должны ссылаться на run/evidence context** (или явно быть “без доказательств”).

---

## 16041–16100 — Evidence Courts: “суды доказательности” (среднее)

### 16041) Evidence Court = журнал проверок
Это не суд про людей — это “суд” про утверждения.
Пример утверждения:
- “этот рецепт отправляет дайджест RSS в Telegram стабильно”
- “этот bundle не утечёт секреты и не пишет PII в логи”

### 16042) Что хранит court record
- claim_id (что утверждается)
- evidence_refs (L0–L3)
- verdict (PASS/WARN/FAIL)
- reasoning (почему)
- jurisdiction (node/tenant/community)
- signatures/hashes (tamper‑evidence)

### 16043) Почему это сильнее “звёздочек”
Потому что:
- проверяемые критерии
- воспроизводимость
- привязка к версиям, контрактам и policy flags

---

## 16101–16170 — Арбитраж и споры (сложнее)

### 16101) Типовые споры
- “bundle вредоносный / скрытые side effects”
- “издатель украл код/нарушил лицензию”
- “отзывы накручены”
- “trust score несправедливый”
- “доказательства поддельные или нерепрезентативные”

### 16102) Dispute Case
Дело содержит:
- стороны (claimant / respondent)
- объект спора (listing_id, publisher_id)
- требования (take down, re-score, mark as risky, refund, etc.)
- доказательства (audit, runs, contracts, code hashes)
- решения и санкции
- апелляции

### 16103) Уровни решения
- L0: автоматические правила (policy / signatures / malware scan)
- L1: модератор (community)
- L2: арбитражная коллегия (enterprise/consortium)
- L3: федеративный совет узлов (межузловой спор)

---

## 16171–16240 — Лицензии/права и “повторное использование” (IP layer)

### 16171) Почему лицензии обязательны
В экосистеме “миллионы деталей” основная проблема не техника, а право:
- можно ли переработать
- можно ли продавать
- можно ли включать в bundle
- обязателен ли attribution
- можно ли тренировать модели на документации/логах

### 16172) License Policy для артефакта
- license_id (SPDX‑like)
- allowed_uses (commercial/non-commercial)
- redistribution (allowed/forbidden)
- modifications (allowed/forbidden)
- attribution_required
- training_allowed (for AI)
- patent_grant (yes/no)
- export_restrictions (optional)

### 16173) “Compatibility of licenses”
Сборка витрины должна проверять:
- можно ли вместе поставить компоненты
- не конфликтуют ли условия (например GPL‑infecting vs proprietary)

---

## 16241–16320 — Анти‑фрод отзывов и манипуляций (сложное)

### 16241) Основной принцип
Рейтинг должен быть “evidence‑weighted”:
- verified evidence > stars
- реальные run stats > текстовые отзывы
- audit signals > маркетинг

### 16242) Сигналы накрутки (MVP)
- всплеск установок без run usage
- много отзывов с одного диапазона IP/устройств
- одинаковый текст
- отзывы без context (нет run_id, нет version)
- “review rings”: группы аккаунтов, которые ставят друг другу

### 16243) Действия системы
- снижать вес подозрительных отзывов
- требовать evidence для влияния на trust
- отправлять в модерацию
- временно замораживать listing (sandbox-only)

---

## 16321–16400 — “Конституция реестра” и санкции (самый высокий уровень)

### 16321) Конституция = правила экосистемы
Определяет:
- кто может публиковать (KYC/verified publishers — опционально)
- какие минимальные требования (contracts, license, flags)
- процесс модерации и апелляции
- типы санкций и сроки
- федеративную синхронизацию black/allow lists
- прозрачность: публичные отчёты

### 16322) Санкции (Sanctions)
- warning (label + ограничение)
- delist (снять с витрин/поиска)
- quarantine (только sandbox)
- ban publisher (на узле)
- federation ban (межузловой)
- score freeze (заморозить рейтинг до проверки)

### 16323) Апелляции
- срок
- требования к доказательствам
- независимый состав
- публикация результата (summary)

---

## Приложения (в этом пакете)
- JSON Schemas: dispute case, evidence court record, license policy, review fraud signals, sanction, appeal, constitution
- Specs: governance rules, arbitration workflow, licensing/IP, review antifraud, publication compliance
- OpenAPI: Governance API (MVP)
- Examples: claim + court record + dispute + sanction + appeal + license policy + constitution snippet
- Python skeletons: antifraud scoring + dispute workflow state machine
