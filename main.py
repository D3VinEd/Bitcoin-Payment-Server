from fastapi import FastAPI
from bitpay.routes.auth import router as auth_router
from bitpay.routes.wallet import router as wallet_router
import uvicorn

app = FastAPI()

app.include_router(auth_router)
app.include_router(wallet_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
