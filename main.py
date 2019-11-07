from Connection import Connection
import json
from parser import parse_json
from pprint import pprint
import svgling
from parser import Node


def main():
    conn = Connection()
    conn.override_configuration(host="localhost", password="dsp")
    conn.connect()
    query = """
    select
        orders_id,
        sum(extended_price * (1 - discount)) as revenue,
        order_date,
        ship_priority
    from
        customer,
        orders,
        lineitem
    where
        market_segment = 'HOUSEHOLD'
        and customer.id = orders.customer_id
        and lineitem.orders_id = orders.id
        and orders.order_date < date '1995-03-21'
        and lineitem.ship_date > date '1995-03-21'
    group by
        lineitem.orders_id,
        orders.order_date,
        orders.ship_priority
    order by
        revenue desc,
        orders.order_date
    limit 10;
    """

    data = conn.query_json(query)
    node = parse_json(json.dumps(data))

    pprint(vars(node.children[0]))

    print(print_node(node))


def print_node(node):
    ls = [node.node_type]

    for n in node.children:
        ls.append(print_node(n))

    return ls


if __name__ == '__main__':
    main()
