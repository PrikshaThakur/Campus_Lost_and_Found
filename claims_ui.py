import customtkinter as ctk
from tkinter import messagebox
import database


class ClaimsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Manage Claims", font=("Segoe UI", 28, "bold"),
                     text_color="#F4F7FB").pack(anchor="w", padx=28, pady=(25, 2))
        ctk.CTkLabel(self, text="Review ownership requests and manage decisions",
                     text_color="#8798AF").pack(anchor="w", padx=28)
        form = ctk.CTkFrame(self, fg_color="#162338", corner_radius=14)
        form.pack(fill="x", padx=28, pady=20)
        ctk.CTkLabel(form, text="Submit an ownership claim", font=("Segoe UI", 16, "bold"),
                     text_color="#F4F7FB").grid(row=0, column=0, columnspan=4,
                     sticky="w", padx=18, pady=(15, 8))
        self.entries = {}
        for col, label in enumerate(["Item ID", "Claimant Name", "Contact", "Claim Details"]):
            ctk.CTkLabel(form, text=label, text_color="#A7B6C9").grid(
                row=1, column=col, sticky="w", padx=12)
            entry = ctk.CTkEntry(form, height=36, placeholder_text=label,
                                 fg_color="#0F1A2A", border_color="#31445D")
            entry.grid(row=2, column=col, padx=12, pady=(3, 10), sticky="ew")
            self.entries[label] = entry
            form.grid_columnconfigure(col, weight=1)
        ctk.CTkButton(form, text="＋  Submit claim", command=self.submit,
                      fg_color="#168B7C", hover_color="#117567").grid(
            row=3, column=0, padx=12, pady=(0, 15), sticky="w")
        panel = ctk.CTkFrame(self, fg_color="#162338", corner_radius=14)
        panel.pack(fill="both", expand=True, padx=28, pady=(0, 25))
        bar = ctk.CTkFrame(panel, fg_color="transparent")
        bar.pack(fill="x", padx=18, pady=15)
        ctk.CTkLabel(bar, text="Claim requests", font=("Segoe UI", 16, "bold"),
                     text_color="#F4F7FB").pack(side="left")
        ctk.CTkButton(bar, text="Approve", width=90,
                      command=lambda: self.review("APPROVED"), fg_color="#168B7C").pack(side="right", padx=4)
        ctk.CTkButton(bar, text="Reject", width=80,
                      command=lambda: self.review("REJECTED"), fg_color="#A94B58",
                      hover_color="#873B47").pack(side="right", padx=4)
        self.rows = ctk.CTkScrollableFrame(panel, fg_color="#111C2E", corner_radius=10)
        self.rows.pack(fill="both", expand=True, padx=17, pady=(0, 17))
        self.selected = None
        self.refresh()

    def submit(self):
        values = [entry.get().strip() for entry in self.entries.values()]
        if not all(values):
            messagebox.showwarning("Missing details", "Please complete all claim details.")
            return
        try:
            database.execute_procedure("submit_claim", [int(values[0]), *values[1:]])
            messagebox.showinfo("Submitted", "Ownership claim submitted.")
            for entry in self.entries.values():
                entry.delete(0, "end")
            self.refresh()
        except ValueError:
            messagebox.showerror("Invalid ID", "Item ID must be numeric.")
        except Exception as error:
            messagebox.showerror("Unable to submit", str(error))

    def review(self, decision):
        if self.selected is None:
            messagebox.showwarning("Select a claim", "Select a claim row first.")
            return
        try:
            database.execute_procedure("review_claim", [self.selected, decision])
            self.selected = None
            messagebox.showinfo("Updated", f"Claim {decision.lower()} successfully.")
            self.refresh()
        except Exception as error:
            messagebox.showerror("Unable to update", str(error))

    def refresh(self):
        try:
            for widget in self.rows.winfo_children():
                widget.destroy()
            headers = ["CLAIM", "ITEM", "CLAIMANT", "CONTACT", "STATUS"]
            for col, title in enumerate(headers):
                ctk.CTkLabel(self.rows, text=title, text_color="#7F91A9",
                             font=("Segoe UI", 9, "bold")).grid(
                    row=0, column=col, padx=10, pady=12, sticky="w")
            rows = database.fetch_all("SELECT claim_id, item_id, claimant_name, "
                "contact, claim_status FROM item_claims ORDER BY claim_id DESC")
            keys = ["claim_id", "item_id", "claimant_name", "contact", "claim_status"]
            for i, row in enumerate(rows, 1):
                for col, key in enumerate(keys):
                    label = ctk.CTkLabel(self.rows, text=str(row[key]), text_color="#E0E8F2",
                                         cursor="hand2")
                    label.grid(row=i, column=col, padx=10, pady=10, sticky="w")
                    label.bind("<Button-1>", lambda event, cid=row["claim_id"]: self.select_claim(cid))
            for col in range(5):
                self.rows.grid_columnconfigure(col, weight=1)
        except Exception as error:
            messagebox.showerror("Database error", str(error))

    def select_claim(self, claim_id):
        self.selected = claim_id
