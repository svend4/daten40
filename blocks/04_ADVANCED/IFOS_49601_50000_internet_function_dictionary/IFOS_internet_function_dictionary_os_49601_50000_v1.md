# IFOS 49601–50000 — Internet Function Dictionary OS (Thesaurus of Functions) (v1)
Цель: то, что вы описали как “нужен B2B бизнес‑операционная система для всего интернета”,
в терминах языка: **единый словарь функций**, чтобы:
- “приложение = слово” стало реальностью
- запросы пользователя переводились в понятные “команды интернета”
- миллионы модулей из Registry можно было группировать в кластеры и макросы
- синонимы, жаргон и “как люди говорят” приводились к канону

Порядок: простое → среднее → сложное.

---

## 49601–49640 — FunctionTerm: “слово” как атом каталога
**FunctionTerm** описывает одну функцию:
- term_id (канонический идентификатор)
- label (человекочитаемо)
- definition (1–2 абзаца)
- input/output (что принимает, что выдаёт)
- examples (минимальные примеры)
- related (смежные термины)
- tags (вертикали: travel/office/security)
Это “тезаурус для интернета”.

---

## 49641–49690 — Ontology: иерархия (род‑вид) и связи
**FunctionOntology**:
- hierarchy: data.fetch → data.fetch.rss → data.fetch.rss.parse
- relations: requires, produces, alternative_to, conflicts_with
- constraints: “этот термин всегда требует auth”
- maturity: stable/experimental/deprecated
Онтология нужна для логических выводов и правильной компоновки.

---

## 49691–49730 — Synonyms: как люди говорят, и как мы это понимаем
**SynonymsPack**:
- “интеграция” = connector / webhook / api bridge
- “макрос” = automation / workflow / сценарий
- “парсер” = extractor / scraper / parser
- региональные варианты, транслит, опечатки
Синонимы позволяют не “исправлять пользователя”, а понимать его.

---

## 49731–49770 — Grammar: грамматика действий (“команды интернета”)
**FunctionGrammar**:
- ACTION (сделай) + OBJECT (что) + SOURCE (откуда) + TARGET (куда) + POLICY (как)
Пример:
- “Собери новости из RSS и отправь в Telegram без дублей” →
  - data.fetch.rss
  - data.dedup
  - notify.telegram.send
Грамматика превращает текст в структуру.

---

## 49771–49810 — Action Templates: шаблоны действий (с параметрами)
**ActionTemplate**:
- template_id
- required params (rss_url, bot_token)
- optional params (language, schedule)
- default policy (retry, rate limit)
- outputs (message, log)
Это “формулы” для генерации workflows и bundles.

---

## 49811–49850 — MacroSpec: макросы как композиции терминов
**MacroSpec**:
- name: “RSS→Dedup→Conference”
- steps: [fetch, normalize, dedup, summarize, publish]
- quality gates: preflight, smoke tests
- exports: make/n8n/docker
- rollback strategy
Макросы = “операционная система действий”.

---

## 49851–49890 — Mapping: связь Dictionary ↔ Registry ↔ Bundles
**FunctionMapping**:
- FunctionTerm → Capability tags (48441–48490)
- Capability → RegistryItem candidates (48401–48800)
- MacroSpec → BundleManifest (48801–49200)
Это ключевой мост: язык → конкретные инструменты.

---

## 49891–49930 — QueryIntent: понимание запроса пользователя
**QueryIntent**:
- intent_type: compare / install / build / troubleshoot / learn
- entities: (telegram, wordpress, make)
- constraints: (self‑hosted, free, GDPR)
- output_format: (step-by-step / bundle / diagram)
Это позволяет системе отвечать “как офисная программа”: по режимам работы.

---

## 49931–49970 — Vertical Taxonomy: отраслевые словари поверх общего
**VerticalTaxonomy**:
- travel: booking, flights, insurance
- office: docs, crm, invoicing
- security: auth, scanning, secrets
- content: rss, youtube, podcasts
Каждая вертикаль расширяет общий словарь своими терминами и правилами.

---

## 49971–50000 — Composability Rules + Evaluation: правила сборки и качество
**ComposabilityRules**:
- что с чем можно соединять (I/O совместимость)
- какие шаги обязательны (normalize before dedup)
- где нужны проверки/ретраи
**DictionaryEval**:
- покрытие синонимов
- точность маппинга в capabilities
- успешность компоновки макросов

---

## Итог
Dictionary OS — это “грамматика интернета”:
- люди говорят как хотят → система понимает
- термины → capabilities → инструменты → bundles
- хаос превращается в каталог и “одну кнопку”

---

## Что дальше
Следующий блок:
**50001–50400 — UI OS: “Office‑style” интерфейс для функций, бандлов и витрин**  
(режимы: читать/сравнивать/собирать/ставить/запускать; карточки, мастера, панели, “конференция”, журнал действий).  
Скажете “Продолжение” — сделаю.
