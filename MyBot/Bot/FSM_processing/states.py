from aiogram.fsm.state import StatesGroup, State


class ParserHand(StatesGroup):
    recipient_state = State()
    type_state = State()
    category_state = State()
    card_number_state = State()
    card_name_state = State()
    bank_state = State()
    operation_state = State()
    balance_state = State()


class ParserAuto(StatesGroup):
    start_state = State()
    card_name_state = State()
    card_type_state = State()
    card_credit_state = State()
    bank_state_auto = State()
    recipient_state = State()
    type_state_auto = State()
    category_state_auto = State()
    resume_state = State()

