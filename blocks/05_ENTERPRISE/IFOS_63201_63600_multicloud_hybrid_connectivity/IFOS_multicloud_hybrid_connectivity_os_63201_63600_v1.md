# IFOS 63201–63600 — Multi‑Cloud & Hybrid Connectivity OS (v1)
Цель: **соединять разные среды и облака** так, чтобы это было:
- безопасно (Zero‑Trust, минимальные права, аудит)
- повторяемо (promotion, sync, immutable artifacts)
- управляемо (federation control plane)
- наблюдаемо (health, latency, traces)
- совместимо с корпоративными сетями (on‑prem, прокси, allowlists)

Порядок: **простое → среднее → сложное**.

---

## 63201–63225 — Простое: когда вообще нужен hybrid/multi‑cloud
Типовые причины:
1) партнёр/заказчик требует “у нас on‑prem, в облако нельзя”
2) данные должны оставаться в ЕС, но пользователи в разных регионах
3) нужен фиксированный egress IP и корпоративный прокси
4) разные компоненты дешевле/удобнее на разных платформах
5) нужна отказоустойчивость (DR) в другом облаке

---

## 63226–63270 — Federation: единая модель многих сред
**Federation** = набор окружений (env profiles) + правила связности:
- env.dev.eu, env.stage.eu, env.prod.eu
- env.prod.us (если можно)
- env.onprem.corp (корпоративная среда)

В федерации задаём:
- какие среды “официальные”
- какие артефакты и версии разрешены
- как происходит promotion (dev → stage → prod)
- какие сети и маршруты разрешены

---

## 63271–63330 — Tunnel & Gateway (соединяем сети безопасно)
Чтобы on‑prem мог общаться с cloud:
- **tunnel** (входящий/исходящий) через агент/коннектор
- **hybrid gateway** как точка стыка (policy enforcement)

Режимы:
- outbound‑only (корп. сеть не принимает вход)
- mutual tunnels (двусторонне)
- hub‑and‑spoke (центральный gateway + окружения)

Важно: минимум открытых портов, всё через mTLS/identity.

---

## 63331–63380 — Config Sync & Promotion (синхронизация и “выпуск релиза”)
IFOS вводит “job”:
- взять конфиги/секрет‑refs из dev
- применить трансформации (stage/prod substitutions)
- проверить политики (compliance engine)
- задеплоить / обновить gateway routes
- запустить smoke tests и rollback если нужно

**Идея:** “деплой” = управляемое продвижение состояний, а не ручная магия.

---

## 63381–63430 — Cross‑Env Routing Policy (кто с кем может говорить)
Правила:
- prod не ходит в dev
- dev может ходить в stage (опционально)
- on‑prem ↔ prod только через gateway
- webhooks принимаются только в prod/stage
- выделенные каналы для ETL (data plane)

Маршруты задаются как policy‑объекты: “источник → назначение → allowed endpoints/ports”.

---

## 63431–63490 — Cross‑Cloud Identity & Trust (самое важное)
Чтобы сервисы в разных облаках доверяли друг другу:
- выдаём сервис‑идентичности (service accounts)
- используем mTLS + короткоживущие токены
- ротация ключей
- аудит событий

IFOS описывает trust‑модель:
- кто issuer, кто audience
- какие scopes
- как проверяется подпись

---

## 63491–63535 — Data Residency & Multi‑Region Data Plane
Классы данных:
- PII/персональные (строго EU)
- агрегаты/метрики (можно глобально)
- кэш/derived (можно ближе к пользователю)

Политика:
- где хранится “источник правды”
- как реплицируется (read replicas)
- где можно вычислять ранжирование/аналитику
- правила удаления/retention

---

## 63536–63575 — Backup/DR/Failover
DR‑план включает:
- RPO/RTO
- что бэкапим (db, object storage, configs)
- как переключаемся (DNS failover, gateway routing)
- как возвращаемся назад (failback)
- как тестируем DR (игровые дни)

---

## 63576–63600 — Cost Visibility (стоимость multi‑cloud)
IFOS собирает cost model:
- стоимость compute, storage, egress, managed db, NAT
- “дорогие операции” (egress в другое облако, NAT gateway)
- оптимизации (кэш, региональные реплики, batching)

---

## Что дальше
Следующий блок:
**63601–64000 — Edge & Client Connectivity OS**  
(PWA/offline, мобильные сети, captive portals, retry/backoff, websocket fallbacks, CDN edge caching).  
Напишите “Продолжение” — сделаю.
