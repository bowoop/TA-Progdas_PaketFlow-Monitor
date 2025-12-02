# 📚 PENJELASAN LENGKAP PROGRAM PAKETFLOW MONITOR

## 🎯 RINGKASAN SINGKAT
Program ini adalah aplikasi GUI untuk manajemen paket pengiriman. User bisa:
1. Menambah paket baru
2. Mengecek status paket
3. Melihat riwayat pengiriman
4. Melihat urutan pengantaran paket

Status paket **berubah otomatis** sesuai waktu: `diproses` → `shipping` → `dikirim ke alamat` → `selesai`

---

## 🔄 ALUR PROGRAM DARI AWAL SAMPAI AKHIR

### **STEP 1: PROGRAM DIMULAI (`main.py`)**
```python
if __name__ == "__main__":
    root = tk.Tk()
    app = PaketFlowMonitor(root)
    root.mainloop()
```
**Yang terjadi:**
1. `if __name__ == "__main__":` → Cek apakah file dijalankan langsung (bukan diimport)
2. `root = tk.Tk()` → Buat window kosong (root window)
3. `app = PaketFlowMonitor(root)` → Jalankan konstruktor class PaketFlowMonitor
4. `root.mainloop()` → Mulai loop event GUI (tunggu user input, update tampilan, dll)

**Sintaks yang dipakai:**
- `if __name__ == "__main__":` = standar Python untuk main entry point
- `tk.Tk()` = constructor dari tkinter untuk membuat window utama

---

### **STEP 2: GUI DIINISIALISASI (`app.py` - `__init__`)**
```python
def __init__(self, root):
    self.root = root
    self.root.title("🚚 PaketFlow Monitor")
    self.root.geometry("600x500")
    self.root.resizable(False, False)
    
    self.manager = PaketManager()
    self.manager.start_auto_update(callback=self.on_status_changed)
    
    # ... setup frame, button, etc ...
    
    self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
```

**Baris per baris:**

| Kode | Penjelasan |
|------|-----------|
| `self.root = root` | Simpan window reference untuk dipakai di method lain |
| `self.root.title(...)` | Set judul window |
| `self.root.geometry("600x500")` | Set ukuran window: lebar 600px, tinggi 500px |
| `self.root.resizable(False, False)` | Jangan biarkan user resize window |
| `self.manager = PaketManager()` | **PENTING**: Buat instance manager yang handle bisnis logic & auto-update |
| `self.manager.start_auto_update(...)` | Mulai thread background untuk update status otomatis |
| `self.root.protocol("WM_DELETE_WINDOW", self.on_closing)` | Saat user klik X (tutup), panggil `on_closing()` untuk cleanup |

**Sintaks penting:**
- `self.` = reference ke instance sendiri (variabel yg bisa dipakai method lain)
- `PaketManager()` = buat instance baru class PaketManager
- `protocol()` = register handler untuk event window tertentu

---

### **STEP 3: BACKGROUND THREAD MULAI (`manager.py`)**
```python
def start_auto_update(self, callback=None):
    self._status_update_callback = callback
    self._is_running = True
    self._auto_update_thread = threading.Thread(
        target=self._auto_update_loop,
        daemon=True
    )
    self._auto_update_thread.start()
```

**Yang terjadi:**
1. `threading.Thread(...)` → Buat thread baru
2. `target=self._auto_update_loop` → Tentukan fungsi yg dijalankan thread
3. `daemon=True` → Thread adalah daemon (mati saat program utama exit)
4. `.start()` → Mulai jalankan thread

**Thread akan menjalankan:**
```python
def _auto_update_loop(self):
    while self._is_running:
        time.sleep(1)  # Tunggu 1 detik
        
        for id_paket, paket in list(self._daftar_paket.items()):
            # Cek waktu setiap paket
            waktu_dibuat = datetime.strptime(
                paket.get_waktu_dibuat(), 
                "%Y-%m-%d %H:%M:%S"
            )
            selisih_detik = (datetime.now() - waktu_dibuat).total_seconds()
            
            # Update status berdasarkan waktu
            if status == "diproses" and selisih_detik >= 10:
                paket.set_status("shipping")
            elif status == "shipping" and selisih_detik >= 20:
                paket.set_status("dikirim ke alamat")
            elif status == "dikirim ke alamat" and selisih_detik >= 40:
                paket.set_status("selesai")
```

**Sintaks:**
- `while self._is_running:` = loop terus selama flag TRUE (akan berhenti saat flag di-set FALSE)
- `time.sleep(1)` = jeda 1 detik (supaya tidak CPU-intensive)
- `list(self._daftar_paket.items())` = konversi dict ke list pasangan (key, value)
- `datetime.strptime(...)` = parse string jadi datetime object
- `.total_seconds()` = hitung selisih waktu dalam detik

---

### **STEP 4: GUI DITAMPILKAN (`show_menu_utama`)**
```python
def show_menu_utama(self):
    self.clear_frame()  # Hapus widget lama
    tk.Label(...).pack(pady=10)  # Tambah label
    
    buttons = [
        ("Tambahkan Paket Baru", self.show_form_tambah, "#118C13"),
        ("Cek Status Paket", self.show_form_cek, "#F18F01"),
        ("Lihat Riwayat Transaksi", self.show_riwayat, "#310D95"),
        ("❌ Keluar", self.root.quit, "#8F1010"),
    ]
    
    for text, cmd, color in buttons:
        tk.Button(
            self.frame_menu, 
            text=text, 
            command=cmd, 
            font=("Arial", 11),
            bg=color, 
            fg="white", 
            width=30, 
            height=2
        ).pack(pady=10)
```

**Sintaks:**
- `self.clear_frame()` = method untuk delete semua widget di frame
- `tk.Label(...)` = buat text label
- `tk.Button(...)` = buat button
- `command=cmd` = fungsi apa yg dijalankan saat button diklik
- `for text, cmd, color in buttons:` = loop & unpack tuple (3 elemen dari setiap baris)
- `.pack(...)` = layout manager (posisikan widget)

---

### **STEP 5: USER KLIK "TAMBAH PAKET"**
```python
def show_form_tambah(self):
    self.clear_frame()
    # ... setup input form ...
    tk.Button(self.frame_menu, text="✅ Tambah Paket", 
              command=self.proses_tambah_paket, ...).pack(pady=10)
```

User input nama penerima, lalu klik "Tambah Paket" → panggil `proses_tambah_paket()`:

```python
def proses_tambah_paket(self):
    nama = self.entry_nama.get()  # Ambil text dari input field
    paket, pesan = self.manager.tambah_paket(nama)  # Kirim ke manager
    
    if not paket:
        messagebox.showerror("Gagal", pesan)
        return
    
    detail = f"✅ Paket Berhasil Ditambahkan!\n..."
    messagebox.showinfo("Sukses", detail)
```

**Di manager:**
```python
def tambah_paket(self, nama_penerima):
    if not nama_penerima or not nama_penerima.strip():
        return None, "Error: Nama penerima wajib diisi!"
    
    # Buat paket baru
    paket_baru = Paket(nama_penerima)
    
    # Simpan ke 3 tempat:
    self._daftar_paket[paket_baru.get_id_paket()] = paket_baru  # Dict
    self._queue_pengantaran.enqueue(paket_baru.get_id_paket())  # Queue (untuk antrian)
    self._stack_riwayat.push(paket_baru.get_id_paket())  # Stack (untuk history)
    
    paket_baru.mark_status_recorded("diproses")
    
    return paket_baru, "Paket berhasil ditambahkan!"
```

**Sintaks:**
- `.get()` = ambil value dari input widget
- `.strip()` = hapus whitespace awal/akhir
- `Paket(...)` = buat instance baru Paket
- `enqueue()` = masukkan ke Queue
- `push()` = masukkan ke Stack
- Return tuple `(paket, pesan)` = return 2 value sekaligus

---

### **STEP 6: PAKET DI BACKGROUND UPDATE STATUS**

Thread terus running di background, setiap 1 detik cek:
- Paket yg status "diproses" + waktu >= 10s → ubah ke "shipping"
- Paket yg status "shipping" + waktu >= 20s → ubah ke "dikirim ke alamat"
- Paket yg status "dikirim ke alamat" + waktu >= 40s → ubah ke "selesai"

**Di model.py:**
```python
class Paket:
    _paket_counter = 1000  # Class variable (dibagi semua instance)
    
    def __init__(self, nama_penerima):
        self._id_paket = self._generate_id()  # Generate ID unik
        self._nama_penerima = nama_penerima
        self._status = "diproses"  # Status awal
        self._waktu_dibuat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # ... atribut lain ...
    
    @classmethod
    def _generate_id(cls):
        cls._paket_counter += 1  # Increment counter
        return f"PKT-{cls._paket_counter}"  # Return string ID
    
    def set_status(self, status_baru):
        status_valid = ["diproses", "shipping", "dikirim ke alamat", "selesai"]
        if status_baru in status_valid:
            self._status = status_baru
            
            # Catat waktu saat status berubah
            if status_baru == "shipping":
                self._waktu_shipping = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif status_baru == "dikirim ke alamat":
                self._waktu_dikirim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif status_baru == "selesai":
                self._waktu_selesai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return True
        return False
```

**Sintaks:**
- `_paket_counter` = class variable (milik class, bukan instance)
- `@classmethod` = decorator (method yang dapat `cls` bukan `self`)
- `cls._paket_counter += 1` = increment counter di class
- `f"PKT-{cls._paket_counter}"` = f-string (format string dengan variable)
- `datetime.now()` = ambil waktu saat ini
- `.strftime(...)` = format datetime ke string

---

### **STEP 7: USER CEK STATUS PAKET**
```python
def proses_cek_paket(self):
    id_paket = self.entry_id.get().strip().upper()
    paket = self.manager.cari_paket(id_paket)  # Cari di dict
    
    if not paket:
        messagebox.showwarning("Peringatan", "⚠️ Paket tidak tersedia")
        return
    
    info = paket.get_info()  # Ambil informasi
    detail = f"📦 Informasi Paket\n\nID: {info['id']}\nNama: {info['nama']}\nStatus: {info['status']}"
    
    messagebox.showinfo("Status Paket", detail)
```

**Di manager:**
```python
def cari_paket(self, id_paket):
    return self._daftar_paket.get(id_paket)  # Lookup di dict
```

**Sintaks:**
- `.get(key)` = ambil value dari dict (return None jika tidak ada)
- `get_info()` = method yang return dict dengan info paket

---

### **STEP 8: USER LIHAT RIWAYAT**
```python
def show_riwayat(self):
    self.clear_frame()
    
    riwayat = self.manager.get_riwayat()  # Ambil dari Stack
    
    if not riwayat:
        tk.Label(..., text="📭 Belum ada riwayat").pack()
    else:
        tree = ttk.Treeview(self.frame_menu, columns=("ID Paket",), height=12)
        tree.heading("ID Paket", text="Paket")
        
        for id_paket in reversed(riwayat):  # Reverse = lihat yang terbaru dulu
            tree.insert("", "end", values=(id_paket,))  # Tambah baris
        
        tree.pack(...)
```

**Di manager:**
```python
def get_riwayat(self):
    return self._stack_riwayat.display()  # Panggil method display Stack
```

**Di model.py (Stack.display):**
```python
def display(self):
    return self.items.copy()  # Return copy list (aman dari modifikasi)
```

**Sintaks:**
- `ttk.Treeview(...)` = widget table/tabel di Tkinter
- `reversed(riwayat)` = balik urutan list (terbaru di atas)
- `.insert(...)` = tambah baris ke table
- `.copy()` = buat salinan list (supaya data asli aman)

---

### **STEP 9: USER TUTUP PROGRAM**
```python
def on_closing(self):
    self.manager.stop_auto_update()  # Hentikan thread
    self.root.destroy()  # Tutup window
```

**Di manager:**
```python
def stop_auto_update(self):
    self._is_running = False  # Set flag FALSE
    # Thread akan exit karena while loop condition = False
```

**Sintaks:**
- `stop_auto_update()` = set flag untuk berhenti loop
- `destroy()` = tutup window

---

## 📊 DATA STRUCTURES

### **Queue (Antrian - FIFO)**
```python
class Queue:
    def __init__(self):
        self.items = deque()  # Deque = double-ended queue (efisien)
    
    def enqueue(self, item):
        self.items.append(item)  # Masuk dari belakang
    
    def dequeue(self):
        return self.items.popleft() if not self.is_empty() else None  # Ambil dari depan
    
    def display(self):
        return list(self.items)  # Lihat isi
```

**Gunanya di program:**
- Menyimpan urutan ID paket yang sedang dalam pengantaran
- FIFO = First In First Out (yang masuk pertama diproses pertama)

### **Stack (Tumpukan - LIFO)**
```python
class Stack:
    def __init__(self):
        self.items = []  # List biasa
    
    def push(self, item):
        self.items.append(item)  # Masuk ke atas tumpukan
    
    def pop(self):
        return self.items.pop() if not self.is_empty() else None  # Ambil dari atas
    
    def display(self):
        return self.items.copy()  # Lihat isi
```

**Gunanya di program:**
- Menyimpan riwayat paket (newest first)
- LIFO = Last In First Out (yang masuk terakhir diambil pertama)

---

## 🔧 SINTAKS PENTING YANG HARUS DIMENGERTI

| Sintaks | Penjelasan |
|---------|-----------|
| `def method(self, param):` | Definisi method di class (self = instance reference) |
| `self.variabel` | Variabel instance (milik object tertentu) |
| `_variabel` | Convention: private variable (internal use) |
| `if not value:` | Check jika value False/None/kosong |
| `.get()` | Method dict untuk ambil value |
| `.append()` | Tambah element ke list/deque |
| `.popleft()` | Ambil element pertama dari deque |
| `.pop()` | Ambil element terakhir dari list |
| `.strip()` | Hapus whitespace awal/akhir |
| `.upper()` | Ubah ke uppercase |
| `f"text {var}"` | F-string (format string dengan variable) |
| `try/except` | Handle exception (error) |
| `for x in list:` | Loop setiap element |
| `return value1, value2` | Return tuple (2 value sekaligus) |
| `if __name__ == "__main__":` | Jalankan hanya saat file dijalankan langsung |
| `@classmethod` | Decorator (method milik class, bukan instance) |
| `threading.Thread(...)` | Buat thread baru |
| `.daemon = True` | Thread mati saat program exit |
| `.start()` | Jalankan thread |
| `datetime.now()` | Waktu saat ini |
| `.strftime(format)` | Format datetime ke string |
| `.strptime(string, format)` | Parse string ke datetime |
| `.total_seconds()` | Hitung selisih waktu dalam detik |

---

## 📌 RINGKASAN ALUR SINGKAT

```
MULAI (main.py)
    ↓
Buat Window + PaketFlowMonitor (app.py)
    ↓
Mulai Thread Auto-Update (manager.py)
    ↓
Tampilkan Menu Utama (GUI)
    ↓ ← User Input (Tambah/Cek/Riwayat)
├─→ TAMBAH: Input nama → manager.tambah_paket() → Buat Paket baru → Simpan 3 tempat
├─→ CEK: Input ID → manager.cari_paket() → Tampilkan info + waktu
└─→ RIWAYAT: manager.get_riwayat() → Tampilkan tabel
    ↑
Background Thread (terus jalan):
    - Setiap 1s: cek waktu semua paket
    - Update status otomatis (10s→20s→40s)
    - Catat waktu stage
    ↓
User Tutup (on_closing)
    ↓
Hentikan Thread → Tutup Window
    ↓
SELESAI
```

---

## 💡 TIPS UNTUK PRESENTASI

1. **Jelaskan tujuan program dulu** sebelum masuk kode
2. **Gunakan diagram alur** supaya audience mudah paham
3. **Tunjukkan demo live** - tambah paket, tunggu status berubah
4. **Jelaskan threading** - ini adalah konsep kunci (background update)
5. **Jelaskan data structures** - Queue untuk pengantaran, Stack untuk riwayat
6. **Sebutkan teknologi** yang dipakai:
   - Python 3
   - Tkinter (GUI)
   - Threading (multi-tasking)
   - Collections.deque (Queue)
   - Datetime (Timestamp)

---

**Dibuat untuk tugas presentasi Progdas (Semester 1)**
