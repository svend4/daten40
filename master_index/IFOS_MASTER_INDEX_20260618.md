# IFOS Wiki — Internet Function OS

**Проект:** IFOS (InternetFunctionOS) — B2B операционная система для интернет-функций  
**Источник:** Founding Chat РАЗГОВОР 5/1105 (`chat_export_003.txt`) + 856 файлов из _CANONICAL  
**GitHub:** svend4/data70  
**Статус:** Design Specification (paper architecture) — no production code yet

---

## Что такое IFOS

IFOS — это концептуальная платформа для рационализации интернет-функций:
вместо того чтобы изобретать новое, систематизировать и сделать используемым то, что уже есть.

**Ключевая идея:** каждый плагин/сценарий/API/приложение — это **Function Block** с паспортом.  
Паспорт содержит: входы/выходы, зависимости, риски PII, лицензию, quality score (L0–L5).

**6-слойная архитектура:**
```
Layer 1: Function Registry    — каталог блоков с паспортами
Layer 2: Vocabulary/Schema    — единый словарь функций и сущностей  
Layer 3: Composer/Macros      — цепочки блоков, версионирование
Layer 4: Blueprints           — one-click кластеры под бизнес-задачи
Layer 5: Trust Layer          — тесты, рейтинги, безопасность, PII
Layer 6: AI Layer             — паспортизация, дедуп, предложения
```

---

## Статистика проекта

| Метрика | Значение |
|---------|----------|
| OS_PACK блоков (ZIP) | 210 (+ 1 corrupt #14241) |
| Шагов охвачено | 14241 — 88800 |
| Тематических доменов | 165+ |
| JSON-схем | ~1,466 |
| OpenAPI specs | ~139 |
| Python stubs | ~546 |
| Standalone файлов в _CANONICAL | 370 |
| **Всего в _CANONICAL** | **856** |

---

## Навигация по слоям

| Слой | Диапазон | Блоков | Описание |
|------|----------|--------|----------|
| [00_GENESIS](./00_GENESIS/README.md) | 1–14240 | 1 | Founding concept, genesis pack |
| [01_FOUNDATION](./01_FOUNDATION/README.md) | 14241–22000 | 18 | Core registry, recipe OS, marketplace, compiler |
| [02_CORE_PLATFORM](./02_CORE_PLATFORM/README.md) | 22001–30000 | 19 | Trust, catalog mining, install, observability |
| [03_DEVELOPER](./03_DEVELOPER/README.md) | 30001–40000 | 26 | SDK, knowledge graph, identity, agents |
| [04_ADVANCED](./04_ADVANCED/README.md) | 40001–60000 | 58 | UI, office suite, automation, scheduling |
| [05_ENTERPRISE](./05_ENTERPRISE/README.md) | 60001–77600 | 61 | Governance, compliance, security, access |
| [06_FINANCE_LEGAL](./06_FINANCE_LEGAL/README.md) | 77601–88800 | 27 | Tax, treasury, CPQ, audit, domain packs |

---

## Ключевые блоки (точки входа)

### Понять концепцию
- `00_GENESIS/IFOS_00001_14240_concept_genesis/` — полный founding document (разделы 1-6)

### Понять архитектуру  
- `01_FOUNDATION/IFOS_14441_14680_recipe_os/` — "рецепты" как шаблоны функций
- `01_FOUNDATION/IFOS_14681_14940_marketplace_trust_os/` — Trust Layer foundation
- `02_CORE_PLATFORM/IFOS_22801_23200_trust_reputation_os/` — quality ladder L0–L5

### Понять API-контракты
- `02_CORE_PLATFORM/IFOS_23201_23600_catalog_mining_auto_clustering_os/`
- `03_DEVELOPER/IFOS_30001_30400_security_compliance_os/`

### Понять domain scope
- `06_FINANCE_LEGAL/IFOS_83201_83600_gov_domain_pack_production/`
- `06_FINANCE_LEGAL/IFOS_84001_84400_healthcare_domain_pack_production/`
- `06_FINANCE_LEGAL/IFOS_88401_88800_auditor_portal_secure_sharing_links_access_watermarks_expiration/`

---

## Структура каждого OS_PACK блока

```
IFOS_NNNNN_NNNNN_topic/
├── IFOS_topic_os_NNNNN_NNNNN_v1.md      ← главный концептуальный документ
├── IFOS_*_schema_v1.json                ← JSON-схемы сущностей (1–16 файлов)
├── IFOS_*_api_v1.yaml                   ← OpenAPI спецификация
├── IFOS_*_examples_v1.json              ← примеры данных
├── IFOS_*_spec_v1.md                    ← мини-спеки по подтемам
└── IFOS_*_stub_v1.py                    ← Python скелеты (1–5 файлов)
```

---

## Известные проблемы

| Проблема | Файл | Статус |
|----------|------|--------|
| Corrupt ZIP | IFOS_14241_14440_function_wikipedia_pack.zip | Требует регенерации |
| Дублирующиеся диапазоны | IFOS_35601_36000_developer_platform + identity_profiles | Оба сохранены |
| Citation artifacts в Genesis | раздел 1.2–2.3 founding doc | Косметика, не критично |

---

*Сгенерировано: 2026-06-18 | KDFA Three-Zone Architecture — Zone B*
