import numpy as np

def ellipsoid_against_hope_2x2(a, b):
    # konstruira U
    U = U(a, b)
    
    # požene algoritem
    return ellipsoid_against_hope(U)

def U(a, b):
    # konstruiramo matriko U iz definicije koreliranega ravnovesja
    U = np.zeros((4, 4))
    U[0, 0] = a[0, 0] - a[1, 0]
    U[0, 1] = -a[0, 1] + a[1, 1]
    U[1, 2] = -a[0, 0] + a[1, 0]
    U[1, 3] = a[0, 1] - a[1, 1]
    U[2, 0] = b[0, 0] - b[0, 1]
    U[2, 2] = -b[1, 0] + b[1, 1]
    U[3, 1] = -b[0, 0] + b[0, 1]
    U[3, 3] = b[1, 0] - b[1, 1]
    return U


def steady_distribution(P):
    # vrne steady distribution pri predhodni matriki P
    # potrebujemo lastni vektor ki pripada lastni vrednosti 1 transponirane matrike P
    lastne_vrednosti, lastni_vektorji = np.linalg.eig(P.T)

    indeks = np.argmin(np.abs(lastne_vrednosti - 1.0)) # poišče lastno vrednost najbližjo 1 (če slučajno ni 1)
    steady_state_distribution = np.real(lastni_vektorji[:, indeks])
    steady_state_distribution /= np.sum(steady_state_distribution)
    return steady_state_distribution

def lema(y):
    # pri danem y vrne x tako da je xU^T y = 0 -> konstrukcija iz leme
    # za I1:
    # prvi stolpec y - a je za prvega igralca
    y1 = y[:,0] # prvi stolpec

    # če je vsota prve vrstice = 0
    if y1[0] + y1[1] == 0: 
        x1 = np.array([1, 0])

    # če je vsota druge vrstice = 0
    elif y1[2] + y1[3] == 0:
        x1 = np.array([0,1])
    
    else:
        # normaliziramo y
        y1 = y1 / np.sum(y1, axis=1, keepdims=True)

        # prehodna matrika za I1
        P1 = np.array([[y1[0], y1[1]],[y1[2], y1[3]]]) 

        # poiščemo steady distribution
        x1 = steady_distribution(P1)
    
    # za I2:
    # drugi stolpec y - a je za drugega igralca
    y2 = y[:,1] # drugi stolpec

    # če je vsota prve vrstice = 0
    if y2[0] + y2[1] == 0: 
        x2 = np.array([1, 0])

    # če je vsota druge vrstice = 0
    elif y2[2] + y2[3] == 0:
        x2 = np.array([0,1])
    
    else:
        # normaliziramo y
        y2 = y2 / np.sum(y2, axis=1, keepdims=True)

        # prehodna matrika za I1
        P2 = np.array([[y2[0], y2[1]],[y2[2], y2[3]]]) 

        # poiščemo steady distribution
        x2 = steady_distribution(P2)

    x = np.array([x1[0] * x2[0], x1[0] * x2[1], x1[1] * x2[0], x1[1] * x2[1]])
    return x

def ellipsoid_against_hope(U):
    # algoritem

    # Parametri
    N = 8 # št. spremenljivk duala 
    u = np.max(np.abs(U)) # koeficient v U z največjo absolutno vrednostjo 
    L = 10 # št. korakov (zaenkrat naj bo tako....)

    # Začetni elipsoid
    center = np.zeros((4, 2))
    radius = u^N # kot v članku

    # Inicializacija
    k = 0
    x_i = []

    # k - ti korak
    while k < L:
        if all(np.matmul(U.T, center.T)<=-1):
            # če center ustreza neenakosti, ga vrnemo
            return center
        else:
            # če center ne ustreza neenakosti:

            # dodamo x v seznam x-ov
            x_i.append(lema(center))

            ############################################################################################
            # neenakost (x_i U^T) y <= -1 ni izpolnjena, saj je enaka 0
            # uporabimo novo neenakost x_i U^T y <= -1 da ustvarimo nov ellipsoid
            # kako?

            k += 1
            # zanka se ponovi........

    # ko se zanka konča - naredimo L korakov
    return x_i

