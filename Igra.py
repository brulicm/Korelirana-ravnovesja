import numpy as np
import nashpy as nash
from scipy.optimize import linprog

class Igra:
    def __init__(self, koristnosti_igralec1=None, koristnosti_igralec2=None, n=None, m=None): 
        # Konstruktor razreda za ustvarjanje n*m bimatrične igre

        # koristnosti_igralec1: Matrika koristnosti A za igralca 1. Če ni podana, se ustvari naključna n*m matrika.
        # koristnosti_igralec2: Matrika koristnosti B za igralca 2. Če ni podana, se ustvari naključna n*m matrika.
        # n: število potez, ki jih ima na voljo igralec 1.  Če ni podano, je to naključno celo število med 2 in 5. Če je podan samo n, gre za n*n igro.
        # m: število potez, ki jih ima na voljo igralec 2. Če ni podano, je to naključno celo število med 2 in 5.

        # predpostavimo, da sta matriki A in B ustreznih velikosti in je igra dobro definirana - tega ne preverjamo posebej.
        # predpostavimo, da:
            # ali sta podani obe matriki
            # ali sta podana n in m
            # ali ni podano nič

        if koristnosti_igralec1 is None and koristnosti_igralec2 is None:

            if n is None or m is None:
            # nimamo parametrov, n in m sta naključni števili med 2 in 5
                self.n = np.random.randint(2, 6) #popravi do 6
                self.m = np.random.randint(2, 6) #popravi do 6
            else:
                self.n = n
                self.m = m

            # izplačilni matriki sta naključni matriki velikosti n*m z elementi med 0 in 10
            self.koristnosti_igralec1 = np.random.randint(0, 11, size=(self.n, self.m))
            self.koristnosti_igralec2 = np.random.randint(0, 11, size=(self.n, self.m))

        else:
            self.n, self.m = len(koristnosti_igralec1), len(koristnosti_igralec1[0])
            self.koristnosti_igralec1 = np.array(koristnosti_igralec1)
            self.koristnosti_igralec2 = np.array(koristnosti_igralec2)
      
        self.igra = nash.Game(self.koristnosti_igralec1, self.koristnosti_igralec2)

    def izračunaj_nashevo_ravnovesje(self):
        # izračunamo vsa Nasheva ravnovesja dane igre s pomočjo vgrajenega algoritma Support enumeration
        nasheva_ravnovesja = list(self.igra.vertex_enumeration())

        seznam_NR = []
        n, m = self.n, self.m

        # zapišemo Nasheva ravnovesja v obliki kot bodo zapisana korelirana
        for strategija1, strategija2 in nasheva_ravnovesja:
            NR = np.array([strategija1[i] * strategija2[j] for i in range(n) for j in range(m)])
            seznam_NR.append(NR)

        return tuple(seznam_NR)
    
    def U(self):
        # konstruiramo matriko U, s katero so opisani pogoji za korelirano ravnovesje

        # število možnih stanj: nm
        # število neenakosti za igralca 1: n(n-1)
        # število neenakosti za igralca 2: m(m-1)
        # U je matrika velikosti (n(n-1) + m(m-1)) * nm

        A = self.koristnosti_igralec1
        B = self.koristnosti_igralec2
        n, m = self.n, self.m

        U = np.zeros((n*(n-1) + m*(m-1),n*m))

        vrstica = 0

        # neenakosti za igralca 1:
        for i in range(n):
            for j in [x for x in range(n) if x != i]:
                for s in range(m):
                    U[vrstica, i*m + s] = A[i, s] - A[j, s]
                vrstica +=1
    
        # neenakosti za igralca 2:
        for i in range(m):
            for j in [x for x in range(m) if x != i]:
                for s in range(n):
                    U[vrstica, s*m + i] = B[s, i] - B[s,j]
                vrstica += 1
        return U
 
    def izračunaj_korelirana_ravnovesja(self):
        # z reševanjem treh linearnih programov izračuna 3 korelirana ravnovesja:
            # korelirano ravnovesje, ki maksimizira izplačilo igralca 1
            # korelirano ravnovesje, ki maksimizira izplačilo igralca 2
            # korelirano ravnovesje, ki maksimizira skupno izplačilo

        # pri tem rešimo linearen program:
            # max c x (tu je c ustrezno izbrana vrstica)
            # pri pogojih:
            # Ux >= 0
            # 1x = 1
            # x >= 0

        # za reševanje LP v Pythonu, moramo LP prevesti v naslednjo obliko:
            # min -c x
            # pri pogojih:
            # -Ux <= 0
            # 1x = 1
            # x >= 0

        U = self.U() # konstruiramo matriko U iz definicije
        U_minus = -1*U # preoblikujemo U za LP

        A = self.koristnosti_igralec1
        B = self.koristnosti_igralec2

        n = self.n
        m = self.m

        ##### koeficienti ciljne funkcije
        cA = -1*A.reshape(-1) # če maksimizirano koristnost igralca 1
        cB = -1*B.reshape(-1) # če maksimiziramo koristnost igralca 2
        
        C = A + B
        cC = -1*C.reshape(-1) # če maksimiziramo skupno koristnost

        ##### pogoji
        # desna stran neenakosti -Ux<= 0
        b = np.zeros(n*(n-1) + m*(m-1))

        # 1x = 1
        A_eq = np.ones((1, n*m))
        b_eq = np.array([1])

        # x>= 0
        x_meje = (0, float("inf"))  # x_i >= 0 for all i, x <=1

        ##### LP
        # LP pri katerem maksimiziramo koristnost igralca 1
        rezultatA = linprog(c = cA, A_ub = U_minus, b_ub = b, A_eq = A_eq, b_eq = b_eq, bounds = [x_meje]*n*m)

        # LP pri katerem maksimiziramo koristnost igralca 2
        rezultatB = linprog(c = cB, A_ub = U_minus, b_ub = b, A_eq = A_eq, b_eq = b_eq, bounds = [x_meje]*n*m)

        # LP pri katerem maksimiziramo skupno koristnost
        rezultatC = linprog(c = cC, A_ub = U_minus, b_ub = b, A_eq = A_eq, b_eq = b_eq, bounds = [x_meje]*n*m)

        return rezultatA.x, rezultatB.x, rezultatC.x
    
    def izračunaj_koristnost(self, x, igralec=None):
        # če ne podamo igralca izračuna skupno zadovoljstvo, sicer pa izračuna koristnost danega igralca
        A = self.koristnosti_igralec1
        B = self.koristnosti_igralec2
        C = A + B

        if igralec == 1:
            return np.matmul(A.reshape(-1), x)
        elif igralec == 2:
            return np.matmul(B.reshape(-1), x)
        else:
            return np.matmul(C.reshape(-1), x)
    
    def zapisi_kot_matriko(self,ravnovesje):
        # funkcija, ki zapiše vektor (ravnovesje) kot n*m matriko - za lažje izpisovanje v GUI
        return np.array(ravnovesje).reshape((self.n,self.m))

    def nova_ravnovesja(self):
        # preveri ali smo našli še kakšno korelirano ravnovesje

        CR = self.zapiši_samo_različna_KR()
        NR = self.izračunaj_nashevo_ravnovesje()

        return [ravnovesje for ravnovesje in CR if not any(np.allclose(ravnovesje, nashevo_ravnovesje, atol=1e-10) for nashevo_ravnovesje in NR)]

    def zapiši_samo_različna_KR(self):
        # najdena različna KR 
        
        CR = self.izračunaj_korelirana_ravnovesja()
        CR = [tuple(ravnovesje) for ravnovesje in CR]

        return tuple(set(CR)) 

    def ali_je_nashevo(self, ravnovesje):
        # preveri ali je ravnovesje nashevo 

        return any(np.allclose(ravnovesje, nr,1e-10) for nr in self.izračunaj_nashevo_ravnovesje())
