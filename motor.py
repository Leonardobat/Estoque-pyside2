# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path
from datetime import datetime


class estoque_driver:
    def __init__(self):
        path = Path.cwd().joinpath("DB").joinpath("estoque.sqlite")
        self.db = sqlite3.connect(str(path), detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row

    def add_new(self, data: dict) -> dict:
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
            "INSERT INTO tracker (codeid, timestamp, delta) VALUES (?, ?, ?)",
            (id, datetime.now().isoformat(timespec="minutes"), data["qty"]),
        )
        self.db.commit()
        return

    def buy_update(self, data: dict) -> dict:
        self.db.execute(
            "UPDATE estoque SET quantidade = ?, preco_compra = ?, WHERE id = ?",
            (data["qty"], data["buy_price"], data["id"]),
        )
        self.db.execute(
            "UPDATE tracker SET timestamp = ?, delta = ? WHERE ID = ?",
            (
                data["id"],
                datetime.now().isoformat(timespec="minutes"),
                data["delta_qty"],
            ),
        )
        self.db.commit()
        return

    def sell_update(self, data: dict) -> dict:
        self.db.execute(
            "UPDATE estoque SET quantidade = ?, preco_venda = ? WHERE id = ?",
            (data["qty"], data["sell_price"], data["id"]),
        )
        self.db.execute(
            "UPDATE tracker SET timestamp = ?, delta = ? WHERE id = ?",
            (
                data["id"],
                datetime.now().isoformat(timespec="minutes"),
                (data["delta_qty"]),
            ),
        )
        self.db.commit()
        return

    # def update_info(self) -> dict:
    #     info = self.db.execute("SELECT * FROM estoque").fetchall()
    #     return info

    def search(self, word: str) -> dict:
        search_word = "{0}%".format(word)
        info = self.db.execute(
            "SELECT * FROM estoque WHERE code LIKE ? or nome LIKE ?", (search_word, search_word)
        ).fetchall()
        return info

    def show_all(self) -> dict:
        info = self.db.execute("SELECT * FROM estoque").fetchall()
        return info

    def show(self, id: int) -> dict:
        info = self.db.execute("SELECT * FROM estoque WHERE id = ?", (id,)).fetchone()
        return info

    def show_info(self, id: int) -> dict:
        info = self.db.execute(
            "SELECT nome, descricao FROM estoque WHERE id = ?", (id,)
        ).fetchone()
        return info

    def get_id(self, code: str) -> int:
        id = self.db.execute(
            "SELECT id FROM estoque WHERE code = ?", (code,)
        ).fetchone()
        return id["id"]


def init_db():
    directory = Path.cwd().joinpath("DB")
    Path.mkdir(directory, exist_ok=True)
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
