import sqlite3
from typing import Any

from app.schemas import ShipmentCreate

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread= False)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment(
                        id INTEGER PRIMARY KEY,
                        content TEXT,
                        weight REAL,
                        destination_id INTEGER, 
                        status TEXT
                        )
    """)
    


    def save(self, data : ShipmentCreate)-> int:

        self.cur.execute("SELECT COALESCE (MAX(id), 0) FROM shipment")
        result = self.cur.fetchone()
        if result[0] is None:
            new_id = 1
        else:
            new_id = result[0] + 1


        self.cur.execute("""
            INSERT INTO shipment VALUES (
                        :id,
                        :content,
                        :weight,
                        :destination_id, 
                        :status
                        )
    """
        , {"id": new_id,
        **data.model_dump(), 
        "status": "received"})
        self.conn.commit()
        return new_id

        
    def get_shipment_by_id(self, id : int) -> dict[str, Any] | None:
        self.cur.execute("""
            SELECT * FROM shipment
            WHERE id = :id
                        )
    """, (id,))
        self.conn.commit()
        row = self.cur.fetchone()
        if row is None: 
            return None
        
        return {"id": row[0],
                "content": row[1],
                "weight": row[2],
                "destination_id": row[3],
                "status": row[4]
                }

    def get_latest(self)-> dict[str, Any] | None:
        self.cur.execute("""
            SELECT * FROM shipment 
            ORDER BY id DESC 
            LIMIT 1;    
    """)
        row = self.cur.fetchone()
        if row is None: 
            return None
        
        self.conn.commit()
        return {"id": row[0],
                "content": row[1],
                "weight": row[2],
                "destination_id": row[3],
                "status": row[4]
                }

        