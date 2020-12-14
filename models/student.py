"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime, text

from lib.db_mixin import DB
from . import Base


class Student(Base, DB):
    __tablename__ = 'student'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=True)
    active = Column(Boolean, default=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=text('now()'))
    updated_at = Column(DateTime, default=datetime.utcnow, server_default=text('now()'))

    @classmethod
    async def create(cls, conn, values):
        cur = await Student.insert().values(
            **values
        ).returning(Student.__table__).execute(conn)
        result = await cur.first()
        return dict(result)

    @classmethod
    async def update_by_id(cls, conn, student_id,  values):
        cur = await Student.update().values(
            updated_at=datetime.utcnow(),
            **values
        ).where(
            Student.id == student_id
        ).returning(Student.__table__).execute(conn)
        result = await cur.first()
        return dict(result) if result else None

    @classmethod
    async def get_by_id(cls, conn, student_id):
        result = await Student.select() \
            .where(Student.id == student_id) \
            .get(conn)
        return dict(result) if result else None

    @classmethod
    async def get_all(cls, conn):
        result = await Student.select() \
            .where(Student.active.is_(True)) \
            .all(conn)
        return [dict(i) for i in result]

    @classmethod
    async def set_not_active_by_id(cls, conn, student_id):
        await Student.update().values(active=False) \
            .where(Student.id == student_id) \
            .execute(conn)

    @classmethod
    async def delete_by_id(cls, conn, student_id):
        await Student.delete() \
            .where(Student.id == student_id) \
            .execute(conn)


student_table = Student.__table__
