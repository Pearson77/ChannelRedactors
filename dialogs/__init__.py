from aiogram import Router
from .statistics import router as stats_router
from .start_dialog import router as start_router
from .channels_management import channel_add, channel_delete
from .redactors_management import redactors_add, redactors_delete, redacrots_edit

routers: list[Router] = [
    start_router,
    stats_router,
    channel_add.router,
    channel_delete.router,
    redacrots_edit.router,
    redactors_add.router,
    redactors_delete.router,
]

