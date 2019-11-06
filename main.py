from Connection import Connection


conn = Connection()
data = conn.query_json("SELECT * FROM customer;")
print(data)

data2 = conn.query_json("SELECT * FROM region")
print(data2)


