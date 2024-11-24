import asyncio
from db.database import get_db_pool  # Assuming this imports your db connection pool setup


async def execute_custom_sql():
    # Read the SQL queries from the file
    with open("./mysql_init_data.txt", 'r') as file:
        sql_queries = file.read()  # Read all SQL queries as a string

    # Get the connection pool
    pool = await get_db_pool()

    # Acquire a connection from the pool
    async with pool.acquire() as connection:

        queries = sql_queries.split(';')  # Split queries by semicolon
        for query in queries:
            query = query.strip()  # Strip whitespace from query
            if query:  # Skip empty queries
                try:
                    # Directly use the query string with cursor execute
                    async with connection.cursor() as cur:
                        await cur.execute(query)  # Pass query as a string directly
                        # Commit the transaction if needed
                        await connection.commit()
                except Exception as e:
                    print(f"Error executing query: {e}")

# Call the function asynchronously
asyncio.run(execute_custom_sql())
