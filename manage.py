"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from manager import Manager
from app import server

from settings import *

manager = Manager()


@manager.command
def run():
    server.run(api=True)


@manager.command
def consume():
    server.run(consume=True)


@manager.command
def schedule():
    server.run(schedule=True)


if __name__ == '__main__':
    manager.main()
