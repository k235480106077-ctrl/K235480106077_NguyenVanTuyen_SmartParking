import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import ParkingDatabase
from models import ParkingFeeCalculator


class SmartParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần mềm quản lý bãi đỗ xe thông minh")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f8fb")

        self.db = ParkingDatabase()
        self.calculator = ParkingFeeCalculator()

        self.build_ui()
        self.load_slots()
        self.load_tickets()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="PHẦN MỀM QUẢN LÝ BÃI ĐỖ XE THÔNG MINH",
            font=("Arial", 18, "bold"),
            bg="#0b6fa4",
            fg="white",
            pady=12
        )
        title.pack(fill="x")

        main_frame = tk.Frame(self.root, bg="#f4f8fb")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        left = tk.LabelFrame(main_frame, text="Thông tin gửi / lấy xe", font=("Arial", 12, "bold"), bg="#f4f8fb")
        left.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left, text="Biển số xe:", bg="#f4f8fb", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.plate_entry = tk.Entry(left, font=("Arial", 12), width=25)
        self.plate_entry.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(left, text="Vị trí đỗ:", bg="#f4f8fb", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.slot_combo = ttk.Combobox(left, font=("Arial", 12), width=22, state="readonly")
        self.slot_combo.grid(row=1, column=1, padx=10, pady=8)

        tk.Button(left, text="GỬI XE", bg="#178c4f", fg="white", font=("Arial", 11, "bold"), width=18, command=self.check_in).grid(row=2, column=0, columnspan=2, pady=8)
        tk.Button(left, text="LẤY XE / TÍNH TIỀN", bg="#d9534f", fg="white", font=("Arial", 11, "bold"), width=18, command=self.check_out).grid(row=3, column=0, columnspan=2, pady=8)
        tk.Button(left, text="LÀM MỚI", bg="#5b6770", fg="white", font=("Arial", 11, "bold"), width=18, command=self.refresh_all).grid(row=4, column=0, columnspan=2, pady=8)

        note = (
            "Quy định tính phí:\n"
            "- Giờ đầu: 5.000đ\n"
            "- Mỗi giờ tiếp theo: 3.000đ\n"
            "- Làm tròn lên theo giờ"
        )
        tk.Label(left, text=note, bg="#f4f8fb", fg="#333", justify="left", font=("Arial", 10)).grid(row=5, column=0, columnspan=2, padx=10, pady=15)

        right = tk.Frame(main_frame, bg="#f4f8fb")
        right.pack(side="right", fill="both", expand=True)

        slot_frame = tk.LabelFrame(right, text="Sơ đồ vị trí đỗ xe", font=("Arial", 12, "bold"), bg="#f4f8fb")
        slot_frame.pack(fill="x", pady=(0, 12))
        self.slot_grid = tk.Frame(slot_frame, bg="#f4f8fb")
        self.slot_grid.pack(padx=10, pady=10)

        history_frame = tk.LabelFrame(right, text="Lịch sử gửi xe", font=("Arial", 12, "bold"), bg="#f4f8fb")
        history_frame.pack(fill="both", expand=True)

        columns = ("id", "plate", "slot", "in", "out", "fee", "status")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        headings = {
            "id": "ID",
            "plate": "Biển số",
            "slot": "Vị trí",
            "in": "Thời gian gửi",
            "out": "Thời gian lấy",
            "fee": "Chi phí",
            "status": "Trạng thái"
        }
        widths = {"id": 50, "plate": 120, "slot": 80, "in": 160, "out": 160, "fee": 100, "status": 110}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_slots(self):
        for widget in self.slot_grid.winfo_children():
            widget.destroy()

        slots = self.db.get_slots()
        free_slots = [slot.slot_name for slot in slots if not slot.is_occupied]
        self.slot_combo["values"] = free_slots
        if free_slots:
            self.slot_combo.current(0)

        for index, slot in enumerate(slots):
            row = index // 6
            col = index % 6
            color = "#2eb872" if not slot.is_occupied else "#e74c3c"
            text = f"{slot.slot_name}\n{'Trống' if not slot.is_occupied else 'Có xe'}"
            label = tk.Label(
                self.slot_grid,
                text=text,
                bg=color,
                fg="white",
                width=12,
                height=3,
                font=("Arial", 10, "bold"),
                relief="ridge",
                bd=2
            )
            label.grid(row=row, column=col, padx=6, pady=6)

    def load_tickets(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for ticket in self.db.get_all_tickets():
            fee_text = f"{int(ticket.fee):,}đ".replace(",", ".")
            self.tree.insert("", "end", values=(
                ticket.ticket_id,
                ticket.plate_number,
                ticket.slot_name,
                ticket.check_in_time,
                ticket.check_out_time or "",
                fee_text,
                ticket.status
            ))

    def check_in(self):
        plate = self.plate_entry.get().strip().upper()
        slot = self.slot_combo.get().strip()

        if not plate:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập biển số xe.")
            return

        if not slot:
            messagebox.showwarning("Hết chỗ", "Hiện không còn vị trí trống.")
            return

        if self.db.get_active_ticket_by_plate(plate):
            messagebox.showwarning("Trùng biển số", "Xe này đang được gửi trong bãi.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.check_in(plate, slot, now)
        messagebox.showinfo("Thành công", f"Đã gửi xe {plate} vào vị trí {slot}.")
        self.plate_entry.delete(0, tk.END)
        self.refresh_all()

    def check_out(self):
        plate = self.plate_entry.get().strip().upper()
        if not plate:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập biển số xe cần lấy.")
            return

        ticket = self.db.get_active_ticket_by_plate(plate)
        if not ticket:
            messagebox.showerror("Không tìm thấy", "Không tìm thấy xe đang gửi với biển số này.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fee = self.calculator.calculate_fee(ticket.check_in_time, now)
        self.db.check_out(ticket.ticket_id, ticket.slot_name, now, fee)

        fee_text = f"{int(fee):,}đ".replace(",", ".")
        messagebox.showinfo(
            "Thanh toán",
            f"Biển số: {plate}\n"
            f"Vị trí: {ticket.slot_name}\n"
            f"Thời gian gửi: {ticket.check_in_time}\n"
            f"Thời gian lấy: {now}\n"
            f"Chi phí: {fee_text}"
        )
        self.plate_entry.delete(0, tk.END)
        self.refresh_all()

    def refresh_all(self):
        self.load_slots()
        self.load_tickets()


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartParkingApp(root)
    root.mainloop()
