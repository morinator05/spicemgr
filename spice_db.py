import sqlite3
from spice import Spice

class SpiceDB:

    def __init__(self, db_path="data/spicemgr.db"):
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()

        # basic data about the spices
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS spices (
                    spice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT DEFAULT "",
                    category TEXT DEFAULT "common",
                    in_stock BOOLEAN DEFAULT 0 
                )
                """)
        self.con.commit()

    def add_spice(self, name="", category="common", in_stock=False):
        self.cur.execute("""
            INSERT INTO spices (name, category, in_stock)
            VALUES (?, ?, ?)
        """, (name, category, int(in_stock)))
        self.con.commit()
        return Spice(self.cur.lastrowid,  name, category, bool(in_stock))

    def remove_spice(self, spice_id):
        spice = self.get_spice(spice_id)
        self.cur.execute("DELETE FROM spices WHERE spice_id = ?", (spice_id,))
        self.con.commit()
        return spice

    def update_name(self, spice_id, new_name):
        self.cur.execute("""
            UPDATE spices SET name = ? WHERE spice_id = ?
        """, (new_name, spice_id))
        self.con.commit()
        return self.get_spice(spice_id)

    def update_category(self, spice_id, new_category):
        self.cur.execute("""
            UPDATE spices SET category = ? WHERE spice_id = ?
        """, (new_category, spice_id))
        self.con.commit()
        return self.get_spice(spice_id)

    def mark_in_stock(self, spice_id):
        self.cur.execute("""
            UPDATE spices SET in_stock = 1 WHERE spice_id = ?
        """, (spice_id,))
        self.con.commit()
        return self.get_spice(spice_id)

    def mark_empty(self, spice_id):
        self.cur.execute("""
            UPDATE spices SET in_stock = 0 WHERE spice_id = ?
        """, (spice_id,))
        self.con.commit()
        return self.get_spice(spice_id)

    def is_empty(self, spice_id):
        self.cur.execute("""
            SELECT in_stock FROM spices WHERE spice_id = ?
        """, (spice_id,))
        res = self.cur.fetchone()
        return res is not None and res[0] == 0

    def get_all_spices(self):
        self.cur.execute("SELECT * FROM spices")
        result = self.cur.fetchall()
        spices = []
        for db_element in result:
            spices.append(Spice(db_element[0],
                                db_element[1],
                                db_element[2],
                                bool(db_element[3])))
        return spices

    def get_spice(self, spice_id):
        self.cur.execute("SELECT * FROM spices WHERE spice_id = ?", (spice_id,))
        result = self.cur.fetchone()
        if result is None:
            return None  # not found
        return Spice(result[0], result[1], result[2], bool(result[3]))