import tkinter as tk
from Igra import Igra
from tkinter import ttk
from tkinter import messagebox

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.current_frame = None
        self.root.title("Korelirana ravnovesja")

        self.glavni_meni()
        
        self.root.mainloop()

    def centriraj_okno(self, sirina, visina):
        # centrira okno na zaslonu in spremeni dimenzije sirina x visina
        zaslon_sirina = self.root.winfo_screenwidth()
        zaslon_visina = self.root.winfo_screenheight()

        # pozicija okna
        x = (zaslon_sirina // 2) - (sirina // 2)
        y = (zaslon_visina // 2) - (visina // 2)

        # nastavimo novo okno
        self.root.geometry(f"{sirina}x{visina}+{x}+{y}")


    def glavni_meni(self):
        # prikaže glavni meni

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.centriraj_okno(600, 280)
        self.root.resizable(False, False)

        # naslov
        title_frame = tk.Frame(self.current_frame)
        title_frame.pack(fill=tk.X, pady=(20,5))
        tk.Label(title_frame, text="KORELIRANA RAVNOVESJA", font=("Helvetica", 40), fg = "grey10").pack()

        # levi okvir z opisom programa
        left_frame = tk.Frame(self.current_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)

        opis1 = ("Obravnavamo Nasheva in korelirana ravnovesja bimatričnih iger. Izračunamo tudi koristnosti igralcev v poiskanih ravnovesjih.")
        tk.Label(left_frame, text=opis1, wraplength=300,justify="center", font=("Helvetica", 14)).pack(pady=5)
        opis2 = ("Lahko ustvarite povsem naključno bimatrično igro, lahko določite velikost naključne igre, lahko pa tudi vnesete izplačilni matriki.")
        tk.Label(left_frame, text=opis2, wraplength=300, justify="center", font=("Helvetica", 14)).pack(pady=5) 

        # desni okvir z gumbi
        right_frame = tk.Frame(self.current_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Button(right_frame, text="Ustvari naključno igro", command=self.nakljucna_igra, width=20).pack(pady=(5,10))
        tk.Button(right_frame, text="Vnesi izplačilni matriki", command=lambda: self.odpri_izbiro_velikosti("vnesi matrike"), width=20).pack(pady=10)
        tk.Button(right_frame, text="Izberi velikost", command=lambda: self.odpri_izbiro_velikosti("izberi samo velikost"), width=20, bg="blue").pack(pady=10)

    def nakljucna_igra(self, n = None, m = None):
        # prikaže izplačilno matriko naključno ustvarjene igre (ob pritisku na gumb "Ustvari naključno igro" ali pa ob izbiri velikosti)

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.igra = Igra(n = n,m = m)

        koristnosti_igralec1 = self.igra.koristnosti_igralec1
        koristnosti_igralec2 = self.igra.koristnosti_igralec2

        # velikost okna:
        width = max(self.igra.m * 120 + 40,600)
        height = max(self.igra.n * 100 + 100,280)
        self.centriraj_okno(width, height)

        # matrika:
        matrix_frame = tk.Frame(self.current_frame)
        matrix_frame.pack(expand=True)

        tk.Label(matrix_frame, text="Izplačilna matrika:", font=("Helvetica", 15)).grid(row=0, columnspan=self.igra.m + 3, pady = 10)

        for i in range(self.igra.n):
            for j in range(self.igra.m):
                tk.Label(matrix_frame, text=f"{koristnosti_igralec1[i][j]}, {koristnosti_igralec2[i][j]}", borderwidth=1, relief="solid", width=12, height=5).grid(row=i+1, column=j)

        # gumb:
        self.izracunaj_ravnovesja_gumb = tk.Button(matrix_frame, text="Izračunaj ravnovesja", command=self.izracunaj_ravnovesja, width=20)
        self.izracunaj_ravnovesja_gumb.grid(row=self.igra.n + 2, column=0, columnspan=self.igra.m, pady=10)

    def odpri_izbiro_velikosti(self, akcija):
        # okvir za izbiro velikost - odpre se ob pritisku na gumb "Vnesi matriki" ali pa ob pritisku na gumb "Izberi velikost"

        self.izbrana_akcija = akcija

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        self.centriraj_okno(600,280)

        tk.Label(self.current_frame, text="Izberi n:").pack(pady=(20, 5))
        self.n_dropdown = ttk.Combobox(self.current_frame, values=[2, 3, 4, 5])
        self.n_dropdown.pack()
        self.n_dropdown.current(0) 

        tk.Label(self.current_frame, text="Izberi m:").pack(pady=(20, 5))
        self.m_dropdown = ttk.Combobox(self.current_frame, values=[2, 3, 4, 5])
        self.m_dropdown.pack()
        self.m_dropdown.current(0) 

        if akcija == "vnesi matrike":
            confirm_button = tk.Button(self.current_frame, text="Vnesi matriki", command=self.vnesi_nm_matrike)
        else:
            confirm_button = tk.Button(self.current_frame, text="Ustvari igro", command=self.preberi_nm)

        confirm_button.pack(padx = 45, pady = 20)
    def preberi_nm(self):
        # se sproži ob izbiri n in m v drsnem meniju
        n = int(self.n_dropdown.get()) 
        m = int(self.m_dropdown.get())

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.nakljucna_igra(n,m)

    def vnesi_nm_matrike(self):
        # za vnos n x m izplačilnih matrik

        selected_n = int(self.n_dropdown.get())
        selected_m = int(self.m_dropdown.get())
        
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # velikost okna
        width = max(selected_m * 50 + 160,600) 
        height = max(selected_n * 50 + 250,280) 
        self.centriraj_okno(width, height)

        # okvir za igralca 1
        frame_label_1 = tk.Frame(self.current_frame)
        frame_label_1.pack(pady=5)
        tk.Label(frame_label_1, text="Vnesi izplačilno matriko za igralca 1:").pack(side=tk.LEFT, padx=10)

        # polja za izplačila igralca 1
        frame_entries_1 = tk.Frame(self.current_frame)
        frame_entries_1.pack(padx = 10, pady=10)
        self.koristnosti_igralec1_entry = [[tk.Entry(frame_entries_1, width=5) for _ in range(selected_m)] for _ in range(selected_n)]
        for i in range(selected_n):
            for j in range(selected_m):
                self.koristnosti_igralec1_entry[i][j].grid(row=i, column=j, padx=2, pady=2)

        # okvir za igralca 2
        frame_label_2 = tk.Frame(self.current_frame)
        frame_label_2.pack(pady=10)
        tk.Label(frame_label_2, text="Vnesi izplačilno matriko za igralca 2:").pack(side=tk.LEFT, padx=10)

        # polja za izplačila igralca 2
        frame_entries_2 = tk.Frame(self.current_frame)
        frame_entries_2.pack(padx = 10, pady=10)
        self.koristnosti_igralec2_entry = [[tk.Entry(frame_entries_2, width=5) for _ in range(selected_m)] for _ in range(selected_n)]
        for i in range(selected_n):
            for j in range(selected_m):
                self.koristnosti_igralec2_entry[i][j].grid(row=i, column=j, padx=2, pady=2)

        # gumb
        confirm_button = tk.Button(self.current_frame, text="Izračunaj ravnovesja", command=self.preberi_matrike, width = 20)
        confirm_button.pack(padx = 20, pady=20)

    def preberi_matrike(self):
        # se sproži ob pritisku na gumb "izačunaj ravnovesje", ko vnesemo izplačilne matrike

        koristnosti_igralec1 = []
        koristnosti_igralec2 = []

        for i in range(len(self.koristnosti_igralec1_entry)):
            koristnosti_1_vrstica = []
            koristnosti_2_vrstica = []
            for j in range(len(self.koristnosti_igralec1_entry[0])):
                vnos1 = self.koristnosti_igralec1_entry[i][j].get()
                vnos2 = self.koristnosti_igralec2_entry[i][j].get()
                if not vnos1 or not vnos2 or not vnos1.isdigit() or not vnos2.isdigit():
                    messagebox.showerror("Napaka", "Vsa polja morajo biti izpolnjena s celimi števili!") 
                    return
                koristnosti_1_vrstica.append(int(self.koristnosti_igralec1_entry[i][j].get()))
                koristnosti_2_vrstica.append(int(self.koristnosti_igralec2_entry[i][j].get()))
            koristnosti_igralec1.append(koristnosti_1_vrstica)
            koristnosti_igralec2.append(koristnosti_2_vrstica)
        
        self.igra = Igra(koristnosti_igralec1, koristnosti_igralec2)
        self.izracunaj_ravnovesja()

    def izracunaj_ravnovesja(self):
        # izračuna in izpiše ravnovesja

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        self.root.resizable(True, True)

        # Nasheva ravnovesja:
        nasheva_ravnovesja = self.igra.izračunaj_nashevo_ravnovesje()

        # Korelirana ravnovesja, ki niso Nasheva:
        nova_korelirana_ravnovesja = self.igra.nova_ravnovesja()

        # Create a canvas to contain the Nasheva ravnovesja with a scrollbar
        nasheva_canvas = tk.Canvas(self.current_frame)
        nasheva_canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar for the Nasheva ravnovesja canvas
        nasheva_scrollbar = tk.Scrollbar(self.current_frame, orient="vertical", command=nasheva_canvas.yview)
        nasheva_scrollbar.pack(side="right", fill="y")

        nasheva_canvas.configure(yscrollcommand=nasheva_scrollbar.set)
        nasheva_canvas.bind('<Configure>', lambda e: nasheva_canvas.configure(scrollregion=nasheva_canvas.bbox("all")))

        # Create a frame to hold the Nasheva ravnovesja content
        nasheva_frame = tk.Frame(nasheva_canvas)
        nasheva_canvas.create_window((0, 0), window=nasheva_frame, anchor="nw")

        korelirana_frame = tk.Frame(self.current_frame)
        korelirana_frame.pack(side="left",expand=True, fill = "both")

        # Add title for Nasheva ravnovesja
        tk.Label(nasheva_frame, text="Nasheva ravnovesja", font=("Helvetica", 16)).grid(row=0, column=0, padx=5, pady=(10,5), columnspan=2)

        for i, ravnovesje in enumerate(nasheva_ravnovesja):
            NR = self.igra.zapisi_kot_matriko(ravnovesje)
            
            # Frame for each equilibrium
            equilibrium_frame = tk.Frame(nasheva_frame, borderwidth=1, relief="ridge")
            equilibrium_frame.grid(row=i+1, column=0, padx=10, pady=10, sticky="nsew")
            
            # Left inner frame for the matrix
            left_inner_frame = tk.Frame(equilibrium_frame, borderwidth=1, relief="solid")
            left_inner_frame.grid(row=0, column=0, padx=5, pady=5)
            
            for r in range(self.igra.n):
                for c in range(self.igra.m):
                    tk.Label(left_inner_frame, text=str(abs(round(NR[r][c], 2))), borderwidth=1, relief="solid", width=5, height=2).grid(row=r, column=c)
            
            # Right inner frame for the utilities
            right_inner_frame = tk.Frame(equilibrium_frame, relief="solid")
            right_inner_frame.grid(row=0, column=1, padx=5, pady=5)
            
            utility1 = self.igra.izračunaj_koristnost(ravnovesje, igralec=1)
            utility2 = self.igra.izračunaj_koristnost(ravnovesje, igralec=2)
            utility_sk = self.igra.izračunaj_koristnost(ravnovesje)
            tk.Label(right_inner_frame, text=f"Koristnost igralca 1: {round(utility1,2)}", font=("Helvetica", 12)).pack(pady=2)
            tk.Label(right_inner_frame, text=f"Koristnost igralca 2: {round(utility2,2)}", font=("Helvetica", 12)).pack(pady=2)
            tk.Label(right_inner_frame, text=f"Skupno zadovoljstvo: {round(utility_sk,2)}", font=("Helvetica", 12)).pack(pady=2)

        # Configure the scrollbar to work with the canvas
        nasheva_canvas.bind_all("<MouseWheel>", lambda e: nasheva_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Add title for Korelirana ravnovesja
        tk.Label(korelirana_frame, text="Korelirana ravnovesja", font=("Helvetica", 16)).grid(row=0, column=0, padx=5, pady=(10,5), columnspan=2)

        if not nova_korelirana_ravnovesja:
            tk.Label(korelirana_frame, text=f"Najdena so bila samo Nasheva ravnovesja", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        else:
            tk.Label(korelirana_frame, text=f"Poleg Nashevih ravnovesij smo našli še:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        for i, ravnovesje in enumerate(nova_korelirana_ravnovesja):
            CR = self.igra.zapisi_kot_matriko(ravnovesje)

            # Frame for each equilibrium
            equilibrium_frame = tk.Frame(korelirana_frame, borderwidth=1, relief="ridge")
            equilibrium_frame.grid(row=i+2, column=0, padx=10, pady=10, sticky="nsew")
            
            # Left inner frame for the matrix
            left_inner_frame = tk.Frame(equilibrium_frame, borderwidth=1, relief="solid")
            left_inner_frame.grid(row=0, column=0, padx=5, pady=5)
            
            for r in range(self.igra.n):
                for c in range(self.igra.m):
                    tk.Label(left_inner_frame, text=str(abs(round(CR[r][c], 2))), borderwidth=1, relief="solid", width=5, height=2).grid(row=r, column=c)
            
            # Right inner frame for the utilities
            right_inner_frame = tk.Frame(equilibrium_frame, relief="solid")
            right_inner_frame.grid(row=0, column=1, padx=5, pady=5)
            
            utility1 = self.igra.izračunaj_koristnost(ravnovesje, igralec=1)
            utility2 = self.igra.izračunaj_koristnost(ravnovesje, igralec=2)
            utility_sk = self.igra.izračunaj_koristnost(ravnovesje)
            tk.Label(right_inner_frame, text=f"Koristnost igralca 1: {round(utility1,2)}", font=("Helvetica", 12)).pack(pady=2)
            tk.Label(right_inner_frame, text=f"Koristnost igralca 2: {round(utility2,2)}", font=("Helvetica", 12)).pack(pady=2)
            tk.Label(right_inner_frame, text=f"Skupno zadovoljstvo: {round(utility_sk,2)}", font=("Helvetica", 12)).pack(pady=2)

        KR_button = tk.Button(korelirana_frame, text="Več informacij", command=self.show_more_KR, width=20)
        KR_button.grid(row = len(nova_korelirana_ravnovesja) + 3, column = 0, columnspan = 2)

        # Add a button to go back to the main menu
        back_to_menu_button = tk.Button(self.current_frame, text="Nazaj na začetek", command=self.glavni_meni, width=20)
        back_to_menu_button.pack(side="bottom")

        self.root.state('zoomed')

    def show_more_KR(self):
        # več info o KR
        
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
   
        korelirana_ravnovesja = self.igra.izračunaj_korelirana_ravnovesja()

        # Title
        tk.Label(self.current_frame, text="Najdena so bila naslednja korelirana ravnovesja:", pady=10).pack()

        for i, ravnovesje in enumerate(korelirana_ravnovesja):
            CR = self.igra.zapisi_kot_matriko(ravnovesje)

            # Frame for each equilibrium
            equilibrium_frame = tk.Frame(self.current_frame, borderwidth=1, relief="ridge", pady=10)
            equilibrium_frame.pack(pady=10)

            if i == 0:
                tk.Label(equilibrium_frame, text="Korelirano ravnovesje, ki maksimizira korist igralca 1:", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
            elif i == 1:
                tk.Label(equilibrium_frame, text="Korelirano ravnovesje, ki maksimizira korist igralca 2:", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
            else:
                tk.Label(equilibrium_frame, text="Korelirano ravnovesje, ki maksimizira skupno korist:  ", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            # Left inner frame for the matrix
            left_inner_frame = tk.Frame(equilibrium_frame, borderwidth=1, relief="solid")
            left_inner_frame.grid(row=1, column=0, padx=2, pady=2)

            for r in range(self.igra.n):
                for c in range(self.igra.m):
                    tk.Label(left_inner_frame, text=str(abs(round(CR[r][c], 2))), borderwidth=1, relief="solid", width=6, height=2).grid(row=r, column=c)

            # Right inner frame for the utilities
            right_inner_frame = tk.Frame(equilibrium_frame, relief="solid")
            right_inner_frame.grid(row=1, column=1, padx=10, pady=5)

            utility1 = self.igra.izračunaj_koristnost(ravnovesje, igralec=1)
            utility2 = self.igra.izračunaj_koristnost(ravnovesje, igralec=2)
            utility_sk = self.igra.izračunaj_koristnost(ravnovesje)
            tk.Label(right_inner_frame, text=f"Koristnost igralca 1: {round(utility1, 2)}", font=("Helvetica", 12)).pack(pady=2)
            tk.Label(right_inner_frame, text=f"Koristnost igralca 2: {round(utility2, 2)}", font=("Helvetica", 12)).pack(pady=2)
            tk.Label(right_inner_frame, text=f"Skupno zadovoljstvo: {round(utility_sk, 2)}", font=("Helvetica", 12)).pack(pady=2)

            if self.igra.ali_je_nashevo(ravnovesje):
                tk.Label(right_inner_frame, text="To je Nashevo ravnovesje.", font=("Helvetica", 12)).pack(pady=2)
            else:
                tk.Label(right_inner_frame, text="To ni Nashevo ravnovesje", font=("Helvetica", 12)).pack(pady=2)

        # Add a button to go back to the main menu
        back_to_menu_button = tk.Button(self.current_frame, text="Nazaj na začetek", command=self.glavni_meni, width=20)
        back_to_menu_button.pack(pady=(10,5))

        back = tk.Button(self.current_frame, text="Nazaj", command=self.izracunaj_ravnovesja, width=20)
        back.pack(pady=(5,10))
    
if __name__ == "__main__":
    gui = GUI()