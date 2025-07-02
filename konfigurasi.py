import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'laporan_infrastruktur.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

TIPE_LAPORAN = ["Jalan Rusak", "Lampu Mati", "Saluran Air", "Trotoar Rusak", "Lainnya"]
