import customtkinter as ctk
from tkinter import messagebox
import database


class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Dashboard", font=("Segoe UI", 29, "bold"),
                     text_color="#F4F7FB").pack(anchor="w", padx=30, pady=(28, 2))
        ctk.CTkLabel(self, text="Your campus lost & found activity at a glance",
                     text_color="#8798AF").pack(anchor="w", padx=30)
        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.pack(fill="x", padx=25, pady=25)
        self.values = {}
        data = [("TOTAL ITEMS", "#3987E8", "Total Items"),
                ("LOST REPORTS", "#E5A044", "Lost Items"),
                ("FOUND REPORTS", "#28B99A", "Found Items"),
                ("PENDING CLAIMS", "#A78BFA", "Pending Claims")]
        for title, color, key in data:
            card = ctk.CTkFrame(cards, fg_color="#162338", corner_radius=15,
                                border_width=1, border_color="#26364D")
            card.pack(side="left", fill="both", expand=True, padx=7)
            ctk.CTkFrame(card, height=4, fg_color=color, corner_radius=4).pack(
                fill="x", padx=15, pady=(15, 13))
            ctk.CTkLabel(card, text=title, text_color="#91A2B9",
                         font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=17)
            value = ctk.CTkLabel(card, text="—", text_color="#F4F7FB",
                                 font=("Segoe UI", 32, "bold"))
            value.pack(anchor="w", padx=17, pady=(5, 15))
            self.values[key] = value
        panel = ctk.CTkFrame(self, fg_color="#162338", corner_radius=15,
                             border_width=1, border_color="#26364D")
        panel.pack(fill="both", expand=True, padx=32, pady=(0, 28))
        head = ctk.CTkFrame(panel, fg_color="transparent")
        head.pack(fill="x", padx=20, pady=18)
        ctk.CTkLabel(head, text="Open items by category",
                     font=("Segoe UI", 17, "bold"), text_color="#F4F7FB").pack(side="left")
        ctk.CTkButton(head, text="↻  Refresh", width=105, height=34,
                      command=self.refresh, fg_color="#245B68",
                      hover_color="#287A83").pack(side="right")
        self.rows = ctk.CTkScrollableFrame(panel, fg_color="#111C2E", corner_radius=10)
        self.rows.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        self.refresh()

    def refresh(self):
        try:
            data = {
                "Total Items": database.fetch_value("SELECT COUNT(*) FROM items"),
                "Lost Items": database.fetch_value("SELECT get_open_count('LOST') FROM dual"),
                "Found Items": database.fetch_value("SELECT get_open_count('FOUND') FROM dual"),
                "Pending Claims": database.fetch_value(
                    "SELECT COUNT(*) FROM item_claims WHERE claim_status='PENDING'")
            }
            for key, value in data.items():
                self.values[key].configure(text=str(value))
            for widget in self.rows.winfo_children():
                widget.destroy()
            for col, title in enumerate(["CATEGORY", "OPEN ITEMS"]):
                ctk.CTkLabel(self.rows, text=title, text_color="#7F91A9",
                             font=("Segoe UI", 10, "bold")).grid(
                    row=0, column=col, sticky="w", padx=15, pady=12)
            rows = database.fetch_all("SELECT category, COUNT(*) AS total FROM items "
                "WHERE item_status='OPEN' GROUP BY category ORDER BY total DESC")
            for i, row in enumerate(rows, 1):
                ctk.CTkLabel(self.rows, text=str(row["category"]),
                             text_color="#E0E8F2").grid(row=i, column=0, sticky="w", padx=15, pady=10)
                ctk.CTkLabel(self.rows, text=str(row["total"]), text_color="#35C7B4",
                             font=("Segoe UI", 12, "bold")).grid(row=i, column=1, sticky="e", padx=20)
            self.rows.grid_columnconfigure(0, weight=1)
        except Exception as error:
            messagebox.showerror("Database error", str(error))
