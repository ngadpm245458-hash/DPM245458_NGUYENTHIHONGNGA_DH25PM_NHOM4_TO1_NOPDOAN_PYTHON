import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# ====== Kết nối MySQL ======


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="qlhocsinh"
    )

# ====== Căn giữa ======


def center_window(win, w=900, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")


# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản lý học sinh")
center_window(root)
root.resizable(False, False)

# ====== Tiêu đề ======
lbl_title = tk.Label(root, text="QUẢN LÝ HỌC SINH", font=("Arial", 20, "bold"))
lbl_title.pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = tk.LabelFrame(root, text="Thông tin học sinh")
frame_info.pack(padx=10, pady=10, fill="x")

tk.Label(frame_info, text="Mã HS:").grid(row=0, column=0, padx=5, pady=5)
entry_mahs = tk.Entry(frame_info, width=15)
entry_mahs.grid(row=0, column=1)

tk.Label(frame_info, text="Họ tên:").grid(row=0, column=2, padx=5)
entry_hoten = tk.Entry(frame_info, width=30)
entry_hoten.grid(row=0, column=3)

tk.Label(frame_info, text="Giới tính:").grid(
    row=1, column=0, padx=5, pady=5, sticky="w")

gender_var = tk.StringVar(value="Nam")
gender_var = tk.StringVar(value="Nữ")

# Nam
rd_nam = tk.Radiobutton(frame_info, text="Nam",
                        variable=gender_var, value="Nam")
rd_nam.grid(row=1, column=1, sticky="w")

# Nữ
rd_nu = tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ")
rd_nu.grid(row=1, column=2, sticky="w")


tk.Label(frame_info, text="Ngày sinh:").grid(row=2, column=0, padx=5)
date_entry = DateEntry(frame_info, width=15, date_pattern="yyyy-mm-dd")
date_entry.grid(row=2, column=1)

tk.Label(frame_info, text="Lớp:").grid(row=3, column=0, padx=5)
cbb_lop = ttk.Combobox(frame_info, values=[
                       "10A1", "10A2", "11A1", "11A2", "12A1", "12A2"], width=13)
cbb_lop.grid(row=3, column=1)

# ====== Frame tìm kiếm ======
frame_search = tk.LabelFrame(root, text="Tìm kiếm")
frame_search.pack(padx=10, pady=5, fill="x")

tk.Label(frame_search, text="Tìm theo tên hoặc mã HS:").grid(
    row=0, column=0, padx=5)
entry_search = tk.Entry(frame_search, width=25)
entry_search.grid(row=0, column=1, padx=5)

tk.Label(frame_search, text="Lọc theo lớp:").grid(row=0, column=2, padx=5)
cbb_filter_lop = ttk.Combobox(frame_search,
                              values=["Tất cả", "10A1", "10A2",
                                      "11A1", "11A2", "12A1", "12A2"],
                              width=10)
cbb_filter_lop.set("Tất cả")
cbb_filter_lop.grid(row=0, column=3, padx=5)

# ====== Bảng ======
columns = ("mahs", "hoten", "phai", "ngaysinh", "lop")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

tree.heading("mahs", text="Mã HS")
tree.heading("hoten", text="Họ tên")
tree.heading("phai", text="Giới tính")
tree.heading("ngaysinh", text="Ngày sinh")
tree.heading("lop", text="Lớp")

tree.column("mahs", width=80, anchor="center")
tree.column("hoten", width=200)
tree.column("phai", width=80, anchor="center")
tree.column("ngaysinh", width=120, anchor="center")
tree.column("lop", width=80, anchor="center")

tree.pack(padx=10, pady=10)

# ====== Các hàm xử lý ======


def clear_input():
    entry_mahs.delete(0, tk.END)
    entry_hoten.delete(0, tk.END)
    gender_var.set("Nam")
    date_entry.set_date("2000-01-01")
    cbb_lop.set("")


def load_data(condition=""):
    for i in tree.get_children():
        tree.delete(i)

    conn = connect_db()
    cur = conn.cursor()

    query = "SELECT * FROM hocsinh"
    if condition:
        query += " WHERE " + condition

    cur.execute(query)
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

    conn.close()


def them_hs():
    mahs = entry_mahs.get()
    hoten = entry_hoten.get()
    phai = gender_var.get()
    ngaysinh = date_entry.get()
    lop = cbb_lop.get()

    if mahs == "" or hoten == "":
        messagebox.showwarning(
            "Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
        return

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO hocsinh VALUES (%s, %s, %s, %s, %s)",
                    (mahs, hoten, phai, ngaysinh, lop))
        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

    conn.close()


def xoa_hs():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn học sinh để xóa")
        return

    mahs = tree.item(selected)["values"][0]

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM hocsinh WHERE mahs=%s", (mahs,))
    conn.commit()
    conn.close()

    load_data()


def sua_hs():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn học sinh để sửa")
        return

    values = tree.item(selected)["values"]

    entry_mahs.delete(0, tk.END)
    entry_mahs.insert(0, values[0])

    entry_hoten.delete(0, tk.END)
    entry_hoten.insert(0, values[1])

    gender_var.set(values[2])
    date_entry.set_date(values[3])
    cbb_lop.set(values[4])


def luu_hs():
    mahs = entry_mahs.get()
    hoten = entry_hoten.get()
    phai = gender_var.get()
    ngaysinh = date_entry.get()
    lop = cbb_lop.get()

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE hocsinh
        SET hoten=%s, phai=%s, ngaysinh=%s, lop=%s
        WHERE mahs=%s
    """, (hoten, phai, ngaysinh, lop, mahs))

    conn.commit()
    conn.close()
    load_data()
    clear_input()


def tim_kiem():
    text = entry_search.get()
    lop = cbb_filter_lop.get()

    condition = "1=1"

    if text:
        condition += f" AND (hoten LIKE '%{text}%' OR mahs LIKE '%{text}%')"
    if lop != "Tất cả":
        condition += f" AND lop='{lop}'"

    load_data(condition)

# ====== Xem chi tiết khi click ======


def on_tree_select(event):
    selected = tree.selection()
    if not selected:
        return

    values = tree.item(selected)["values"]
    if not values:
        return

    mahs, hoten, phai, ngaysinh, lop = values

    # Cửa sổ chi tiết
    win = tk.Toplevel(root)
    win.title("Chi tiết học sinh")
    win.resizable(False, False)
    center_window(win, 400, 260)

    frm = tk.Frame(win, padx=15, pady=15)
    frm.pack(fill="both", expand=True)

    labels = ["Mã HS:", "Họ tên:", "Giới tính:", "Ngày sinh:", "Lớp:"]
    data = [mahs, hoten, phai, ngaysinh, lop]

    for i in range(5):
        tk.Label(frm, text=labels[i], font=("Arial", 11, "bold")).grid(
            row=i, column=0, sticky="w", pady=4)
        tk.Label(frm, text=str(data[i]), font=("Arial", 11)).grid(
            row=i, column=1, sticky="w", pady=4)

    def quick_edit():
        entry_mahs.delete(0, tk.END)
        entry_mahs.insert(0, mahs)
        entry_hoten.delete(0, tk.END)
        entry_hoten.insert(0, hoten)
        gender_var.set(phai)
        date_entry.set_date(ngaysinh)
        cbb_lop.set(lop)
        win.destroy()

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Sửa trên form", width=12,
              command=quick_edit).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Đóng", width=12,
              command=win.destroy).grid(row=0, column=1, padx=10)


# Gắn sự kiện click
tree.bind("<<TreeviewSelect>>", on_tree_select)

# ====== Frame nút ======
frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)

tk.Button(frame_btn, text="Thêm", width=10,
          command=them_hs).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Sửa", width=10,
          command=sua_hs).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Lưu", width=10,
          command=luu_hs).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Xóa", width=10,
          command=xoa_hs).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Làm mới", width=10,
          command=lambda: load_data()).grid(row=0, column=4, padx=5)
tk.Button(frame_btn, text="Tìm kiếm", width=10,
          command=tim_kiem).grid(row=0, column=5, padx=5)
tk.Button(frame_btn, text="Thoát", width=10,
          command=root.quit).grid(row=0, column=6, padx=5)

# ====== Load dữ liệu ======
load_data()

root.mainloop()
