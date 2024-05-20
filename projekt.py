import numpy as np
import nashpy as nash
import cvxpy as cp

def tau(u1, u2, u3, u4):
    return [u3, u4, u1, u2]

# ravnovesja za coordination games
def ravnovesja(alfa, beta):
    return ([1, 0, 0, 0], 
            [0, 0, 0, 1],
            [1/((1+alfa)*(1+beta)), alfa/((1+alfa)*(1+beta)), beta/((1+alfa)*(1+beta)), alfa*beta/((1+alfa)*(1+beta))],
            [1/(1 + beta + alfa * beta), 0, beta/(1 + beta + alfa * beta), alfa * beta /(1 + beta + alfa * beta)],
            [1/(1 + alfa + alfa * beta), alfa/(1 + alfa + alfa * beta),0, alfa * beta /(1 + alfa + alfa * beta)])

class Igra:
    def __init__(self, koristnosti_igralec1=None, koristnosti_igralec2=None):
        # če pustimo prazno da naključne vrednosti, če vpišemo določimo

        if koristnosti_igralec1 is None:
            self.koristnosti_igralec1 = np.array([[np.random.randint(0, 11), np.random.randint(0, 11)],[np.random.randint(0, 11), np.random.randint(0, 11)]])
        else:
            self.koristnosti_igralec1 = np.array(koristnosti_igralec1)

        if koristnosti_igralec2 is None:
            self.koristnosti_igralec2 = np.array([[np.random.randint(0, 11), np.random.randint(0, 11)],[np.random.randint(0, 11), np.random.randint(0, 11)]])
        else:
            self.koristnosti_igralec2 = np.array(koristnosti_igralec2)

        self.igra = nash.Game(self.koristnosti_igralec1, self.koristnosti_igralec2)

       
    def izračunaj_nashevo_ravnovesje(self):
        eqs = self.igra.vertex_enumeration()
        return list(eqs)
    

    def tip_igre(self):
        # dominirana strategija
        if (self.koristnosti_igralec1[1, 0] >= self.koristnosti_igralec1[0, 0] and self.koristnosti_igralec1[1, 1] >= self.koristnosti_igralec1[0, 1]) or (self.koristnosti_igralec1[0, 0] >= self.koristnosti_igralec1[1, 0] and self.koristnosti_igralec1[0, 1] >= self.koristnosti_igralec1[1, 1]) or (self.koristnosti_igralec2[0, 1] >= self.koristnosti_igralec2[0, 0] and self.koristnosti_igralec2[1, 1] >= self.koristnosti_igralec2[1, 0]) or (self.koristnosti_igralec2[0, 0] >= self.koristnosti_igralec2[0, 1] and self.koristnosti_igralec2[1, 0] >= self.koristnosti_igralec2[1, 1]):
            if (self.koristnosti_igralec1[1, 0] == self.koristnosti_igralec1[0, 0] or self.koristnosti_igralec1[1, 1] == self.koristnosti_igralec1[0, 1]) or (self.koristnosti_igralec1[0, 0] == self.koristnosti_igralec1[1, 0] or self.koristnosti_igralec1[0, 1] == self.koristnosti_igralec1[1, 1]) or (self.koristnosti_igralec2[0, 1] == self.koristnosti_igralec2[0, 0] or self.koristnosti_igralec2[1, 1] == self.koristnosti_igralec2[1, 0]) or (self.koristnosti_igralec2[0, 0] == self.koristnosti_igralec2[0, 1] and self.koristnosti_igralec2[1, 0] == self.koristnosti_igralec2[1, 1]):
                return "šibko dominirana"
            return "strogo dominirana"
        
        ## brez dominirane strategije
        # coordination
        elif self.koristnosti_igralec1[0, 0] > self.koristnosti_igralec1[1, 0] and self.koristnosti_igralec1[1, 1] > self.koristnosti_igralec1[0, 1] and self.koristnosti_igralec2[0, 0] > self.koristnosti_igralec2[0, 1] and self.koristnosti_igralec2[1, 1] > self.koristnosti_igralec2[1, 0]:
            return "coordination"
        # anticoordination
        elif self.koristnosti_igralec1[0, 0] < self.koristnosti_igralec1[1, 0] and self.koristnosti_igralec1[1, 1] < self.koristnosti_igralec1[0, 1] and self.koristnosti_igralec2[0, 0] < self.koristnosti_igralec2[0, 1] and self.koristnosti_igralec2[1, 1] < self.koristnosti_igralec2[1, 0]:
            return "anticoordination"
        # competitive
        else:
            return "competitive"

    def izračunaj_korelirano_ravnovesje(self):
        (a00, a01, a10, a11) = (self.koristnosti_igralec1[0,0], self.koristnosti_igralec1[0,1], self.koristnosti_igralec1[1,0], self.koristnosti_igralec1[1,1])
        (b00, b01, b10, b11) = (self.koristnosti_igralec2[0,0], self.koristnosti_igralec2[0,1], self.koristnosti_igralec2[1,0], self.koristnosti_igralec2[1,1])
        
        # šibko dominirana
        if self.tip_igre == "šibko dominirana":
            return "TBA"
        
        else: 
            alfa = abs(a00 - a10) / abs(a11 - a01)
            beta = abs(b00 - b01) / abs(b11 - b10)

            # cooperation
            if (self.tip_igre() == "competitive" or self.tip_igre() == "strogo dominirana"):
                nasheva = self.izračunaj_nashevo_ravnovesje()
                korelirana = []
                for ravnovesje in nasheva:
                    strategija1 = ravnovesje[0]
                    strategija2 = ravnovesje[1]

                    korelirano_ravnovesje = [strategija1[0] * strategija2[0], strategija1[0] * strategija2[1], strategija1[1] * strategija2[1]]
                    korelirana.append(korelirano_ravnovesje)
                return tuple(korelirana)
            
            # coordination
            elif self.tip_igre() == "coordination":
                return ravnovesja(alfa, beta)
            
            # anticoordination
            if self.tip_igre() == "anticoordination":
                seznam = []
                for ravnovesje in ravnovesja(alfa, 1/beta):
                    seznam.append(tau(*ravnovesje))
            return tuple(seznam)
    

# primer iz wikipedije ok
igra1= Igra([[0,7], [2,6]], [[0,2],[7,6]])
print(igra1.igra)
nashevo_ravnovesje1 = igra1.izračunaj_nashevo_ravnovesje()
print("Nashevo ravnovesje:")
print(nashevo_ravnovesje1)

print("Korelirano ravnovesje:")
korelirano_ravnovesje1 = igra1.izračunaj_korelirano_ravnovesje()
print(korelirano_ravnovesje1)
print("______________________________________________________")

# primer iz članka ok
igra2 = Igra([[4, 1],[5, 0]], [[4,5], [1, 0]])
print(igra2.igra)
nashevo_ravnovesje2 = igra2.izračunaj_nashevo_ravnovesje()
print("Nashevo ravnovesje:")
print(nashevo_ravnovesje2)

print("Korelirano ravnovesje:")
korelirano_ravnovesje2 = igra2.izračunaj_korelirano_ravnovesje()
print(korelirano_ravnovesje2)
print("______________________________________________")

# primer ok
igra3 = Igra([[0, 0], [1, -100]],[[0, 1], [0,-100]])
print(igra3.igra)
nashevo_ravnovesje3 = igra3.izračunaj_nashevo_ravnovesje()
print("Nashevo ravnovesje:")
print(nashevo_ravnovesje3)

print("Korelirano ravnovesje:")
korelirano_ravnovesje3 = igra3.izračunaj_korelirano_ravnovesje()
print(korelirano_ravnovesje3)
print("______________________________________________")

# primer - battle of sexes nevem ce je ok ker ne dobim 1/2, 0 0 1/2
igra4 = Igra([[2, 0],[0, 1]], [[1,0], [0, 2]])
print(igra4.igra)
nashevo_ravnovesje4 = igra4.izračunaj_nashevo_ravnovesje()
print("Nashevo ravnovesje:")
print(nashevo_ravnovesje4)

print("Korelirano ravnovesje:")
korelirano_ravnovesje4 = igra4.izračunaj_korelirano_ravnovesje()
print(korelirano_ravnovesje4)
print("______________________________________________")

# primer - battle of sexes 2 ok
igra5 = Igra([[3, 0],[0, 2]], [[2,0], [0, 3]])
print(igra5.igra)
nashevo_ravnovesje5 = igra5.izračunaj_nashevo_ravnovesje()
print("Nashevo ravnovesje:")
print(nashevo_ravnovesje5)

print("Korelirano ravnovesje:")
korelirano_ravnovesje5 = igra5.izračunaj_korelirano_ravnovesje()
print(korelirano_ravnovesje5)
