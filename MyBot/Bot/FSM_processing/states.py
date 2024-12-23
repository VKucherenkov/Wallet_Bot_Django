from aiogram.fsm.state import StatesGroup, State


class ParserHand(StatesGroup):
    recipient_state = State()
    type_state = State()
    category_state = State()
    bank_state = State()
    card_state = State()
    operation_state = State()