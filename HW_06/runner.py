import os
from pathlib import Path

database_file = Path("hw_06.db")
if database_file.exists():
    os.remove("hw_06.db")

# Create and load tables.
exec(open("create_load_tables.py").read())

# Execute gurobi optimizer.
exec(open("nfl_part1.py").read())


