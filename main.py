import logging

from fastapi import FastAPI
import uvicorn

from bitpay.routes.auth import router as auth_router
from bitpay.routes.wallet import router as wallet_router
from bitpay.utils.logging_config import setup_logger

app = FastAPI()
app.include_router(auth_router)
app.include_router(wallet_router)

setup_logger()

if __name__ == "__main__":
    logging.info("Server started")
    uvicorn.run(app, host="0.0.0.0", port=8000)

