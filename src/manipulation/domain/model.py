from uuid import uuid4
from datetime import date
from dataclasses import dataclass


class Importation:
    def __init__(self, name, products, version_number=uuid4().hex):
        self.name = name
        self.products = products
        self.version_number = version_number

    def allocate(self, purchase, product_ref, keyword=None):
        product = next(p for p in self.products if p.reference==product_ref)
        product.allocate(purchase)

        if keyword:
            product.allocate_keys(keyword)
            
        self.version_number = uuid4().hex
        return product.reference
    

@dataclass(unsafe_hash=True)
class Purchase:
    price: float
    qty: int
    month: int
    year: int
    siscori_description: str = None


@dataclass(unsafe_hash=True)
class Keyword:
    main_key: str
    secondary_key: str = None


class Product:
    def __init__(self, name, description, brand, code, image=None, ref=None):
        if ref:
            reference = ref
        else:
            reference = f'{name}:{brand}:{code}'

        self.name = name
        self.description = description
        self.brand = brand
        self.code = code
        self.image = image
        self.reference = reference
        self._keywords = set()
        self._allocations = set()

    def __str__(self):
        return f'{self.name}: {self.brand}'

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def allocate(self, purchase):
        self._allocations.add(purchase)

    def allocate_keys(self, keyword):
        self._keywords.add(keyword)

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

