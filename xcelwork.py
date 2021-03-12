import openpyxl
import openpyxl.utils
from typing import List, Dict
import us_state_abbrev

def get_xcel_jobs_stats(filename:str)->List[Dict]:
    xcel_file = openpyxl.load_workbook(filename)
    worksheet = xcel_file.active
    all_data_we_care_about = []
    for current_row in worksheet.rows:
        if current_row[9].value != "major":  # only get the major groups
            continue
        state_name = current_row[1].value  # I'm getting the state names with hard coded number to contrast with later
        state_abbrev = us_state_abbrev.us_state_abbrev[state_name]  # didn't need abbrev for sprint3 but it helps with 4
        occ_title_column = openpyxl.utils.column_index_from_string("I")-1  # this time demo not using hard coded numbers
        occupation_title = current_row[occ_title_column].value
        tot_emp_column = openpyxl.utils.column_index_from_string("K")-1  # this function is 1-based so subtract 1
        total_employment_in_field = current_row[tot_emp_column].value
        salary_lower25_col = openpyxl.utils.column_index_from_string("Y")-1
        salary_lower25 = current_row[salary_lower25_col].value
        occ_code_col = openpyxl.utils.column_index_from_string("H")-1
        occupation_code = current_row[occ_code_col].value
        data_from_row = {'state_name': state_name,
                         'state_abbrev': state_abbrev,
                         'occupation_title': occupation_title,
                         'total_employment_in_field': total_employment_in_field,
                         "salary_lower25": salary_lower25,
                         'occupation_code': occupation_code,
                         }
        all_data_we_care_about.append(data_from_row)
    return all_data_we_care_about

def demo_xcel():
    results = get_xcel_jobs_stats("state_M2019_dl.xlsx")
    print(results[0])


if __name__ == '__main__':
    demo_xcel()