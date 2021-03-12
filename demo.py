import api_data
import database_handler
import xcelwork



def main():
#    api_data = api_data.get_data()
    api_data = []
    xcel_data = xcelwork.get_xcel_jobs_stats('state_M2019_dl.xlsx')
    conn, cursor = database_handler.open_db("comp490.sqlite")
    database_handler.make_tables(cursor, xcel_data[0])
    database_handler.save_data(api_data, cursor)
    database_handler.close_db(conn)


if __name__ == '__main__':
    main()
