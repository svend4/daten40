# IFOS 18001–18400 — UX & One‑Click‑OS: карточки‑витрины, wizard‑установщик, авто‑формы, one‑click кластеры, onboarding, explainable кнопки (why/what/undo), accessibility (v1)

Это слой, который делает вашу идею “всё уже есть — надо скомпоновать” **реально пригодной для людей**:
- не “1000 модулей”,
- а **понятные кнопки**,
- **установка одним нажатием**,
- **почему это безопасно/разрешено**,
- и **как откатить** (undo).

Ниже — по порядку, от простого к сложному.

---

## 18001–18060 — UI Cards (простое): как “прославлять” правильно

### 18001) Card = витрина ассета
Карточка — главный UI объект:
- что это (1 строка)
- что делает (3–5 bullets)
- уровень доверия (badges)
- время до первого результата (TTFS)
- “установить” + “показать план” + “откатить”
- примеры (use cases)
- отзывы + evidence score
- “что нужно” (аккаунты, токены, права)

### 18002) Card sections (стандартизировать)
- Summary
- Requirements
- Install options
- Evidence & Trust
- Tutorials
- Troubleshooting
- Pricing (если есть)
- Changelog

---

## 18061–18140 — Installer Wizard (среднее): одна кнопка, но с умом

### 18061) Wizard steps
1) Проверка режима (sandbox/personal/team/b2b/gov)  
2) Проверка требований (accounts, tokens, scopes)  
3) Выбор адаптеров (make/n8n/wp/native)  
4) Dry‑run / smoke test  
5) Install plan (что будет создано)  
6) Apply  
7) Post‑install checklist (первый успешный запуск)

### 18062) Install Plan (всё прозрачно)
План установки — как “terraform plan”:
- какие сущности создаст (jobs, secrets, webhooks)
- какие права запросит
- какие изменения сделает
- какие риски (network access, PII)

---

## 18141–18210 — Auto‑Forms (среднее+): “ввод данных без боли”

### 18141) Auto‑Form generator
Из schema/requirements автоматически строится форма:
- поле
- валидации
- подсказки
- безопасный ввод секретов
- проверки токена (test connection)

### 18142) Form presets
Готовые наборы:
- Telegram bot token
- Google OAuth
- RSS sources
- WordPress admin creds
- Stripe keys (если биллинг)

---

## 18211–18290 — Onboarding (сложнее): обучение как “быстрое прохождение”

### 18211) Onboarding flow
- “выберите цель”: news digest / compare portal / dropship
- “выберите платформу”: make/n8n/wp/native
- “соберите первый кластер” (шаблон)
- “первый запуск” + “что дальше улучшить”
- “план роста” (2‑3 улучшения)
- “ссылка на плейбуки”

### 18212) Skill‑aware onboarding
Если в Knowledge‑OS есть skill graph:
- показывать только нужные шаги
- объяснять термины на лету (glossary tooltip)

---

## 18291–18360 — Explainable actions (why/what/undo): кнопка должна объясняться

### 18291) Explainable button model
Любая кнопка “Install/Run/Publish” имеет:
- WHY: почему это предлагается (trace)
- WHAT: что именно произойдёт (plan)
- RISK: риски и режимы
- UNDO: как откатить (rollback plan)
- PROOF: ссылки на evidence, policy decision, audit event

### 18310) Undo/Rollback
Откат должен быть:
- пошаговым
- проверяемым
- безопасным (не удалять пользовательские данные без подтверждения)
- логируемым (audit)

---

## 18361–18400 — Accessibility & Reliability UI (самое сложное в UX‑слое)

### 18361) Accessibility profile
Поддержка:
- крупные шрифты, контраст
- “режим простых слов”
- озвучивание подсказок (TTS) — опционально
- минимизация шагов (wizard compact)
- “режим оператора” (минимум текста, максимум статусов)

### 18380) Telemetry “где люди ломаются”
UI‑телеметрия (анонимно/с согласием):
- на каком шаге wizard бросили
- какая ошибка чаще
- какой пресет непонятен
Это критично для рационализации: улучшать реальное узкое место.

---

## Приложения (в этом пакете)
- JSON Schemas: ui card, install wizard, auto form, onboarding flow, explainable button, undo plan, cluster template, ui state machine, ui telemetry, accessibility profile
- Specs: cards, installer wizard, auto forms, onboarding, undo/rollback, explainable actions, accessibility
- OpenAPI: UX & One‑Click API (MVP)
- Examples: card + wizard + form + onboarding + explainable buttons + undo plan + telemetry events + a11y profile
- Python skeletons: ui cards renderer, installer engine, form builder, undo engine, telemetry collector
