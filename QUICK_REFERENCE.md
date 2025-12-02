# 📋 QUICK REFERENCE - RINGKASAN CEPAT

## 🎯 ALUR PROGRAM (Gambar Mental)

```
START
  ↓
main.py jalankan PaketFlowMonitor
  ↓
app.py buat window + setup GUI
  ↓
manager.py mulai thread background
  ↓
GUI tampil menu utama ← → User klik button
                     ← (Interaksi)
                         ↓
                    Jalankan aksi:
                    - show_form_tambah
                    - show_form_cek
                    - show_riwayat
                         ↓
                    Panggil manager method:
                    - tambah_paket()
                    - cari_paket()
                    - get_riwayat()
  ↓
Background thread (setiap 1s):
  1. Loop semua paket di dict
  2. Hitung selisih waktu
  3. Update status jika threshold tercapai
  4. Catat waktu stage
  ↓
User tutup program → on_closing()
  ↓
Set flag _is_running = False → thread berhenti
  ↓
Window tutup (destroy)
  ↓
END
```

---

## 📁 FILE BREAKDOWN

| File | Baris | Fungsi | Kelas/Method |
|------|-------|--------|--------------|
| `main.py` | 1-10 | Entry point | Jalankan window |
| `app.py` | 1-200+ | GUI layer | `PaketFlowMonitor` |
| `manager.py` | 1-150+ | Business logic | `PaketManager` |
| `model.py` | 1-150+ | Data structure | `Queue`, `Stack`, `Paket` |

---

## 🔑 KELAS & METHOD PENTING

### Paket (model.py)
```python
class Paket:
    _paket_counter = 1000  # Class var: auto-increment ID
    
    __init__(nama_penerima)           # Buat paket baru
    get_id_paket()                    # Return ID
    get_status()                      # Return status saat ini
    get_waktu_dibuat()                # Return waktu dibuat
    get_waktu_shipping()              # Return waktu shipping (atau None)
    get_waktu_dikirim()               # Return waktu dikirim (atau None)
    get_waktu_selesai()               # Return waktu selesai (atau None)
    set_status(status_baru)           # Ubah status + catat waktu
    mark_status_recorded(status)      # Tandai status sudah tercatat
    is_status_recorded(status)        # Cek apakah status sudah tercatat
```

### Queue (model.py)
```python
class Queue:
    __init__()              # Buat queue kosong
    enqueue(item)          # Masuk ke belakang
    dequeue()              # Ambil dari depan
    peek()                 # Lihat item pertama tanpa ambil
    size()                 # Jumlah item
    is_empty()             # Cek apakah kosong
    display()              # Return list isi queue
    remove_item(item)      # Hapus item tertentu
```

### Stack (model.py)
```python
class Stack:
    __init__()              # Buat stack kosong
    push(item)             # Masuk ke atas tumpukan
    pop()                  # Ambil dari atas
    size()                 # Jumlah item
    is_empty()             # Cek apakah kosong
    display()              # Return list isi stack (copy)
```

### PaketManager (manager.py)
```python
class PaketManager:
    __init__()                           # Initialize semua struktur data
    tambah_paket(nama_penerima)         # Tambah paket baru → return (paket, pesan)
    cari_paket(id_paket)                # Cari paket by ID → return paket atau None
    start_auto_update(callback=None)    # Mulai thread background
    stop_auto_update()                  # Hentikan thread background
    _auto_update_loop()                 # [Thread] Loop update status
    _check_and_update_status(id, paket) # [Thread] Check & update satu paket
    hitung_urutan_pengantaran(id_paket) # Hitung urutan paket di queue
    get_riwayat()                       # Return list dari stack riwayat
    get_queue_pengantaran()             # Return list dari queue
    get_semua_paket()                   # Return dict semua paket
```

### PaketFlowMonitor (app.py)
```python
class PaketFlowMonitor:
    __init__(root)                  # Setup window + GUI + manager
    on_closing()                    # Handler tutup window (cleanup)
    show_menu_utama()               # Tampil menu utama
    show_form_tambah()              # Tampil form tambah paket
    proses_tambah_paket()           # Process tambah (validation + manager call)
    show_form_cek()                 # Tampil form cek paket
    proses_cek_paket()              # Process cek (lookup + display info)
    show_urutan_pengantaran(id)     # Hitung & tampil urutan pengantaran
    show_riwayat()                  # Tampil tabel riwayat dari stack
    show_progress_paket(tree, riwayat) # Tampil timeline progress paket
    clear_frame()                   # Hapus semua widget di frame
```

---

## 🔄 ALUR SAAT TAMBAH PAKET

```
User klik "TAMBAH PAKET"
    ↓
show_form_tambah() dipanggil
    ↓
Tampil form dengan Entry field
    ↓
User input nama "Budi" + klik "Tambah"
    ↓
proses_tambah_paket() dipanggil
    ↓
nama = entry_nama.get()  // nama = "Budi"
    ↓
paket, pesan = manager.tambah_paket("Budi")
    ├─→ Validasi nama (not empty)
    ├─→ Buat Paket("Budi")
    │   └─→ Generate ID: PKT-1001
    ├─→ Simpan: dict[PKT-1001] = paket
    ├─→ Simpan: queue.enqueue(PKT-1001)
    ├─→ Simpan: stack.push(PKT-1001)
    └─→ Return (paket, "Berhasil!")
    ↓
if not paket: 
    → show error
else:
    → show popup sukses dengan detail
    ↓
clear entry field
```

---

## 🔄 ALUR SAAT CEK STATUS

```
User klik "CEK STATUS"
    ↓
show_form_cek() dipanggil
    ↓
Tampil form dengan Entry field ID
    ↓
User input "PKT-1001" + klik "Cek"
    ↓
proses_cek_paket() dipanggil
    ↓
id_paket = entry_id.get().strip().upper()  // "PKT-1001"
    ↓
paket = manager.cari_paket("PKT-1001")
    └─→ return dict.get("PKT-1001")  // return Paket object atau None
    ↓
if not paket:
    → show warning "Paket tidak ada"
else:
    info = paket.get_info()  // return dict dengan info
    ↓
    Buat string detail dengan info + timestamps
    ↓
    if status == "dikirim ke alamat":
        → show detail popup
        → hitung_urutan_pengantaran()
    else:
        → show detail popup
```

---

## 🔄 ALUR BACKGROUND THREAD

```
Thread start running:
    ↓
while _is_running:
    time.sleep(1)  // Tunggu 1 detik
    ↓
    for id_paket, paket in dict.items():
        ├─→ Parse waktu dibuat:
        │   datetime.strptime(paket.get_waktu_dibuat(), "%Y-%m-%d %H:%M:%S")
        │
        ├─→ Hitung selisih:
        │   (datetime.now() - waktu_dibuat).total_seconds()
        │
        ├─→ Check status:
        │   if status=="diproses" and selisih>=10:
        │       paket.set_status("shipping")
        │   elif status=="shipping" and selisih>=20:
        │       paket.set_status("dikirim ke alamat")
        │   elif status=="dikirim ke alamat" and selisih>=40:
        │       paket.set_status("selesai")
        │
        └─→ Mark status recorded
```

---

## 📊 STRUKTUR DATA VISUAL

### Dict (Paket Storage)
```
_daftar_paket = {
    "PKT-1001": Paket("Budi") → {id, nama, status, waktu...},
    "PKT-1002": Paket("Ani")  → {id, nama, status, waktu...},
    "PKT-1003": Paket("Citra") → {id, nama, status, waktu...},
}

Lookup: _daftar_paket.get("PKT-1001")  // O(1) fast!
```

### Queue (Pengantaran)
```
_queue_pengantaran = deque([
    "PKT-1001",  ← Akan diproses pertama (FIFO)
    "PKT-1002",
    "PKT-1003"
])

enqueue: tambah ke belakang
dequeue: ambil dari depan
```

### Stack (Riwayat)
```
_stack_riwayat = [
    "PKT-1003",  ← Ditampil pertama (LIFO - newest)
    "PKT-1002",
    "PKT-1001"
]

push: tambah ke atas
pop: ambil dari atas
```

---

## 🎛️ TIMELINE STATUS PAKET

```
Waktu (detik)    Status Paket          Timestamp yang Tercatat
─────────────────────────────────────────────────────────────
0s               DIPROSES              waktu_dibuat = "2025-12-02 10:00:00"
                 (status_recorded = {diproses})

10s              SHIPPING              waktu_shipping = "2025-12-02 10:00:10"
                 (status_recorded = {diproses, shipping})

20s              DIKIRIM KE ALAMAT      waktu_dikirim = "2025-12-02 10:00:20"
                 (status_recorded = {diproses, shipping, dikirim ke alamat})

40s              SELESAI               waktu_selesai = "2025-12-02 10:00:40"
                 (status_recorded = {diproses, shipping, dikirim ke alamat, selesai})
```

---

## 🚀 SYNTAKS YANG PALING SERING DIPAKAI

| Syntaks | Contoh | Penjelasan |
|---------|--------|-----------|
| `self.var` | `self.manager = ...` | Instance variable |
| `dict.get(key)` | `dict.get("PKT-1001")` | Ambil value dengan key |
| `dict[key] = value` | `dict["PKT-1001"] = paket` | Set value ke dict |
| `list.append(x)` | `self.items.append(item)` | Tambah ke list |
| `list.pop()` | `self.items.pop()` | Ambil dari list |
| `deque.append()` | `self.items.append(item)` | Tambah ke deque |
| `deque.popleft()` | `self.items.popleft()` | Ambil dari depan deque |
| `for x in list:` | `for id_paket in dict:` | Loop iterasi |
| `.get()` | `entry.get()` | Tkinter: ambil value input |
| `.pack()` | `button.pack(...)` | Tkinter: layout widget |
| `f"{var}"` | `f"PKT-{counter}"` | F-string format |
| `datetime.now()` | Waktu saat ini | |
| `.strftime()` | Format datetime ke string | |
| `.strptime()` | Parse string ke datetime | |
| `.total_seconds()` | Hitung selisih waktu | |
| `threading.Thread()` | Buat thread baru | |
| `@classmethod` | Decorator untuk class method | |
| `try/except` | Handle exception | |
| `if not x:` | Check jika empty/None/False | |
| `return x, y` | Return tuple 2 value | |

---

## ⚡ POIN-POIN KUNCI PRESENTASI

```
❌ JANGAN:
- Jangan baca slide mentah-mentahan
- Jangan jelasin semua code line-by-line
- Jangan berdiri kaku (gunakan gesture)
- Jangan terburu-buru (speak slowly & clearly)
- Jangan lupa close program dengan on_closing()

✅ HARUS:
- Jelaskan tujuan program dulu
- Gunakan diagram alur & visual
- Tunjukkan demo live (tambah → tunggu → update status)
- Highlight konsep threading (ini yang paling penting)
- Sebutkan teknologi yang dipakai
- Bersiap untuk Q&A
- Tutup dengan kesimpulan yang jelas
```

---

## 🎯 CHECKLIST SIAP PRESENTASI

- [ ] Program sudah tested & berjalan dengan baik
- [ ] Slide presentation sudah siap (10 slide)
- [ ] Script pembicara sudah ditulis (di file ini)
- [ ] Contoh kode sudah disiapkan untuk demo
- [ ] Laptop & projector sudah dicek
- [ ] Font/size slide cukup besar untuk dibaca audience
- [ ] Durasi presentasi sudah dicek (~15 menit)
- [ ] Sudah berdiri di depan & practice 1-2x
- [ ] Sudah berpikir kemungkinan pertanyaan Q&A

---

**Siap presentasi! Good luck! 🎉**
