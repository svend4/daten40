# IFOS 57201–57600 — Community & Contribution OS (сообщество и вклад) (v1)
Цель: превратить хаос “миллион плагинов/модулей” в **живую экосистему качества**:
люди добавляют коннекторы, макросы, уроки, витрины — а система обеспечивает:
- стандарты
- ревью
- модерацию
- репутацию
- борьбу со спамом
И всё это совместимо с Marketplace OS, Policy Engine, Learning OS и AI‑Refactoring OS.

Порядок: простое → среднее → сложное.

---

## 57201–57220 — Минимальный вклад (Personal → Public)
Самый простой сценарий:
1) Пользователь сделал полезный workflow/macro
2) Нажал “Share to Community”
3) Система:
   - обезличила (убрала PII)
   - проверила policy
   - собрала manifest
   - создала draft карточку + документацию
Выход: **черновик публикации**.

---

## 57221–57260 — Роли и права (Roles & Permissions)
Роли:
- Contributor (публикует черновики)
- Reviewer (ставит approve/changes)
- Maintainer (владелец пакета)
- Moderator (T&S)
- Council/Admin (правила, апелляции)
Принцип: **минимальные права**, “поднимайся по репутации”.

---

## 57261–57310 — Submission pipeline (как GitHub PR, но для IFOS)
Шаги submission:
- lint: формат карточки/manifest
- tests: smoke tests (run in sandbox)
- security: secret scan, policy checks
- doc: авто‑генерация runbook + примеры
- license: проверка лицензии
- version: semver + changelog
Статусы:
- draft → submitted → review → approved → published → deprecated

---

## 57311–57360 — Review model (PR‑ревью)
Как в pull request:
- diff (что изменилось)
- комментарии по строкам
- “request changes”
- approve
- merge/publish
Правила:
- минимум 1 review для low‑risk
- минимум 2 review для high‑risk
- security review для коннекторов/платежей

---

## 57361–57410 — Moderation & Trust & Safety
Что модератор делает:
- удаляет вредные/мошеннические пакеты
- блокирует спам
- реагирует на жалобы
- ставит quarantine
- ведёт кейсы и апелляции
Важно: прозрачные причины (reason codes).

---

## 57411–57460 — Ratings, Reviews, Reputation (почему “нет отзывов”)
Модель отзывов:
- rating (1–5) + “что понравилось/что нет”
- verified install/run (отзывы “проверены”)
- review categories: docs, reliability, value, support
Репутация автора:
- grows: installs, успешные runs, низкий refund rate, хороший support
- падает: жалобы, refunds, policy violations
Цель: показать людям **лучшие решения**, а не просто самые новые.

---

## 57461–57510 — Anti‑spam / Anti‑Sybil (борьба с мусором и накрутками)
Техники:
- rate limits
- proof-of-work / friction (капча/ожидание) для новых аккаунтов
- verified identity для “trusted”
- anomaly detection (всплески отзывов)
- graph‑based sybil detection
Если подозрение:
- quarantine
- manual review
Это делает поле “не диким”.

---

## 57511–57540 — Bounties & Grants (стимулы вместо хаоса)
Пулы задач:
- “нужен коннектор X”
- “нужен макрос Y”
- “нужна документация Z”
Формат:
- bounty (фикс)
- grant (проект)
- revenue share (маркетплейс)
Привязка к метрикам:
- оплачивать за **успешное внедрение** (runs), а не за “код”.

---

## 57541–57570 — Localization (многоязычие как вклад)
Локализация:
- перевод карточек/уроков/доков
- терминологический словарь (glossary)
- QA переводов
Роли:
- translator
- reviewer‑translator
Важно: не ломать смысл и policy-тексты.

---

## 57571–57590 — Marketplace publishing (выпуск в витрину)
После approve:
- создаётся витрина “официально”
- появляется кнопка install
- включается billing (если paid)
- заводится support channel
Требования:
- SLA для paid
- security baseline
- changelog

---

## 57591–57600 — Support & Triage (поддержка как часть качества)
Система поддержки:
- тикеты
- FAQ
- runbooks
- triage (bug/feature/question)
- связь с analytics (ошибка → тикет)
Поддержка повышает репутацию.

---

## Итог
Community & Contribution OS отвечает на ваш вопрос “почему нет вертикали и отзывов”:
- вводит PR‑модель, репутацию, модерацию
- связывает вклад с качеством и реальным использованием
- делает экосистему управляемой, как “магазин приложений + GitHub + офисный справочник”

---

## Что дальше
Следующий блок:
**57601–58000 — Standards & Interop OS: единые интерфейсы входов/выходов, совместимость плагинов, “driver model”, профили коннекторов**  
Скажете “Продолжение” — сделаю.
