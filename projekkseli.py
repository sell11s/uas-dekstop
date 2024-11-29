import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

conn = sqlite3.connect("produk.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    harga INTEGER NOT NULL
)
""")
conn.commit()

def tambah_produk():
    nama = entry_nama.get()
    harga = entry_harga.get()
    if nama and harga.isdigit():
        cursor.execute("INSERT INTO produk (nama, harga) VALUES (?, ?)", (nama, int(harga)))
        conn.commit()
        update_tabel()
        entry_nama.delete(0, tk.END)
        entry_harga.delete(0, tk.END)
    else:
        messagebox.showwarning("Peringatan", "Nama dan harga harus diisi!")

def ubah_produk():
    try:
        selected_item = tabel.selection()[0]
        produk_id = tabel.item(selected_item)['values'][0]
        nama_baru = entry_nama.get()
        harga_baru = entry_harga.get()
        if nama_baru and harga_baru.isdigit():
            cursor.execute("UPDATE produk SET nama = ?, harga = ? WHERE id = ?", 
                           (nama_baru, int(harga_baru), produk_id))
            conn.commit()
            update_tabel()
            entry_nama.delete(0, tk.END)
            entry_harga.delete(0, tk.END)
        else:
            messagebox.showwarning("Peringatan", "Nama dan harga harus diisi!")
    except IndexError:
        messagebox.showwarning("Peringatan", "Pilih item yang ingin diubah!")

def hapus_produk():
    try:
        selected_item = tabel.selection()[0]
        produk_id = tabel.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM produk WHERE id = ?", (produk_id,))
        conn.commit()
        update_tabel()
    except IndexError:
        messagebox.showwarning("Peringatan", "Pilih item yang ingin dihapus!")

def cari_produk():
    keyword = entry_cari.get().lower()
    cursor.execute("SELECT * FROM produk WHERE LOWER(nama) LIKE ?", ('%' + keyword + '%',))
    hasil = cursor.fetchall()
    update_tabel(hasil)

def update_tabel(data=None):
    for item in tabel.get_children():
        tabel.delete(item)
    if data is None:
        cursor.execute("SELECT * FROM produk")
        data = cursor.fetchall()
    for idx, row in enumerate(data):
        tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
        tabel.insert('', 'end', values=(row[0], row[1], f"Rp{row[2]:,}"), tags=(tag,))

root = tk.Tk()
root.title("Bukalapakk - SQLite")
root.geometry("900x600")  

root.configure(bg='#800080')  

frame_input = tk.Frame(root, bg='#800080')  
frame_input.pack(pady=10, fill="x", padx=10)

tk.Label(frame_input, text="Nama Produk:", font=("Arial", 12), bg='#800080', fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_nama = tk.Entry(frame_input, font=("Arial", 12), width=30, bg='#800080', fg='white', bd=2)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Harga Produk:", font=("Arial", 12), bg='#800080', fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_harga = tk.Entry(frame_input, font=("Arial", 12), width=30, bg='#800080', fg='white', bd=2)
entry_harga.grid(row=1, column=1, padx=5, pady=5)

button_tambah = tk.Button(frame_input, text="Tambah", command=tambah_produk, font=("Arial", 12), width=10, bg="#4CAF50", fg="white", bd=0)
button_tambah.grid(row=0, column=2, padx=5, pady=5)

button_ubah = tk.Button(frame_input, text="Ubah", command=ubah_produk, font=("Arial", 12), width=10, bg="#008CBA", fg="white", bd=0)
button_ubah.grid(row=1, column=2, padx=5, pady=5)

button_hapus = tk.Button(frame_input, text="Hapus", command=hapus_produk, font=("Arial", 12), width=10, bg="#f44336", fg="white", bd=0)
button_hapus.grid(row=0, column=3, padx=5, pady=5)

frame_cari = tk.Frame(root, bg='#800080')  
frame_cari.pack(pady=10, fill="x", padx=10)

tk.Label(frame_cari, text="Cari Produk:", font=("Arial", 12), bg='#800080', fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_cari = tk.Entry(frame_cari, font=("Arial", 12), width=40, bg='#800080', fg='white', bd=2)
entry_cari.grid(row=0, column=1, padx=5, pady=5)

tk.Button(frame_cari, text="Cari", command=cari_produk, font=("Arial", 12), width=10, bg="#ff9800", fg="white", bd=0).grid(row=0, column=2, padx=5, pady=5)

frame_tabel = tk.Frame(root, bg='#800080')  
frame_tabel.pack(pady=10, fill="both", expand=True, padx=10)

scrollbar = tk.Scrollbar(frame_tabel, orient="vertical")
scrollbar.pack(side="right", fill="y")

tabel = ttk.Treeview(frame_tabel, columns=("ID", "Nama Produk", "Harga"), show="headings", height=15, yscrollcommand=scrollbar.set)
tabel.heading("ID", text="ID")
tabel.heading("Nama Produk", text="Nama Produk")
tabel.heading("Harga", text="Harga")
tabel.column("ID", width=50, anchor=tk.CENTER)
tabel.column("Nama Produk", width=500)
tabel.column("Harga", width=150, anchor=tk.E)

tabel.tag_configure('evenrow', background="#9932CC", foreground="white")  
tabel.tag_configure('oddrow', background="#800080", foreground="white") 

tabel.pack(fill="both", expand=True)
scrollbar.config(command=tabel.yview)

update_tabel()

root.mainloop()
conn.close()