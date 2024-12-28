from aiogram import Router

from Bot.routers.cards.cards_router import router as cards_router


router = Router(name=__name__)
router.include_router(cards_router)