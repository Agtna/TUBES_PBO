from model import Laporan
import database

class ManajerLaporan:
    def tambah_laporan(self, laporan: Laporan):
        database.insert_laporan(laporan.to_dict())

    def semua_laporan_df(self):
        return database.get_all_laporan()

    def hapus_laporan(self, id_laporan: int) -> bool:
        return database.delete_laporan_by_id(id_laporan)
