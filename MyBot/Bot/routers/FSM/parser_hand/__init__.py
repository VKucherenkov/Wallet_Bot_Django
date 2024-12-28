from aiogram import Router

from Bot.routers.FSM.parser_hand.parser_hand import router as parser_hand
from Bot.routers.FSM.parser_hand.type_operation_state import router as type_operation_state
from Bot.routers.FSM.parser_hand.recepient_state import router as recepient_state
from Bot.routers.FSM.parser_hand.category_operation_state import router as category_operation_state
from Bot.routers.FSM.parser_hand.bank_card_state import router as bank_card_state
from Bot.routers.FSM.parser_hand.card_user_state import router as card_user_state
from Bot.routers.FSM.parser_hand.operation_user_state import router as operation_user_state
from Bot.routers.FSM.parser_hand.balance_state import router as balance_state

router = Router(name=__name__)
router.include_router(parser_hand)
router.include_router(recepient_state)
router.include_router(type_operation_state)
router.include_router(category_operation_state)
router.include_router(card_user_state)
router.include_router(bank_card_state)
router.include_router(operation_user_state)
router.include_router(balance_state)
