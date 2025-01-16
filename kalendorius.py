import os
from tkinter import messagebox, ttk
import tkinter as tk
from PIL import Image, ImageTk
import unidecode



class SodinimoKalendorius:
    def __init__(self, kalendorius):
        self.kalendorius = kalendorius
        self.kalendorius.title("SodoRunkelis")
        self.kalendorius.geometry("600x700")
        self.kalendorius.config(bg="#F4F4F9")

        icon_image = Image.open('images/runkelis1.png')
        icon_image = icon_image.resize((64, 64))
        self.kalendorius.iconphoto(True, ImageTk.PhotoImage(icon_image))

        self.darzoves = {
            "": "",
            "Bulvės": {
                "dates": "Balandžio 25 - Gegužės 10 dienomis",
                "info": "Bulvės mėgsta gerai nusausintą dirvą. Užtikrinkite, kad sodinant būtų pakankamai šviesos."
            },
            "Svogūnai": {
                "dates": "Balandžio 15 iki Gegužės 5 dienos",
                "info": "Svogūnai geriausiai auga vėsioje temperatūroje, sodinkite juos anksti pavasarį."
            },
            "Morka": {
                "dates": "Balandžio 25 iki Gegužės 10 dienos",
                "info": "Morkos mėgsta smėlėtą dirvą. Užtikrinkite, kad sodinant būtų pakankamai drėgmės."
            },
            "Agurkai": {
                "dates": "Gegužės 15 iki Gegužės 30 dienos",
                "info": "Agurkai mėgsta šilumą ir daug saulės šviesos. Laikykite dirvą nuolat drėgną."
            },
            "Žirniai": {
                "dates": "Balandžio 1 iki Balandžio 15 dienos",
                "info": "Žirniai auga geriausiai vėsesniu oru. Sodinkite anksti, kad išvengtumėte karščio."
            },
            "Cukinija": {
                "dates": "Gegužės 15 iki Gegužės 30 dienos",
                "info": "Cukinijos mėgsta derlingą dirvą ir šilumą. Užtikrinkite pakankamai vietos augimui."
            }
        }

        self.nuotraukos = {}
        self.create_widget()
        self.reset_screen()

    def load_image(self, augalas):
        try:
            augalo_pavadinimas = unidecode.unidecode(augalas).lower()
            image_path = f"images/{augalo_pavadinimas}.png"

            if os.path.exists(image_path):
                pil_image = Image.open(image_path).resize((400, 300))
                self.nuotraukos[augalas] = ImageTk.PhotoImage(pil_image)
                self.image_label.config(image=self.nuotraukos[augalas])
                self.image_label.image = self.nuotraukos[augalas]
            else:
                self.image_label.config(text="Nuotraukos nera", image="")
                self.image_label.image = None
        except FileNotFoundError:
            self.image_label.config(text="Nuotraukos nera", image="")
            self.image_label.image = None

    def create_widget(self):
        try:
            backround_image = Image.open("images/background.png")
            backround_image = backround_image.resize((650, 650))
            self.bg_photo = ImageTk.PhotoImage(backround_image)
        except FileNotFoundError:
            print("Error: The image file was not found.")
            return

        background_label = tk.Label(self.kalendorius, image=self.bg_photo)
        background_label.place(relwidth=1, relheight=1)

        top_bar = tk.Frame(self.kalendorius, bg="#E0E0E0")
        top_bar.pack(fill=tk.X)

        meniu = tk.Menu(self.kalendorius, tearoff=0)
        self.kalendorius.config(menu=meniu)

        pagrindinis_menu = tk.Menu(meniu, tearoff=0)
        meniu.add_cascade(label="Meniu", menu=pagrindinis_menu)
        pagrindinis_menu.add_command(label="Grįžti į pradžią", command=self.reset_screen)
        pagrindinis_menu.add_separator()
        pagrindinis_menu.add_command(label="Apie", command=self.show_about)
        pagrindinis_menu.add_separator()
        pagrindinis_menu.add_command(label="Išeiti", command=self.kalendorius.quit)

        self.search_entry = tk.Entry(top_bar, font=("Helvetica", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=10, pady=5)

        search_button = tk.Button(top_bar, text="Ieškoti", command=self.search_plant, font=("Helvetica", 10), bg="#4CAF50",
                                  fg="white")
        search_button.pack(side=tk.LEFT, padx=5)

        self.kalendorius.bind('<Return>', self.search_plant_event)

        header_label = tk.Label(self.kalendorius, text="Sodinimo kalendoriaus datos", font=("Helvetica", 18, "bold"),
                                bg="#4CAF50", fg="white")
        header_label.pack(pady=20)

        darzove_label = tk.Label(self.kalendorius, text="Pasirinkite norimą augalą", font=("Helvetica", 12), bg="#4CAF50",
                                 fg="white")
        darzove_label.pack(pady=5)

        self.darzove_var = tk.StringVar(self.kalendorius)
        self.darzove_var.set("")
        darzove_options = list(self.darzoves.keys())

        darzoves_menu = ttk.Combobox(self.kalendorius, textvariable=self.darzove_var, values=darzove_options,
                                     font=("Helvetica", 12))
        darzoves_menu.pack(pady=10)

        self.image_label = tk.Label(self.kalendorius, text="Pamatysi kaip atrodo augalas",
                                    font=("Helvetica", 10, "italic"),
                                    bg="#F4F4F9")
        self.image_label.pack(pady=10)

        self.show_button = tk.Button(self.kalendorius, text="Parodomos sodinimo datos", command=self.show_dates,
                                     font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", relief="raised")
        self.show_button.pack(pady=10)

        self.status_bar = tk.Label(self.kalendorius, text="Sveiki! Pasirinkite augalą.", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Helvetica", 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def search_plant_event(self, event):
        self.search_plant()

    def search_plant(self):
        search_term = self.search_entry.get().strip()
        if search_term:
            search_term = unidecode.unidecode(search_term).lower()
            darzove_found = next((plant for plant in self.darzoves if unidecode.unidecode(plant).lower() == search_term),
                               None)
            if darzove_found:
                self.show_custom_popup(f"Radome augalą: {darzove_found}", f"{self.darzoves[darzove_found]['dates']}\n\nPapildoma informacija:\n{self.darzoves[darzove_found]['info']}")
                self.darzove_var.set(darzove_found)
                self.load_image(darzove_found)
                self.status_bar.config(text=f"Radome: {darzove_found}")
            else:
                self.show_custom_popup("Augalas nerastas", "Pabandykite dar kartą su kitu pavadinimu. Pvz.Morka ")
                self.status_bar.config(text="Augalo nerasta. Pabandykite dar kartą.")
        else:
            self.show_custom_popup("Klaida", "Prašome įvesti augalo pavadinimą.")
            self.status_bar.config(text="Prašome įvesti augalo pavadinimą.")

        self.search_entry.delete(0, tk.END)

    def show_dates(self):
        augalas = self.darzove_var.get()
        augalo_data = self.darzoves.get(augalas, {"dates": "Datos nėra", "info": "Informacija nėra"})
        datos = augalo_data.get("dates", "Datos nėra")
        info = augalo_data.get("info", "Informacija nėra")

        message = f"Geriausia sodinti {augalas}: {datos}\n\nPapildoma informacija:\n{info}"
        self.show_custom_popup(f"Sodinimo datos – {augalas}", message)
        self.load_image(augalas)
        self.status_bar.config(text=f"Parodytos sodinimo datos augalui: {augalas}")

    def show_about(self):
        about_text = (
            "Sodinimo kalendorius naujokui :\n\n"
            "Tai paprasta programa, kuri padeda sužinoti geriausias sodinimo datas "
            "tam tikriems augalams.\nTiesiog pasirinkite augalą iš sąrašo ir sužinosite, "
            "kada geriausia jį pasodinti.\n\nVersija: Beta 0.1\nAutorius: Karolis A."
        )
        messagebox.showinfo("Apie", about_text)
        self.status_bar.config(text="Informacija apie programą.")

    def reset_screen(self):
        self.darzove_var.set("")
        self.image_label.config(image="", text="Pasirinkite augalą ir sužinokite sodinimo datas.")
        self.load_image("pradzia")
        self.status_bar.config(text="Sveiki atyvke! Pradžios puslapis.")

    def show_custom_popup(self, title, message):
        popup = tk.Toplevel(self.kalendorius)
        popup.title(title)

        popup.geometry("400x250")

        window_width = 400
        window_height = 250
        screen_width = self.kalendorius.winfo_screenwidth()
        screen_height = self.kalendorius.winfo_screenheight()

        position_top = (screen_height // 2) - (window_height // 2)
        position_left = (screen_width // 2) - (window_width // 2)

        popup.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

        popup.config(bg="#FFFFFF")

        label = tk.Label(popup, text=message, font=("Helvetica", 12), bg="#FFFFFF", fg="black", wraplength=350, padx=20, pady=20)
        label.pack(fill=tk.BOTH, expand=True)

        close_button = tk.Button(popup, text="Uždaryti", command=popup.destroy, font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="raised")
        close_button.pack(pady=10)


if __name__ == "__main__":
    kalendorius = tk.Tk()
    app = SodinimoKalendorius(kalendorius)
    kalendorius.mainloop()
