import sys
from pathlib import Path
# Add project root to sys.path to resolve 'db' imports when running the script directly
sys.path.append(str(Path(__file__).resolve().parent.parent))
from db import database as _database

def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)


if __name__ == "__main__":
    _add_tables()