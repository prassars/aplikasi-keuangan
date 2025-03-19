import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import init_db, simpan_transaksi, get_transaksi, hapus_transaksi

saldo = 0  # Variabel saldo global

def update_saldo():
    global saldo
    saldo_label.config(text=f"Saldo: Rp {saldo:,}")

def load_data():
    global saldo
    saldo = 0
    tree.delete(*tree.get_children())  # Hapus data lama

    for row in get_transaksi():
        id_transaksi, tanggal, kategori, deskripsi, jumlah = row
        tree.insert("", "end", iid=id_transaksi, values=(tanggal, kategori, deskripsi, f"Rp {abs(jumlah):,}"))
        saldo += jumlah
    
    update_saldo()

def hapus_item():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Peringatan", "Pilih transaksi yang ingin dihapus!")
        return

    if not messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus transaksi ini?"):
        return

    id_transaksi = int(selected_item[0])  # Ambil ID transaksi dari TreeView
    hapus_transaksi(id_transaksi)
    tree.delete(selected_item)
    load_data()

def tambah_transaksi():
    form = tk.Toplevel(root)
    form.title("Tambah Transaksi")
    form.geometry("300x270")

    tk.Label(form, text="Tanggal").pack(anchor="w", padx=10, pady=2)
    date_entry = DateEntry(form)
    date_entry.pack(padx=10, pady=5)

    tk.Label(form, text="Kategori").pack(anchor="w", padx=10, pady=2)
    kategori_combobox = ttk.Combobox(form, values=["Pemasukan", "Pengeluaran"])
    kategori_combobox.pack(padx=10, pady=5)
    kategori_combobox.current(0)

    tk.Label(form, text="Deskripsi").pack(anchor="w", padx=10, pady=2)
    deskripsi_entry = tk.Entry(form, width=30)
    deskripsi_entry.pack(padx=10, pady=5)

    tk.Label(form, text="Jumlah (Rp)").pack(anchor="w", padx=10, pady=2)
    jumlah_entry = tk.Entry(form, width=30)
    jumlah_entry.pack(padx=10, pady=5)

    def simpan():
        try:
            jumlah = int(jumlah_entry.get())
            if kategori_combobox.get() == "Pengeluaran":
                jumlah = -jumlah
            simpan_transaksi(date_entry.get(), kategori_combobox.get(), deskripsi_entry.get(), jumlah)
            form.destroy()
            load_data()
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka")

    tk.Button(form, text="Simpan", command=simpan, bg="green", fg="white").pack(pady=10)

# Inisialisasi UI
root = tk.Tk()
root.title("Aplikasi Pencatat Keuangan")
root.geometry("600x400")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Pencatat Keuangan", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
saldo_label = tk.Label(root, text="Saldo Rp.0", font=("Arial", 12, "bold"), bg="#f0f0f0")
saldo_label.pack()

# Table
columns = ("Tanggal", "Kategori", "Deskripsi", "Jumlah")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(pady=10, expand=True, fill="both")

# Frame tombol
frame_tombol = tk.Frame(root, bg="#f0f0f0")
frame_tombol.pack(pady=10)

btn_tambah = tk.Button(frame_tombol, text="Tambah", command=tambah_transaksi, bg="green", fg="white")
btn_tambah.pack(side="left", padx=5)

btn_hapus = tk.Button(frame_tombol, text="Hapus", command=hapus_item, bg="red", fg="white")
btn_hapus.pack(side="left", padx=5)

# Load data saat aplikasi dimulai
init_db()
load_data()
root.mainloop()
