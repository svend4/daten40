# IFOS Block 76801–77200: Legal Agreements, Terms & EULA (Versioning + Acceptance)

## Зачем этот блок нужен (идея с самого начала)
IFOS строится как «операционная система функций интернета»: пользователь приходит не за отдельным SaaS, а за **гарантированным результатом** (функцией) — например, «опубликовать витрину», «подключить партнёрку», «синхронизировать данные», «запустить workflow».
Чтобы это работало в реальном мире (особенно B2B/enterprise/marketplace), нужны **юридические рамки**: кто за что отвечает, какие правила использования, какие ограничения, какие условия оплаты/возвратов, какие лицензии/права на контент, какие условия для разработчиков и поставщиков пакетов.

Этот блок вводит:
- **реестр юридических документов** (ToS, EULA, Marketplace Terms, Developer Terms, MSA, DPA и т.д.),
- **версионирование и публикацию** (draft → review → published),
- **привязку к продуктам / пакетам / ролям / юрисдикциям / языкам**,
- **сбор согласий (acceptance / clickwrap / signature)** и доказательства согласия,
- **интеграцию с политиками, биллингом, маркетплейсом, комплаенсом и provenance**.

---

## Границы блока (что он делает / что НЕ делает)

### Делает
1. **Legal Document Registry**
   - каталог типов документов (TOS/EULA/Marketplace/Developer/Privacy notice/…),
   - метаданные: аудитория, применимость (product/plan/package), юрисдикция, язык, версия, эффективная дата.
2. **Версионирование и релиз**
   - семантика версий (major/minor/patch),
   - статусы (DRAFT/IN_REVIEW/PUBLISHED/DEPRECATED),
   - правила совместимости (например: major → требует повторного согласия).
3. **Acceptance / Evidence**
   - запись события принятия (кто/когда/что/какую версию/каким методом),
   - хранение артефакта доказательства (hash документа, snapshot, device/browser hints),
   - экспорт доказательств для аудита/спора.
4. **Delivery / Gating**
   - API «какие условия действуют сейчас для этого пользователя/организации/страны/языка»,
   - принудительное принятие перед доступом к функциям (gating),
   - «re-consent» при обновлениях.
5. **Связь с остальными подсистемами**
   - с биллингом/платежами (условия оплаты/возвратов/подписок),
   - с маркетплейсом (условия для поставщиков пакетов, ответственность),
   - с provenance/аттестацией (подписанные манифесты документов и хэши),
   - с политиками/комплаенсом (правила для регионов, возраст, санкции и т.п.).

### НЕ делает (осознанные ограничения)
- Не заменяет юристов и не «создаёт юридически идеальные тексты».
- Не является «системой электронного документооборота» для сложных MSA (но может хранить артефакты и статусы).
- Не решает целиком privacy/DSAR/ROPA — это в блоках Privacy/Compliance/Records, но здесь есть «крючки» (hooks) и совместные модели.

---

## Основные сущности и поля

### 1) LegalDoc (документ как тип)
- `doc_id` (UUID)
- `doc_type` (TOS | EULA | MARKETPLACE_TERMS | DEVELOPER_TERMS | MSA | DPA | …)
- `product_scope` (IFOS Core | Marketplace | конкретный пакет/бандл)
- `audience` (end_user | vendor | developer | enterprise_admin)
- `jurisdiction` (DE/EU/US/… + опционально state)
- `language` (ru/de/en/…)
- `owner_org_id` (кто управляет документом)
- `tags` (payments, content, ai, connectors, …)

### 2) LegalDocVersion (конкретная версия)
- `version_id` (UUID)
- `doc_id`
- `semver` (например 2.0.0)
- `status` (DRAFT/IN_REVIEW/PUBLISHED/DEPRECATED)
- `effective_at`, `published_at`, `deprecated_at`
- `content_uri` (где хранится «тело» документа: html/pdf/markdown)
- `content_hash_sha256`
- `requires_reaccept` (bool)
- `change_summary` (коротко что изменилось)
- `approval_workflow_ref` (ссылка на release-workflow)

### 3) AcceptanceEvent (принятие)
- `event_id` (UUID)
- `subject_type` (user | org | workspace | api_client)
- `subject_id`
- `doc_id`, `version_id`
- `accepted_at`
- `method` (clickwrap | checkbox | signature | api_token_ack)
- `actor_ip_hash` (хэш IP/ASN, чтобы не хранить персональные данные напрямую)
- `user_agent_hash`
- `evidence_artifact_uri` (snapshot, PDF, подпись, лог)
- `evidence_hash_sha256`
- `locale` (язык UI в момент принятия)

### 4) LegalBinding (применимость)
Правило выбора «какие условия действуют».
- `binding_id`
- `doc_id`
- `match_rules` (страна, язык, план, пакет, роль, возраст)
- `default_fallback` (если не найдено точного совпадения)
- `priority`

---

## Ключевые потоки (workflow)

### A) Публикация новой версии
1. Создать `LegalDocVersion` в статусе DRAFT.
2. Привязать к release workflow (блок 70801–71600 / 46001–46400).
3. Сгенерировать `content_hash_sha256`, сохранить в object storage.
4. Опционально: подписать метаданные (sigstore/attestation) и сохранить в provenance (76001–76400).
5. Перевести в PUBLISHED, установить `effective_at`.
6. Запустить нотификацию (email/in-app) тем, кого касается.
7. Если `requires_reaccept = true` — включить gating для соответствующих функций.

### B) Проверка перед использованием функции (gating)
1. Клиент вызывает `GET /terms/current?scope=...`.
2. Сервер вычисляет binding и возвращает «актуальный набор» документов.
3. Клиент сверяет: есть ли acceptance на версии.
4. Если нет — показать экран принятия и вызвать `POST /terms/accept`.
5. После принятия — открыть доступ.

### C) Спор/аудит (evidence)
1. Админ/поддержка запрашивает экспорт доказательств: `GET /terms/acceptance/export`.
2. Система формирует пакет: metadata + hashes + snapshot.
3. Пакет подписывается, сохраняется, выдаётся ссылкой с ограниченным TTL.

---

## Политики и правила (минимальный набор)
- **Major version** по умолчанию требует повторного согласия.
- Нельзя «понизить» права пользователя без явного re-consent.
- Для marketplace/vendor условий — отдельные audience и binding.
- Для enterprise — допускаются кастомные документы (MSA/DPA) с ограничением доступа.
- Для локализации: один `doc_id` может иметь несколько языков, но **один и тот же смысл** должен быть связан общим `doc_family_id` (опционально).

---

## API (минимальный контракт)
См. файл `IFOS_legal_terms_acceptance_api_76801_77200_v1.yaml`.

---

## UI/UX элементы (концепт)
- Экран «Terms Update» (что изменилось, когда вступает, кнопка Accept).
- Admin: реестр документов, версии, bindings, аудит принятий.
- История согласий пользователя/организации.

---

## Интеграции (dependencies)
- **Publishing / Progressive Delivery**: релиз версий документов.
- **Notifications / Activity Feed**: уведомления о новых условиях.
- **Policy Engine**: правила выбора документов и gating.
- **Provenance / Attestation**: подпись хэшей документов и пакетов доказательств.
- **Case Management**: связывать disputes/тикеты с конкретными версиями Terms.

---

## Результат блока (Definition of Done)
- Реестр документов и версий (CRUD + publish).
- Binding engine (выбор действующих условий).
- Acceptance event logging + экспорт доказательств.
- Пример интеграции gating (минимально — middleware/guard).
- Документация + seed-данные.
