# IFOS — Publishing & Release Workflow (Блок 46001–46400)

Версия: v1 · Пакет: `IFOS_46001_46400_publishing_release_workflow_os_pack.zip` · Дата: 2026-01-02

## 0) Зачем нужен этот блок

У IFOS много компонентов: **коннекторы, макросы, витрины, пакеты знаний, one-click bundles, шаблоны**.
Если их просто «загрузить и показать», получаем хаос: нет версий, нет стадий проверки, нет откатов, нет понятного «что изменилось».

Этот блок вводит **единый издательский конвейер (publishing pipeline)**:
- draft → review → approved → published → deprecated/retired
- release channels (alpha/beta/stable)
- совместимость и миграции
- changelog и release notes
- быстрый rollback/disable

Он связывает качество (45601–46000) с публичной подачей (46401–46800 «конференция/витрины»).

## 1) Что делает (функции)

1) **Lifecycle state machine** для publishable объектов.
2) **Release channels**: alpha/beta/stable + правила продвижения.
3) **Versioning**: semver для пакетов/коннекторов/шаблонов.
4) **Compatibility gates**: минимальная версия IFOS, зависимости, breaking changes.
5) **Changelog/Release notes**: автоматически собираемые заметки.
6) **Rollback**: откат на предыдущую версию/канал.
7) **Deprecation**: сроки снятия, предупреждения, миграции.

## 2) Что НЕ делает (границы)

- Не выполняет саму модерацию контента (это импорт/модерация и curation блоки).
- Не является платежным биллингом (это payments/settlement).
- Не заменяет security signing (может использовать, но подпись описывается в security/trust блоках).

## 3) MVP (простое → среднее)

### Шаг 3.1 — Универсальная модель Publishable

Ввести сущность `publishable` (или интерфейс) для типов:
`connector | macro | template | bundle | knowledge_pack | vitrine`.

Минимальные поля:
- `object_type`, `object_id`
- `workspace_id` (владение)
- `state` (draft|review|approved|published|deprecated|retired)
- `channel` (alpha|beta|stable)
- `version` (semver: 1.2.3)
- `created_by`, `updated_by`
- `created_at`, `updated_at`

### Шаг 3.2 — Переходы состояний (state machine)

MVP переходы:
- draft → review (submit)
- review → approved (approve)
- approved → published (publish)
- published → deprecated (deprecate)
- deprecated → retired (retire)
- published → draft (rollback_to_draft) — только admin

Каждый переход пишет событие в audit log.

### Шаг 3.3 — Проверка совместимости перед publish

Перед переходом `approved → published` выполнить проверки:
- зависимости существуют (requires_slugs/versions)
- нет конфликтов
- минимальная версия IFOS удовлетворена (`min_ifos_version`)
- заполнены метаданные (описание, лицензия, контакты, документация)

### Шаг 3.4 — Changelog (ручной минимум)

MVP: у версии есть список изменений:
- `change_type` (fix|feat|breaking|security|docs)
- `summary`
- `details` (опционально)

Позже можно автогенерировать из PR/issue/коммитов.

## 4) Средний уровень: релиз-каналы, откат, миграции

### Шаг 4.1 — Release channels и продвижение

Правила:
- alpha: разрешено публиковать из workspace (внутреннее)
- beta: доступно подписчикам/пилотам
- stable: публично в маркетплейсе

Продвижение: alpha → beta → stable (с проверками и порогами качества).

### Шаг 4.2 — Rollback и feature flags

Rollback варианты:
1) `disable` (быстро выключить публикацию)
2) `rollback_version` (назначить предыдущую версию как активную)
3) `pin_version` для конкретного workspace (enterprise контроль)

### Шаг 4.3 — Deprecation policy

Сущность `deprecation_notice`:
- `object_type`, `object_id`, `version`
- `deprecated_at`, `retire_at`
- `migration_guide_url`
- `reason`

UI должен показывать предупреждение и предлагать миграцию.

## 5) Ближе к сложному: автосборка релизов и «конференц-режим»

1) Автопакетирование: build → test → sign → publish.
2) Сбор метрик качества (crash rate, failure rate) → gating.
3) Подготовка «витрин-конференций» (46401–46800):
   - стабильные наборы объектов, привязанные к версии релиза
   - авто-генерация слайдов/карточек «что нового».

## 6) API (минимум)

- `POST /publishables/{type}/{id}/submit`
- `POST /publishables/{type}/{id}/approve`
- `POST /publishables/{type}/{id}/publish?channel=stable`
- `POST /publishables/{type}/{id}/deprecate`
- `POST /publishables/{type}/{id}/retire`
- `POST /publishables/{type}/{id}/rollback?to_version=...`
- `GET  /publishables/{type}/{id}/changelog`

## 7) Зависимости

### Hard deps
- 32401–32800 `marketplace_billing_os` (для stable-публикаций в marketplace)
- 34001–34400 `enterprise_governance` (правила ролей/политики)
- 45601–46000 `marketplace_curation_quality` (оценка и качество)

### Optional deps
- 34401–34800 `security_trust` (подпись/верификация)
- 34801–35200 `observability_reliability` (метрики качества)
- 40401–40800 `data_lineage_provenance` (provenance)

## 8) Чек-лист

- [ ] Универсальный state machine
- [ ] Каналы релиза
- [ ] SemVer и метаданные
- [ ] Проверка совместимости
- [ ] Changelog
- [ ] Rollback (disable/previous version)
- [ ] Deprecation notices
