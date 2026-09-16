import os
import sqlalchemy as _sql
import sqlalchemy.orm as _orm


#DATABASE_URL = "postgresql://ADMIN:2371@localhost:5432/testdb" #url for sqldb
#     #postgresql:// - database type
#     #ADMIN:2371  - username nd password
#     #@localhost:5432 - host addr
#     #/testdb - db name


DATABASE_URL = os.getenv(
    "DATABASE_URL"
    #"postgresql://ADMIN:2371@localhost:5432/testdb"   # fallback for local development
)

engine = _sql.create_engine(DATABASE_URL)
SessionLocal = _orm.sessionmaker(autocommit = False,autoflush=False,bind=engine)
Base = _orm.declarative_base()