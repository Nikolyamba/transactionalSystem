
from sqlalchemy import text

from backend.celery_dir.celery_config import celery_app
from backend.database.session import SessionLocal

@celery_app.task
def expire_orders():
    db = SessionLocal()
    try:
        db.execute(text("""
            UPDATE orders
            SET status = 'expired'
            WHERE status = 'pending'
            AND expires_at < now()
        """))

        db.execute(text("""
            UPDATE inventories i
            SET reserved_quantity = reserved_quantity - 1
            FROM orders o
            WHERE o.product_id = i.product_id
            AND o.status = 'expired'
        """))

        db.commit()
    finally:
        db.close()