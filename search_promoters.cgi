#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector


def main():
    print("Content-Type: application/json\n\n")
    form = cgi.FieldStorage()
    term = form.getvalue('search_term')

    conn = mysql.connector.connect(user='user', password='pass', host='localhost', database='kgerhar4')
    cursor = conn.cursor()

    qry = """SELECT p.bba_id, p.name, p.designer, p.design_group, p.times_used, p.rating, pf.polymerase, pf.direction, pf.chassis, pf.regulation_type, pf.sequence
    FROM promoters p
    JOIN promoter_features pf ON pf.numeric_id = p.numeric_id
    WHERE (p.name LIKE %s)"""
    cursor.execute(qry, ('%' + term + '%', ))

    # structure results
    results = { 'match_count': 0, 'matches': list(), 'pols': list(), 'regulation': list(), 'direction': list(), 'chassis': list(), 'design_group': list(), 'designer': list(), 'rating': list(), 'times_used': list() }

    for (bba_id, name, designer, design_group, times_used, rating, polymerase, direction, chassis, regulation_type, sequence) in cursor:
        results['matches'].append({'bba_id': bba_id, 'name': name, 'designer': designer, 'design_group': design_group, 'times_used': times_used, 'rating': rating, 'polymerase': polymerase, 'direction': direction, 'chassis': chassis, 'regulation_type': regulation_type, 'sequence': sequence})
        results['match_count'] += 1


    cursor.close()
    conn.close()

    print(json.dumps(results))


if __name__ == '__main__':
    main()
