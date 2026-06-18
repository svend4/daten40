# IFOS 72401–72800 — AIOps: Correlation, Regression Detection & Root Cause

**Slug:** `aiops_correlation_root_cause`  
**Категория:** Observability & Reliability · **Приоритет:** P2 · **Версия:** 0.31.0

## 0) Контекст и цель (почему этот блок появляется именно сейчас)
К этому моменту у IFOS уже есть:
- SLO/SLI + error budgets (70401–70800)
- progressive delivery/rollbacks (70801–71200)
- synthetic monitoring journeys (71601–72000)
- RUM (72001–72400)
- incident response/postmortems (69201–69600)

Проблема: данные **есть**, но без «мозга корреляций» люди тонут в сигнале.
Этот блок — **AIOps слой**, который:
1) связывает события между слоями (frontend → API → сервисы → релизы/флаги → SLO)  
2) автоматически ищет **регрессии** и **вероятные причины**  
3) формирует **объяснимые выводы**: “что сломалось”, “где”, “после чего”, “что откатить/выключить”, “кому пинговать”.

---

## 1) Что делает блок (от простого к сложному)

### Уровень A — Нормализация сигналов и «единый язык инцидентов»
1. **Единый формат сигнала** (Signal Event):
   - метрика, окно времени, агрегат, измерения (tenant/region/release/flag)
   - степень отклонения (z-score / delta% / p-value)
2. **Unify IDs**:
   - release_id, deploy_id
   - trace_id (если есть)
   - feature_flag_snapshot
   - service/endpoint identity (из service catalog / topology)

### Уровень B — Детектор регрессий (Regression Engine)
3. **Базовые правила (Rule-based)**:
   - error_rate вырос X% за Y минут
   - p95 LCP/INP вырос выше порога после релиза
   - SLO burn-rate превышен
4. **Сравнение окон (before/after)**:
   - pre-release window vs post-release window
   - контрольный сегмент vs проблемный сегмент
5. **Сегментация**:
   - браузер/OS (RUM), регион, tenant, plan
   - endpoint/service (backend)
   - фичефлаг (flag on/off cohorts)

### Уровень C — Корреляция и кандидат «root cause»
6. **Корреляция по времени**:
   - “спайк начался через N минут после deploy”
7. **Корреляция по общим измерениям**:
   - тот же release_version, тот же region, тот же endpoint
8. **Causal hints (простые причинные эвристики)**:
   - если деградирует только один endpoint → вероятная причина: сервис/endpoint
   - если деградация только на flag=ON → причина: флаг/фича
   - если деградация в одном регионе → сеть/инфра/edge
   - если только один браузер → frontend compatibility
9. **Top-K candidates**:
   - ранжирование причин по score (impact × confidence × scope)

### Уровень D — Рекомендации и автоматические действия (Action Suggestions)
10. **Explainable Recommendations**:
   - “Откатить deploy_id=…”
   - “Выключить feature_flag=… для cohort=…”
   - “Переключить трафик/регион”
   - “Увеличить лимиты/квоты”
11. **Подготовка артефактов для инцидента**:
   - auto-timeline
   - ссылки на дашборды
   - список affected tenants
   - первичный postmortem skeleton

---

## 2) Что блок НЕ делает (важно)
- Не заменяет инженера SRE/DevOps: даёт **гипотезы**, а не «абсолютную истину».
- Не гарантирует ML-модель «как у больших облаков». MVP — эвристики + статистика.
- Не чинит сам по себе — он **информирует** и может запускать безопасные автодействия только при политике/разрешениях.

---

## 3) Ключевые сущности данных

### 3.1 SignalEvent
- `signal_id`, `ts_start`, `ts_end`
- `source`: `rum|synthetic|slo|logs|traces|deploy|flags`
- `metric`: `lcp_p95|error_rate|burn_rate|latency_p95|...`
- `delta`: абсолют/процент
- `severity`: `info|warn|critical`
- `dimensions`: {region, release, tenant, service, endpoint, browser, flag}
- `links`: dashboard URLs / trace sample links

### 3.2 RegressionFinding
- `finding_id`
- `signals[]` (какие сигналы вызвали finding)
- `baseline_window`, `current_window`
- `impact_score`, `confidence_score`, `scope_score`
- `affected_entities`: tenants/services/routes

### 3.3 RootCauseCandidate
- `candidate_type`: `release|flag|service|endpoint|region|dependency`
- `candidate_id` (например, `deploy_id`, `flag_key`, `service_name`)
- `evidence[]` (ссылки на сигналы)
- `score`: 0..1
- `recommended_actions[]`

### 3.4 Recommendation
- `action_type`: `rollback|disable_flag|route_shift|scale|notify_owner`
- `action_payload` (что именно)
- `safety_level`: `suggest|require_approval|auto_if_policy_allows`
- `explanation` (человеческое)

---

## 4) Минимальный API (MVP)
- `POST /aiops/signal` — принять сигнал (или batch)
- `POST /aiops/detect` — прогнать детекторы (cron/trigger)
- `GET /aiops/findings?since=...`
- `GET /aiops/root_cause?finding_id=...`
- `POST /aiops/recommendations/apply` — применить действие (если политика разрешает)

---

## 5) Алгоритмы MVP (практично)

### 5.1 Regression detection
- rolling baseline: median/p75 из прошлого окна
- change-point: простая проверка z-score / percent jump
- burn rate: классическая формула SLO (быстрое/медленное окно)

### 5.2 Correlation scoring (простое)
Score = w1*time_overlap + w2*dimension_match + w3*impact + w4*cohort_split

Пример эвристик:
- +0.3 если совпадает release_version
- +0.2 если совпадает region
- +0.2 если совпадает endpoint/service
- +0.2 если spike начался в пределах 0–15 минут после deploy
- +0.1 если cohort flag=ON деградирует сильнее flag=OFF

### 5.3 Cohort comparison (фичефлаги)
- сравнение распределений метрики в двух группах: ON vs OFF
- “lift” = (p95_on - p95_off) / p95_off

---

## 6) Зависимости и интеграции

### Входы
- 70401–70800 SLO/SLI
- 70801–71200 progressive delivery
- 51201–51600 feature flags
- 71601–72000 synthetic journeys
- 72001–72400 RUM
- (опционально) 69201–69600 постмортемы как “обучающие примеры”

### Выходы
- 69201–69600 Incident Response (авто-тикеты, авто-таймлайн)
- 72801–73200 Service Catalog/Topology (owner routing)
- 55201–55600 policy engine (разрешение автодействий)

---

## 7) Дашборды (минимальные)
1. **Regressions overview** (последние 24h)
2. **Finding details** (сигналы + кандидаты причин)
3. **Release impact** (релиз → метрики → SLO/ошибки)

---

## 8) “One-click” результат
После установки блока пользователь получает:
- поток findings (регрессии)
- top-K root cause кандидатов с объяснением
- кнопки “rollback/disable flag/open incident” (при разрешениях)
- автогенерацию таймлайна инцидента

