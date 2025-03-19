import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3

# buat database dan tabel jika belum ada
conn = sqlite3.connect(r"./aplikasi/keuangan.db")
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

saldo = 0
def update_saldo():
    saldo_label.config(text=f"Saldo: Rp {saldo:,}")

def load_data():
    global saldo
    saldo = 0 #reset saldo
    cursor.execute("SELECT tanggal, kategori, deskripsi, jumlah FROM transaksi")
    for row in cursor.fetchall():
        tanggal, kategori, deskripsi, jumlah = row
        tree.insert("", "end", values=(tanggal, kategori, deskripsi, f"Rp {abs(jumlah):,}"))
        saldo += jumlah
    
    update_saldo()

def simpan_transaksi(date_entry, kategori_combobox, deskripsi_entry, jumlah_entry, form):
    global saldo
    # mengambil nilai dari input
    tanggal = date_entry.get()
    kategori = kategori_combobox.get()
    deskripsi = deskripsi_entry.get()
    jumlah = jumlah_entry.get()

    # memastikan semua input terisi
    if tanggal and kategori and deskripsi and jumlah:
        try:
            jumlah = int(jumlah)
            if kategori == "Pengeluaran":
                jumlah = -jumlah
            
            # Simpan ke database
            cursor.execute("INSERT INTO transaksi (tanggal, kategori, deskripsi, jumlah) VALUES     (?, ?, ?, ?)",(tanggal, kategori, deskripsi, jumlah))
            conn.commit()

            saldo += jumlah
            update_saldo()
            # Masukkan data ke tabel utama
            tree.insert("", "end", values=(tanggal, kategori, deskripsi, f"Rp {abs(jumlah):,}"))

            form.destroy()
        except ValueError:
            messagebox.showerror("Error", "jumlah harus berupa angka")
    else:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")

def buka_form_transaksi():
    # buat jendela baru
    form = tk.Toplevel(root)
    form.title("Tambah Transaksi")
    form.geometry("300x300")

    # label dan input tanggal
    tk.Label(form, text="Tanggal").pack(anchor="w", padx=10, pady=2)
    date_entry = DateEntry(form, width=20)
    date_entry.pack(padx=10, pady=5)

    # label dan input kategory
    tk.Label(form, text="Kategori: ").pack(anchor="w", padx=10,pady=2)
    kategori_combobox = ttk.Combobox(form, values=["Pemasukan", "Pengeluaran"])
    kategori_combobox.pack(padx=10, pady=5)
    kategori_combobox.current(0)

    # label dan input deskripsi
    tk.Label(form, text="Deskripsi").pack(anchor="w", padx=10, pady=2)
    deskripsi_entry = tk.Entry(form, width=30)
    deskripsi_entry.pack(padx=10, pady=5)

    # Label dan input jumlah
    tk.Label(form, text="jumlah (Rp): ").pack(anchor="w", padx=10, pady=2)
    jumlah_entry = tk.Entry(form, width=30)
    jumlah_entry.pack(padx=10, pady=5)

    # tombol simpan
    tk.Button(form, text="Simpan", command=lambda:simpan_transaksi(date_entry, kategori_combobox, deskripsi_entry, jumlah_entry, form)).pack(pady=10)


# buat jendela utama
root = tk.Tk()
root.title("Aplikasi Pencatat Keuangan")
root.geometry("600x400") #ukuran jendela

# Label judul
label_title = tk.Label(root, text="Pencatat Keuangan", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

# label saldo
saldo_label = tk.Label(root,  text="Saldo Rp.0", font=("Arial", 12, "bold"))
saldo_label.pack()

# table daftar transaksi
columns = ("Tanggal", "Kategori", "Deskripsi", "jumlah")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(pady=10, expand=True, fill="both")

# tombol tambah transaksi
btn_tambah = tk.Button(root, text="Tambah Transaksi", font=("Arial", 12), command=buka_form_transaksi)
btn_tambah.pack(pady=5)

# load data saat aplikasi di jalankan
load_data()

# jalankan aplikasi
root.mainloop()

# tutup koneksi db saat aplikasi di tutup
conn.close()