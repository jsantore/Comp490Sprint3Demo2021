import demo
import database_handler
import xcelwork
import pytest
import us_state_abbrev


@pytest.fixture
def get_db():
    conn, cursor = database_handler.open_db('testdb.sqlite')
    return conn, cursor


@pytest.fixture
def get_demo_job_data():
    test_dict = {'state_name': "TEST",
                 'state_abbrev': 'ME',
                 'occupation_title': "Student",
                 'total_employment_in_field': 10000,
                 "salary_lower25": 20000.65,
                 'occupation_code': '11-0000',
                 }
    return test_dict

def test_get_data():
    data = demo.get_data()
    assert len(data) > 3000


def test_data_save(get_db):
    # first lets add test data
    conn, cursor = get_db
    database_handler.make_tables(cursor)
    test_data = [{'school.name': 'Test University', '2018.student.size': 1000, 'school.state': 'MA', 'id': 11001,
                  '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 456,
                  '2016.repayment.3_yr_repayment.overall': 4004}]
    database_handler.save_data(test_data, cursor)
    database_handler.close_db(conn)
    # test data is saved - now lets see if it is there
    conn, cursor = get_db
    # the sqlite_master table is a metadata table with information about all the tables in it
    cursor.execute('''SELECT name FROM sqlite_master
    WHERE type ='table' AND name LIKE 'university_%';''')  # like does pattern matching with % as the wildcard
    results = cursor.fetchall()
    assert len(results) == 1
    cursor.execute(''' SELECT university_name FROM university_data''')
    results = cursor.fetchall()
    test_record = results[0]
    assert test_record[0] == 'Test University'


def test_tables_created_properly(get_db, get_demo_job_data):
    conn, cursor = get_db
    test_dict = get_demo_job_data
    database_handler.make_tables(cursor, test_dict)
    cursor.execute('''SELECT name FROM sqlite_master
    WHERE type ='table' AND name LIKE 'university_%';''')  # like does pattern matching with % as the wildcard
    results = cursor.fetchall()
    assert len(results) == 1
    cursor.execute('''SELECT name FROM sqlite_master
    WHERE type ='table' AND name LIKE 'job_%';''')  # like does pattern matching with % as the wildcard
    results = cursor.fetchall()
    assert len(results) == 1


def test_excel_read():
    data = xcelwork.get_xcel_jobs_stats('state_M2019_dl.xlsx')
    all_states = list(us_state_abbrev.us_state_abbrev) # get all state and territory names as list
    for item in data:
        state_name = item['state_name']
        if state_name in all_states:
            all_states.remove(state_name)
    assert len(all_states) <= 6  # there are 5 territories + dc in the list which are not states.


def test_write_job_to_db(get_db, get_demo_job_data):
    conn, cursor = get_db
    database_handler.make_tables(cursor, get_demo_job_data)
    database_handler.save_xcel_data([get_demo_job_data], cursor)
    cursor.execute("""SELECT state_name from job_stats WHERE state_name = 'TEST'""")
    results = cursor.fetchall()
    assert len(results) == 1
