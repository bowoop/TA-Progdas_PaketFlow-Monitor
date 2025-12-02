# 🎬 SCRIPT PRESENTASI + CATATAN PEMBICARA

## SLIDE 1: JUDUL & TUJUAN (1 menit)

**Text di Slide:**
```
🚚 PAKETFLOW MONITOR
Aplikasi GUI untuk Manajemen Paket Pengiriman Otomatis

Dibuat oleh: [Nama Kamu]
Mata Kuliah: Pemrograman Dasar (Progdas)
```

**Catatan Pembicara:**
"Halo, nama saya [nama]. Hari ini saya akan menjelaskan program PaketFlow Monitor. Program ini adalah aplikasi desktop yang bisa digunakan untuk mengelola paket pengiriman. User bisa menambah paket, mengecek status, dan melihat riwayat pengiriman. Yang unik adalah status paket **berubah otomatis** di background tanpa perlu user melakukan apa-apa."

---

## SLIDE 2: FITUR UTAMA (1.5 menit)

**Text di Slide:**
```
📋 FITUR UTAMA

1. ➕ TAMBAH PAKET
   - Input nama penerima
   - Generate ID otomatis (PKT-1001, PKT-1002, dst)
   - Status otomatis: "DIPROSES"

2. 🔍 CEK STATUS PAKET
   - Input ID paket
   - Lihat status saat ini
   - Lihat timeline (waktu setiap stage)
   - Lihat urutan pengantaran

3. 📭 LIHAT RIWAYAT
   - Daftar semua paket yang pernah ditambahkan
   - Urutan terbaru di atas
   - Double-click untuk lihat detail

4. ⏱️ AUTO-UPDATE STATUS
   - Diproses (0-10s)
   - Shipping (10-20s)
   - Dikirim ke Alamat (20-40s)
   - Selesai (40s+)
```

**Catatan Pembicara:**
"Program ini memiliki 4 fitur utama. Pertama, user bisa menambah paket dengan input nama penerima. Sistem akan otomatis generate ID unik. Kedua, user bisa mencari paket dengan ID dan melihat status terkini plus waktu setiap stage. Ketiga, ada fitur riwayat untuk melihat semua paket yang pernah ditambahkan. Terakhir, fitur paling penting adalah auto-update status — paket secara otomatis berubah status setiap 10 detik sesuai dengan timeline pengiriman."

---

## SLIDE 3: ARSITEKTUR PROGRAM (2 menit)

**Text di Slide (Diagram Box):**
```
┌─────────────────────────────────────────┐
│         MAIN.PY (Entry Point)           │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼───────┐
         │   APP.PY      │  (GUI - Tkinter)
         │  - UI Layout  │
         │  - Button     │
         │  - Input Form │
         └───────┬───────┘
                 │
        ┌────────▼────────┐
        │  MANAGER.PY     │  (Business Logic)
        │  - tambah_paket │
        │  - cari_paket   │
        │  - auto_update  │◄── BACKGROUND THREAD
        │    (Thread)     │
        └────────┬────────┘
                 │
         ┌───────▼───────┐
         │   MODEL.PY    │
         │  - Queue      │
         │  - Stack      │
         │  - Paket      │
         └───────────────┘
```

**Catatan Pembicara:**
"Program ini terbagi menjadi 4 file dengan tugas yang jelas:

1. **Main.py** adalah entry point — file yang dijalankan pertama. Cuma 5 baris kode yang menggunakan if name == main untuk memastikan program baru dijalankan saat file ini dijalankan langsung.

2. **App.py** adalah GUI layer menggunakan Tkinter. Semua yang user lihat adalah button, label, input field — semuanya di sini.

3. **Manager.py** adalah jantung program — menyimpan semua data paket, handle logic tambah/cari, dan **paling penting** menjalankan thread background untuk auto-update status.

4. **Model.py** adalah data structure — mendefinisikan class Queue, Stack, dan Paket. Data yg dipakai program ada di sini.

Perhatikan panah ini (tunjuk diagram) — ada thread yang jalan di background dari manager. Thread ini yang membuat status paket berubah otomatis."

---

## SLIDE 4: ALUR EKSEKUSI (2 menit)

**Text di Slide:**
```
🔄 ALUR EKSEKUSI PROGRAM

STARTUP:
1. Python jalankan main.py
2. Buat window dengan tk.Tk()
3. Inisialisasi PaketFlowMonitor
4. Mulai thread auto-update
5. Tampilkan GUI menu utama
6. root.mainloop() ← Tunggu interaksi user

SAAT USER TAMBAH PAKET:
1. User input nama penerima
2. Klik button "Tambah Paket"
3. GUI ambil input dengan .get()
4. Panggil manager.tambah_paket(nama)
5. Manager buat instance Paket baru
6. Simpan ke: dict, queue, stack
7. Tampilkan popup "Sukses"

BACKGROUND (Thread):
1. Loop setiap 1 detik
2. Cek setiap paket di dict
3. Hitung selisih waktu dari dibuat
4. Update status sesuai threshold:
   - 10s: diproses → shipping
   - 20s: shipping → dikirim
   - 40s: dikirim → selesai
5. Catat waktu setiap stage

SHUTDOWN:
1. User klik X (tutup window)
2. Trigger WM_DELETE_WINDOW
3. Panggil on_closing()
4. Set flag _is_running = False
5. Thread berhenti
6. Window ditutup
```

**Catatan Pembicara:**
"Mari kita lihat alur saat program jalan. Saat startup, Python jalankan main.py, buat window, inisialisasi GUI, dan yang penting — **mulai thread background**. Thread ini terus jalan di belakang.

Saat user tambah paket, GUI catch event dan panggil manager. Manager membuat Paket baru dan simpan ke 3 tempat sekaligus: dict untuk lookup cepat, queue untuk antrian pengantaran, dan stack untuk riwayat.

Di background, thread terus memonitor. Setiap 1 detik dia cek semua paket. Dia hitung berapa lama paket sudah ada. Kalau sudah 10 detik, ubah status jadi shipping. 20 detik, ubah jadi dikirim. 40 detik, jadi selesai.

Saat user tutup program, handler WM_DELETE_WINDOW akan panggil on_closing() yang set flag FALSE. Thread akan berhenti karena while loop condition jadi False. Window ditutup dengan rapi."

---

## SLIDE 5: THREADING & CONCURRENCY (2 menit)

**Text di Slide:**
```
🔗 THREADING - Multi-tasking

TANPA THREADING (Masalah):
GUI Update Status
   ↓ (BLOCK - tunggu 10s)
Tidak bisa click button
   ↓
User experience buruk

DENGAN THREADING (Solusi):
┌─────────────────────┐
│  MAIN THREAD (GUI)  │
│  - Handle user      │
│  - Update display   │
│  - Respond cepat    │
└─────────────────────┘
         ↑ (Independent)
         │
┌─────────────────────┐
│ BACKGROUND THREAD   │
│  - Update status    │
│  - Hitung waktu     │
│  - Tidak ganggu GUI │
└─────────────────────┘

IMPLEMENTASI:
threading.Thread(
    target=self._auto_update_loop,
    daemon=True
).start()
```

**Catatan Pembicara:**
"Ini adalah konsep yang paling penting di program ini: **threading**.

Bayangkan jika program tidak pakai thread. GUI akan check status paket setiap 10 detik. Saat check status, GUI akan 'freeze' — user tidak bisa klik button, tidak bisa ketik, tidak bisa apa-apa. Ini disebut 'blocking'. User experience akan sangat jelek.

Dengan threading, kita punya 2 'worker' independent:
- **Main thread**: handle GUI, respond terhadap user input dengan cepat
- **Background thread**: handle update status di belakang, tidak ganggu GUI

Implementasinya sangat sederhana: `threading.Thread()` untuk buat thread, `target=` untuk tentukan fungsi yang dijalankan, `daemon=True` untuk buat thread ini mati otomatis saat program exit. Lalu `.start()` untuk mulai.

Ini adalah teknik professional yang dipakai di banyak aplikasi desktop."

---

## SLIDE 6: DATA STRUCTURES (2 menit)

**Text di Slide:**
```
📦 DATA STRUCTURES

QUEUE (Antrian - FIFO):
Input: [1, 2, 3]
Output: 1 (First In)
Gunanya: Urutan pengantaran paket

┌───┬───┬───┐
│ 1 │ 2 │ 3 │ ← output dari sini (FIFO)
└───┴───┴───┘
      ↑
   input ke sini

STACK (Tumpukan - LIFO):
Input: [1, 2, 3]
Output: 3 (Last In)
Gunanya: Riwayat paket (newest first)

      ↑
   output dari sini
   │ 3 │
   ├───┤
   │ 2 │
   ├───┤
   │ 1 │
   └───┘
   input ke sini

DICT (Dictionary):
Key: "PKT-1001"
Value: Paket Object
Gunanya: Lookup paket dengan cepat O(1)
```

**Catatan Pembicara:**
"Setiap data structure punya tujuan berbeda di program ini.

**Queue** dipakai untuk menyimpan urutan pengantaran. FIFO berarti 'First In First Out' — paket yang masuk pertama akan diproses pertama. Ini logis untuk pengantaran: jika Ada masuk antrian duluan, dia harus dikirim duluan.

**Stack** dipakai untuk riwayat. LIFO berarti 'Last In First Out' — paket yang masuk terakhir akan ditampilkan di atas. Ini sama seperti history di browser — yang terbaru di atas.

**Dict** dipakai untuk lookup cepat. Ketika user cek paket dengan ID 'PKT-1001', program tidak perlu loop semua paket. Cukup akses dict langsung dengan key. Ini sangat cepat O(1).

Ketiga data structure ini bekerja sama menyimpan data paket dari sudut pandang berbeda."

---

## SLIDE 7: DEMO LIVE (2 menit)

**Apa yang ditampilkan:**
1. Jalankan program
2. Klik "Tambah Paket Baru"
3. Input nama (contoh: "Budi")
4. Klik "Tambah Paket"
5. Lihat popup sukses dengan ID
6. Klik "Cek Status Paket"
7. Input ID, klik cek
8. Lihat status berubah (tunggu ~10s, status berubah dari "DIPROSES" ke "SHIPPING")
9. Klik "Lihat Riwayat"
10. Lihat paket di table

**Script saat demo:**
"Sekarang saya akan menjalankan program. Lihat — window buka. Di menu utama ada 4 pilihan.

Saya tambah paket. Input nama 'Budi'. Klik tambah. Lihat popup — paket berhasil ditambahkan dengan ID PKT-1001 dan status DIPROSES.

Sekarang saya cek status paket. Input ID PKT-1001. Lihat — status masih DIPROSES, waktu dibuat baru saja.

Mari kita tunggu... (tunggu 10+ detik) ... dan lihat status berubah menjadi SHIPPING otomatis! Background thread bekerja.

Saya bisa lihat timeline: DIPROSES berhasil, SHIPPING berhasil (dengan timestamp), dan DIKIRIM KE ALAMAT masih menunggu.

Terakhir, saya lihat riwayat. Table menampilkan PKT-1001 yang baru saja dibuat."

---

## SLIDE 8: CODE SNIPPET - CONTOH KUNCI (2 menit)

**Text di Slide:**

### CONTOH 1: Generate ID (Auto-increment)
```python
class Paket:
    _paket_counter = 1000  # Class variable
    
    @classmethod
    def _generate_id(cls):
        cls._paket_counter += 1
        return f"PKT-{cls._paket_counter}"

# Hasil:
Paket() → PKT-1001
Paket() → PKT-1002
Paket() → PKT-1003
```

### CONTOH 2: Update Status Otomatis
```python
waktu_dibuat = datetime.strptime(paket.get_waktu_dibuat(), "%Y-%m-%d %H:%M:%S")
selisih_detik = (datetime.now() - waktu_dibuat).total_seconds()

if status == "diproses" and selisih_detik >= 10:
    paket.set_status("shipping")
```

### CONTOH 3: Simpan ke 3 Tempat Sekaligus
```python
def tambah_paket(self, nama_penerima):
    paket_baru = Paket(nama_penerima)
    
    self._daftar_paket[paket_baru.get_id_paket()] = paket_baru  # Dict
    self._queue_pengantaran.enqueue(paket_baru.get_id_paket())  # Queue
    self._stack_riwayat.push(paket_baru.get_id_paket())        # Stack
    
    return paket_baru, "Sukses!"
```

**Catatan Pembicara:**
"Mari saya jelaskan 3 code snippet penting:

1. **Generate ID**: Ini gunakan class variable `_paket_counter` yang dibagi semua instance. Setiap kali buat Paket baru, counter increment. Hasilnya ID unik PKT-1001, 1002, dst. Method ini pake decorator `@classmethod` karena dia akses class variable, bukan instance variable.

2. **Update Status**: Ini logic dari background thread. Parse string waktu menjadi datetime object, hitung selisih dengan sekarang dalam detik, dan jika >= threshold, ubah status. Ini dijalankan setiap 1 detik untuk setiap paket.

3. **Simpan ke 3 Tempat**: Ini menunjukkan bagaimana data structure dipakai. Saat tambah paket, ID disimpan ke: dict untuk lookup cepat, queue untuk antrian, stack untuk riwayat. Satu paket, tiga view."

---

## SLIDE 9: CHALLENGES & LEARNING (1.5 menit)

**Text di Slide:**
```
🎯 TANTANGAN & PEMBELAJARAN

TANTANGAN YANG DIHADAPI:
1. ❌ Threading & GUI interaction
   → Tkinter tidak aman dipanggil dari thread lain
   → Solusi: Event queue + polling

2. ❌ Data race condition
   → Multiple thread akses dict bersamaan
   → Solusi: Lock / synchronization

3. ❌ Waktu & datetime
   → Parse string berulang buruk performance
   → Solusi: Simpan datetime object

4. ❌ Clean shutdown
   → Thread daemon tidak tercontrol
   → Solusi: Event + join()

YANG DIPELAJARI:
✅ Python: OOP, class variable, @classmethod
✅ GUI: Tkinter, widget, event handling
✅ Concurrency: Threading, daemon, race condition
✅ Data Structures: Queue, Stack, dictionary
✅ Datetime: timestamp, parsing, calculation
✅ Software design: separation of concerns
```

**Catatan Pembicara:**
"Saat membuat program ini, saya menghadapi beberapa tantangan.

Pertama, threading dan GUI interaction. Tkinter tidak aman jika dipanggil dari thread selain main thread — bisa crash atau behavior aneh. Solusinya adalah event queue: background thread push event ke queue, main thread polling queue dan update GUI.

Kedua, data race condition. Ketika background thread modify dict dan GUI thread baca dict di saat yang sama, data bisa corrupt. Solusinya adalah lock atau mechanism synchronization lain.

Ketiga, problem datetime. Kalau parse string berulang-ulang di loop yang berjalan 1000x per menit, akan buruk performance. Lebih baik simpan datetime object dari awal.

Terakhir, clean shutdown. Thread daemon akan terbunuh paksa saat program exit, tapi tidak selalu rapi. Lebih baik gunakan Event dan join() untuk graceful shutdown.

Dari proyek ini, saya belajar banyak tentang Python concurrency, Tkinter, dan software architecture yang baik."

---

## SLIDE 10: KESIMPULAN (1 menit)

**Text di Slide:**
```
✨ KESIMPULAN

Program PaketFlow Monitor menunjukkan:
• OOP & encapsulation
• Threading & concurrency
• Data structures (Queue, Stack)
• GUI development (Tkinter)
• Clean code architecture

Teknologi yang dipakai:
• Python 3
• Tkinter library
• Threading module
• Collections.deque
• Datetime module

Fitur yang berfungsi:
✅ Tambah paket dengan ID otomatis
✅ Cek status paket real-time
✅ Lihat riwayat pengiriman
✅ Update status otomatis (background thread)
✅ Antrian pengantaran terurut

Improvement di masa depan:
→ Persistence (save to file/database)
→ Unit testing
→ Better UI/UX
→ Status notification
```

**Catatan Pembicara:**
"Ringkasnya, program PaketFlow Monitor adalah aplikasi yang menunjukkan konsep-konsep penting dalam software development. Dari OOP, threading, data structures, sampai GUI development — semuanya ada.

Teknologi yang dipakai adalah tools industri standard: Python, Tkinter untuk GUI, threading untuk concurrency.

Semua fitur yang saya target berhasil diimplementasikan. Yang paling kompleks dan menarik adalah auto-update status menggunakan background thread — ini membuat user experience terasa responsive.

Kalau ada waktu lagi, saya mau tambah persistence (save data), unit testing, dan UI yang lebih baik. Tapi untuk saat ini, program sudah functional dan menunjukkan prinsip-prinsip good software design.

Terima kasih."

---

## 💡 TIPS PRESENTASI TAMBAHAN

### Alokasi Waktu:
- Slide 1-2: 2.5 menit (intro + fitur)
- Slide 3-6: 6 menit (arsitektur + detail teknis)
- Slide 7: 2 menit (demo live)
- Slide 8-10: 4.5 menit (code + learning + conclusion)
- **TOTAL: ~15 menit + Q&A**

### Yang Perlu Disiapkan:
- [ ] Laptop dengan program sudah berjalan
- [ ] Kabel HDMI (kalau perlu proyektor)
- [ ] Slide presentation (PowerPoint/Google Slides)
- [ ] Cheat sheet dengan code snippet
- [ ] Catatan pembicara dicetak

### Tips saat Presentasi:
1. **Jangan baca slide** — slide cuma visual aid, jelaskan dengan kata-kata sendiri
2. **Fokus ke satu orang** saat berbicara (eye contact)
3. **Demo dulu** baru jelasin — audience lebih engaged
4. **Pakai teknik "show & tell"** — tunjukkan kode, tunjukkan hasil
5. **Bersiap untuk Q&A** — pikirkan pertanyaan yg mungkin ditanya
6. **Jangan terburu-buru** — berbicara perlahan dan jelas
7. **Gunakan gesture** saat menjelaskan (tunjuk diagram, tunjuk kode)

### Pertanyaan yang Mungkin Ditanya:

**Q: Kenapa pakai threading?**
A: Supaya program tidak freeze. Background thread update status tanpa mengganggu GUI yang handle user input.

**Q: Apa perbedaan Queue dan Stack?**
A: Queue FIFO (masuk pertama, keluar pertama), Stack LIFO (masuk terakhir, keluar pertama). Queue untuk antrian, Stack untuk riwayat.

**Q: Bagaimana kalau ada crash di thread?**
A: Ada try/except di loop, atau bisa tambah logging untuk debug.

**Q: Gimana cara menyimpan data saat program ditutup?**
A: Bisa pakai file JSON atau database SQLite. Simpan dict paket ke file saat shutdown.

**Q: Apakah ini scalable untuk banyak paket?**
A: Dict lookup adalah O(1) jadi cepat. Tapi kalau sangat banyak paket (jutaan), mungkin perlu database.

---

**Selamat mempresentasikan! Semoga lancar! 🚀**
