# IFOS 35201–35600 — Knowledge Graph & Semantic OS (v1)
Цель: превратить каталог IFOS из “просто списка функций” в **семантическую систему**:
- онтология (что такое “функция”, “коннектор”, “capability”, “шаблон”)
- граф связей (depends_on, similar_to, replaces, requires, outputs)
- эмбеддинги (векторный поиск)
- кластеры (группы по смыслу/задачам)
- объяснимость (почему рекомендовано / почему заблокировано)
- Q/A по каталогу (“что выбрать для X?”)
- теги, синонимы, таксономии (упорядочивание языка)

Порядок: простое → среднее → сложное.

---

## 35201–35240 — Словарь и таксономия: язык каталога
### Tag
- короткая метка (например: “email”, “ocr”, “invoice”, “telegram”)
- применяется к bundle, blueprint, connector, capability

### Taxonomy
- дерево категорий (например: Communication → Email → SMTP)
- правила: каждый объект должен иметь ≥1 категорию

### Synonym
- “письмо” ≈ “email”, “отчёт” ≈ “report”, “чек” ≈ “receipt”
- нужен, чтобы пользователь и ИИ говорили на одном языке

---

## 35241–35310 — Онтология (ontology nodes)
### OntologyNode
Типы сущностей (минимальный набор):
- Function (конечный результат: “Отправить письмо”)
- Capability (права/умения: “can_send_email”)
- Connector (интеграция: Gmail, Telegram, Stripe…)
- Blueprint (рецепт/сценарий)
- Bundle (упакованное решение)
- Dataset (данные/реестры/словари)
- Policy (правила безопасности/комплаенса)
- UI Card (витрина, карточка, форма)

Нода содержит:
- canonical_id
- title/description
- type
- tags
- examples (коротко)

---

## 35311–35380 — Связи в графе (ontology edges)
### OntologyEdge
Типы связей:
- depends_on (требует)
- requires_capability (нужны права)
- uses_connector (использует интеграцию)
- produces_output (что выдаёт)
- consumes_input (что принимает)
- similar_to (похоже)
- replaces (заменяет)
- conflicts_with (конфликт)
- compliant_with (соответствует policy)

**Важно:** один и тот же bundle может иметь разные edges в зависимости от режима безопасности.

---

## 35381–35430 — Embeddings: векторный индекс
### Embedding
- object_ref (bundle/blueprint/node)
- model (имя модели эмбеддингов)
- vector (список чисел)
- text_fingerprint (hash текста)
- updated_at

Эмбеддинги дают:
- поиск по смыслу (“хочу сравнить страховки”)
- похожие решения
- автотеги

---

## 35431–35490 — Semantic Queries: запросы “как человек”
### SemanticQuery
- raw_query (“нужно письмо в телеграм и копия в гугл диск”)
- interpreted intents (send, notify, store)
- constraints (free/paid, GDPR, no-code)
- candidate matches (bundle ids)
- explanation summary

Результат не просто “нашёл”, а **объяснил**: почему это подходит.

---

## 35491–35540 — Clustering: генерация групп и “витрин”
### Cluster
- cluster_id, title
- members (bundles/blueprints)
- centroid embedding
- labels (возможные названия)
- use_cases (список задач)

Кластеры решают вашу боль:
> “Есть 100k плагинов/сценариев — но нет понятных наборов.”
Кластер = набор + витрина + документация + кнопка “установить”.

---

## 35541–35580 — Explainability: почему так?
### Explanation
- context (query/install/run/block)
- decision (recommend/block/warn)
- reasons (буллеты)
- evidence refs (ссылки на registry entries)
- confidence
- next_actions

Это превращает “чёрный ящик” в “инженерный инструмент”.

---

## 35581–35600 — Q/A по каталогу (Catalog QA)
### QACard
- question
- short answer
- recommended bundles
- pitfalls
- setup steps
- alternatives

QACard можно показывать в UI как “мини‑консультацию”.

---

## Результат блока
После внедрения Semantic OS:
- у каталога появляется **язык**
- появляется **граф смысла**
- появляется **кластеризация**
- появляется **объяснимость**
- пользователь видит “простые наборы” вместо хаоса

---

## Что дальше
Следующий блок:
**35601–36000 — Developer Platform OS** (SDK, плагины, шаблоны, генераторы, CLI, тест‑харнесс, локальный рантайм, песочницы, marketplace publishing pipeline).  
Скажете “Продолжение” — сделаю.
