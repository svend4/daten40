# IFOS NEXT_QUEUE v1 — 2026-06-18

## Статус

| Поле | Значение |
|---|---|
| Последний DONE | 88800 |
| Следующий блок | 88801–89200 |
| Версия Master Index | v31 |
| Runbook | v32 (не создан) |

## Очередь задач

### 🔴 CRITICAL
- [ ] Регенерировать: `IFOS_14241_14440_function_wikipedia_pack.zip` (corrupt)
- [ ] Регенерировать 5 потерянных блоков: 21201-21600, 21601-22000, 26001-26400, 30401-30800, 31201-31600

### 🟠 HIGH
- [ ] Создать Runbook v32 (last DONE=88800, NEXT=88801-89200)
- [ ] Продолжить нумерацию: блоки 88801–89200 (Domain Packs — Gov)
- [ ] Загрузить chat_export_008.txt (разговор 25)

### 🟡 MEDIUM
- [ ] Проверить пробелы в нумерации 14241–88800
- [ ] GitHub Pages для blocks/index.html

### 🟢 NEXT RANGE
- Следующие блоки: 88801–89200 (Domain Packs: Gov Service Portal)
- Формат: IFOS_88801_89200_domain_gov_service_portal

## Правила
- Append-only: не перезаписывать файлы
- Источник истины: последний файл в master_index/ по дате
