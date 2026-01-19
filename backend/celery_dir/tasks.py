
from sqlalchemy import text

from backend.celery_dir.celery_config import celery_app
from backend.database.session import SessionLocal

@celery_app.task
def expire_orders():
    db = SessionLocal()
    try:
        result = db.execute(text("""
            UPDATE orders
            SET status = 'expired'
            WHERE status = 'pending'
            AND expired_at < now()
            RETURNING product_id
        """))

        expired_products = result.fetchall()

        for row in expired_products:
            db.execute(text("""
                UPDATE inventories
                SET reserved_quantity = reserved_quantity - 1
                WHERE product_id = :product_id
            """), {"product_id": row.product_id})

        db.commit()
    finally:
        db.close()