import customtkinter as ctk
from tkinter import messagebox
from items_ui import ItemsPage
from claims_ui import ClaimsPage
from reports_ui import ReportsPage


class LostFoundApp:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        root.title("Campus Lost & Found")
        root.geometry("1320x820")
        root.minsize(1100, 700)
        root.configure(fg_color="#0B1220")
        side = ctk.CTkFrame(root, width=235, corner_radius=0, fg_color="#111C2E")
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        ctk.CTkLabel(side, text="CAMPUS", font=("Segoe UI", 25, "bold"),
                     text_color="#F4F7FB").pack(anchor="w", padx=25, pady=(35, 0))
        ctk.CTkLabel(side, text="LOST & FOUND", font=("Segoe UI", 15, "bold"),
                     text_color="#35C7B4").pack(anchor="w", padx=25)
        ctk.CTkLabel(side, text="STUDENT SERVICES", font=("Segoe UI", 9, "bold"),
                     text_color="#71839D").pack(anchor="w", padx=25, pady=(7, 38))
        ctk.CTkLabel(side, text="WORKSPACE", text_color="#71839D",
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25, pady=(0, 12))
        self.nav = {}
        pages = [("⌂   Dashboard", ReportsPage), ("▣   Manage Items", ItemsPage),
                 ("◇   Manage Claims", ClaimsPage), ("▤   Reports", ReportsPage)]
        for label, page in pages:
            btn = ctk.CTkButton(side, text=label, anchor="w", height=46,
                corner_radius=10, fg_color="transparent", hover_color="#24364F",
                text_color="#C7D2E2", font=("Segoe UI", 12, "bold"),
                command=lambda p=page, n=label: self.show_page(p, n))
            btn.pack(fill="x", padx=13, pady=4)
            self.nav[label] = btn
        ctk.CTkFrame(side, height=1, fg_color="#29384D").pack(fill="x", padx=20, pady=25)
        ctk.CTkLabel(side, text="MCA • DATABASE PROJECT", text_color="#71839D",
                     font=("Segoe UI", 9)).pack(side="bottom", pady=22)
        main = ctk.CTkFrame(root, fg_color="#0B1220", corner_radius=0)
        main.pack(side="right", fill="both", expand=True)
        top = ctk.CTkFrame(main, height=62, corner_radius=0, fg_color="#111C2E")
        top.pack(fill="x")
        top.pack_propagate(False)
        ctk.CTkLabel(top, text="Campus Services   /   Lost & Found",
                     text_color="#91A2B9").pack(side="left", padx=28)
        ctk.CTkLabel(top, text="●  SYSTEM ONLINE", text_color="#35C7A4",
                     font=("Segoe UI", 10, "bold")).pack(side="right", padx=28)
        self.content = ctk.CTkFrame(main, fg_color="#0B1220", corner_radius=0)
        self.content.pack(fill="both", expand=True)
        self.show_page(ReportsPage, "⌂   Dashboard")

    def show_page(self, page, active):
        for widget in self.content.winfo_children():
            widget.destroy()
        for name, button in self.nav.items():
            button.configure(fg_color="#1C344E" if name == active else "transparent",
                             text_color="white" if name == active else "#C7D2E2")
        try:
            page(self.content).pack(fill="both", expand=True)
        except Exception as error:
            messagebox.showerror("Application error", str(error))


if __name__ == "__main__":
    root = ctk.CTk()
    LostFoundApp(root)
    root.mainloop()
