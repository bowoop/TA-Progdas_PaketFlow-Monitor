# STRUKTUR DATA & CLASS PAKET

from collections import deque
from datetime import datetime

class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        return self.items.popleft() if not self.is_empty() else None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def display(self):
        return list(self.items)
    
    def peek(self):
        return self.items[0] if not self.is_empty() else None
    
    def remove_item(self, item):
        try:
            self.items.remove(item)
            return True
        except ValueError:
            return False


class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop() if not self.is_empty() else None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def display(self):
        return self.items.copy()


class Paket:
    _paket_counter = 1000
    
    def __init__(self, nama_penerima):
        self._id_paket = self._generate_id()
        self._nama_penerima = nama_penerima
        self._status = "diproses"
        self._waktu_dibuat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._waktu_shipping = None
        self._waktu_dikirim = None
        self._waktu_selesai = None
        self._urutan_pengantaran = None
        self._status_recorded = set()
    
    @classmethod
    def _generate_id(cls):
        cls._paket_counter += 1
        return f"PKT-{cls._paket_counter}"
    
    def get_id_paket(self):
        return self._id_paket
    
    def get_nama_penerima(self):
        return self._nama_penerima
    
    def get_status(self):
        return self._status
    
    def get_waktu_dibuat(self):
        return self._waktu_dibuat
    
    def get_waktu_shipping(self):
        return self._waktu_shipping
    
    def get_waktu_dikirim(self):
        return self._waktu_dikirim
    
    def get_waktu_selesai(self):
        return self._waktu_selesai
    
    def get_urutan_pengantaran(self):
        return self._urutan_pengantaran
    
    def get_info(self):
        return {
            'id': self._id_paket,
            'nama': self._nama_penerima,
            'status': self._status,
            'waktu': self._waktu_dibuat,
            'urutan': self._urutan_pengantaran
        }
    
    def set_status(self, status_baru):
        status_valid = ["diproses", "shipping", "dikirim ke alamat", "selesai"]
        if status_baru in status_valid:
            self._status = status_baru
            if status_baru == "shipping":
                self._waktu_shipping = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif status_baru == "dikirim ke alamat":
                self._waktu_dikirim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif status_baru == "selesai":
                self._waktu_selesai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True
        return False
    
    def set_urutan_pengantaran(self, urutan):
        self._urutan_pengantaran = urutan
    
    def is_status_recorded(self, status):
        return status in self._status_recorded
    
    def mark_status_recorded(self, status):
        self._status_recorded.add(status)