import sqlite3

DATABASE = "./db/history.db"

def try_connect(db_path: str) -> sqlite3.Connection:
    """Подключение к БД"""
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db


def select_data(database: sqlite3.Connection) -> list[dict]:
    """Выборка записей из БД"""
    cur = database.cursor()
    query = "select * from Detections;"
    cur.execute(query)
    records = [dict(row) for row in cur.fetchall()]
    cur.close()

    return records


def insert_data(database: sqlite3.Connection, record: dict) -> bool:
    """Создание записи обработки в БД"""
    try:
        cur = database.cursor()
        query = ("insert into Detections (datetime_detect, source_img_url, result_img_url, json_data_url)"
                "values ({}, '{}', '{}', '{}')").format(
            record["datetime_detect"],
                    record["source_img_url"],
                    record["result_img_url"],
                    record["json_data_url"]
            )
        cur.execute(query)
        database.commit()
        return True
    except Exception as ex:
        print(ex)
        return False

def clear_data(database: sqlite3.Connection) -> bool:
    """Очистка истории обработок БД"""
    try:
        cur = database.cursor()
        query = "delete from Detections;"
        cur.execute(query)
        database.commit()
        return True
    except Exception as ex:
        print(ex)
        return False

def select_by_id(database: sqlite3.Connection, id_file: int) -> dict:
    """Получение записи по ID"""
    try:
        cur = database.cursor()
        query = "select * from Detections where ID = {};".format(id_file)
        cur.execute(query)
        record = cur.fetchone()
        return record
    except Exception as ex:
        print(ex)
        return {}