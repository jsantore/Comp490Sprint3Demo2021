import requests
import secrets
import sqlite3
from typing import Tuple


def get_data():
    all_data = []
    response = requests.get(f'https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant='
                            f'2,3&fields=id,school.state,school.name,2018.student.size,2016.repayment.3_yr_repayment.overall,'
                            f'2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line&api_key={secrets.api_key}')
    first_page = response.json()
    if response.status_code != 200:
        print(F"Error Getting Data from API: {response.raw}")
        return []
    total_results = first_page['metadata']['total']
    page = 0
    per_page = first_page['metadata']['per_page']
    all_data.extend(first_page['results'])
    while (page+1)*per_page < total_results:
        page += 1
        response = requests.get(
            f'https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,school.'
            f'state,school.name,2018.student.size,2016.repayment.3_yr_repayment.overall,2017.earnings.3_yrs_after_completion.'
            f'overall_count_over_poverty_line&api_key={secrets.api_key}&page={page}')
        if response.status_code != 200:  # if we didn't get good data keep going
            continue
        current_page = response.json()
        all_data.extend(current_page['results'])

    return all_data


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def make_tables(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS university_data(
    school_id INTEGER PRIMARY KEY,
    university_name TEXT NOT NULL,
    student_size INTEGER,
    university_state TEXT,
    three_year_earnings_over_poverty INT,
    loan_repayment INT);''')


def save_data(all_data, cursor):
    for univ_data in all_data:
        cursor.execute("""
        INSERT INTO university_data(school_id, university_name, student_size, university_state, three_year_earnings_over_poverty,
         loan_repayment)
         VALUES (?,?,?,?,?,?);
        """, (univ_data['id'], univ_data['school.name'], univ_data['2018.student.size'],
              univ_data['school.state'], univ_data['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
              univ_data['2016.repayment.3_yr_repayment.overall']))


def main():
    all_data = get_data()
    conn, cursor = open_db("comp490.sqlite")
    make_tables(cursor)
    save_data(all_data, cursor)
    close_db(conn)


if __name__ == '__main__':
    main()
