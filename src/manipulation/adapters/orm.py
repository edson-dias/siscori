from sqlalchemy import Table, MetaData, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import registry, relationship

from ..domain import model

registry = registry()
metadata = registry.metadata

purchase_table = Table(
    'purchases',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('price', Float),
    Column('qty', Integer),
    Column('month', Integer),
    Column('year', Integer),
    Column('siscori_description', String)
)
    
keyword_table = Table(
    'keywords',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('main_key', String),
    Column('secondary_key', String, nullable=True)
)

product_table = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', ForeignKey('importations.name')),
    Column('description', String),
    Column('brand', String),
    Column('code', String),
    Column('image', String, nullable=True),
    Column('reference', String)
)

allocation_table = Table(
    'allocations',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('purchases_id', ForeignKey('purchases.id')),
    Column('product_id', ForeignKey('products.id')),
)

siscori_keyword_table = Table(
    'siscori_keywords',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('keywords_id', ForeignKey('keywords.id')),
    Column('product_id', ForeignKey('products.id')),    
)

importation_table = Table(
    'importations',
    metadata,
    Column('name', String, primary_key=True),
    Column('version_number', String),
)

def start_mappers():
    purchases_mapper = registry.map_imperatively(model.Purchase, purchase_table)
    keywords_mapper = registry.map_imperatively(model.Keyword, keyword_table)
    product_mapper = registry.map_imperatively(
        model.Product,
        product_table,
        properties={
            '_allocations': relationship(purchases_mapper, secondary=allocation_table, collection_class=set),
            '_keywords': relationship(keywords_mapper, secondary=siscori_keyword_table, collection_class=set)
        },
    )
    registry.map_imperatively(
        model.Importation,
        importation_table,
        properties={'products': relationship(product_mapper)}
    )
    
