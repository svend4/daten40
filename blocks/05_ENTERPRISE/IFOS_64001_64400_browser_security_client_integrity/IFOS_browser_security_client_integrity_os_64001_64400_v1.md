# IFOS 64001–64400 — Browser Security & Client Integrity OS (v1)
Цель: превратить “безопасность браузера” из набора случайных хаков в **политику**, которую:
- легко применять (шаблоны, пресеты)
- легко проверять (security checks, audit)
- легко отлаживать (playbook)
- трудно сломать “случайным изменением”

Порядок: **простое → среднее → сложное**.

---

## 64001–64020 — Простое: минимальная модель угроз для IFOS
Что реально ломают в браузерных системах:
1) **XSS** (скрипт встраивается в страницу и крадёт токены/данные)
2) **CSRF** (чужой сайт заставляет браузер отправить действие)
3) **Clickjacking** (невидимый iframe, пользователь “кликает не туда”)
4) **Token leakage** (токены лежат в localStorage или попали в URL/логи)
5) **Dependency / supply‑chain** (подменили библиотеку/скрипт CDN)
6) **CORS misconfig** (любой домен читает API)
7) **WebView pitfalls** (мобильные webview ломают cookie/redirect/ssl pin)
8) **Session fixation / replay** (неправильные refresh/rotate политики)
9) **Abuse/bots** (скрейпинг, накрутка отзывов, bruteforce)
10) **Misleading UX** (двойные клики, повторные запросы → финансовый ущерб)

Вывод: безопасность = набор **ограничений по умолчанию** + явные исключения.

---

## 64021–64070 — Security Headers OS (быстрое усиление)
Базовый набор заголовков:
- `Strict-Transport-Security` (HSTS)
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy`
- `Permissions-Policy`
- `Content-Security-Policy` (см. следующий блок)
- `X-Frame-Options` или CSP `frame-ancestors` (от clickjacking)

IFOS хранит **headers_policy**: какие заголовки, значения, исключения по путям.

---

## 64071–64140 — CSP + SRI (главный щит от XSS и подмен)
### CSP
- запрет inline‑скриптов (или только nonce)
- запрет eval
- whitelist доменов для script/img/connect
- отдельная политика для admin/console (строже)

### SRI
Если подключаете внешние скрипты/стили:
- фиксируете hash (`integrity="sha384-..."`)
- `crossorigin="anonymous"`

IFOS хранит **csp_policy** и **sri_rules**.

---

## 64141–64210 — CSRF + Sessions (не путать с XSS)
Если вы используете cookie‑сессии:
- включайте `SameSite=Lax/Strict` где возможно
- для опасных операций применяйте CSRF токен (double submit или server-side token)
- разделяйте домены: `app.` и `api.` (осторожно с cookie scopes)

Если вы используете bearer‑токены:
- CSRF обычно не применим, но важнее XSS (не хранить токен в localStorage)

IFOS хранит **csrf_policy** и **session_rotation**.

---

## 64211–64280 — Cookies & Storage (куда класть токены)
Правило по умолчанию:
- **session cookie httpOnly + Secure** для web (если архитектура позволяет)
- refresh token хранить максимально защищённо (httpOnly cookie)
- access token короткий (5–15 минут), refresh rotation
- избегать localStorage для чувствительных токенов (XSS)

IFOS хранит **cookie_policy**: домен, path, SameSite, Secure, httpOnly, TTL.

---

## 64281–64330 — CORS / Isolation / Cross‑Origin
Установки по умолчанию:
- `Access-Control-Allow-Origin` = строго список доменов
- `Allow-Credentials` только при необходимости
- ограничить методы/заголовки
- использовать preflight кэширование корректно

Дополнительно (средне‑сложно):
- `COOP/COEP/CORP` для изоляции контекста (когда нужно)

IFOS хранит **cors_policy** и **isolation_profile**.

---

## 64331–64370 — Clickjacking & Iframe Model
Если вы не хотите быть встроены в iframe:
- `frame-ancestors 'none'` (CSP) или allowlist
Если нужно встраивание (витрина/виджет):
- отдельный домен/путь с ослаблениями
- postMessage протокол + origin checks

IFOS хранит **embed_policy**: allowlist origins, message schema, sandbox flags.

---

## 64371–64400 — Mobile WebView + Client Integrity (сложное)
### WebView pitfalls
- неправильная обработка cookies/third‑party cookies
- запрет редиректов/открытий окна авторизации
- SSL inspection / кастомные trust stores
- deep links и app‑links (подмена)

### Client integrity / anti‑abuse (не “шпионаж”, а защита сервиса)
- rate limiting на действия (отзывы, сравнения, поиск)
- device/session fingerprint **минимальный**, без лишних данных
- challenge при аномалиях (капча/PoW/step‑up auth)
- журналирование “почему заблокировали” (для поддержки)

IFOS хранит **webview_policy** и **integrity_policy**.

---

## Что дальше
Следующий блок:
**64401–64800 — Authentication Flows OS**  
(OAuth2/OIDC, PKCE, device code, SSO, refresh rotation, step‑up MFA, secure logout).  
Напишите “Продолжение” — сделаю.
