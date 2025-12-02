# LOGIC & AUTO-UPDATE

from datetime import datetime
import threading
import time
from model import Queue, Stack, Paket

class PaketManager:
    def __init__(self):
        self._daftar_paket = {}
        self._queue_pengantaran = Queue()
        self._stack_riwayat = Stack()
        self._auto_update_thread = None
        self._is_running = True
        self._status_update_callback = None
    
    def tambah_paket(self, nama_penerima):
        if not nama_penerima or not nama_penerima.strip():
            return None, "Error: Nama penerima wajib diisi!"
        
        paket_baru = Paket(nama_penerima)
        self._daftar_paket[paket_baru.get_id_paket()] = paket_baru
        paket_baru.mark_status_recorded("diproses")
        self._queue_pengantaran.enqueue(paket_baru.get_id_paket())
        self._stack_riwayat.push(paket_baru.get_id_paket())
        
        return paket_baru, "Paket berhasil ditambahkan!"
    
    def cari_paket(self, id_paket):
        return self._daftar_paket.get(id_paket)
    
    def start_auto_update(self, callback=None):
        self._status_update_callback = callback
        self._is_running = True
        self._auto_update_thread = threading.Thread(
            target=self._auto_update_loop,
            daemon=True
        )
        self._auto_update_thread.start()
    
    def stop_auto_update(self):
        self._is_running = False
    
    def _auto_update_loop(self):
        while self._is_running:
            try:
                time.sleep(1)
                
                for id_paket, paket in list(self._daftar_paket.items()):
                    waktu_dibuat = datetime.strptime(paket.get_waktu_dibuat(), "%Y-%m-%d %H:%M:%S")
                    selisih_detik = (datetime.now() - waktu_dibuat).total_seconds()
                    status_sekarang = paket.get_status()
                    
                    if status_sekarang == "diproses" and selisih_detik >= 10:
                        if self._bisa_update_status(id_paket, "diproses"):
                            paket.set_status("shipping")
                            if not paket.is_status_recorded("shipping"):
                                paket.mark_status_recorded("shipping")
                            if self._status_update_callback:
                                self._status_update_callback(id_paket, "shipping")
                    
                    elif status_sekarang == "shipping" and selisih_detik >= 20:
                        if self._bisa_update_status(id_paket, "shipping"):
                            paket.set_status("dikirim ke alamat")
                            self._hitung_urutan_pengantaran_internal(id_paket)
                            if not paket.is_status_recorded("dikirim ke alamat"):
                                paket.mark_status_recorded("dikirim ke alamat")
                            if self._status_update_callback:
                                self._status_update_callback(id_paket, "dikirim ke alamat")
                    
                    elif status_sekarang == "dikirim ke alamat" and selisih_detik >= 40:
                        self._queue_pengantaran.remove_item(id_paket)
                        paket.set_status("selesai")
                        if not paket.is_status_recorded("selesai"):
                            paket.mark_status_recorded("selesai")
                        if self._status_update_callback:
                            self._status_update_callback(id_paket, "selesai")
            except:
                pass
    
    def _bisa_update_status(self, id_paket, status_saat_ini):
        queue_list = self._queue_pengantaran.display()
        if id_paket not in queue_list:
            return False
        
        paket_target_idx = queue_list.index(id_paket)
        for i in range(paket_target_idx):
            paket_lain = self._daftar_paket.get(queue_list[i])
            if paket_lain and paket_lain.get_status() == status_saat_ini:
                return False
        return True
    
    def _hitung_urutan_pengantaran_internal(self, id_paket):
        paket = self.cari_paket(id_paket)
        if not paket:
            return
        
        urutan = 1
        for id_dalam_queue in self._queue_pengantaran.display():
            if id_dalam_queue == id_paket:
                paket.set_urutan_pengantaran(urutan)
                return
            paket_cek = self._daftar_paket.get(id_dalam_queue)
            if paket_cek and paket_cek.get_status() == "dikirim ke alamat":
                urutan += 1
        paket.set_urutan_pengantaran(urutan)
    
    def hitung_urutan_pengantaran(self, id_paket):
        paket = self.cari_paket(id_paket)
        if not paket:
            return None, "Paket tidak tersedia"
        
        if paket.get_status() != "dikirim ke alamat":
            return None, f"⏳ Paket masih dalam status: {paket.get_status()}\n(Tunggu otomatis berubah)"
        
        urutan = 1
        penerima_sebelumnya = None
        for id_dalam_queue in self._queue_pengantaran.display():
            if id_dalam_queue == id_paket:
                return {
                    'urutan': urutan,
                    'total_dalam_queue': self._queue_pengantaran.size(),
                    'penerima_sebelumnya': penerima_sebelumnya
                }, "Sukses"
            paket_lain = self._daftar_paket.get(id_dalam_queue)
            if paket_lain and paket_lain.get_status() == "dikirim ke alamat":
                penerima_sebelumnya = paket_lain.get_nama_penerima()
                urutan += 1
        return None, "Paket tidak ditemukan dalam antrian pengantaran"
    
    def get_semua_paket(self):
        return self._daftar_paket
    
    def get_riwayat(self):
        return self._stack_riwayat.display()
    
    def get_queue_pengantaran(self):
        return self._queue_pengantaran.display()