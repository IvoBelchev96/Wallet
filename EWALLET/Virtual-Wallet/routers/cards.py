from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from data.schemas import Card, CardCreate, CardUpdate
from services import cards_services
from common.authorization import get_current_user

router = APIRouter()

@router.post("/", response_model=Card, status_code=status.HTTP_201_CREATED)
def create_card(card: CardCreate, user_id: int = Depends(get_current_user)):
    card_data = card.dict()
    card_data["user_id"] = user_id
    try:
        created_card = cards_services.create_card(card_data)
        return created_card
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[Card])
def read_cards(user_id: int = Depends(get_current_user)):
    try:
        return cards_services.get_all_cards()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{card_id}", response_model=Card)
def read_card(card_id: int, user_id: int = Depends(get_current_user)):
    try:
        card = cards_services.get_card_by_id(card_id)
        if not card:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
        return card
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{card_id}", response_model=Card)
def update_card(card_id: int, card: CardUpdate, user_id: int = Depends(get_current_user)):
    card_data = card.dict(exclude_unset=True)
    try:
        updated_card = cards_services.update_card(card_id, card_data)
        if not updated_card:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
        return updated_card
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, user_id: int = Depends(get_current_user)):
    try:
        deleted_card = cards_services.delete_card(card_id)
        if not deleted_card:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
        return {}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
