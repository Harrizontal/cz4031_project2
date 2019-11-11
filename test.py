from NodesComparison import NodesComparison
from Connection import Connection
from Session import Session

query_one = '''
select *
from supplier, region, nation
where supplier.s_nationkey = nation.n_nationkey and nation.n_regionkey = region.r_regionkey
'''

query_two = '''
SELECT * FROM
region CROSS JOIN nation
'''
con = Connection()
con.connect()
session = Session(con,query_one,query_two)
nc = NodesComparison(session.query_one_qep_root_node,session.query_two_qep_root_node)
nc.compare_joins()