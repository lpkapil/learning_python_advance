import os
import json
import threading
from typing import List, Dict, Any
from datetime import datetime


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.lock = threading.Lock()
        self.tables = {}
        self._init_db()

    def _init_db(self):
        """Initialize the database with the required files."""
        if not os.path.exists(self.db_name):
            os.makedirs(self.db_name)
        self.db_file = os.path.join(self.db_name, "db.json")
        self.journal_file = os.path.join(self.db_name, "db.journal")
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({}, f)  # Initialize the db with an empty JSON object

    def create_table(self, table_name: str, columns: List[str], primary_key: str = None):
        """Creates a new table."""
        with self.lock:
            table = Table(self, table_name, columns, primary_key)
            self.tables[table_name] = table
            table.save()

    def get_table(self, table_name: str) -> 'Table':
        """Fetches a table."""
        if table_name in self.tables:
            return self.tables[table_name]
        raise ValueError(f"Table '{table_name}' not found.")

    def drop_table(self, table_name: str):
        """Drops a table."""
        with self.lock:
            if table_name in self.tables:
                table = self.tables[table_name]
                table.drop()
                del self.tables[table_name]

    def backup(self):
        """Backup the database."""
        backup_file = self.db_file + ".bak"
        with open(self.db_file, 'r') as src, open(backup_file, 'w') as dest:
            dest.write(src.read())
        print(f"Backup saved to {backup_file}")

    def restore(self):
        """Restore the database from backup."""
        backup_file = self.db_file + ".bak"
        if os.path.exists(backup_file):
            with open(backup_file, 'r') as src, open(self.db_file, 'w') as dest:
                dest.write(src.read())
            self.load_tables()  # Reload tables after restore
            print("Database restored from backup.")
        else:
            print("No backup found.")

    def load_tables(self):
        """Load tables from the db.json file."""
        with open(self.db_file, 'r') as f:
            db_data = json.load(f)
            for table_name, table_data in db_data.items():
                table = Table(self, table_name, table_data['columns'], table_data['primary_key'])
                table.records = table_data['records']
                self.tables[table_name] = table

    def save_global_state(self):
        """Save the global state of the database (all tables) to db.json."""
        with open(self.db_file, 'w') as f:
            db_data = {}
            for table_name, table in self.tables.items():
                db_data[table_name] = {
                    'columns': table.columns,
                    'primary_key': table.primary_key,
                    'records': table.records
                }
            json.dump(db_data, f, indent=4)


class Table:
    def __init__(self, db: Database, table_name: str, columns: List[str], primary_key: str = None):
        self.db = db
        self.table_name = table_name
        self.columns = columns
        self.primary_key = primary_key
        self.records = []
        self.load()

    def load(self):
        """Load table data from JSON file."""
        table_file = os.path.join(self.db.db_name, f"{self.table_name}.json")
        if os.path.exists(table_file):
            with open(table_file, 'r') as f:
                table_data = json.load(f)
                self.records = table_data.get('records', [])

    def save(self):
        """Save table data to JSON file."""
        table_file = os.path.join(self.db.db_name, f"{self.table_name}.json")
        table_data = {
            'columns': self.columns,
            'primary_key': self.primary_key,
            'records': self.records
        }
        with open(table_file, 'w') as f:
            json.dump(table_data, f, indent=4)

        # Save the table data into the global db.json as well
        self.db.save_global_state()

    def insert(self, row: Dict[str, Any]):
        """Insert a new row into the table."""
        if self.primary_key and self.primary_key in row:
            for existing_row in self.records:
                if existing_row.get(self.primary_key) == row.get(self.primary_key):
                    raise ValueError(f"Duplicate primary key '{self.primary_key}' value.")

        # Validate row data matches table schema
        if set(row.keys()) != set(self.columns):
            raise ValueError("Row columns do not match table columns.")
        
        # Insert the row and save it
        self.records.append(row)
        self.save()

    def select(self, condition: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Select rows from the table that match the condition."""
        if condition:
            return [row for row in self.records if all(row[key] == value for key, value in condition.items())]
        return self.records

    def update(self, condition: Dict[str, Any], new_values: Dict[str, Any]):
        """Update rows in the table matching the condition."""
        updated = False
        for row in self.records:
            if all(row[key] == value for key, value in condition.items()):
                row.update(new_values)
                updated = True
        if updated:
            self.save()

    def delete(self, condition: Dict[str, Any]):
        """Delete rows from the table matching the condition."""
        self.records = [row for row in self.records if not all(row[key] == value for key, value in condition.items())]
        self.save()

    def drop(self):
        """Drop the table data."""
        table_file = os.path.join(self.db.db_name, f"{self.table_name}.json")
        if os.path.exists(table_file):
            os.remove(table_file)
        self.records = []  # Clear in-memory data


class MultiThreadedDatabase(Database):
    def __init__(self, db_name: str):
        super().__init__(db_name)

    def execute_query(self, query: str):
        """Execute a SQL query."""
        parsed_query = SQLParser.parse_query(query)
        table = self.get_table(parsed_query["table"])

        if parsed_query["type"] == "select":
            condition = eval(parsed_query["condition"]) if parsed_query["condition"] else None
            results = table.select(condition)
            return results
        elif parsed_query["type"] == "insert":
            values = eval(parsed_query["values"])
            table.insert(values)
        elif parsed_query["type"] == "update":
            set_values = eval(parsed_query["set"])
            condition = eval(parsed_query["condition"]) if parsed_query["condition"] else None
            table.update(condition, set_values)
        elif parsed_query["type"] == "delete":
            condition = eval(parsed_query["condition"]) if parsed_query["condition"] else None
            table.delete(condition)


class SQLParser:
    """Parser for SQL queries."""

    @staticmethod
    def parse_query(query: str):
        """Parse SQL query into components."""
        query = query.strip().lower()
        if query.startswith("select"):
            return SQLParser.parse_select(query)
        elif query.startswith("insert"):
            return SQLParser.parse_insert(query)
        elif query.startswith("update"):
            return SQLParser.parse_update(query)
        elif query.startswith("delete"):
            return SQLParser.parse_delete(query)
        else:
            raise ValueError("Unsupported query type")

    @staticmethod
    def parse_select(query: str):
        """Parse SELECT query."""
        parts = query[len("select"):].strip().split("from")
        select_columns = parts[0].strip()
        table_name = parts[1].strip().split()[0]
        condition = None
        if "where" in parts[1]:
            condition = parts[1].split("where")[1].strip()
        return {"type": "select", "columns": select_columns, "table": table_name, "condition": condition}

    @staticmethod
    def parse_insert(query: str):
        """Parse INSERT query."""
        parts = query[len("insert into"):].strip().split("values")
        table_name = parts[0].strip()
        values = parts[1].strip()
        return {"type": "insert", "table": table_name, "values": values}

    @staticmethod
    def parse_update(query: str):
        """Parse UPDATE query."""
        parts = query[len("update"):].strip().split("set")
        table_name = parts[0].strip()
        set_part = parts[1].split("where")[0].strip()
        condition = parts[1].split("where")[1].strip() if "where" in parts[1] else None
        return {"type": "update", "table": table_name, "set": set_part, "condition": condition}

    @staticmethod
    def parse_delete(query: str):
        """Parse DELETE query."""
        parts = query[len("delete from"):].strip().split("where")
        table_name = parts[0].strip()
        condition = parts[1].strip() if len(parts) > 1 else None
        return {"type": "delete", "table": table_name, "condition": condition}
