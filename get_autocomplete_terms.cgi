#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector
import re

def main():
    print("Content-Type: application/json\n\n")
    form = cgi.FieldStorage()
    term = form.getvalue('search_term')

    conn = mysql.connector.connect(user='user', password='pass', host='localhost', database='kgerhar4')
    cursor = conn.cursor(named_tuple=True)

    qry = """SELECT name
    FROM promoters
    WHERE name LIKE %s"""

    cursor.execute(qry, ("%" + term + "%", ))


    query_terms = {}
    number = 0

    for row in cursor:
        term=row.name
        query_terms.update({number:term})
        number += 1


    conn.close()

    print(json.dumps(query_terms))


if __name__ == '__main__':
    main()
