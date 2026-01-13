# build_pack.py — идея (локальная сборка ZIP)

Если ZIP нельзя стабильно грузить через Make.com, собирайте ZIP **локально** из `pack_files_YYYYMMDD/`.

## Минимальная логика
- вход: `blocks/<BLOCK>/pack_files_YYYYMMDD/`
- выход: `releases/<BLOCK>_pack_YYYYMMDD.zip`

## Команда
```bash
python tools/build_pack.py --block NEXT-XX --date 20260113
```

(Скрипт можно добавить позже, когда решите, что нужен обязательный ZIP.)
