from datetime import date
from src.manipulation.domain.model import Importation, Product, Purchase, Keyword


def test_allocate_changes_version_number():
    purchase = Purchase(qty=100, price=15.43, month=6, year=date.today().year)
    importation = Importation('importation-01',
        [
         Product(
             name='importation-01',
             description='white',
             brand='brand-01',
             code='code-01',
             ref=1
             ),
        ]
    )

    original_uuid_generated = importation.version_number
    importation.allocate(purchase, 1)
    assert importation.version_number != original_uuid_generated
    

def test_allocate_purchase_in_second_product():
    purchase = Purchase(qty=10, price=15, month=6, year=date.today().year)
    first_product = Product(
        name='importation-01',
        description='white',
        brand='brand-01',
        code='code-01',
    )

    second_product = Product(
        name='importation-01',
        description='black',
        brand='brand-02',
        code='code-02',
    )

    reference = 'importation-01:brand-02:code-02'
    importation = Importation('importation-01', [first_product, second_product])
    importation.allocate(purchase, reference)

    product = next(p for p in importation.products if p.reference==reference)
    assert product.total_quantity == 10
    assert product.total_amount == 150


def test_returns_allocated_product_reference():
    purchase = Purchase(qty=10, price=15, month=6, year=date.today().year)
    first_product = Product(
        name='importation-01',
        description='white',
        brand='brand-01',
        code='code-01',
    )

    second_product = Product(
        name='importation-01',
        description='black',
        brand='brand-02',
        code='code-02',
    )

    reference = 'importation-01:brand-01:code-01'
    importation = Importation('importation-01', [first_product, second_product])
    allocation =  importation.allocate(purchase, reference)
    assert allocation == first_product.reference


def test_allocate_keywords_if_product_exists():
    first_purchase = Purchase(qty=10, price=15, month=6, year=date.today().year)
    second_purchase = Purchase(qty=10, price=15, month=6, year=date.today().year)

    first_keyword = Keyword('apple', 'bananas')
    second_keyword = Keyword('apple', 'pineapple')
    
    first_product = Product(
        name='importation-01',
        description='white',
        brand='brand-01',
        code='code-01',
        ref=1
    ) 
    importation = Importation('importation-01', [first_product,])
    importation.allocate(first_purchase, 1, first_keyword)
    importation.allocate(second_purchase, 1, second_keyword)
    keywords = [k for k in first_product._keywords]
    
    assert len(keywords) == 2
    
