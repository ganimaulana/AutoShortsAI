# AutoShortsAI AI Rules

## Mission

AutoShortsAI adalah aplikasi desktop untuk mengubah video panjang menjadi YouTube Shorts secara otomatis menggunakan AI.

Target utama:

- Stabil
- Mudah di-maintain
- Modular
- Production Ready

---

# Architecture

Selalu ikuti dependency berikut.

GUI
↓

Application
↓

Domain
↓

Infrastructure

Pipeline hanya orchestration.

Business Logic hanya berada di Application.

Domain tidak boleh bergantung pada GUI ataupun Infrastructure.

---

# Code Style

- Python 3.12
- Type Hint wajib
- Dataclass untuk Domain Model
- Logging wajib
- Hindari Magic Number
- Hindari Global Variable
- Gunakan Pathlib
- Gunakan Enum bila sesuai

---

# Pipeline

Pipeline hanya mengatur urutan Step.

Pipeline tidak boleh berisi business logic.

Step hanya mengerjakan satu tanggung jawab.

---

# Error Handling

Selalu gunakan exception yang jelas.

Log seluruh error.

Jangan menggunakan bare except.

---

# Refactoring

Jangan membuat duplicate class.

Jangan membuat duplicate pipeline.

Jangan mengubah public API tanpa alasan.

Jangan memindahkan file kecuali diperlukan.

---

# Testing

Feature baru minimal memiliki unit test.

---

# Git

Gunakan Conventional Commit.

feat:
fix:
refactor:
docs:
test:
perf:
style:
chore:

---

# AI Behavior

Sebelum mengubah kode:

1. Pahami dependency.
2. Cari semua penggunaan class tersebut.
3. Jangan mengubah file yang tidak diperlukan.
4. Berikan ringkasan perubahan.