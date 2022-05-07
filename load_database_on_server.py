#!/usr/local/bin/python3

import csv
import mysql.connector

def main():
    # read CSV file and turn back into list of lists
    promoter_data = []
    with open('complete_promoter_data.csv') as input:
        rows = csv.reader(input)
        for row in rows:
            promoter_data.append(row)

    # connect to database
    connection = mysql.connector.connect(user='user', password='pass'', host='localhost', database='kgerhar4')

    insert_query1 = """INSERT INTO promoters (numeric_id, bba_id, name, designer, design_group, times_used, rating, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
    promoters_table_data = []

    for row in promoter_data:
        numeric_id = row[11]
        bba_id = row[0]
        name = row[1]
        designer = row[2]
        design_group = row[3]
        times_used = row[4]
        rating = row[5]
        url = row[10]
        info = (numeric_id, bba_id, name, designer, design_group, times_used, rating, url)
        promoters_table_data.append(info)

    insert_query2 = """ INSERT INTO promoter_features (numeric_id, polymerase, direction, chassis, regulation_type, sequence) VALUES (%s, %s, %s, %s, %s, %s) """
    promoter_features_table_data = []

    for row in promoter_data:
        numeric_id = row[11]
        polymerase = row[6]
        direction = row[7]
        chassis = row[8]
        regulation_type = row[9]
        sequence = row[12]
        info = (numeric_id, polymerase, direction, chassis, regulation_type, sequence)
        promoter_features_table_data.append(info)

    cursor = connection.cursor()
    cursor.executemany(insert_query1, promoters_table_data)
    connection.commit()
    print(cursor.rowcount, "Promoters table data inserted successfully")

    cursor.executemany(insert_query2, promoter_features_table_data)
    connection.commit()
    print(cursor.rowcount, "Promoter features table data inserted successfully")

    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
