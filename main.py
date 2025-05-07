from pypm.cli import main
from pypm.db import init_db

if __name__ == "__main__":
    init_db()
    main()
