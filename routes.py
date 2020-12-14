"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from sanic import Blueprint

from handler.api.v1 import student, timezone
from handler.srv.v1 import health_check as v_srv

srv = Blueprint('srv', url_prefix='/srv/v1')
srv.add_route(v_srv.ping, '/ping', methods=('GET',))

api = Blueprint('api', url_prefix='/api/v1')
api.add_route(student.get_all_students, '/students', methods=('GET',))
api.add_route(student.create_student, '/students', methods=('POST',))
api.add_route(student.get_student_by_id, '/students/<student_id:int>', methods=('GET',))
api.add_route(student.update_student_by_id, '/students/<student_id:int>', methods=('PATCH',))
api.add_route(student.delete_student_by_id, '/students/<student_id:int>', methods=('DELETE',))
api.add_route(timezone.get_timezone, '/timezone', methods=('GET',))
