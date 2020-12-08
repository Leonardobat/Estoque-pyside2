# -*- coding: utf-8 -*-
import sqlite3, time, sys
from pathlib import Path
from datetime import datetime, timedelta


class estoque_driver():

    def __init__(self):
        if sys.platform.startswith('linux'):
            path = Path.home().joinpath('Documentos', 'Oficina', 'Estoque',
                                        'estoque.sqlite')
        elif sys.platform.startswith('win'):
            path = Path.home().joinpath('Documents', 'Oficina', 'Estoque',
                                        'estoque.sqlite')
        self.db = sqlite3.connect(str(path),
                                  detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row

        path = Path.cwd().joinpath("DB").joinpath("estoque.sqlite")
        self.db = sqlite3.connect(str(path),
                                  detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row

    def add_new(self, data: dict) -> None:
        self.db.execute(
            "INSERT INTO estoque (code, quantidade, preco_compra,"
            " preco_venda, nome, descricao) VALUES (?,?,?,?,?,?)",
            (
                data["code"],
                data["qty"],
                data["buy_price"],
                data["sell_price"],
                data["name"],
                data["description"],
            ),
        )
        self.db.commit()
        id = self.get_id(data["code"])
        self.db.execute(
            "INSERT INTO tracker (codeid, time, delta) VALUES (?, ?, ?)",
            (id, int(time.time()), data["qty"]),
        )
        self.db.commit()
        return

    def buy_update(self, data: dict) -> None:
        id = self.get_id(data["code"])
        self.db.execute(
            "INSERT INTO tracker (codeid, time, delta) VALUES (?, ?, ?)",
            (id, int(time.time()), data["qty"]),
        )
        old_data = dict(
            self.db.execute(
                "SELECT quantidade, preco_compra FROM estoque WHERE id = ?",
                (id,),
            ).fetchone())
        data["buy_price"] = (data["buy_price"] * data["qty"] +
                             old_data["quantidade"] * old_data["preco_compra"]
                            ) / (old_data["quantidade"] + data["qty"])
        data["qty"] += old_data["quantidade"]
        self.db.execute(
            "UPDATE estoque SET quantidade = ?, preco_compra = ? WHERE id = ?",
            (data["qty"], data["buy_price"], id),
        )
        self.db.commit()

    # def update_info(self) -> dict:
    #     info = self.db.execute("SELECT * FROM estoque").fetchall()
    #     return info

    def search(self, word: str) -> dict:
        search_word = "{0}%".format(word)
        info = self.db.execute(
            "SELECT * FROM estoque WHERE code LIKE ? OR nome LIKE ? ORDER BY id",
            (search_word, search_word),
        ).fetchall()
        return info

    def show_all(self) -> dict:
        info = self.db.execute("SELECT * FROM estoque").fetchall()
        return info

    def show(self, id: int) -> dict:
        info = self.db.execute("SELECT * FROM estoque WHERE id = ?",
                               (id,)).fetchone()
        return info

    def show_info(self, id: int) -> dict:
        info = self.db.execute(
            "SELECT nome, descricao FROM estoque WHERE id = ?",
            (id,)).fetchone()
        info = dict(info)
        info["delta"] = 0
        now = int(datetime.now().timestamp())
        week_ago = int((datetime.now() - timedelta(days=7)).timestamp())
        tracker_info = self.db.execute(
            "SELECT delta FROM tracker WHERE codeid = ?"
            " AND time > ? AND time <= ? ORDER BY id",
            (id, week_ago, now),
        ).fetchall()
        tracker_info, delta = tuple(tracker_info), 0
        if tracker_info != []:
            for i in range(len(tracker_info)):
                delta += tracker_info[i]["delta"]
            info["delta"] = int(delta)
        return info

    def get_id(self, code: str) -> int:
        id = self.db.execute("SELECT id FROM estoque WHERE code = ?",
                             (code,)).fetchone()
        return id["id"]


def init_db():
    directory = Path.cwd().joinpath("DB")
    Path.mkdir(directory, parents=True, exist_ok=True)
    path_db = directory.joinpath("estoque.sqlite")
    db = sqlite3.connect(str(path_db))
    with open(directory.joinpath("schema_estoque.sql")) as f:
        db.executescript(f.read())
        db.execute("PRAGMA foreign_keys = ON")
        db.execute("VACUUM")
        db.commit()
        db.close()


if __name__ == "__main__":
    init_db()
