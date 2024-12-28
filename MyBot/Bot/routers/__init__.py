__all__ = ('router',)

from aiogram import Router

from Bot.routers.cards import router as cards_router
from Bot.routers.commands import router as command_router
from Bot.routers.last import echo_router
from Bot.routers.FSM import router as fsm_router

router = Router(name=__name__)

router.include_router(command_router)
router.include_router(cards_router)
router.include_router(fsm_router)

'''echo_router подключается последним'''
router.include_router(echo_router)