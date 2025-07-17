from db import get_db
from models.user import User
from models.pick import Pick


def get_all():
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("SELECT * FROM picks")
            return [Pick(p) for p in db.fetchall()]
        
def get_pick(id: int):
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("SELECT * FROM players WHERE player_id=%s", [id])
            return Pick(db.fetchall())
        

def new_pick(draft_id: int, player_id: int, round_num: int, pick_num: int):
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("INSERT INTO picks (pick_id, pick_draft_id, pick_player_id, pick_round_num, pick_num) " \
                "VALUES (%s, %s, %s, %s, %s)", 
                [draft_id + '' + player_id, draft_id, player_id, round_num, pick_num])
            conn.commit()