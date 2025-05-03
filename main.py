from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import subscriptions, webhooks, status

app = FastAPI(title="Webhook Delivery Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])
app.include_router(status.router, prefix="/api/status", tags=["status"])

@app.get("/")
async def root():
    return {"message": "Webhook Delivery Service"}
