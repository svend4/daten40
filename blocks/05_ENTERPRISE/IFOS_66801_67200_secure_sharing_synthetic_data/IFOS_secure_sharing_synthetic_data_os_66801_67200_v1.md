# IFOS 66801–67200 — Secure Data Sharing & Synthetic Data OS (v1)
Цель: дать миру “миллионов интеграций” безопасный способ **делиться данными** (между командами/тенантами/партнёрами),
не превращая это в утечки, хаос и ручную бюрократию. Блок закрывает 3 практические задачи:

1) **Data Rooms** (комнаты данных): ограниченные пространства для обмена
2) **Доступ по запросу**: ShareRequest → Approval → ShareGrant
3) **Безопасные датасеты**: *sample / de‑id / synthetic* вместо “живых” данных

Связи:
- опирается на **DLP & Classification OS** (66401–66800)
- пишет receipts для **Forensics OS** (66001–66400)
- работает поверх **Identity/Access** и **Connectors Credential Vault**

Порядок: **простое → среднее → сложное**.

---

## 66801–66840 — Простое: понятия и минимальный “контур”
### DataRoom
DataRoom — “контейнер” с правилами:
- кто может публиковать наборы (publishers)
- кто может запрашивать доступ (consumers)
- какие классы данных допускаются (allowed_classes)
- какие трансформации обязательны (de‑id/synthetic)
- какие receipts и сроки хранения обязательны

### DatasetAsset
DatasetAsset — объект обмена:
- тип (table/files/api snapshot)
- метаданные (владелец, 목적, регион)
- классификация (classes+labels)
- политика выдачи (sample policy)
- варианты представления (raw запрещён, только безопасные)

---

## 66841–66920 — Базовое: запрос на доступ (ShareRequest)
ShareRequest — стандартный документ:
- кто просит (actor/role)
- зачем (purpose)
- что нужно (dataset_id + fields scope)
- на сколько (time window)
- куда выносится (destination) — если вообще выносится
- подтверждение контракта (data contract check)
- auto‑risk score (по классам и маршрутам)

ShareRequest должен быть **машиночитаемым**, чтобы большая часть решений принималась автоматически.

---

## 66921–67000 — Среднее: approval workflow и ShareGrant
### ApprovalWorkflow
Сборка “правил согласования”:
- auto‑approve для PUBLIC / INTERNAL
- mandatory approve для CONFIDENTIAL
- dual‑approve (security + owner) для PII/FINANCIAL
- deny by default для SECRETS/HEALTH (если нет спец. режима)

### ShareGrant
Результат:
- выдан доступ (ALLOW/ALLOW+TRANSFORM/DENY)
- на какой срок
- какая версия датасета
- какой профиль обезличивания/синтетики применён
- какие receipts обязательны
- ограничения: max_rows, rate limit, watermarking

---

## 67001–67070 — Среднее+: обезличивание (De‑Identification)
### DeIdProfile
Набор преобразований:
- suppression (удаление столбцов)
- generalization (возраст → диапазоны)
- pseudonymization (stable token)
- k‑anonymity (на уровне агрегатов)
- masking (частичная маска)
- noise injection (для статистики)

Важно: профиль должен быть **версионирован** и воспроизводим.

---

## 67071–67140 — Сложное: синтетические данные (SyntheticProfile)
### SyntheticProfile
Определяет, как создавать “похожий” датасет без реальных записей:
- генерация из статистик (marginals, correlations)
- табличный генератор (rules + constraints)
- дифф. приватность (если применимо)
- генерация типовых случаев (edge cases) для тестирования
- контроль утечек (membership inference checks)

Цель синтетики в IFOS:
- демо/обучение
- тестирование интеграций
- воспроизводимые кейсы для QA
- публичные “витрины” без утечек

---

## 67141–67200 — Сложное+: Sample policies + Access receipts + Watermarking
### SamplePolicy
Как выдавать “кусочек”:
- max_rows / max_columns
- stratified sample (по сегментам)
- time-window sample
- schema-only (только структура)
- masked preview (обзор без данных)

### AccessReceipt
Каждая выдача/скачивание/экспорт фиксируется:
- кто, когда, что
- какую версию
- какие трансформации
- в какую “точку” (destination route)
- correlation ids (workflow/tenant/case)

### Watermarking
Для файлов/экспортов:
- invisible watermark token
- canary rows (ловушки)
- per‑download unique token

---

## Что дальше
Следующий блок:
**67201–67600 — Test Keys & Safe Demo Assets OS**  
(каталог тестовых ключей/песочниц по SaaS, “честные” демо‑токены, безопасные примеры для разработчиков, упаковка в one‑click trial bundles).
