from dataclasses import dataclass
from datetime import date


class Importation:
    def __init__(self, products):
        self.products = products

    def allocate(self, purchase):
        pass
    

@dataclass(unsafe_hash=True)
class Purchase:
    price: float
    qty: int
    month: int
    year: int


@dataclass(unsafe_hash=True)
class Keyword:
    main_key: str
    secondary_key: str


class Product:
    def __init__(self, name, description, brand, code, image=None):
        self.name = name
        self.description = description
        self.brand = brand
        self.code = code
        self.image = image
        self._keywords = set()
        self._allocations = set()

    def allocate(self, purchase):
        self._allocations.add(purchase)

    @property
    def total_amount(self):
        return sum(purchase.price * purchase.qty for purchase in self._allocations)

    @property
    def total_quantity(self):
        return sum(purchase.qty for purchase in self._allocations)

    @property
    def year_amount(self):
        return sum(
            purchase.price * purchase.qty
            for purchase in self._allocations
            if purchase.year == date.today().year
        )

    @property
    def year_quantity(self):
        return sum(
            purchase.qty
            for purchase in self._allocations
            if purchase.year == date.today().year
        )
