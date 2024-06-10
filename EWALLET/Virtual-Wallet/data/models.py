from pydantic import BaseModel
from datetime import datetime, date


class Transaction(BaseModel):
    id: int
    created_at: datetime
    amount: float
    status: str
    category: str

    @classmethod
    def from_query_result(cls, id, created_at, amount, status, category):
        return cls(
            id=id,
            created_at=created_at,
            amount=amount,
            status=status,
            category=category)


class User(BaseModel):
    id: int
    username: str
    password: str
    email: str
    phone_number: str
    created_at: datetime

    @classmethod
    def from_query_result(cls, id: int, username: str, password: str, email: str, phone_number: str,
                          created_at: datetime):
        return cls(
            id=id,
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            created_at=created_at

        )


class Card(BaseModel):
    id: int
    user_id: int
    type: str
    expiration_date: str
    cvv: int
    number: str

    @classmethod
    def from_query_result(cls, id: int, user_id: int, type: str, expiration_date: str, cvv: int, number: str):
        return cls(
            id=id,
            user_id=user_id,
            type=type,
            expiration_date=expiration_date,
            cvv=cvv,
            number=number
        )