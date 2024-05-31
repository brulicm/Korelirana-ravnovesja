# lepši izpis bimatrike izplačil
import tkinter as tk
from Igra import Igra
from tkinter import ttk
from tkinter import messagebox

class GUI:
    def __init__(self):
        self.okno = tk.Tk()
        self.okno.title("KORELIRANA RAVNOVESJA")

        # Velikost okna 
        self.okno.geometry("400x300")

        # Naslov
        self.naslov = tk.Label(self.okno, text="KORELIRANA RAVNOVESJA", font=("Helvetica", 16))
        self.naslov.place(relx=0.5, rely=0.2, anchor="center")

        # Gumbi
        button_width = 20
        self.ustvari_nakljucno_igro_gumb = tk.Button(self.okno, text="Ustvari naključno igro", command=self.ustvari_nakljucno_igro, width=button_width)
        self.ustvari_nakljucno_igro_gumb.place(relx=0.5, rely=0.4, anchor="center")

        self.vnesi_izplacilni_matriki_gumb = tk.Button(self.okno, text="Vnesi izplačilni matriki", command=lambda: self.odpri_izbiro_velikosti("vnesi matrike"), width=button_width)
        self.vnesi_izplacilni_matriki_gumb.place(relx=0.5, rely=0.55, anchor="center")

        self.izberi_velikost_gumb = tk.Button(self.okno, text="Izberi velikost", command=lambda: self.odpri_izbiro_velikosti("izberi samo velikost"), width=button_width)
        self.izberi_velikost_gumb.place(relx=0.5, rely=0.7, anchor="center")

        self.n = None
        self.m = None
        self.izbrana_akcija = None  # Flag to remember which button was pressed

        self.okno.mainloop()

    def odpri_izbiro_velikosti(self, akcija):
        self.izbrana_akcija = akcija

        self.vnesi_izplacilni_matriki_okno = tk.Toplevel()
        self.vnesi_izplacilni_matriki_okno.title("Izberi velikost")

        tk.Label(self.vnesi_izplacilni_matriki_okno, text="Izberi n:").grid(row=0, column=0, padx=10, pady=10)
        self.n_dropdown = ttk.Combobox(self.vnesi_izplacilni_matriki_okno, values=[2, 3, 4, 5])
        self.n_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.n_dropdown.current(0) 

        tk.Label(self.vnesi_izplacilni_matriki_okno, text="Izberi m:").grid(row=1, column=0, padx=10, pady=10)
        self.m_dropdown = ttk.Combobox(self.vnesi_izplacilni_matriki_okno, values=[2, 3, 4, 5])
        self.m_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.m_dropdown.current(0) 

        if akcija == "vnesi matrike":
            confirm_button = tk.Button(self.vnesi_izplacilni_matriki_okno, text="Vnesi matriki", command=self.vnesi_nm_matrike)
        else:
            confirm_button = tk.Button(self.vnesi_izplacilni_matriki_okno, text="Ustvari igro", command=self.preberi_nm)

        confirm_button.grid(row=2, column=0, columnspan=2, pady=20)
        self.vnesi_izplacilni_matriki_okno.mainloop()

    def ustvari_nakljucno_igro(self):
    # koda ob pritisku na gumb USTVARI NAKLJUČNO IGRO
    
        self.igra = Igra(n=self.n, m=self.m)

        koristnosti_igralec1 = self.igra.koristnosti_igralec1
        koristnosti_igralec2 = self.igra.koristnosti_igralec2

        # Ustvari novo okno za prikaz izplačilnih matrik
        self.okno_izplacilne_matrike = tk.Toplevel()
        self.okno_izplacilne_matrike.title("Izplačilne matrike")
        self.okno_izplacilne_matrike.geometry("900x900")
    
        # Text above matrix A
        tk.Label(self.okno_izplacilne_matrike, text="Izplačilna matrika", font=("Helvetica", 12)).grid(row=0, columnspan=len(koristnosti_igralec1[0])+3)

        # Prikazi izplačilne matrike v novem oknu
        for i in range(len(koristnosti_igralec1)):
            for j in range(len(koristnosti_igralec1[0])):
                tk.Label(self.okno_izplacilne_matrike, text=str(koristnosti_igralec1[i][j]) + str(" , ") + str(koristnosti_igralec2[i][j]), borderwidth=1, relief="solid", width=12, height=5).grid(row=i+1, column=j)
                
    
        # Dodaj gumb izračunaj ravnovesja
        self.izracunaj_ravnovesja_gumb = tk.Button(self.okno_izplacilne_matrike, text="Izračunaj ravnovesja", command=self.izracunaj_ravnovesja, width=20)
        self.izracunaj_ravnovesja_gumb.grid(row=len(koristnosti_igralec1) + len(koristnosti_igralec2) + 4, column=0, columnspan=len(koristnosti_igralec1[0])+3)

        self.okno_izplacilne_matrike.mainloop()

    def izracunaj_ravnovesja(self):
        # izračuna Nasheva ravnovesja in korelirana ravnovesja igre. 
        # izpiše vsa Nasheva ravnovesja in izračuna koristnosti
        # izpiše najdena korelirana ravnovesja, ki niso Nasheva in koristnosti

        # Nasheva ravnovesja:
        nasheva_ravnovesja = self.igra.izračunaj_nashevo_ravnovesje()
    
        # Korelirana ravnovesja:
        vsa_najdena_KR = self.igra.zapiši_samo_različna_KR()

        # Korelirana ravnovesja, ki niso Nasheva:
        nova_korelirana_ravnovesja = self.igra.nova_ravnovesja()
    
        # Okno za rezutate
        self.okno_rezultati = tk.Toplevel()
        self.okno_rezultati.title("Rezultati ravnovesij")
        self.okno_rezultati.geometry("900x700")

        main_frame = tk.Frame(self.okno_rezultati)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add title for Nasheva ravnovesja
        tk.Label(main_frame, text="Nasheva ravnovesja", font=("Helvetica", 14)).grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        for i, ravnovesje in enumerate(nasheva_ravnovesja):
            NR = self.igra.zapisi_kot_matriko(ravnovesje)
        
            # Frame for each equilibrium
            equilibrium_frame = tk.Frame(main_frame, borderwidth=1, relief="ridge")
            equilibrium_frame.grid(row=i+1, column=0, padx=10, pady=10, sticky="nsew")
        
            # Left inner frame for the matrix
            left_inner_frame = tk.Frame(equilibrium_frame, relief="solid")
            left_inner_frame.grid(row=0, column=0, padx=5, pady=5)
        
            for r in range(self.igra.n):
                for c in range(self.igra.m):
                    tk.Label(left_inner_frame, text=str(abs(round(NR[r][c], 2))), borderwidth=1, relief="solid", width=10, height=3).grid(row=r, column=c)
        
            # Right inner frame for the utilities
            right_inner_frame = tk.Frame(equilibrium_frame, relief="solid")
            right_inner_frame.grid(row=0, column=1, padx=5, pady=5)
        
            utility1 = self.igra.izračunaj_koristnost(ravnovesje, igralec=1)
            utility2 = self.igra.izračunaj_koristnost(ravnovesje, igralec=2)
            utility_sk = self.igra.izračunaj_koristnost(ravnovesje)

            tk.Label(right_inner_frame, text=f"Koristnost igralca 1: {round(utility1,2)}", font=("Helvetica", 12)).pack(pady=10)
            tk.Label(right_inner_frame, text=f"Koristnost igralca 2: {round(utility2,2)}", font=("Helvetica", 12)).pack(pady=10)
            tk.Label(right_inner_frame, text=f"Skupno zadovoljstvo: {round(utility_sk,2)}", font=("Helvetica", 12)).pack(pady=10)

        # Add title for Korelirana ravnovesja
        tk.Label(main_frame, text="Korelirana ravnovesja", font=("Helvetica", 14)).grid(row=len(nasheva_ravnovesja)+1, column=0, padx=5, pady=5, columnspan=2)

        if nova_korelirana_ravnovesja == []:
            tk.Label(main_frame, text=f"Našli smo samo Nasheva ravnovesja: {vsa_najdena_KR}", font=("Helvetica", 14)).grid(row=len(nasheva_ravnovesja)+2, column=0, padx=5, pady=5, columnspan=2)
        else:
            tk.Label(main_frame, text=f"Poleg Nashevih ravnovesij: {vsa_najdena_KR}, smo našli še: {nova_korelirana_ravnovesja}", font=("Helvetica", 14)).grid(row=len(nasheva_ravnovesja)+2, column=0, padx=5, pady=5, columnspan=2)

        for i, ravnovesje in enumerate(nova_korelirana_ravnovesja):
            CR = self.igra.zapisi_kot_matriko(ravnovesje)

            # Frame for each equilibrium
            equilibrium_frame = tk.Frame(main_frame, borderwidth=1, relief="ridge")
            equilibrium_frame.grid(row=len(nasheva_ravnovesja)+i+3, column=0, padx=10, pady=10, sticky="nsew")
        
            # Left inner frame for the matrix
            left_inner_frame = tk.Frame(equilibrium_frame, borderwidth=1, relief="solid")
            left_inner_frame.grid(row=0, column=0, padx=5, pady=5)
        
            for r in range(self.igra.n):
                for c in range(self.igra.m):
                    tk.Label(left_inner_frame, text=str(round(CR[r][c], 2)), borderwidth=1, relief="solid", width=10, height=3).grid(row=r, column=c)
        
            # Right inner frame for the utilities
            right_inner_frame = tk.Frame(equilibrium_frame, borderwidth=1, relief="solid")
            right_inner_frame.grid(row=0, column=1, padx=5, pady=5)
        
            utility1 = self.igra.izračunaj_koristnost(ravnovesje, igralec=1)
            utility2 = self.igra.izračunaj_koristnost(ravnovesje, igralec=2)
            utility_sk = self.igra.izračunaj_koristnost(ravnovesje)
            tk.Label(right_inner_frame, text=f"Koristnost igralca 1: {round(utility1,2)}", font=("Helvetica", 12)).pack(pady=10)
            tk.Label(right_inner_frame, text=f"Koristnost igralca 2: {round(utility2,2)}", font=("Helvetica", 12)).pack(pady=10)
            tk.Label(right_inner_frame, text=f"Skupno zadovoljstvo: {round(utility_sk,2)}", font=("Helvetica", 12)).pack(pady=10)

        self.okno_rezultati.mainloop()

    def preberi_matrike(self):
        # Koda za izracunaj ravnovesja gumb po vnosu vrednosti v matrike
        koristnosti_igralec1 = []
        koristnosti_igralec2 = []

        for i in range(len(self.koristnosti_igralec1_entry)):
            koristnosti_1_vrstica = []
            koristnosti_2_vrstica = []
            for j in range(len(self.koristnosti_igralec1_entry[0])):
                vnos1 = self.koristnosti_igralec1_entry[i][j].get()
                vnos2 = self.koristnosti_igralec2_entry[i][j].get()
                if not vnos1 or not vnos2:
                    messagebox.showerror("Napaka", "Vsa polja morajo biti izpolnjena!")
                    return
                koristnosti_1_vrstica.append(int(self.koristnosti_igralec1_entry[i][j].get()))
                koristnosti_2_vrstica.append(int(self.koristnosti_igralec2_entry[i][j].get()))
            koristnosti_igralec1.append(koristnosti_1_vrstica)
            koristnosti_igralec2.append(koristnosti_2_vrstica)
        
        self.igra = Igra(koristnosti_igralec1, koristnosti_igralec2)
        self.izracunaj_ravnovesja()

    def vnesi_nm_matrike(self):
        # Koda za potrditev izbire v dropdown menijih
        selected_n = int(self.n_dropdown.get()) 
        selected_m = int(self.m_dropdown.get())


        # Ustvari novo okno za vnos matrik
        self.vnesi_matriki_okno = tk.Toplevel()
        self.vnesi_matriki_okno.title("Vnesi matriki")

        # Dodaj mrežo za koristnosti igralca 1
        tk.Label(self.vnesi_matriki_okno, text="Koristnosti igralec 1:").grid(row=0, column=0, padx=10, pady=10)
        self.koristnosti_igralec1_entry = [[None] * selected_m for _ in range(selected_n)]
        for i in range(selected_n):
            for j in range(selected_m):
                self.koristnosti_igralec1_entry[i][j] = tk.Entry(self.vnesi_matriki_okno, width=10)
                self.koristnosti_igralec1_entry[i][j].grid(row=i+1, column=j, padx=5, pady=5)

        # Dodaj mrežo za koristnosti igralca 2
        tk.Label(self.vnesi_matriki_okno, text="Koristnosti igralec 2:").grid(row=selected_n+1, column=0, padx=10, pady=10)
        self.koristnosti_igralec2_entry = [[None] * selected_m for _ in range(selected_n)]
        for i in range(selected_n):
            for j in range(selected_m):
                self.koristnosti_igralec2_entry[i][j] = tk.Entry(self.vnesi_matriki_okno, width=10)
                self.koristnosti_igralec2_entry[i][j].grid(row=i+selected_n+2, column=j, padx=5, pady=5)

        # Dodaj gumb za potrditev vnosov
        confirm_button = tk.Button(self.vnesi_matriki_okno, text="Izračunaj ravnovesja", command=self.preberi_matrike)
        confirm_button.grid(row=2*selected_n+2, column=0, columnspan=selected_m, pady=20)

        self.vnesi_matriki_okno.mainloop()  

    def preberi_nm(self):
          # Koda za potrditev izbire v dropdown menijih
        self.n = int(self.n_dropdown.get()) 
        self.m = int(self.m_dropdown.get())

        # Zapri trenutno okno
        self.igra = Igra(n = self.n, m = self.m)
        self.ustvari_nakljucno_igro()


if __name__ == "__main__":
    gui = GUI()