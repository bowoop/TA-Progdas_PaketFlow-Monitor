# GUI INTERFACE

import tkinter as tk
from tkinter import messagebox, ttk
from manager import PaketManager


class PaketFlowMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("🚚 PaketFlow Monitor")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.manager = PaketManager()
        self.manager.start_auto_update(callback=self.on_status_changed)
        
        frame_header = tk.Frame(root, bg="#2E86AB", height=60)
        frame_header.pack(fill="x")
        tk.Label(
            frame_header,
            text="🚚 PAKETFLOW MONITOR",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#2E86AB"
        ).pack(pady=8)
        
        self.frame_menu = tk.Frame(root, bg="white")
        self.frame_menu.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.show_menu_utama()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        self.manager.stop_auto_update()
        self.root.destroy()
    
    def on_status_changed(self, id_paket, status_baru):
        pass
    
    def show_menu_utama(self):
        self.clear_frame()
        tk.Label(self.frame_menu, text="Menu Utama", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        buttons = [
            ("Tambahkan Paket Baru", self.show_form_tambah, "#118C13"),
            ("Cek Status Paket", self.show_form_cek, "#F18F01"),
            ("Lihat Riwayat Transaksi", self.show_riwayat, "#310D95"),
            ("❌ Keluar", self.root.quit, "#8F1010"),
        ]
        
        for text, cmd, color in buttons:
            tk.Button(self.frame_menu, text=text, command=cmd, font=("Arial", 11),
                     bg=color, fg="white", width=30, height=2).pack(pady=10)
    
    def show_form_tambah(self):
        self.clear_frame()
        tk.Label(self.frame_menu, text="Tambahkan Paket Baru", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        frame_input = tk.Frame(self.frame_menu, bg="white")
        frame_input.pack(pady=10)
        tk.Label(frame_input, text="Nama Penerima:", font=("Arial", 10), bg="white").pack(side="left", padx=5)
        self.entry_nama = tk.Entry(frame_input, font=("Arial", 10), width=30)
        self.entry_nama.pack(side="left", padx=5)
        self.entry_nama.focus()
        
        tk.Button(self.frame_menu, text="✅ Tambah Paket", command=self.proses_tambah_paket,
                 font=("Arial", 10), bg="#28A745", fg="white", width=25).pack(pady=10)
        tk.Button(self.frame_menu, text="⬅️  Kembali ke Menu", command=self.show_menu_utama,
                 font=("Arial", 10), bg="#6C757D", fg="white", width=25).pack(pady=5)
    
    def proses_tambah_paket(self):
        nama = self.entry_nama.get()
        paket, pesan = self.manager.tambah_paket(nama)
        
        if not paket:
            messagebox.showerror("Gagal", pesan)
            self.entry_nama.delete(0, tk.END)
            return
        
        detail = f"✅ Paket Berhasil Ditambahkan!\n\nID Paket: {paket.get_id_paket()}\nNama Penerima: {paket.get_nama_penerima()}\nStatus: {paket.get_status().upper()}\nWaktu: {paket.get_waktu_dibuat()}\n"
        messagebox.showinfo("Sukses", detail)
        self.entry_nama.delete(0, tk.END)
    
    def show_form_cek(self):
        self.clear_frame()
        tk.Label(self.frame_menu, text="Cek Status Paket", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        tk.Label(self.frame_menu, text="Masukkan ID Paket (contoh: PKT-1001)", font=("Arial", 9), bg="white", fg="gray").pack(pady=5)
        
        frame_input = tk.Frame(self.frame_menu, bg="white")
        frame_input.pack(pady=10)
        tk.Label(frame_input, text="ID Paket:", font=("Arial", 10), bg="white").pack(side="left", padx=5)
        self.entry_id = tk.Entry(frame_input, font=("Arial", 10), width=30)
        self.entry_id.pack(side="left", padx=5)
        self.entry_id.focus()
        
        tk.Button(self.frame_menu, text="🔍 Cek Status", command=self.proses_cek_paket,
                 font=("Arial", 10), bg="#17A2B8", fg="white", width=25).pack(pady=10)
        tk.Button(self.frame_menu, text="⬅️  Kembali ke Menu", command=self.show_menu_utama,
                 font=("Arial", 10), bg="#6C757D", fg="white", width=25).pack(pady=5)
    
    def proses_cek_paket(self):
        id_paket = self.entry_id.get().strip().upper()
        paket = self.manager.cari_paket(id_paket)
        
        if not paket:
            messagebox.showwarning("Peringatan", "⚠️  Paket tidak tersedia")
            self.entry_id.delete(0, tk.END)
            return
        
        info = paket.get_info()
        detail = f"📦 Informasi Paket\n\nID Paket: {info['id']}\nNama Penerima: {info['nama']}\nStatus: {info['status'].upper()}\nWaktu Dibuat: {info['waktu']}"
        
        if paket.get_waktu_shipping():
            detail += f"\nWaktu Shipping: {paket.get_waktu_shipping()}"
        if paket.get_waktu_dikirim():
            detail += f"\nWaktu Dikirim: {paket.get_waktu_dikirim()}"
        if paket.get_waktu_selesai():
            detail += f"\nWaktu Selesai: {paket.get_waktu_selesai()}"
        
        if info['status'] == "dikirim ke alamat":
            detail += "\n\n✅ Paket sedang dalam pengiriman!"
            messagebox.showinfo("Status Paket", detail)
            self.show_urutan_pengantaran(id_paket)
        else:
            messagebox.showinfo("Status Paket", detail)
        
        self.entry_id.delete(0, tk.END)
    
    def show_urutan_pengantaran(self, id_paket):
        result, pesan = self.manager.hitung_urutan_pengantaran(id_paket)
        if not result:
            messagebox.showwarning("Info", pesan)
            return
        
        urutan, total, penerima_sebelum = result['urutan'], result['total_dalam_queue'], result['penerima_sebelumnya'] or "Paket pertama"
        detail = f"🚗 Urutan Pengantaran\n\nPaket Anda berada di urutan: {urutan} dari {total}\n\nPenerima sebelumnya:\n{penerima_sebelum}"
        messagebox.showinfo("Urutan Pengantaran", detail)
    
    def show_riwayat(self):
        self.clear_frame()
        tk.Label(self.frame_menu, text="Riwayat Transaksi", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        riwayat = self.manager.get_riwayat()
        if not riwayat:
            tk.Label(self.frame_menu, text="📭 Belum ada riwayat transaksi", font=("Arial", 11), bg="white", fg="gray").pack(pady=20)
        else:
            columns = ("ID Paket",)
            tree = ttk.Treeview(self.frame_menu, columns=columns, height=12, show="headings")
            tree.column("ID Paket", width=400, anchor="w")
            tree.heading("ID Paket", text="Paket")
            
            for id_paket in reversed(riwayat):
                tree.insert("", "end", values=(id_paket,))
            
            tree.bind("<Double-1>", lambda e: self.show_progress_paket(tree, riwayat))
            tree.pack(padx=10, pady=10, fill="both", expand=True)
            
            tk.Label(self.frame_menu, text="💡 Double-click paket untuk lihat progress", 
                    font=("Arial", 8), bg="white", fg="gray").pack(pady=5)
        
        tk.Button(self.frame_menu, text="⬅️  Kembali ke Menu", command=self.show_menu_utama,
                 font=("Arial", 10), bg="#6C757D", fg="white", width=25).pack(pady=5)
    
    def show_progress_paket(self, tree, riwayat):
        selection = tree.selection()
        if not selection:
            return
        
        item = tree.item(selection[0])
        id_paket = item['values'][0]
        
        paket = self.manager.cari_paket(id_paket)
        if not paket:
            messagebox.showwarning("Error", "Paket tidak ditemukan")
            return
        
        progress_text = f"📦 PROGRESS PAKET: {id_paket}\n"
        progress_text += f"Penerima: {paket.get_nama_penerima()}\n\n"
        progress_text += "="*40 + "\n"
        
        progress_steps = [
            ("1️⃣ DIPROSES", paket.get_waktu_dibuat()),
            ("2️⃣ SHIPPING", paket.get_waktu_shipping()),
            ("3️⃣ DIKIRIM KE ALAMAT", paket.get_waktu_dikirim()),
            ("4️⃣ SELESAI", paket.get_waktu_selesai()),
        ]
        
        for step, waktu in progress_steps:
            if waktu:
                progress_text += f"✅ {step}\n    Waktu: {waktu}\n"
            else:
                progress_text += f"⏳ {step}\n    (Menunggu...)\n"
            progress_text += "-"*40 + "\n"
        
        messagebox.showinfo("Progress Paket", progress_text)
    
    def clear_frame(self):
        for widget in self.frame_menu.winfo_children():
            widget.destroy()