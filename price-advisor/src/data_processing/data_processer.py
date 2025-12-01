"""
Logica per eseguire conversioni e pulire i dati
"""

import numpy as np

class DataProcesser():
    def to_float(self, text_price: str) -> float:
        """
        Trasforma un prezzo di tipo stringa con indicata la valuta in un valore float
        """
        # slicing per isolare il valore numerico
        price = text_price[4:]
        # conversione in float
        price = float(price.replace(".", "").replace(",", "."))

        return price
    

    def clean_data_from_outliers(self, x: np.ndarray, q_low: float = 25.0, 
                                 q_hi: float = 75.0, k: float = 1.5):
        """
        Rimuove gli outliers dal dataset
        """
        q1 = np.percentile(x, q_low)
        q3 = np.percentile(x, q_hi)
        iqr = q3 - q1

        lower_bound = q1 - k * iqr
        upper_bound = q3 + k * iqr

        mask = (x >= lower_bound) & (x <= upper_bound)

        x_cleaned = x[mask]

        return x_cleaned