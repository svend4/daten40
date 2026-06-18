# IFOS 63601–64000 — Edge & Client Connectivity OS (v1)
Цель: считать “плохую сеть” **нормой**, а не исключением.  
Этот блок превращает клиентские проблемы (Android, PWA, нестабильный Wi‑Fi/4G, VPN, captive portal) в:
- политики (offline/retry/sync)
- шаблоны (service worker, resumable upload)
- измеримость (RUM/telemetry)
- воспроизводимость (debug playbook)

Порядок: **простое → среднее → сложное**.

---

## 63601–63620 — Простое: 10 реальностей “плохой сети”
1) сеть пропадает на 2–10 секунд (handover, лифт, метро)  
2) DNS иногда “задумывается”  
3) captive portal (Wi‑Fi требует логин)  
4) прокси/VPN режет WebSocket  
5) HTTPS инспекция (enterprise MITM) ломает цепочку сертификатов  
6) мобильный браузер выгружает вкладку из памяти  
7) фоновые таймеры “спят”  
8) большие файлы рвутся на 60–90%  
9) один и тот же запрос отправляется дважды (повтор кнопки/ретраи)  
10) на слабом устройстве UI фризит → пользователь жмёт снова

Вывод: нужен набор **политик**, а не “ещё один фикс”.

---

## 63621–63670 — PWA / Offline‑First OS
### Компоненты
- Service Worker (кэш стратегий)
- IndexedDB (локальная очередь)
- background sync (где доступно)
- offline UI состояния (banner, queue size, retry)

### Стратегии кэша
- `Cache First` для статики (иконки/шрифты)
- `Stale‑While‑Revalidate` для каталогов/витрин
- `Network First` для критичных данных (платежи/профиль)

IFOS хранит offline_policy: что кэшируем, что очередим, что запрещаем.

---

## 63671–63740 — Retries/Backoff/Idempotency OS
**Главная мысль:** ретраи без idempotency создают дубликаты.
- генерируем `Idempotency-Key` для POST/PUT
- на сервере храним результат по ключу (TTL)
- используем exponential backoff + jitter
- различаем retryable ошибки (timeouts, 502, 503) и non‑retryable (400, 401, 403)

IFOS хранит retry_policy: лимиты, таймауты, классификацию ошибок.

---

## 63741–63810 — Client Sync & Conflict Resolution
Когда клиент работает офлайн:
- операции пишутся в локальную очередь
- при онлайне отправляются батчами
- конфликты решаются:
  - LWW (последняя запись побеждает) для простого
  - merge по полям (для документов)
  - CRDT/OT (для совместного редактирования) — сложный режим

IFOS задаёт sync_plan: сущности, разрешение конфликтов, окно синхронизации.

---

## 63811–63870 — Реалтайм: WebSocket/SSE/Long‑Polling Fallback
Порядок деградации:
1) WebSocket (идеально)
2) SSE (часто проходит там, где WS режут)
3) long‑polling (всегда работает, но дороже)

IFOS хранит realtime_profile: протоколы, интервалы, heartbeat, условия переключения.

---

## 63871–63920 — CDN/Edge Cache OS
Задачи:
- ускорить витрины/поиск/карточки
- снизить нагрузку на API
- пережить пики трафика

Правила:
- статика кэшируется долго
- “каталоги” коротко с revalidate
- персональные ответы не кэшируются на edge (или строго по Vary/Authorization)

IFOS хранит cdn_plan: пути, TTL, Vary, purge, версионирование ассетов.

---

## 63921–63970 — Resumable Upload/Download OS
Для больших файлов:
- chunked upload (частями)
- контроль целостности (hash)
- resume после обрыва
- parallel chunks (по политике)
- server-side assembly

IFOS хранит transfer_policy: размер чанка, параллельность, лимиты, правила повторов.

---

## 63971–64000 — RUM/Telemetry + Debug Playbook
Чтобы не “угадывать”:
- собираем RUM события (TTFB, CLS, errors, network type)
- фиксируем trace-id из API ответов
- делаем playbook “если жалоба X → проверь Y → исправь Z”

---

## Что дальше
Следующий блок:
**64001–64400 — Browser Security & Client Integrity OS**  
(CSP, SRI, CSRF, cookies, storage isolation, clickjacking, mobile webview pitfalls).  
Напишите “Продолжение” — сделаю.
