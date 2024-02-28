import re
import fitz
import psycopg2 as psql


def read_PDF(file_name):
    doc = fitz.open(file_name)
    result_list = []
    for page in doc:
        text = page.get_textbox(fitz.Rect(0, 0, 400, 150))
        lst = [re.findall(r'\d{2}-\d{6,7}', text)[0], re.findall(r'\d{2} [а-яА-Я]{3,10} \d{4}', text)[0]]
        result_list.append(lst)
    result_list = [[item[0], format_date(item[1])] for item in result_list]
    return result_list


def format_date(date):
    date = date.split(' ')
    months = ['января', 'февраля', 'марта', 'апреля',
              'мая', 'июня', 'июля', 'августа',
              'сентября', 'октября', 'ноября', 'декабря']
    result_date = f'{date[0]}-{str(months.index(date[1].lower())+1).rjust(2, "0")}-{date[2]}'
    return result_date

def save_to_db(db_name, db_table, data_list):
    with psql.connect(
            database=db_name, user='postgres', password='12345', host='127.0.0.1', port='5432'
    ) as conn:
        cursor = conn.cursor()
        conn.autocommit = True
        query_row = f'''INSERT INTO {db_table} (number, ver_date)
                        VALUES (%s, %s)'''
        cursor.executemany(query_row, data_list)
    print(f'Сохранение в {db_table} прошло успешно')