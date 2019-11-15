from NodesComparison import NodesComparison
from Connection import Connection
from Session import Session
import vocalizer2
import json

# query_one = '''
# select *
# from supplier, region, nation
# where supplier.s_nationkey = nation.n_nationkey and nation.n_regionkey = region.r_regionkey
# '''

# query_one = '''
# SELECT *
# FROM customer JOIN orders
# ON c_custkey = o_custkey
# JOIN lineitem
# ON o_orderkey = l_orderkey
# WHERE c_mktsegment = 'HOUSEHOLD';
# '''
#
# query_two = '''
# SELECT *
# FROM customer JOIN orders
# ON c_custkey = o_custkey
# WHERE o_custkey = 78002;
# '''



# query_two = '''
# SELECT *
# FROM customer JOIN orders
# ON c_custkey = o_custkey
# JOIN lineitem
# ON o_orderkey = l_orderkey
# WHERE o_custkey = 78002;
# '''


# query_two = '''
# SELECT *
# FROM region JOIN nation
# ON r_regionkey = n_regionkey
# '''

# query_one = '''
# SELECT * FROM nation, customer, orders, region
# WHERE orders.o_custkey = customer.c_custkey
# AND customer.c_nationkey = nation.n_nationkey
# AND nation.n_regionkey = region.r_regionkey
# AND customer.c_custkey = 20;
# '''
#
# query_two = '''
# SELECT * FROM nation, customer, orders, region
# WHERE orders.o_custkey = customer.c_custkey
# AND customer.c_nationkey = nation.n_nationkey
# AND nation.n_regionkey = region.r_regionkey
# AND region.r_regionkey = 0;
# '''

# query_two = '''
# SELECT * FROM
# region CROSS JOIN nation
# '''

# query_one = '''
# SELECT * FROM customer, orders
# WHERE c_custkey = o_custkey
# '''
#
# query_two = '''
# SELECT * FROM customer, orders
# WHERE c_custkey = o_custkey
# AND c_custkey = 20;
# '''

# # comparison 1
# query_one = '''
# SELECT * FROM customer NATURAL JOIN orders;
# '''
#
# query_two ='''
# SELECT * FROM customer JOIN orders ON C_CUSTKEY = O_CUSTKEY
# ORDER BY C_CUSTKEY;
# '''


# comparison 2
# query_one = '''
# SELECT * FROM part JOIN lineitem
# ON P_PARTKEY = L_PARTKEY;
# '''
#
# query_two = '''
# SELECT * FROM part JOIN lineitem
# ON P_PARTKEY = L_PARTKEY
# ORDER BY P_PARTKEY;
# '''

# comparison 3
# query_one ='''
# SELECT *
# FROM customer JOIN orders
# ON c_custkey = o_custkey
# JOIN lineitem
# ON o_orderkey = l_orderkey
# WHERE c_mktsegment = 'HOUSEHOLD';
# '''
#
# query_two = '''
# SELECT *
# FROM customer JOIN orders
# ON c_custkey = o_custkey
# JOIN lineitem
# ON o_orderkey = l_orderkey
# WHERE o_custkey = 78002;
# '''

# comparison 4
# query_one = '''
# SELECT *
# FROM nation, customer, orders, region
# WHERE orders.o_custkey = customer.c_custkey
# AND customer.c_nationkey = nation.n_nationkey
# AND nation.n_regionkey = region.r_regionkey
# AND customer.c_custkey = 20;
# '''
#
# query_two = '''
# SELECT *
# FROM nation, customer, orders, region
# WHERE orders.o_custkey = customer.c_custkey
# AND customer.c_nationkey = nation.n_nationkey
# AND nation.n_regionkey = region.r_regionkey
# AND region.r_regionkey = 0;
# '''

# comparison 5
# query_one = '''
# SELECT *
# FROM supplier, lineitem, part
# WHERE supplier.s_suppkey = lineitem.l_suppkey
# AND lineitem.l_partkey = part.p_partkey
# '''
#
# query_two = '''
# SELECT * FROM
# supplier, lineitem, orders
# WHERE s_suppkey = l_suppkey AND l_orderkey = o_orderkey;
# '''


# comparison 6
query_one = '''
SELECT supplier.s_suppkey, supplier.s_name, supplier.s_acctbal, nation.n_name
FROM supplier, nation
WHERE supplier.s_nationkey = nation.n_nationkey
AND nation.n_name = 'GERMANY'
GROUP BY supplier.s_suppkey, nation.n_name
ORDER BY supplier.s_acctbal
'''

query_two='''
SELECT supplier.s_suppkey, supplier.s_name, supplier.s_acctbal, nation.n_name
FROM supplier, nation
WHERE supplier.s_nationkey = nation.n_nationkey
AND nation.n_name = 'GERMANY'
GROUP BY supplier.s_suppkey
ORDER BY supplier.s_acctbal
'''
'''
# ---- yi ern and kenneth -----

# query_one = '''
# SELECT *
# FROM supplier, lineitem, part
# WHERE supplier.s_suppkey = lineitem.l_suppkey
# AND lineitem.l_partkey = part.p_partkey
# '''
#
# query_two = '''
# SELECT * FROM
# supplier, lineitem, orders
# WHERE s_suppkey = l_suppkey AND l_orderkey = o_orderkey;
# '''

con = Connection()
con.connect()
session = Session(con,query_one,query_two)
print("Query 1 json: ")
print(str(json.dumps(session.query_one_qep_raw)))

print("Query 2 json: ")
print(str(json.dumps(session.query_two_qep_raw)))
head_node = vocalizer2.parse_json(session.query_two_qep_raw)
print(head_node)
steps = vocalizer2.textVersion(head_node)
print(steps)

nc = NodesComparison(session.query_one_qep_root_node,session.query_two_qep_root_node)
nc.compare_joins()