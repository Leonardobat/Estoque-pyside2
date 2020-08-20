# -*- coding: utf-8 -*-
import sqlite3, time
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
            "INSERT INTO tracker (codeid, time, delta) VALUES (?, ?, ?)",
            (id, int(time.time()), data["qty"]),
        )
        self.db.commit()
        return

    def buy_update(self, data: dict) -> dict:
        id = self.get_id(data["code"])
        self.db.execute(
            "UPDATE tracker SET time = ?, delta = ? WHERE id = ?",
            (int(time.time()), data["qty"], id),
        )
        old_data = dict(
            self.db.execute(
                "SELECT quantidade, preco_compra FROM estoque WHERE id = ?", (id,),
            ).fetchone()
        )
        data["buy_price"] = (
            data["buy_price"] * data["qty"]
            + old_data["quantidade"] * old_data["preco_compra"]
        ) / (old_data["quantidade"] + data["qty"])
        data["qty"] += old_data["quantidade"]
        self.db.execute(
            "UPDATE estoque SET quantidade = ?, preco_compra = ? WHERE id = ?",
            (data["qty"], data["buy_price"], id),
        )

        self.db.commit()
        return

    def sell_update(self, data: dict) -> dict:
        id = self.get_id(data["code"])
        self.db.execute(
            "UPDATE tracker SET time = ?, delta = ? WHERE id = ?",
            (int(time.time()), (-data["qty"]), id),
        )
        old_data = dict(
            self.db.execute(
                "SELECT quantidade, preco_venda FROM estoque WHERE id = ?", (id,),
            ).fetchone()
        )
        data["sell_price"] = (
            old_data["quantidade"] * old_data["preco_venda"]
            - data["sell_price"] * data["qty"]
        ) / (old_data["quantidade"] - data["qty"])
        old_data["quantidade"] -= data["qty"]
        self.db.execute(
            "UPDATE estoque SET quantidade = ?, preco_venda = ? WHERE id = ?",
            (old_data["quantidade"], data["sell_price"], id),
        )
        self.db.commit()
        return

    # def update_info(self) -> dict:
    #     info = self.db.execute("SELECT * FROM estoque").fetchall()
    #     return info

    def search(self, word: str) -> dict:
        search_word = "{0}%".format(word)
        info = self.db.execute(
            "SELECT * FROM estoque WHERE code LIKE ? or nome LIKE ?",
            (search_word, search_word),
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
