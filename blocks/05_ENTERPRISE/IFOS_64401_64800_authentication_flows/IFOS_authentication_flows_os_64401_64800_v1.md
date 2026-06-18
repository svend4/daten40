# IFOS 64401–64800 — Authentication Flows OS (v1)
Цель: сделать аутентификацию/SSO/сессии/токены **как управляемый “политикой” модуль**, который:
- одинаково работает в web, mobile, desktop, webview
- выдерживает enterprise SSO (OIDC/SAML мосты)
- минимизирует риск XSS/CSRF/session replay
- имеет отладочные сценарии и метрики

Порядок: **простое → среднее → сложное**.

---

## 64401–64425 — Простое: “что мы хотим защитить”
### Активы
- аккаунт пользователя, профиль, платежные операции
- ключи/секреты интеграций (credential vault)
- доступ к “установкам” (marketplace install/run)
- права администратора, тенанты

### Типы клиентов
- Web app (браузер)
- Mobile app (нативный)
- Desktop/CLI
- Headless automation (агенты/раннеры)

### Минимальные решения по умолчанию
- Web: OIDC Authorization Code + **PKCE**
- Mobile: OIDC Authorization Code + PKCE (через system browser, не webview)
- CLI/TV: **Device Code Flow**
- Headless: **Client Credentials** (только для сервисов, не пользователей)

---

## 64426–64470 — Среднее: базовый стек OAuth2/OIDC
IFOS вводит сущности:
- **OIDC Provider** (встроенный или внешний: Google, Microsoft, Keycloak и т.п.)
- **OAuth Client App** (app/console/agent) с redirect URIs
- **Auth Profile** (пресет: “consumer”, “enterprise”, “strict-admin”)

Ключевые параметры клиента:
- `grant_types`: authorization_code, refresh_token, device_code, client_credentials
- `pkce_required`: true
- `redirect_uris`: allowlist
- `token_endpoint_auth_method`: none / client_secret_post / private_key_jwt
- `scopes`: минимально необходимый набор

---

## 64471–64540 — PKCE flow (web & mobile) — “правильный логин 2026”
Почему PKCE обязателен:
- уменьшает риск перехвата кода авторизации
- безопаснее для public clients (SPA/mobile)

Практика IFOS:
1) client генерирует `code_verifier` и `code_challenge`
2) redirect на authorize endpoint
3) backend/edge обмен кода на токены
4) **короткий access token + refresh rotation**
5) хранение refresh — защищённо (cookie httpOnly или secure storage на мобиле)

Важное:
- **не хранить access/refresh в localStorage** для web
- использовать nonce/state, проверять строго

---

## 64541–64595 — Device Code Flow (CLI, TV, “второй экран”)
Когда нужно:
- нет безопасного redirect URI
- пользователь логинится на телефоне/браузере

IFOS стандарт:
- endpoint выдаёт `device_code`, `user_code`, `verification_uri`
- клиент показывает код и ждёт poll
- сервер “привязывает” устройство к аккаунту после подтверждения
- дальше — выдача токена с ограниченными scopes

---

## 64596–64650 — Enterprise SSO (OIDC + SAML мост)
В enterprise мире часто:
- Azure AD / Entra ID, Okta, Ping, Keycloak
- требуются: group/role mapping, SCIM provisioning, conditional access

IFOS делает:
- **SSO connector profile** (метаданные провайдера)
- **claim mapping** (email, sub, groups → roles)
- режим “domain based routing” (если email @company.com → enterprise login)
- “break-glass” local admin (на случай падения IdP)

---

## 64651–64720 — Токены, ротация, отзыв, “безопасный выход”
Политика токенов:
- Access: 5–15 минут
- Refresh: 7–30 дней, **rotation on use**
- Detect reuse: если refresh token использован дважды → revoke family

Отзыв (revocation):
- logout: отзывать refresh + session
- server-side denylist/allowlist в зависимости от режима
- для enterprise: central session store

Logout:
- локальный logout (клиент) + server logout (revocation)
- SSO logout best-effort (IdP часто сложен) → документировать ожидания

---

## 64721–64770 — Step-up MFA и “опасные действия”
Не всегда нужно MFA на каждый вход. Часто лучше:
- включать MFA **для критичных действий**:
  - платежи, смена реквизитов, установка коннекторов, экспорт данных, админка
- адаптивные сигналы: новое устройство, новый регион, аномальная активность
- механики: TOTP, WebAuthn/passkeys, push

IFOS хранит **mfa_policy** как набор правил: “когда требовать” и “что принимать”.

---

## 64771–64800 — Roles/Scopes/Permissions (модель доступа)
Слои:
- **Scopes** (что может токен: read/write/install/run)
- **Roles** (что может пользователь в тенанте)
- **Permissions** (точечные действия в продуктах/коннекторах)

IFOS рекомендует:
- минимальные scopes по умолчанию
- отдельный admin scope
- короткие “delegated grants” (для временного доступа)
- аудит: кто дал доступ, кому, когда, зачем

---

## Что дальше
Следующий блок:
**64801–65200 — Secrets & Credential Vault OS**  
(хранение ключей API, тестовые ключи, шифрование, ротация, policy, доступ по ролям, audit, break-glass).  
Напишите “Продолжение” — сделаю.
