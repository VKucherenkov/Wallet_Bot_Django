from aiogram import Router

from Bot.routers.commands.base_commands import router as base_commands

router = Router(name=__name__)

router.include_router(base_commands)