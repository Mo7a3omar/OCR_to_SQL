import pandas as pd
from sqlalchemy import create_engine

def excel_to_sql(excel_file, db_file, table_name):
    """
    Convert an Excel file to a SQL database.
    
    :param excel_file: Path to the Excel file.
    :param db_file: Path to the SQLite database file.
    :param table_name: The name of the table to store the Excel data in.
    """
    # Step 1: Read the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file)

    # Step 2: Create a SQLAlchemy engine to connect to SQLite (or any other database)
    engine = create_engine(f'sqlite:///{db_file}', echo=False)

    # Step 3: Write the DataFrame to the SQL database
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

    print(f"Data successfully written to the '{table_name}' table in the database: {db_file}")

