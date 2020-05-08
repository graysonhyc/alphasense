# This gist contains a direct connection to a local PostgreSQL database
# called "suppliers" where the username and password parameters are "postgres"

# This code is adapted from the tutorial hosted below:
# http://www.postgresqltutorial.com/postgresql-python/connect/

USER = "udgiapuy"
PASSWORD = "HVaHbqd1S07gXIvUJYSJQFw_X0z25WhM"
print('python db_integration_test.py')

import psycopg2

# Establish a connection to the database by creating a cursor object
conn = psycopg2.connect(host="john.db.elephantsql.com", port = 5432, database=USER, user=USER, password=PASSWORD)

# Create a cursor object
cur = conn.cursor()

is_failed = False
def check_integrity(actual, expected, scenario):
    if actual != expected:
        is_failed = True
        print('Data integrity compromised for {}.'.format(scenario))
    else:
        print('Data integrity maintained for {}.'.format(scenario))

# A simple query to create a dummy table in the database
try:
    cur.execute('select * from foo')
    query_results = cur.fetchall()
    if query_results == []:
        print('Table foo already exist, aborting.')
        cur.close()
        conn.close()
except Exception as e:
    conn.rollback()
cur.execute('create table foo(id serial PRIMARY KEY, name VARCHAR(10) UNIQUE NOT NULL);')
conn.commit()

# Check data integrity for table creation
cur.execute('select * from foo')
check_integrity(cur.fetchall(), [], 'Table creation')
# Insertion
cur.execute('insert into foo (id, name) VALUES (1, \'test_name\');')
cur.execute('select * from foo')
check_integrity(cur.fetchall(), [(1, 'test_name')], 'Insertion')
# Updating
cur.execute('update foo set id = 2 where id = 1;')
cur.execute('select * from foo')
check_integrity(cur.fetchall(), [(2, 'test_name')], 'Updating')
# Deletion
cur.execute('delete from foo where id = 2;')
cur.execute('select * from foo')
check_integrity(cur.fetchall(), [], 'Deletion')

# Clean up
cur.execute('drop table foo;')
conn.commit()

# Close the cursor and connection to so the server can allocate
cur.close()
conn.close()

if is_failed:
    print('### At least one test failed ###')
else:
    print('### All tests passed ###')
