"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm.attributes import QueryableAttribute


class SelectQuery:
    def __init__(self, model, fields):
        self._model = model
        self._from = None
        _fields = []
        self._relations = {field.class_ if isinstance(field, QueryableAttribute) else field for field in fields}
        if model in self._relations:
            self._relations.remove(model)
        for field in fields:
            if isinstance(field, QueryableAttribute):
                _fields.append(getattr(field.class_.__table__.c, field.key))
            elif hasattr(field, '__table__'):
                for f in field.__table__.c:
                    _fields.append(f)
            else:
                _fields.append(field)

        self._stmt = sa.select([model, *self._relations]).with_only_columns(_fields)

    def join(self, right, on):
        if self._from is None:
            self._from = sa.join(self._model, right, on)
        else:
            self._from = self._from.join(right, on)
        return self

    def outerjoin(self, right, on):
        if self._from is None:
            self._from = sa.outerjoin(self._model, right, on)
        else:
            self._from = self._from.outerjoin(right, on)
        return self

    def where(self, condition):
        self._stmt = self._stmt.where(condition)
        return self

    def group_by(self, column):
        self._stmt = self._stmt.group_by(column)
        return self

    def order_by(self, *fields):
        self._stmt = self._stmt.order_by(*fields)
        return self

    def distinct(self, *fields):
        self._stmt = self._stmt.distinct()
        return self

    def limit(self, limit):
        self._stmt = self._stmt.limit(limit)
        return self

    def offset(self, offset):
        self._stmt = self._stmt.offset(offset)
        return self

    def for_update(self):
        self._stmt = self._stmt.with_for_update(nowait=True)
        return self

    async def get(self, conn):
        if self._from is not None:
            self._stmt = self._stmt.select_from(self._from)

        result = await conn.execute(self._stmt)
        result = await result.first()
        return result

    async def exists(self, conn):
        return True if await self.get(conn) else False

    async def all(self, conn):
        if self._from is not None:
            self._stmt = self._stmt.select_from(self._from)

        result = await conn.execute(self._stmt)
        return await result.fetchall()

    def get_query(self):
        if self._from is not None:
            return self._stmt.select_from(self._from)
        return self._stmt

    @property
    def raw_sql(self):
        stmt = self._stmt
        if self._from is not None:
            stmt = stmt.select_from(self._from)
        return stmt.compile(compile_kwargs={'literal_binds': True})

    def _create_model(self, model_class, data):
        model_fields = {
            getattr(field, 'name'): data[str(field)] for field in model_class.__table__.c if str(field) in data
        }
        model = model_class(**model_fields)
        for relation in model_class.__mapper__.relationships:
            if relation.mapper.class_ in self._relations:
                relation_model = self._create_model(relation.mapper.class_, data)
                setattr(model, relation.key, relation_model)

        return model


class StatementQuery:
    def __init__(self, model, stmt):
        self._model = model
        self._stmt = stmt
        self._values = None

    def values(self, **values):
        self._values = self._filter_values(values)
        return self

    def where(self, condition):
        self._stmt = self._stmt.where(condition)
        return self

    def returning(self, *cols):
        self._stmt = self._stmt.returning(*cols)
        return self

    async def execute(self, conn):
        self._values = self._filter_values(self._values)
        if not self._values:
            return
        if hasattr(self._model, 'updated_at'):
            self._values['updated_at'] = datetime.utcnow()
        self._stmt = self._stmt.values(self._values)
        result = await conn.execute(self._stmt)
        return result

    def get_query(self):
        values = self._filter_values(self._values)
        return self._stmt.values(values)

    def _filter_values(self, values):
        return {
            f.key: values[f.key] for f in self._model.__table__.c if f.key in values
        }


class DeleteQuery:
    def __init__(self, model, stmt):
        self._model = model
        self._stmt = stmt

    def where(self, condition):
        self._stmt = self._stmt.where(condition)
        return self

    async def execute(self, conn):
        return await conn.execute(self._stmt)

    def get_query(self):
        return self._stmt


class DB:
    @classmethod
    def select(cls, fields=['*']):
        return SelectQuery(cls, fields)

    @classmethod
    def update(cls):
        return StatementQuery(cls, sa.update(cls))

    @classmethod
    def insert(cls):
        return StatementQuery(cls, sa.insert(cls))

    @classmethod
    def delete(cls):
        return DeleteQuery(cls, sa.delete(cls))

    @staticmethod
    def before_save(data):
        pass

    @staticmethod
    def after_save(data):
        pass

    @classmethod
    def model_fields(cls):
        return list(filter(lambda x: not x.startswith('_'), dir(cls)))
