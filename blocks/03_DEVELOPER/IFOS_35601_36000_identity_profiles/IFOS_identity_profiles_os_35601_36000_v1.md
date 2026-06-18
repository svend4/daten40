# IFOS — Core Identity & Profiles (Блок 35601–36000)

Версия: v1 · Пакет: `IFOS_35601_36000_identity_profiles_os_pack.zip` · Дата: 2026-01-02

## 0) Зачем нужен этот блок

Этот блок закрывает **базовую идентичность пользователя** (аккаунт, сессии, профили, права, согласия) для IFOS. Он нужен, чтобы все остальные подсистемы (витрины, маркетплейс, отзывы, макросы, знание, агенты) могли безопасно понимать: **кто пользователь, что ему можно, что он выбрал, что он разрешил**.

Почему отдельный блок, а не часть Enterprise IAM?

- Здесь — **простая и средняя** сложность: login/signup, сессии, MFA (опционально), базовый RBAC/ABAC, профиль, настройки.
- В блоке **36001–36400 (Enterprise Identity & Access)** — сложные корпоративные вещи: SSO (SAML/OIDC), SCIM, advanced policy, external IdP, enterprise audit.

## 1) Результаты (что система умеет после внедрения)

1. Регистрация/вход/выход пользователя.
2. Безопасные сессии (JWT или session cookie) + refresh/rotation.
3. Профиль пользователя: имя, язык, часовой пояс, предпочтения.
4. Управление доступом: роли/права (RBAC) + правила (минимальный ABAC).
5. Согласия и privacy-настройки (consent): рассылки, персонализация, экспорт/удаление.
6. Связь аккаунта с внешними провайдерами (OAuth) — опционально.
7. Логи событий аутентификации и административных действий.

## 2) Границы блока (что НЕ делает этот блок)

- **Не реализует полноценный enterprise SSO/SCIM** (это следующий блок 36001–36400).
- **Не реализует платёжные KYC/AML** (это отдельные будущие блоки, если финтех).
- **Не решает** поисковую выдачу/витрины/маркетплейс — только предоставляет идентичность/права/согласия.

## 3) Минимальный MVP (простое → среднее)

### Шаг 3.1 — Минимальная модель пользователя (MVP)

- Таблица/коллекция `users`: `id`, `email`, `email_verified`, `password_hash`, `created_at`, `status`.
- Таблица `sessions` или JWT-стратегия.
- Таблица `user_settings`: `lang`, `timezone`, `ui_density`, `email_notifications`.

### Шаг 3.2 — Login/Signup без «зоопарка»

Вариант A (самый простой): email + password
- Signup → verify email → login.
- Пароль хранить только в виде **argon2id/bcrypt** хеша.
- Ограничение частоты попыток (rate limit) и блокировка по IP/аккаунту.

Вариант B (простота для пользователей): magic link (пароль не хранить)
- Signup → письмо со ссылкой → одноразовый токен → сессия.

### Шаг 3.3 — Сессии (корректно и безопасно)

- Если cookie: `HttpOnly`, `Secure`, `SameSite=Lax/Strict`.
- Если JWT: access_token короткий (5–15 мин), refresh_token долгий (7–30 дней) + ротация.
- Хранение refresh_token: hashed + revocation list.

### Шаг 3.4 — Базовые роли/права (RBAC)

Минимум 4 роли:
- `guest` (аноним)
- `user` (зарегистрирован)
- `editor` (создаёт/редактирует контент/карточки)
- `admin` (управляет системой)

Права — как набор разрешений: `read:*`, `write:reviews`, `manage:connectors`, `manage:marketplace`.

## 4) Средний уровень (пользовательские профили, OAuth, MFA)

### Шаг 4.1 — Профиль как продуктовый объект

- `profile_display_name`, `avatar_url`, `bio`, `links`.
- Приватность: `profile_visibility` (public/private/friends/org).
- История изменений профиля (audit).

### Шаг 4.2 — Внешние провайдеры (OAuth)

- Подключение Google/Microsoft/GitHub (если нужно для B2B/разработчиков).
- Таблица `user_identities`: `user_id`, `provider`, `provider_user_id`, `scopes`, `created_at`.
- Отвязка провайдера → если нет пароля, обеспечить fallback (magic link).

### Шаг 4.3 — MFA (опционально)

- TOTP (Google Authenticator) как базовый.
- Backup codes.
- Политика: MFA обязателен для admin и действий высокой ценности.

## 5) Consent, Privacy, Data Rights

### Шаг 5.1 — Согласия (consent records)
- `consents`: `user_id`, `type`, `granted`, `source`, `timestamp`.
- Типы: `marketing_email`, `personalization`, `data_sharing`, `cookies`.

### Шаг 5.2 — Экспорт/удаление (GDPR-ready минимально)
- Export: собрать user + settings + activity summary.
- Delete: soft-delete → scheduled purge → аннулировать refresh tokens.

## 6) События и аудит

- Логировать: signup, login success/fail, password reset, MFA enable/disable, role change.
- Формат события: `event_type`, `actor_user_id`, `target_user_id`, `ip`, `user_agent`, `ts`, `meta`.
- Интеграция с Observability (34801–35200): метрики logins, fail rate, suspicious attempts.

## 7) API (контракт)

### Public
- `POST /auth/signup`
- `POST /auth/login`
- `POST /auth/logout`
- `POST /auth/refresh`
- `POST /auth/magiclink/request` (если выбран)
- `POST /auth/magiclink/verify`
- `GET /me`
- `PATCH /me/profile`
- `PATCH /me/settings`

### Admin
- `GET /admin/users`
- `PATCH /admin/users/{id}/roles`
- `GET /admin/audit`

## 8) Архитектура (микро-сервисы или модуль монолита)

- `auth-service` (signup/login/sessions)
- `profile-service` (profile/settings)
- `policy-engine` (RBAC/ABAC) — минимально можно внутри backend.
- `audit-log` (события)
Для MVP допускается монолит, но контракты должны быть отделимы.

## 9) Зависимости (в терминах IFOS)

### Hard deps
- 34401–34800 `security_trust`: базовые политики безопасности, секреты, rate limits.

### Optional deps
- 34001–34400 `enterprise_governance`: если нужен орг-уровень политик и роли.
- 34801–35200 `observability_reliability`: если нужен мониторинг/алерты.
- 36001–36400 `enterprise_identity_access`: если нужен SSO/SCIM.

## 10) Чек-лист готовности

- [ ] Пароли только хешированные + password reset flow
- [ ] Rate limit + lockout
- [ ] Email verification (если password)
- [ ] Refresh rotation + revoke
- [ ] RBAC роли + разрешения
- [ ] Consent UI + записи согласий
- [ ] Audit events
- [ ] Базовые тесты безопасности (OWASP top 10 минимум)
