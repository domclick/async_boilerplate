"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
import settings


def get_app_config():
    return dict(
        connections=[
            dict(
                prefix='example',
                params=dict(
                    host=settings.EXAMPLE_AMQP_HOST,
                    login=settings.EXAMPLE_AMQP_USER,
                    password=settings.EXAMPLE_AMQP_PASS,
                    virtualhost=settings.EXAMPLE_AMQP_VHOST,
                    port=int(settings.EXAMPLE_AMQP_PORT),
                )
            )
        ]
    )
