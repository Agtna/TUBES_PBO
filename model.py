import datetime

class Laporan:
    def __init__(self, nama, deskripsi, tipe, latitude, longitude, tanggal, id_laporan=None):
        self.id = id_laporan
        self.nama = nama or "Tanpa Nama"
        self.deskripsi = deskripsi or "-"
        self.tipe = tipe or "Lainnya"
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.tanggal = tanggal if isinstance(tanggal, datetime.date) else datetime.date.today()

    def to_dict(self):
        return {
            "nama": self.nama,
            "deskripsi": self.deskripsi,
            "tipe": self.tipe,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "tanggal": self.tanggal.strftime("%Y-%m-%d")
        }
