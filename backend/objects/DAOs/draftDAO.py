from db import get_db
from models.user import User
from models.draft import Draft

def get_all():
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("SELECT * FROM picks")
            return [Draft(d) for d in db.fetchall()]
        
def get_draft(id: int):
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("SELECT * FROM drafts WHERE draft_id=%s", [id])
            return Draft(db.fetchall())
        

def new_draft(draft_id: int, user_id: int, draft_slot: int, season: int):
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("INSERT INTO drafts (draft_id, user_id, draft_slot, season) " \
                "VALUES (%s, %s, %s, %s)", 
                [draft_id, user_id, draft_slot, season])
            conn.commit()