import collections


def intersection(first_node_list, second_node_list):
    results = []
    for n in first_node_list:
        for nn in second_node_list:
            if(n.relation_name == nn. relation_name):
                results.append(n)

    return results



def diff(first_node_list, second_node_list):
    results = []
    for n in first_node_list:
        found = False
        for nn in second_node_list:
            if n.relation_name == nn.relation_name:
                if n.node_type == nn.node_type:
                    found = True
                else:
                    s = dict()
                    s['L']
                found = True
        # end inner for
        if not found:
            results.append(n)
    # end outer for




def sets_info(left_node_list, right_node_list):
    result = dict()
    result["L"] = diff(left_node_list, right_node_list)
    result["R"] = diff(right_node_list, left_node_list)
    result["I"] = intersection(left_node_list, right_node_list)
    print(result)


class NodesComparison:
    def __init__(self, head_node_1,head_node_2):
        self.head_node_1 = head_node_1
        self.head_node_2 = head_node_2
        self.store_get_all_nodes_type_1 = [] # stores the requested node. please clear if you want to retrieve a new set of nodes
        self.store_get_all_nodes_type_2 = []
        self.store_get_tables_for_join = []
        self.list_joins = ['Nested Loop', 'Hash Join', 'Merge Join']

    def get_all_node_type(self,node, request_node_type, select_node):
        if node.node_type in request_node_type:
            if select_node == 1:
                self.store_get_all_nodes_type_1.append(node)
            elif select_node == 2:
                self.store_get_all_nodes_type_2.append(node)
        for child in node.children:
            self.get_all_node_type(child, request_node_type,select_node)

    """
    recursive function to get the tables used for join
    access self.store_get_tables_for_join for the list of tables used for join
    """
    def get_tables_for_join(self,node):
        if node.relation_name != None:
            self.store_get_tables_for_join.append(node)

        if node.children != None:
            for child_node in node.children:
                self.get_tables_for_join(child_node)


    def get_node_and_tables(self, list_node_type):
        nodes_and_tables = []
        for node in list_node_type:
            self.store_get_tables_for_join.clear()
            self.get_tables_for_join(node)
            tables = self.store_get_tables_for_join.copy()
            nodes_and_tables.append([node, tables])

        return nodes_and_tables



    def compare_joins(self):

        pairs_different_join_but_same_table = []
        pairs_missing_join = [] # stores those missing joins in query 1 that is not found in query 2

        # clear attribute of this class
        self.store_get_all_nodes_type_1.clear()
        self.store_get_all_nodes_type_2.clear()
        self.store_get_tables_for_join.clear()

        # get all nodes that has join
        self.get_all_node_type(self.head_node_1, self.list_joins, 1)
        self.get_all_node_type(self.head_node_2, self.list_joins, 2)

        # print("List of joins in query 1:")
        # for node in self.store_get_all_nodes_type_1:
        #     print(node.node_type)
        #     for child in node.children:
        #         print(child.node_type)
        #     print("----")
        #
        # print("List of joins in query 2:")
        # for node in self.store_get_all_nodes_type_2:
        #     print(node.node_type)
        #     for child in node.children:
        #         print(child.node_type)
        #     print("----")

        # check for different join, and join with different tables
        nodes_and_tables_1 = self.get_node_and_tables(self.store_get_all_nodes_type_1)
        nodes_and_tables_2 = self.get_node_and_tables(self.store_get_all_nodes_type_2)

        # print("List of joins and their tables for first query:")
        # print(nodes_and_tables_1)
        # for nodes in nodes_and_tables_1:
        #     print(nodes[0].node_type)
        #     for child_nodes in nodes[1]:
        #         print(child_nodes.node_type + " on "+child_nodes.relation_name)
        #     print("---")
        # print("List of joins and their tables for second query:")
        # print(nodes_and_tables_2)
        # for nodes in nodes_and_tables_2:
        #     print(nodes[0].node_type)
        #     for child_nodes in nodes[1]:
        #         print(child_nodes.node_type + " on "+child_nodes.relation_name)
        #     print("---")

        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

        count_node2 = 0
        match = False
        for node1 in nodes_and_tables_1:
            for node2 in nodes_and_tables_2:

                relation_name_array_1 = self.convert_node_array_to_relation_name_array(node1[1])
                relation_name_array_2 = self.convert_node_array_to_relation_name_array(node2[1])

                # if both joins uses the same tables, but different type of join
                if compare(relation_name_array_1,relation_name_array_2) and node1[0].node_type != node2[0].node_type:
                    print(node1[0].node_type + " in query 1 has evolved to "+node2[0].node_type + " and still uses the same tables ("+','.join(relation_name_array_2)+")")

                    leave_nodes_array_1 = node1[1]
                    leave_nodes_array_2 = node2[1]

                    # now lets compare the leaves nodes of the join.
                    for leave_node1 in leave_nodes_array_1:
                        for leave_node2 in leave_nodes_array_2:
                            # if we found a matching table for both query,
                            #print(leave_node1.node_type + " "+leave_node2.node_type +" "+leave_node1.relation_name + " "+leave_node2.relation_name)
                            if leave_node1.relation_name == leave_node2.relation_name:
                                if leave_node1.node_type != leave_node2.node_type:
                                    print("In addition, for the table, "+leave_node2.relation_name+", the scan has changed from " +leave_node1.node_type + " to "+leave_node2.node_type)

                    del nodes_and_tables_2[count_node2] # remove item from array, since is already matched
                    match = True

                count_node2 = count_node2 + 1

            count_node2 = 0
            # if there is no match, this means that join is not found in query 2
            if match != True:
                relation_name_array = self.convert_node_array_to_relation_name_array(node1[1])
                print(node1[0].node_type +" (" +','.join(relation_name_array) + ") is not used in query 2 though.")
                match = False


    def convert_node_array_to_relation_name_array(self,node_array):
        relation_names = []
        for node in node_array:
            relation_names.append(node.relation_name)
        return relation_names


