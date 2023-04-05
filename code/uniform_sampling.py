import sqlite3
from query_engine.code.model import model
import re


def simple_query_engine(sql_query, cursor):
    # Parse the query
    query_parts = sql_query.lower().split()
    select_index = query_parts.index("select")
    from_index = query_parts.index("from")

    # Extract columns, table, and condition
    columns = " ".join(query_parts[select_index + 1:from_index]).split(", ")
    table = query_parts[from_index + 1]
  

    actual_query = f"SELECT {', '.join(columns)} FROM {table}"

    # Execute the query and fetch the results
    cursor.execute(actual_query)
    results = cursor.fetchall()

    return results

