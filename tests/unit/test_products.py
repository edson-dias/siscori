from datetime import date
from src.manipulation.domain.model import Product, Purchase, Keyword


def create_product_and_purchase(
    name="product-01",
    description="white",
    brand="brand-01",
    code="code-01",
    qty=100,
    price=15.43,
    month=6,
    year=date.today().year,
):
    product = Product(name, description, brand, code)
    purchase = Purchase(price, qty, month, year)
    return (product, purchase)


def test_allocating_to_a_product_increases_year_quantity_and_total_amount():
    product, purchase =  create_product_and_purchase()
    product.allocate(purchase)
    assert product.total_quantity == 100
    assert product.total_amount == 1543


def test_allocatig_to_product_increases_year_amount_and_year_quantity():
    product, year_purchase = create_product_and_purchase(qty=20, price=3)
    product.allocate(year_purchase)
    assert product.year_amount == 60
    assert product.year_quantity == 20


def test_allocating_to_a_product_increases_only_totals():
    product, purchase = create_product_and_purchase(qty=10, price=2.5, year=date.today().year - 1)
    product.allocate(purchase)
    assert product.total_quantity == 10
    assert product.total_amount == 25
    assert product.year_amount == 0
    assert product.year_quantity == 0


def test_allocating_different_keywords_to_same_product():
    product, _ = create_product_and_purchase()
    first_keyword = Keyword('apple', 'bannana')
    second_keyword = Keyword('apple')
    product.allocate_keys(first_keyword)
    product.allocate_keys(second_keyword)
    keys = [k for k in product._keywords]
    assert len(product._keywords) == 2
    

def test_allocation_is_idempotent():
    product, purchase = create_product_and_purchase()
    product.allocate(purchase)
    product.allocate(purchase)
    assert product.total_amount == 1543


def test_allocate_keys_is_idempotent():
    product, _ = create_product_and_purchase()
    keys = Keyword('main_keyword', 'seconday_keyword')
    product.allocate_keys(keys)
    product.allocate_keys(keys)
    assert len(product._keywords) == 1
    
