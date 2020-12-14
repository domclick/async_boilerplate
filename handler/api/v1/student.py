"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from sanic.request import Request
from sanic_openapi import doc

from lib.request import validate_json
from lib.swagger import open_api_schemas
from models import Student
from schemas.student import CreateStudentSchema, UpdateStudentSchema, StudentResultSchema
from lib.shortcuts.view import http_created, http_ok, http_bad_request, http_empty


@doc.summary('Создание записи "Студент"')
@doc.consumes(open_api_schemas(CreateStudentSchema()), location='body')
@doc.produces(open_api_schemas(StudentResultSchema()))
@validate_json(CreateStudentSchema)
async def create_student(request: Request):
    data = request['validated_json']

    async with request.app.db_engine.acquire() as conn:
        result = await Student.create(conn=conn, values=data)
    return http_created(StudentResultSchema().dump(result))


@doc.summary('Получение записи "Студент" по id')
@doc.produces(open_api_schemas(StudentResultSchema()))
async def get_student_by_id(request: Request, student_id):
    async with request.app.db_engine.acquire() as conn:
        result = await Student.get_by_id(conn=conn, student_id=student_id)
    if not result:
        return http_bad_request('student not found')
    return http_ok(StudentResultSchema().dump(result))


@doc.summary('Получение списка студентов')
@doc.produces(open_api_schemas(StudentResultSchema(many=True)))
async def get_all_students(request: Request):
    async with request.app.db_engine.acquire() as conn:
        result = await Student.get_all(conn=conn)
    return http_ok(StudentResultSchema().dump(result, many=True))


@doc.summary('Обновление записи "Студент"')
@doc.consumes(open_api_schemas(UpdateStudentSchema()), location='body')
@doc.produces(open_api_schemas(StudentResultSchema()))
@validate_json(UpdateStudentSchema)
async def update_student_by_id(request: Request, student_id):
    data = request['validated_json']

    async with request.app.db_engine.acquire() as conn:
        result = await Student.update_by_id(conn=conn, student_id=student_id, values=data)
    if not result:
        return http_bad_request('student not found')
    return http_ok(StudentResultSchema().dump(result))


@doc.summary('Удаление записи "Студент"')
async def delete_student_by_id(request: Request, student_id):
    async with request.app.db_engine.acquire() as conn:
        await Student.set_not_active_by_id(conn=conn, student_id=student_id)
    return http_empty()
