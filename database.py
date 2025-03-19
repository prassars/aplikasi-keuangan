import sqlite3

DB_PATH = "./aplikasi/keuangan.db"

def init_db():
    # buat database dan tabel jika belum ada
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            kategori TEXT,
            deskripsi TEXT,
            jumlah INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Simpan transaksi ke database
def simpan_transaksi(tanggal, kategori, deskripsi, jumlah):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transaksi (tanggal, kategori, deskripsi, jumlah) VALUES (?, ?, ?, ?)",
                   (tanggal, kategori, deskripsi, jumlah))
    conn.commit()
    conn.close()

# Ambil semua transaksi dari database
def get_transaksi():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, tanggal, kategori, deskripsi, jumlah FROM transaksi")
    data = cursor.fetchall()
    conn.close()
    return data

# Hapus transaksi berdasarkan ID
def hapus_transaksi(id_transaksi):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transaksi WHERE id=?", (id_transaksi,))
    conn.commit()
    conn.close()