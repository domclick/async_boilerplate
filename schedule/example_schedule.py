"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from sanic.log import logger

from models.student import Student


async def example_schedule(app):
    logger.info('start example_schedule')
    async with app.db_engine.acquire() as conn:
        all_students = await Student.get_all(conn=conn)
        for s in all_students:
            await Student().update_by_id(
                conn=conn,
                student_id=s['id'],
                values={
                    'name': s['name'] + '_new'
                }
            )
    logger.info('end example_schedule')
