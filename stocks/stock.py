
class Stock:
    Symbol: str
    Name: str
    LowPrice: int
    HighPrice: int
    Date: str
    def __init__(self, sym: str, name: str, low: str, hi: str, date: str = ''):
        self.Symbol = sym
        self.Name = name
        self.LowPrice = int(low)
        self.HighPrice = int(hi)
        self.Date = date

    def __repr__(self):
        return f"{self.Symbol} [{self.LowPrice},{self.HighPrice}]"