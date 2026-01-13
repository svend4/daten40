# IFOS GitHub публикация — вариант 2 (append-only)

## Цель
Публиковать артефакты из чата в GitHub через Make.com, без операций UPDATE (sha), чтобы избежать ошибок Contents API.

## Правило
**Никогда не перезаписываем файлы.** Любое изменение — это новый файл с новой версией/датой.

## Именование
- Master Index: `master-index/IFOS_Master_Index_vNNN_YYYYMMDD.(md|json|csv)`
- Очереди: `tools/NEXT_QUEUE_YYYYMMDD.md`
- Блоки: `blocks/NEXT-XX/README_YYYYMMDD.md` или `blocks/IFOS_#####_#####/spec_YYYYMMDD.md`
- ZIP: `releases/<block_id>_<slug>_YYYYMMDD.zip` (или `blocks/.../pack_YYYYMMDD.zip`)

## Инструменты Make.com
- Текст: “GitHub: Сохранить текст”
- Бинарники: “GitHub: Binary Saver (Advanced)” (рекомендуется)
- Contents API (<=1MB): используем только при необходимости стабильного LATEST (не в варианте 2)

## Чеклист публикации блока
1) `blocks/<block>/README_YYYYMMDD.md`
2) `blocks/<block>/checksums_YYYYMMDD.json`
3) `releases/<block>_..._YYYYMMDD.zip` (если есть)
4) `master-index/IFOS_Master_Index_vNNN_YYYYMMDD.md` + `.json`
