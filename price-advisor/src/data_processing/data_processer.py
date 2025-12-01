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