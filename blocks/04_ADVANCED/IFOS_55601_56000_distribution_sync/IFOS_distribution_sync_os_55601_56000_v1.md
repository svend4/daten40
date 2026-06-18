# IFOS 55601–56000 — Distribution & Sync OS (распространение и синхронизация) (v1)
Цель: чтобы IFOS работал **локально, оффлайн, в команде и между организациями** — без потери правды.
Это “Git + Vault + Policy” для артефактов и bundles, но ориентированный на бизнес‑процессы.

Порядок: простое → среднее → сложное.

---

## 55601–55630 — Local Vault (Personal Offline)
Локальный режим:
- хранить blobs/artifacts/metadata локально (SQLite + файловая папка)
- работать без интернета (создавать docs, bundles, процессы)
- очередь синхронизации (outbox)

Минимальный UI:
- статус: “offline/online”
- кнопка: “Sync now”
- список конфликтов (если есть)

---

## 55631–55680 — Replication protocol (Sync jobs)
Синхронизация = обмен “change log”:
- каждая операция добавляет запись в журнал (append-only)
- репликация передаёт только delta (что ещё не было у другой стороны)
- blobs передаются по хэшу (dedup)

Шаги sync job:
1) handshake (версия протокола, policy overlay)
2) exchange heads (последний commit/offset)
3) send missing change records
4) fetch missing blobs by hash
5) verify signatures
6) apply changes
7) emit audit + metrics

---

## 55681–55730 — Conflict resolution (простое → сложное)
Типы конфликтов:
- metadata conflict (теги/название)
- document merge conflict (MD/JSON)
- bundle version conflict
- policy conflict (разные правила у разных тенантов)

Стратегии:
- last-writer-wins (только для low-risk metadata)
- three-way merge (для текстов)
- fork & reconcile (для bundle/policy)
- require approval (для high-risk)

UI для конфликта:
- показать “A vs B vs base”
- подсказать автомердж
- кнопки: accept A / accept B / merge manual

---

## 55731–55780 — Bundle distribution (deltas и “одна кнопка”)
Для marketplace/install/run важно:
- уметь распространять bundles как “delta packs”
- поддержка rollbacks: хранить предыдущие версии
Bundle delta pack:
- from_version
- to_version
- files changed + hashes
- signed
Установка:
- проверить policy (Policy Engine)
- подтянуть зависимости (resolver)
- применить delta
- записать snapshot

---

## 55781–55820 — Federation sync (между организациями)
Federation link:
- org A ↔ org B
- какие domains разрешены (data/process/bundles)
- фильтры (теги, проекты)
- правила “что можно экспортировать”
- частота синка

Важно:
- federation не означает общий доступ к секретам
- применяются overlays политик

---

## 55821–55860 — Security: подписи, доверие, цепочка поставки
Каждый pack/delta:
- подписан
- содержит manifest + hashes
- проверяется перед применением
Supply chain:
- “trusted publisher” (marketplace)
- “unknown source” → quarantine + review

---

## 55861–55900 — Observability: видеть, что sync работает
Метрики:
- bytes_sent/received
- blobs_dedup_saved
- conflicts_count
- sync_latency
- failures_by_reason
Логи:
- trace sync job (шаги протокола)
- audit events (Policy Engine)

---

## 55901–55950 — Backup/Restore & Migration
Режимы:
- full backup (vault snapshot + metadata)
- selective export (project pack)
- disaster restore (rebuild indexes)
Migration:
- перенос между storage backends (local → S3, S3 → on-prem)
- re-key encryption (смена ключей)

---

## 55951–56000 — Offline-first UX: чтобы было просто пользователю
UX принципы:
- “работай всегда” (offline)
- “синк как электричество” (не думаешь)
- конфликты — редкость и понятный экран
- “share pack” вместо хаотичных файлов

---

## Итог
Distribution & Sync OS делает IFOS “живучим”:
- локально и оффлайн
- командно и межорганизационно
- безопасно, с политиками и подписями
- с понятными конфликтами

---

## Что дальше
Следующий блок:
**56001–56400 — Analytics & Insights OS: аналитика использования, качество данных, рекомендации “что улучшить”**  
Скажете “Продолжение” — сделаю.
