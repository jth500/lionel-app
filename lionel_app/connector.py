import sqlalchemy as sa
from sqlalchemy import (
    create_engine,
    text,
)


class DBManager:
    def __init__(self, db_path, metadata=None):
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.metadata = metadata
        self.tables = self.metadata.tables

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        if value is None:
            self._metadata = sa.MetaData()
            self._metadata.reflect(bind=self.engine)
        else:
            self._metadata = value

    def delete_rows(self, table_name, season):
        table = self.tables[table_name]
        dele = table.delete().where(table.c.season == season)
        with self.engine.connect() as conn:
            conn.execute(dele)
            conn.commit()

    def query(self, sql_query):
        query = text(sql_query)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            conn.commit()
            return result
