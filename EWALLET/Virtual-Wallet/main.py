from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from routers import cards, transactions, users
from common.authorization import create_token, get_current_user
import uvicorn
from services.user_services import try_login, get_logged_user

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # This will allow all HTTP methods including OPTIONS
    allow_headers=["*"],
)

# Include your routers
app.include_router(users.users_router)
app.include_router(cards.router)
app.include_router(transactions.transaction_router)

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = try_login(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/profile", response_model=dict)
async def read_profile(current_user: int = Depends(get_current_user)):
    user = get_logged_user(current_user)
    return {"username": user.username, "email": user.email, "phone_number": user.phone_number}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
