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