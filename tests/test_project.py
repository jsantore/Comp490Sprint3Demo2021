import demo
import pytest


@pytest.fixture
def get_db():
    conn, cursor = demo.open_db('testdb.sqlite')
    return conn, cursor


def test_get_data():
    data = demo.get_data()
    assert len(data) > 3000


def test_data_save(get_db):
    # first lets add test data
    conn, cursor = get_db
    demo.make_tables(cursor)
    test_data = [{'school.name': 'Test University', '2018.student.size': 1000, 'school.state': 'MA', 'id': 11001,
                  '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 456,
                  '2016.repayment.3_yr_repayment.overall': 4004}]
    demo.save_data(test_data, cursor)
    demo.close_db(conn)
    # test data is saved - now lets see if it is there
    conn, cursor = demo.open_db('testdb.sqlite')
    # the sqlite_master table is a metadata table with information about all the tables in it
    cursor.execute('''SELECT name FROM sqlite_master
    WHERE type ='table' AND name LIKE 'university_%';''')  # like does pattern matching with % as the wildcard
    results = cursor.fetchall()
    assert len(results) == 1
    cursor.execute(''' SELECT university_name FROM university_data''')
    results = cursor.fetchall()
    test_record = results[0]
    assert test_record[0] == 'Test University'
