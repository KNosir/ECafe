from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# db_url = 'postgresql://username:password@host:port/dbname'
# db_url = 'postgresql://eovqbhzz:OnGBM6Eza9hK6X2u2KGFeCAfmrIMsrM_@kesavan.db.elephantsql.com:5432/eovqbhzz'

db_url = 'sqlite:///data.db'
# создание машины соединения
engine = create_engine(db_url, echo=False)