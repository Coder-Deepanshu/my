from celery import shared_task
from .logic import process_qr_and_leaves
import logging

logger = logging.getLogger(__name__)

@shared_task(name="process_qr_expiry_task")
def process_qr_expiry_task():
    """
    Celery task to process QR expiry and leaves
    """
    try:
        logger.info("🚀 Celery task started: Processing QR expiry")
        result = process_qr_and_leaves()
        logger.info("✅ Celery task completed successfully")
        return "Success"
    except Exception as e:
        logger.error(f"❌ Celery task failed: {str(e)}")
        return f"Error: {str(e)}"