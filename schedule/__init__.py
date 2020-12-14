"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from sanic import Sanic
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from schedule.example_schedule import example_schedule


def initialize_scheduler(app: Sanic, loop):
    scheduler = AsyncIOScheduler({
        'event_loop': loop,
        'apscheduler.timezone': 'UTC',
    })

    scheduler.add_job(example_schedule, 'interval', minutes=1, kwargs={'app': app})
    scheduler.add_job(example_schedule, 'cron', hour="*", minute=00, kwargs={'app': app})

    return scheduler
