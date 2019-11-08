from parser import parse_json, convert_tree_string
from ete3 import Tree
import json


class Session:
    def __init__(self, connection, query_one, query_two):
        self.connection = connection
        self.query_one = query_one
        self.query_two = query_two
        self.query_one_qep_raw = connection.query_json(query_one)
        self.query_two_qep_raw = connection.query_json(query_two)
        self.query_one_qep_root_node = parse_json(json.dumps(self.query_one_qep_raw))
        self.query_two_qep_root_node = parse_json(json.dumps(self.query_two_qep_raw))

        query_one_tree_string = convert_tree_string(self.query_one_qep_root_node)
        query_two_tree_string = convert_tree_string(self.query_two_qep_root_node)

        self.query_one_graph = Tree(query_one_tree_string+";", format=1)
        self.query_two_graph = Tree(query_two_tree_string+";", format=1)

    def show_query_one_graph(self):
        self.query_one_graph.show()

    def show_query_two_graph(self):
        self.query_two_graph.show()
