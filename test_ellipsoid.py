import numpy as np

def steady_distribution(P):
    # potrebujemo lastni vektor ki pripada lastni vrednosti 1 transponirane matrike P
    lastne_vrednosti, lastni_vektorji = np.linalg.eig(P.T)

    indeks = np.argmin(np.abs(lastne_vrednosti - 1.0))
    steady_state_distribution = np.real(lastni_vektorji[:,indeks])
    steady_state_distribution /= np.sum(steady_state_distribution)
    return steady_state_distribution

P =  np.array([[0.5, 0.5],
                              [0.4, 0.6]])

print(steady_distribution(P))