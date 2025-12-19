"""
Modello di regressione lineare per predire correttamente il costo da consigliare all'utente
"""

import numpy as np

class LinearRegressionModel:
    def perform_gradient_descent(self, x: np.ndarray, y: np.ndarray, w_in: float, b_in: float, 
                                 l_r: float, iterations: int):
        """
        Esegue la discesa del gradiente sul modello y = wx + b
        e restituisce i parametri w, b addestrati sul dataset (x, y).
        """
        w = w_in # inizializzazione w
        b = b_in # inizializzazione b

        x = np.asarray(x, dtype=float) # conversione in array np
        y = np.asarray(y, dtype=float)

        for _ in range(iterations):
            dj_dw, dj_db = self.compute_gradient(x, y, w, b)

            w = w - l_r * dj_dw
            b = b - l_r * dj_db
        
        return w, b # parametri per il modello 
        

    def compute_gradient(self, x: np.ndarray, y: np.ndarray, w: float, b: float):
        """
        Calcola il gradiente nel punto della superficie w e b per il dataset x, y
        modello: f_wb = wx + b
        errore quadratico medio: (f_wb - y[i]) ** 2
        derivata parziale della funzione di costo rispetto a w: (wx[i] + b - y[i])x[i]
        derivata parziale della funzione di costo rispetto a b: wx[i] + b - y[i]
        Restituisce i valori del gradiente dj_dw e dj_db nel punto w, b
        """
        m = x.shape[0] # dimensione dataset

        dj_dw = 0.0
        dj_db = 0.0

        for i in range(m):
            f_wb = w * x[i] + b
            dj_dw_i = (f_wb - y[i]) * x[i] # derivata parziale rispetto a w
            dj_db_i = f_wb - y[i] # derivata parziale rispetto a b

            dj_dw += dj_dw_i
            dj_db += dj_db_i

        dj_dw /= m
        dj_db /= m

        return dj_dw, dj_db # gradiente nel punto w, b