from app.autoria_scraper import get_links, get_vehicle_data
from app.schema import ValidationSchema
from database.database import SessionLocal
from database.models import Autoria_model
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "DATAOX")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123321")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "autoria")


def run():
    links = get_links()
    if not links:
        print('No links found')
        return
    
    data = get_vehicle_data(links)
    if not data:
        print('No data parsed')
        return
    
    with SessionLocal() as session:
        for d in data.values():
            try:
                valid_data = ValidationSchema(**d).model_dump()
                stmt = (
                    insert(Autoria_model)
                    .values(**valid_data)
                    .on_conflict_do_nothing(index_elements=['url'])
                )
                session.execute(stmt)
                
            except Exception as e:
                print(f"Ошибка при обработке записи {d.get('url')}: {e}")
                session.rollback()
                continue

        session.commit()


def make_db_dump():
    print("--- Creating dump file ---")

    if not os.path.exists('dumps'):
        os.makedirs('dumps')

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"dumps/dump_{timestamp}.sql"

    try:
        with open(filename, "w") as f:
            subprocess.run(
                [
                    "pg_dump", 
                    "-h", DB_HOST, 
                    "-p", DB_PORT, 
                    "-U", DB_USER, 
                    "-d", DB_NAME
                ],
                stdout=f,
                check=True,
                env={**os.environ, "PGPASSWORD": DB_PASSWORD}
            )
        print(f"--- Dump successfully saved: {filename} ---")
    except Exception as e:
        print(f"!!! Error While Creating Dump file: {e}")

if __name__ == "__main__":
    run()
    make_db_dump()