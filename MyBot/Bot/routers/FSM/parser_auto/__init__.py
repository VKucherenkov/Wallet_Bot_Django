from aiogram import Router

from Bot.routers.FSM.parser_auto.parser_auto import router as parser_auto
from Bot.routers.FSM.parser_auto.card_state_auto import router as card_state_auto

router = Router(name=__name__)
router.include_router(parser_auto)
router.include_router(card_state_auto)