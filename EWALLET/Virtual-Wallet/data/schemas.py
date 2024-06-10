import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, constr, conint, Field, validator
from datetime import datetime, date


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    phone_number: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
    created_at: datetime


class UserLogin(BaseModel):
    email: str
    password: str


class UpdateAmount(BaseModel):
    amount: float


class AmountOut(BaseModel):
    message: str
    old_balance: float
    new_balance: float


class AccountBalanceOut(BaseModel):
    balance: float


class DepositAmount(BaseModel):
    deposit_amount: float


class WithdrawMoney(BaseModel):
    withdraw_sum: float


class CreateTransaction(BaseModel):
    receiver_id: int
    amount: float
    category: str


class ConfirmOrDecline(BaseModel):
    confirm_or_decline: str


CardType = Annotated[str, Field(regex=r'^(credit|debit)$')]
ExpirationDate = Annotated[str, Field(regex=r'^(0[1-9]|1[0-2])\/[0-9]{2}$')]
CardNumber = Annotated[str, Field(min_length=16, max_length=16, regex=r'^\d{16}$')]
CVV = Annotated[str, Field(regex=r'^\d{3}$')]


class CardBase(BaseModel):
    type: CardType
    expiration_date: ExpirationDate
    cvv: CVV
    number: CardNumber

    @validator('expiration_date')
    def validate_expiration_date(cls, v):
        if not re.match(r'^(0[1-9]|1[0-2])/[0-9]{2}$', v):
            raise ValueError('Invalid expiration date format. It should be MM/YY')
        return v


class CardCreate(CardBase):
    pass


class CardUpdate(BaseModel):
    type: CardType = None
    expiration_date: ExpirationDate = None
    cvv: CVV = None
    number: CardNumber = None


class Card(CardBase):
    id: int
    user_id: int


class AcceptTransaction(BaseModel):
    acceptation: str


class UpdateProfile(BaseModel):
    password: str
    email: str
    phone_number: str
