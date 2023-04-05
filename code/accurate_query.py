import sqlite3
from query_engine.code.model import model
import re
from query_engine.code.main import insert_mapping_table


def accruate_query_engine(sql_query, cursor):
    # Parse the query
    query_parts = sql_query.lower().split()
    select_index = query_parts.index("select")
    from_index = query_parts.index("from")
    where_index = query_parts.index("where") if "where" in query_parts else -1
    like_index = query_parts.index("like") if "like" in query_parts else -1

    # Extract columns, table, and condition
    columns = " ".join(query_parts[select_index + 1:from_index]).split(", ")
    table = query_parts[from_index + 1]
    condition = " ".join(query_parts[where_index + 1:]) if where_index != -1 else None


    # Check if the SUM operation is requested
    sum_requested = any("sum" in col.lower() for col in columns)

    # Build the actual SQL query
    if sum_requested:
        sum_match = re.search(r"sum\((\w+)\)", " ".join(columns), re.IGNORECASE)
        if sum_match:
            column = sum_match.group(1)
            if where_index != -1:
                actual_query = f"SELECT SUM({column}) FROM {table} WHERE {condition}"
            else:
                actual_query = f"SELECT SUM({column}) FROM {table}"
        else:
            raise ValueError("Invalid SUM expression in query")

    # Build the actual SQL query
    if where_index != -1:
        like_match = re.search(r"(\w+)\s+like\s+'([^']+)'", condition)
        equal_match = re.search(r"(\w+)\s*=\s*('([^']+)'|(\d+))", condition)

        if like_index != -1:
            column, value = like_match.groups()
            actual_query = f"SELECT {', '.join(columns)} FROM {table} WHERE {column} LIKE '{value}'"
        elif equal_match:
            column, value = equal_match.group(1), equal_match.group(3) or equal_match.group(4)
            
            # do structured query first
            temp_query = f"SELECT {', '.join(columns)} FROM {table} WHERE {column} = '{value}'"
            cursor.execute(temp_query)
            results = cursor.fetchall()

            # load unstructured data into mapping_table
            if results == []:
                cursor = insert_mapping_table(value)

            actual_query = f"SELECT {', '.join(columns)} FROM {table} WHERE {column} = '{value}'"
    else:
        actual_query = f"SELECT {', '.join(columns)} FROM {table}"

    # Execute the query and fetch the results
    cursor.execute(actual_query)
    results = cursor.fetchall()

    return results