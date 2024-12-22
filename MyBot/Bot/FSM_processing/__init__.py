from aiogram import Router
from Bot.FSM_processing.parser_hand import router as parser_hand_router


router = Router(name=__name__)
router.include_router(parser_hand_router)

