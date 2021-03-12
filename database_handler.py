import sqlite3
from typing import Tuple, Dict


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def make_tables(cursor: sqlite3.Cursor, jobs_datashape: Dict):
    cursor.execute('''CREATE TABLE IF NOT EXISTS university_data(
    school_id INTEGER PRIMARY KEY,
    university_name TEXT NOT NULL,
    student_size INTEGER,
    university_state TEXT,
    three_year_earnings_over_poverty INT,
    loan_repayment INT);''')
    # in the code below I'm going to practice the DRY priciple, rather than representing the structure of the data
    # in hard coded form in both the xcel reader and here in the table creation, I will use the dictionary from the
    # excel reader to create the tables. It should work even if we get more data later
    columns = create_columns(jobs_datashape)
    create_statement = f"""CREATE TABLE IF NOT EXISTS job_stats {columns}"""
    print (create_statement)
    cursor.execute(create_statement)


def create_columns(jobs_datashape: Dict)-> str:
    column_list = ""
    for key in jobs_datashape:
        column_list = f"{column_list}, {key} {get_sql_type(jobs_datashape[key])}"
    final_column_statement = f"(id INTEGER PRIMARY KEY {column_list} );"
    return final_column_statement


def get_sql_type(sample_val)->str:
    if type(sample_val) == str:
        return "TEXT"
    elif type(sample_val) == int:
        return "INTEGER"
    elif type(sample_val) == float:
        return "FLOAT"
    else:
        return "TEXT" # for a default I'll go with text for now


def save_data(all_data, cursor):
    for univ_data in all_data:
        cursor.execute("""
        INSERT INTO university_data(school_id, university_name, student_size, university_state, three_year_earnings_over_poverty,
         loan_repayment)
         VALUES (?,?,?,?,?,?);
        """, (univ_data['id'], univ_data['school.name'], univ_data['2018.student.size'],
              univ_data['school.state'], univ_data['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
              univ_data['2016.repayment.3_yr_repayment.overall']))