# Bitcoin-Payment-Server
API-Driven Bitcoin Payment Server

## Build on
- [x] Bit
- [x] Redis
- [x] FastAPI
- [x] Uvicorn

## How to use
1. docker-compose up -d to start redis
2. change the config.ini file to your own config (Change the secret!)
3. python3 main.py to start the server

## API
### Info
- Authorization via Bearer token


### /register
- POST
- Request
```json
{
    "username": "username",
    "password": "password"
}
```
- Response
```json
{
    "message": "User registered"
}
```
### /login
- POST
- Request
```json
{
    "username": "username",
    "password": "password"
}
```
- Response
```json
{
    "access_token": "jwt-here"
}
```
### /create_key
### /get_keys
### /delete_key (inactive)
### /get_balance
### /get_transaction_history (inactive)
### /send_transaction (inactive)
### /get_transaction_status (inactive)
### /get_transaction_fee (inactive)