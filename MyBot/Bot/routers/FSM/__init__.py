from aiogram import Router
from Bot.routers.FSM.parser_auto import router as parser_auto

router = Router(name=__name__)
router.include_router(parser_auto)