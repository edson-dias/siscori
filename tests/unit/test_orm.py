from src.manipulation.domain import model


def test_purchase_mapper_can_load_purchases(session):
    session.execute(
        """
       INSERT INTO purchases (price, qty, month, year, siscori_description)
       VALUES (1.56, 10, 3, 2021, 'first description') 
"""
    )
    expected = model.Purchase(1.56, 10, 3, 2021, "first description")
    assert session.query(model.Purchase).first() == expected


def test_purchase_mapper_can_save_purchases(session):
    purchase = model.Purchase(2.5, 20, 6, 2022, "description")
    session.add(purchase)
    session.commit()

    purchases_db = list(
        session.execute(
            'SELECT  price, qty, month, year, siscori_description FROM "purchases"'
        )
    )
    assert purchases_db == [(2.5, 20, 6, 2022, "description")]


def test_keyword_mapper_can_load_keywords(session):
    session.execute(
        """INSERT INTO keywords (main_key)
VALUES ('primary_keyword')
"""
    )
    expected = model.Keyword("primary_keyword")
    assert session.query(model.Keyword).first() == expected


def test_keyword_mapper_can_save_kewords(session):
    first_key = model.Keyword("first_main_keyword", "first_secondary_keyword")
    second_key = model.Keyword("second_main_keyword")

    session.add(first_key)
    session.add(second_key)
    session.commit()

    keywords_db = list(session.execute("SELECT main_key, secondary_key FROM keywords"))
    assert keywords_db == [
        ("first_main_keyword", "first_secondary_keyword"),
        ("second_main_keyword", None),
    ]


def test_product_mapper_can_load_products(session):
    session.execute(
        """
       INSERT INTO products (name, description, brand, code, reference)
       VALUES ('Air Jordan', '4 - White', 'Nike', 'MJ-24', 'Air Jordan:Nike:MJ-24') 
"""
    )
    expected = model.Product("Air Jordan", "4 - White", "Nike", "MJ-24")
    assert session.query(model.Product).first() == expected


def test_product_mapper_can_save_products(session):
    product = model.Product("Air Jordan", "4 - White", "Nike", "MJ-24")
    session.add(product)
    session.commit()
    products_db = list(
        session.execute("SELECT name, description, brand, code FROM products")
    )

    assert products_db == [("Air Jordan", "4 - White", "Nike", "MJ-24")]


def test_saving_allocations(session):
    key = model.Keyword("main_keyword", "secondary_keyword")
    purchase = model.Purchase(2.5, 20, 6, 2022, "description")
    product = model.Product("Air Jordan", "4 - White", "Nike", "MJ-24")
    product.allocate(purchase)
    session.add(product)
    session.commit()
    allocations_db = list(
        session.execute("""SELECT purchases_id, product_id FROM allocations""")
    )
    assert allocations_db == [(purchase.id, product.id)]


def test_saving_keys_allocations(session):
    key = model.Keyword("main_keyword", "secondary_keyword")
    product = model.Product("Air Jordan", "4 - White", "Nike", "MJ-24")
    product.allocate_keys(key)
    session.add(product)
    session.commit()
    keywords_db = list(
        session.execute("""SELECT keywords_id, product_id FROM siscori_keywords""")
    )
    assert keywords_db == [(key.id, product.id)]


def test_importation_mapper_can_save_importations(session):
    product = model.Product('Air Jordan', '4 - White', 'Nike', 'MJ-24')
    importation = model.Importation('Air Jordan', [product])
    version_number = importation.version_number
    session.add(importation)
    session.commit()
    importations_db = list(
        session.execute(
    """
SELECT i.name, i.version_number, p.name, p.description, p.brand, p.code FROM importations AS i
JOIN products as p ON i.name = p.name
""")
    )

    assert importations_db == [('Air Jordan', version_number,'Air Jordan', '4 - White', 'Nike', 'MJ-24')]

