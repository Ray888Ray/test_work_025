import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.routers import transactions, statistics


app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router, prefix="/api", tags=["Transactions"])
app.include_router(statistics.router, prefix="/api", tags=["Statistics"])

if __name__ == 'main.py':
    uvicorn.run(app, host="0.0.0.0", port=8000)
