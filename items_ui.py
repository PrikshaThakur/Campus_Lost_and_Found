import customtkinter as ctk
from tkinter import messagebox
import database


class ItemsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Manage Items", font=("Segoe UI", 28, "bold"),
                     text_color="#F4F7FB").pack(anchor="w", padx=28, pady=(25, 2))
        ctk.CTkLabel(self, text="Register and find lost or found belongings",
                     text_color="#8798AF").pack(anchor="w", padx=28)
        form = ctk.CTkFrame(self, fg_color="#162338", corner_radius=14)
        form.pack(fill="x", padx=28, pady=20)
        ctk.CTkLabel(form, text="New item report", font=("Segoe UI", 16, "bold"),
                     text_color="#F4F7FB").grid(row=0, column=0, columnspan=3,
                     sticky="w", padx=18, pady=(15, 8))
        self.fields = {}
        labels = ["Item Name", "Category", "Description", "Location", "Reporter", "Contact"]
        for i, label in enumerate(labels):
            row, col = divmod(i, 3)
            ctk.CTkLabel(form, text=label, text_color="#A7B6C9").grid(
                row=row * 2 + 1, column=col, sticky="w", padx=18, pady=(7, 2))
            entry = ctk.CTkEntry(form, height=36, placeholder_text=label,
                                 fg_color="#0F1A2A", border_color="#31445D")
            entry.grid(row=row * 2 + 2, column=col, sticky="ew", padx=18, pady=(0, 5))
            self.fields[label] = entry
            form.grid_columnconfigure(col, weight=1)
        self.kind = ctk.StringVar(value="LOST")
        ctk.CTkOptionMenu(form, variable=self.kind, values=["LOST", "FOUND"],
                          width=130, fg_color="#245B68").grid(
            row=6, column=0, padx=18, pady=15, sticky="w")
        ctk.CTkButton(form, text="＋  Save item report", command=self.add_item,
                      fg_color="#168B7C", hover_color="#117567").grid(
            row=6, column=1, padx=18, pady=15, sticky="w")
        panel = ctk.CTkFrame(self, fg_color="#162338", corner_radius=14)
        panel.pack(fill="both", expand=True, padx=28, pady=(0, 25))
        bar = ctk.CTkFrame(panel, fg_color="transparent")
        bar.pack(fill="x", padx=17, pady=15)
        ctk.CTkLabel(bar, text="Item directory", font=("Segoe UI", 16, "bold"),
                     text_color="#F4F7FB").pack(side="left")
        self.search = ctk.CTkEntry(bar, width=220, placeholder_text="Search name or category")
        self.search.pack(side="right", padx=(8, 0))
        ctk.CTkButton(bar, text="Search", width=75, command=self.refresh).pack(side="right")
        self.rows = ctk.CTkScrollableFrame(panel, fg_color="#111C2E", corner_radius=10)
        self.rows.pack(fill="both", expand=True, padx=17, pady=(0, 17))
        self.refresh()

    def add_item(self):
        names = ["Item Name", "Category", "Description", "Location", "Reporter", "Contact"]
        values = [self.fields[name].get().strip() for name in names]
        if not all(values):
            messagebox.showwarning("Missing details", "Please complete all fields.")
            return
        try:
            database.execute_procedure("add_item", [self.kind.get()] + values)
            messagebox.showinfo("Saved", "Item report registered successfully.")
            for entry in self.fields.values():
                entry.delete(0, "end")
            self.refresh()
        except Exception as error:
            messagebox.showerror("Unable to save", str(error))

    def refresh(self):
        try:
            for widget in self.rows.winfo_children():
                widget.destroy()
            headers = ["ID", "TYPE", "ITEM", "CATEGORY", "LOCATION", "STATUS"]
            for col, title in enumerate(headers):
                ctk.CTkLabel(self.rows, text=title, text_color="#7F91A9",
                             font=("Segoe UI", 9, "bold")).grid(
                    row=0, column=col, padx=8, pady=12, sticky="w")
            word = f"%{self.search.get().strip()}%"
            rows = database.fetch_all("SELECT item_id, item_type, item_name, category, "
                "location_found, item_status FROM items WHERE LOWER(item_name) LIKE LOWER(:word) "
                "OR LOWER(category) LIKE LOWER(:word) ORDER BY item_id DESC", {"word": word})
            keys = ["item_id", "item_type", "item_name", "category", "location_found", "item_status"]
            for i, row in enumerate(rows, 1):
                for col, key in enumerate(keys):
                    ctk.CTkLabel(self.rows, text=str(row[key]), text_color="#E0E8F2").grid(
                        row=i, column=col, padx=8, pady=9, sticky="w")
            for col in range(6):
                self.rows.grid_columnconfigure(col, weight=1)
        except Exception as error:
            messagebox.showerror("Database error", str(error))
