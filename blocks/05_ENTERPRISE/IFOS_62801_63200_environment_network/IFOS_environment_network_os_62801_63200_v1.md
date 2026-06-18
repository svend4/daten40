# IFOS 62801–63200 — Environment & Network OS (v1)
Цель: сделать сетевую “магию” **описуемой, проверяемой и автоматизируемой**.  
Если 62401–62800 отвечал “какой профиль деплоя выбрать”, то этот блок отвечает:
- как устроены **dev/stage/prod** среды
- как “видят друг друга” сервисы (private net, service discovery)
- почему внешние API иногда не доступны (egress/NAT/allowlist)
- как правильно настроить DNS/сертификаты
- как реализовать Zero‑Trust доступ (для корпоративных интеграций)

Порядок: **простое → среднее → сложное**.

---

## 62801–62820 — Простое: 5 типовых причин сетевых проблем
1) **Неверный DNS** (домен не указывает туда, куда надо)  
2) **TLS/сертификат** (не тот CN/SAN, нет chain, просрочен, нет HTTPS → cookies ломаются)  
3) **CORS/Origin mismatch** (на самом деле это сетевой policy на уровне браузера)  
4) **Egress ограничения** (платформа блокирует исходящий трафик или нужен allowlist у партнёра)  
5) **Private network** (сервисы в разных сетях/регионах, нет маршрута/ACL)

---

## 62821–62870 — Модель окружений (dev/stage/prod) и конфиги
IFOS фиксирует стандарт:
- **dev**: быстро, можно “грязно”, максимум логов, mock/replay разрешены
- **stage**: похоже на prod, но с тестовыми ключами/данными, контракт‑тесты обязательны
- **prod**: строгие политики, минимум прав, мониторинг/алерты, секреты только через vault

Каждая среда = env_profile:
- домены (app/api/webhooks)
- разрешённые origins
- зависимости (db/queue/object storage)
- сетевые политики (ingress/egress)
- лимиты и квоты
- регион/резиденция данных

---

## 62871–62930 — DNS & Certificates OS
### DNS записи
- A/AAAA: прямой IP (редко в PaaS)
- CNAME: домен → домен платформы
- TXT: верификация, DKIM/SPF, ACME challenges
- MX: почта (если нужно)

### Сертификаты
- автоматические (Let’s Encrypt/managed certs)
- корпоративные (custom CA)
- wildcard (*.example.com) для мультисервисных систем

IFOS хранит “DNS план” и “cert план” как артефакт: чтобы не было ручного хаоса.

---

## 62931–63010 — Egress/NAT/Allowlist OS (самая больная тема B2B)
Когда внешний партнёр говорит: “мы пускаем только **разрешённые IP**”:
- нужен **STATIC_EGRESS_IP** (фиксированный исходящий IP)
- или NAT gateway, или egress proxy
- IFOS должен уметь показать текущие egress IP и дать “IP package” для партнёра

Egress policy описывает:
- разрешённые домены/порты
- запреты (например, блокировать “любой интернет” в enterprise)
- прокси/сертификаты (MITM в корп. сетях)
- rate limits и backoff

---

## 63011–63080 — Private Network + Service Discovery
Для multi‑service систем (frontend/api/worker/db):
- сервисы общаются по **внутренним именам** (service discovery)
- доступ к db/queue только из private net
- публичный вход только через gateway

Service discovery может быть:
- DNS‑based (api.internal)
- platform‑native (service name)
- mesh/sidecar (сложнее, enterprise)

---

## 63081–63140 — API Gateway / Reverse Proxy OS
Задача gateway:
- единая точка входа (https://api.example.com)
- маршрутизация (/v1/*, /webhooks/*)
- rate limiting
- auth/headers normalization
- WAF rules (если надо)
- TLS termination

В IFOS gateway — это “драйвер”: набор правил маршрутов, который можно переносить между платформами.

---

## 63141–63180 — Network Observability (trace id, логи, диагностика)
Чтобы быстро понимать “где ломается”:
- добавляем `X-Request-Id` / `Trace-Id` в каждый запрос
- логируем вход/выход (без PII)
- собираем latency и ошибки по маршрутам
- делаем “network trace report”

---

## 63181–63200 — Zero‑Trust Access (корпоративные интеграции)
Для enterprise:
- доступ к админке/консолям только через SSO/VPN/ZTNA
- IP allowlist для входа
- mTLS между сервисами (если нужно)
- policies: кто и что может вызвать (service‑to‑service auth)

---

## Что дальше
Следующий блок:
**63201–63600 — Multi‑Cloud & Hybrid Connectivity OS**  
(федерация окружений, синхронизация конфигов, on‑prem ↔ cloud, tunnel, connector gateways).  
Напишите “Продолжение” — сделаю.
