
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector



def find_class_by_tableName(Base, tableName):
    all_classes = set(
        c for c in Base._decl_class_registry.values()        
        if hasattr(c, '__table__') or hasattr(c, '__view__')
    )   
    for cls in all_classes:             
                mapper = sa.inspect(cls)
                if tableName == mapper.tables[0].name:
                    return cls


def db_connect(username, password, hostname, port, dbname):
    db_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(username, password, hostname, port, dbname)
    engine = create_engine(db_URI)
    return engine


def get_table_names(engine):
    ins = Inspector.from_engine(engine)
    table_names = ins.get_table_names()
    return table_names


def get_column_names(engine, tableName):
    ins = Inspector.from_engine(engine)
    columns = ins.get_columns(tableName)
    column_names = [i['name'] for i in columns]
    return column_names


def get_table_class(engine, tableName):
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    metadata.reflect(engine, views=True)
    Base = automap_base(metadata=metadata)
    Base.prepare()
    found_class = find_class_by_tableName(Base, tableName)
    table_query = session.query(found_class).all()
    return(table_query)


def obj2dic(row):
    return dict([(col, str(getattr(row,col))) for col in row.__table__.columns.keys()])
