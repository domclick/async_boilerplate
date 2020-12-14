"""
Copyright Ⓒ 2020 "Sberbank Real Estate Center" Limited Liability Company. Licensed under the MIT license.
Please, see the LICENSE.md file in project's root for full licensing information.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from models.student import *
