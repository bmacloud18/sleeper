from db import get_db
from models.user import User
from models.player import Player
from models.position import Position



def get_all():
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("SELECT * FROM players")
            return [Player(p) for p in db.fetchall()]
        
def get_player(id: int):
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("SELECT * FROM players WHERE player_id=%s", [id])
            return Player(db.fetchall())
        

def new_player(id: int, first_name: str, last_name: str, team: str, number: int, position: Position):
    if (Position[position]):
        with get_db() as conn:
            with conn.cursor() as db:
                db.execute("INSERT INTO players (player_id, player_first_name, player_last_name, player_team, player_num, player_pos) " \
                    "VALUES (%s, %s, %s, %s, %s, %s)", 
                    [id, first_name, last_name, team, number, position])
                conn.commit()

def calc_stats(player: Player):
    with get_db() as conn:
        with conn.cursor() as db:
            db.execute("SELECT pick_player_id, ROUND(AVG(pick_num, 2) AS avg_pick" \
            "FROM picks" \
            "WHERE pick_player_id=%s)", [player.id])

            avg_pick = db.fetchall()

            db.execute("SELECT pick_player_id, ROUND(AVG(round_num, 0) AS avg_pick" \
            "FROM picks" \
            "WHERE pick_player_id=%s)", [player.id])

            avg_round = db.fetchall()
            
            db.execute("SELECT d.draft_slot, COUNT(*) AS slot_count" \
            "FROM picks p" \
            "JOIN drafts d ON p.draft_id = d.id" \
            "WHERE p.player_id = %s" \
            "GROUP BY d.draft_slot" \
            "ORDER BY d.draft_slot", [player.id])

            slots = db.fetchall()

            highest_count = max(slots, key=lambda x: x[1])

            return {
                "avg_pick": f"{avg_pick}",
                "avg_round": f"{avg_round}",
                "slots": slots,
                "max": highest_count
            }