#!/usr/local/bin/python3

# Obtains data categories to use as search filters by querying the database they
#   are stored in.

import cgi, json
import os
import mysql.connector

def main():
    print("Content-Type: application/json\n\n")
    form = cgi.FieldStorage()
    term = form.getvalue('search_term')

    conn = mysql.connector.connect(user='user, password='pass', host='localhost', database='kgerhar4')
    cursor = conn.cursor()

    filter_terms = { 'pols': list(), 'regulation': list(), 'direction': list(), 'chassis': list(), 'design_group': list(), 'designer': list(), 'rating': list(), 'times_used': list()}

    # Get polymerase types
    qry = """SELECT pf.polymerase, COUNT(*)
    FROM promoter_features pf
    JOIN promoters p ON p.numeric_id = pf.numeric_id
    WHERE p.name LIKE %s
    GROUP BY pf.polymerase
    ORDER BY COUNT(*) DESC"""
    cursor.execute(qry, ("%" + term + "%", ))
        # Add pol data
    for row in cursor:
        pol = row[0]
        count = row[1]
        filter_terms['pols'].append({'label' : pol, 'count' : count})

    # Get regulation types
    qry2 = """SELECT pf.regulation_type, COUNT(*)
    FROM promoter_features pf
    JOIN promoters p ON p.numeric_id = pf.numeric_id
    WHERE p.name LIKE %s
    GROUP BY pf.regulation_type
    ORDER BY COUNT(*) DESC"""
    cursor.execute(qry2, ("%" + term + "%", ))
        # add regulation data
    for row in cursor:
        regulation = row[0]
        count = row[1]
        filter_terms['regulation'].append({'label' : regulation, 'count' : count})

    # Get directions
    qry3 = """SELECT pf.direction, COUNT(*)
    FROM promoter_features pf
    JOIN promoters p ON p.numeric_id = pf.numeric_id
    WHERE p.name LIKE %s
    GROUP BY pf.direction
    ORDER BY COUNT(*) DESC"""
    cursor.execute(qry3, ("%" + term + "%", ))
        # add direction data
    for row in cursor:
        direction = row[0]
        count = row[1]
        filter_terms['direction'].append({'label' : direction, 'count' : count})

    # Get chassis
    qry4 = """SELECT pf.chassis, COUNT(*)
    FROM promoter_features pf
    JOIN promoters p ON p.numeric_id = pf.numeric_id
    WHERE p.name LIKE %s
    GROUP BY pf.chassis
    ORDER BY COUNT(*) DESC"""
    cursor.execute(qry4, ("%" + term + "%", ))
        # add chassis data
    for row in cursor:
        chassis = row[0]
        count = row[1]
        filter_terms['chassis'].append({'label' : chassis, 'count' : count})

    # Get Rating
    qry5 = """SELECT rating, COUNT(*)
    FROM promoters
    WHERE name LIKE %s
    GROUP BY rating
    ORDER BY COUNT(*) DESC"""
    cursor.execute(qry5, ("%" + term + "%", ))
        # add rating data
    for row in cursor:
        rating= row[0]
        count = row[1]
        filter_terms['rating'].append({'label' : rating, 'count' : count})

    # Get uses
    qry6 = """SELECT times_used, COUNT(*)
    FROM promoters
    WHERE name LIKE %s
    GROUP BY times_used
    ORDER BY COUNT(*) DESC"""
    cursor.execute(qry6, ("%" + term + "%", ))
        # add uses data
    for row in cursor:
        times_used = row[0]
        count = row[1]
        filter_terms['times_used'].append({'label' : times_used, 'count' : count})

    # Get group
    qry7 = """SELECT design_group, COUNT(*)
    FROM promoters
    WHERE name LIKE %s
    GROUP BY design_group
    ORDER BY COUNT(*) DESC"""
    cursor.execute(qry7, ("%" + term + "%", ))
        # add group data
    for row in cursor:
        design_group = row[0]
        count = row[1]
        filter_terms['design_group'].append({'label' : design_group, 'count' : count})

    # Get designer
    qry8 = """SELECT designer, COUNT(*)
    FROM promoters
    WHERE name LIKE %s
    GROUP BY designer
    ORDER BY COUNT(*) DESC"""
    cursor.execute(qry8, ("%" + term + "%", ))
        # add designer data
    for row in cursor:
        designer = row[0]
        count = row[1]
        filter_terms['designer'].append({'label' : designer, 'count' : count})

    # close connections
    cursor.close()
    conn.close()

    print(json.dumps(filter_terms))


if __name__ == '__main__':
    main()
