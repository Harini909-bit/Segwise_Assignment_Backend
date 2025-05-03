from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.subscription import Subscription
from ..workers.celery_worker import deliver_webhook

router = APIRouter()

@router.post("/ingest/{subscription_id}")
async def ingest_webhook(subscription_id: int, request: Request, db: Session = Depends(get_db)):
    # Get subscription
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Get payload
    payload = await request.json()
    
    # Queue delivery task
    deliver_webhook.delay(subscription_id, payload)
    
    return JSONResponse(content={"status": "queued"}, status_code=202)
