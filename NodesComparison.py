import collections


class NodesComparison:
    def __init__(self, head_node_1, head_node_2):
        self.head_node_1 = head_node_1
        self.head_node_2 = head_node_2
        self.store_get_all_nodes_type = []
        self.store_get_tables_for_join = []
        self.list_joins = ['Nested Loop', 'Hash Join', 'Merge Join']
        self.unique_tables_for_both_query = []

    """
    recursive function to get all the node based on the node types
    """
    def get_all_node_type(self, node, request_node_type):
        if node.node_type in request_node_type:
            self.store_get_all_nodes_type.append(node)
        for child in node.children:
            self.get_all_node_type(child, request_node_type)

    """
    recursive function to get the tables used for join
    access self.store_get_tables_for_join for the list of tables used for join
    """
    def get_tables_for_join(self, node):
        if node.relation_name != None:
            self.store_get_tables_for_join.append(node)

        if node.children != None:
            for child_node in node.children:
                self.get_tables_for_join(child_node)

    ## get tables node for a join
    def get_tables_for_join(self, node):
        if node.relation_name != None:
            self.store_get_tables_for_join.append(node)

        if node.children != None:
            for child_node in node.children:
                self.get_tables_for_join(child_node)

    # populate the table attribute for those node type has a join.
    # populate with the nodes.
    def populate_tables_to_join_nodes(self, node):
        # if node.node_type is in one of the joins
        if node.node_type in self.list_joins:
            self.store_get_tables_for_join.clear()
            self.get_tables_for_join(node)
            node.tables = self.store_get_tables_for_join.copy()

        for child in node.children:
            self.populate_tables_to_join_nodes(child)

    def populate_nodes_with_level(self,node,starting_level):
        if node.node_type != None:
            node.level = starting_level
        for child in node.children:
            self.populate_nodes_with_level(child ,starting_level+1)

    # unused
    def get_node_and_tables(self, list_node_type):
        nodes_and_tables = []
        for node in list_node_type:
            self.store_get_tables_for_join.clear()
            self.get_tables_for_join(node)
            tables = self.store_get_tables_for_join.copy()
            nodes_and_tables.append([node, tables])

        return nodes_and_tables

    def compare_joins(self):
        compareString = ""
        # clear attribute of this class
        self.store_get_all_nodes_type.clear()
        self.store_get_tables_for_join.clear()

        # We populate the 'tables' attribute for those node has a join type (Merge Join, Nested Loop, Hash Join).
        # It will populate with Node object, and not the table name instead.
        # e.g Hash Join uses relation table of Customer and Order. Hence, In the Hash Join, the 'tables' attribute keeps the Node Object
        # of Customer and Order in an array.
        self.populate_tables_to_join_nodes(self.head_node_1)
        self.populate_tables_to_join_nodes(self.head_node_2)

        # We populate the 'level' attribute for all the nodes in both query 1 and query 2.
        self.populate_nodes_with_level(self.head_node_1, 1) # starting level is 1 - Means the highest level of the tree has a level of 1.
        self.populate_nodes_with_level(self.head_node_2, 1)

        # get all nodes that has join type for Query 1
        self.get_all_node_type(self.head_node_1, self.list_joins)
        all_join_nodes_in_query_1 = self.store_get_all_nodes_type.copy()

        # We clear this so we can run the function, get_all_node_type, again for Query 2.
        self.store_get_all_nodes_type.clear()

        # get all nodes that has join type for Query 2
        self.get_all_node_type(self.head_node_2, self.list_joins)
        all_join_nodes_in_query_2 = self.store_get_all_nodes_type.copy()

        # We reverse the list so, the biggest node (in terms of no. of table joins - usually is the must top level of join node)
        # is at the back of the list.
        all_join_nodes_in_query_1.reverse()
        all_join_nodes_in_query_2.reverse()

        all_join_node_full_difference = []
        all_join_nodes_in_query_2_duplicate = all_join_nodes_in_query_2.copy()
        found = False
        for node2 in all_join_nodes_in_query_2:
            for node1 in all_join_nodes_in_query_1:
                if self.is_there_similiarities(node1, node2):
                    # check what is the difference between this two join nodes,
                    # and check whether they have the same table used, and the types of scan they used.
                    compareString += self.difference(node1, node2)

                    # store all the tables in the array so that for the next loop, it WILL NOT print duplicate changes.
                    self.store_tables(node1)
                    self.store_tables(node2)

                    # We remove from the nodes involved over here from the lists.
                    all_join_nodes_in_query_1.remove(node1)
                    all_join_nodes_in_query_2_duplicate.remove(node2)
                    found = True
                    break

                # Did not find any join nodes in Query 1 that is similar.
                # Hence, we deem this join node (and its tables joined) is totally different from Query 1.
                if found != False:
                    all_join_nodes_in_query_2_duplicate.remove(node1)
                    all_join_node_full_difference.append(node2)


        # Whatever left in query 1 is not used in Query 2. Hence, we just display the changes out.
        for node in all_join_nodes_in_query_1:
            string_table = ""
            for table in node.tables:
                string_table = string_table + table.relation_name + " "
            string_table = string_table.strip()
            compareString = "The "+node.node_type +" node with tables of "+string_table+" in Query 1 is not used in Query 2." + "\n"

        # Those nodes that are not similar at all, will be push to all_join_node_full_difference
        # We can say this nodes is does not appear in the previous query (query 1) at all.
        for node in all_join_node_full_difference:
            string_table = ""
            for table in node.tables:
                string_table = string_table + table.relation_name + " "
            string_table = string_table.strip()
            compareString += "There is a new "+node.node_type+" node with tables of "+string_table+ " in Query 2 " +"\n"

        return compareString

    def store_tables(self, node):
        for node in node.tables:
            if node.relation_name not in self.unique_tables_for_both_query:
                self.unique_tables_for_both_query.append(node.relation_name)


    def is_there_similiarities(self, node1, node2):
        dependency_nodes_1 = node1.tables
        dependency_nodes_2 = node2.tables

        total_matches = 0
        # index2 = 0
        match = False
        for node1 in dependency_nodes_1:
            for node2 in dependency_nodes_2:
                if node1.relation_name == node2.relation_name:
                    return True

        if match == False:
            return False

    # check whether both join node uses the same/different no. of tables,
    # and check whether the tables that are the same uses the same scan (index, bitmap, seq scan)
    def difference(self, node1, node2):
        diffString = ""
        previous_node = node1
        current_node = node2
        if node1.node_type != node2.node_type:
            diffString += "The "+node1.node_type + " (Level " + str(node1.level) + ") in Query 1 has evolved to " + node2.node_type + " (Level "+ str(node2.level) + ") in Query 2" + "\n"

        dependency_nodes_1 = node1.tables.copy()  # query 1
        dependency_nodes_2 = node2.tables.copy()  # query 2

        table_pairs_nodes = []
        # Lets do a n^2 comparison (not always n^2 as we will be removing items from inner loop)
        # And then we create table pairs for the Query 1 and Query 2
        # e.g [[A],[A]] -> The first array contains the relation that is found in Query 1. The second array contains the relation that is found in Query 2.
        # Both must has the same relation, which is A - for this example. Note that we will be keeping the Node Object instead of the relation name.
        #e.g [[A],[]] -> This pair could happen too. It means A is found in Query 1, but not in Query 2.
        # However, for this pair, [[],[A]], it will not happen. Although it is valid to say that A is only found in Query 2,
        # we decided to take what is left over in dependency_nodes_2.
        for node1 in dependency_nodes_1:
            found = False
            for node2 in dependency_nodes_2:
                # print("Accessing "+node1.relation_name + "="+node2.relation_name)
                if (node1.relation_name == node2.relation_name):
                    table_pairs_nodes = self.insert_table_pairs(node1, node2, table_pairs_nodes)
                    dependency_nodes_2.remove(node2)
                    found = True

            # if is not found, then we add a table pair with 2nd array being empty. (not found in Q2)
            if found == False:
                table_pairs_nodes = self.insert_table_pairs(node1, None, table_pairs_nodes)

        # remove all matching scan type of the tables for both query
        table_pairs = table_pairs_nodes.copy()
        for pair in table_pairs:
            if pair[0][0].relation_name not in self.unique_tables_for_both_query:
                if len(pair[0]) > 0 and len(pair[1]) > 0:
                    for node1 in pair[0]:
                        for node2 in pair[1]:
                            # If both has the same node_type
                            # e.g Seq Scan == Seq Scan
                            if (node1.node_type == node2.node_type):
                                pair[0].remove(node1)
                                pair[1].remove(node2)

        # remove empty pairs
        i = 0
        while i < len(table_pairs):
            if len(table_pairs[i][0]) == 0 and len(table_pairs[i][1]) == 0:
                del table_pairs[i]
            else:
                i+=1

        # print the difference in scan type for the same tables.
        for pair in table_pairs:
            if pair[0][0].relation_name not in self.unique_tables_for_both_query:
                for node1 in pair[0]:
                    for node2 in pair[1]:
                        # print("With the evolved "+current_node.node_type+", the type of scan has evolve from "+node1.node_type +" to "+node2.node_type +" for the table, "+node1.relation_name)
                        diffString += "With the evolved "+current_node.node_type+ ", the type of scan has evolve from " + node1.node_type + " to " + node2.node_type + " for the table, " + node1.relation_name + "\n"
                        pair[0].remove(node1)
                        pair[1].remove(node2)

        # remove those empty pairs E.g [[],[]]
        i = 0
        while i < len(table_pairs):
            if len(table_pairs[i][0]) == 0 and len(table_pairs[i][1]) == 0:
                del table_pairs[i]
            else:
                i += 1

        tables_used_in_q1_only = False
        tables_used_in_q2_only = False

        string_table_used_in_q1_but_not_in_q2 = ""
        for pair in table_pairs:
            if len(pair[1]) == 0:
                if pair[0][0].relation_name not in self.unique_tables_for_both_query:
                    tables_used_in_q1_only = True
                    string_table_used_in_q1_but_not_in_q2 = string_table_used_in_q1_but_not_in_q2 + pair[0][0].relation_name + " "

        string_table_used_in_q2_but_not_in_q1 = ""

        for node in dependency_nodes_2:
            if node.relation_name not in self.unique_tables_for_both_query:
                tables_used_in_q2_only = True
                string_table_used_in_q2_but_not_in_q1 = string_table_used_in_q2_but_not_in_q1 + node.relation_name + " "

        string_table_used_in_q2_but_not_in_q1 = string_table_used_in_q2_but_not_in_q1.strip()
        string_table_used_in_q1_but_not_in_q2 = string_table_used_in_q1_but_not_in_q2.strip()


        # if there are tables in used in q1 and tables used in q2. We know that there tables in q1 is not used in q2.
        if tables_used_in_q1_only and tables_used_in_q2_only:
            diffString += "It seems like the tables ("+string_table_used_in_q1_but_not_in_q2 + \
                  ") for "+previous_node.node_type+" (Level "+str(previous_node.level) + \
                  ") in Query 1 is replaced with tables ("+string_table_used_in_q2_but_not_in_q1 + ") for "+current_node.node_type+" (Level "+str(current_node.level)+") in Query 2" + "\n"
        elif(not tables_used_in_q1_only and tables_used_in_q2_only):
            # If there is no tables in q1, and there is table in q2. We can say that there are new tables used in Q2
            diffString += "It seems like that there is new tables ("+string_table_used_in_q2_but_not_in_q1+") used in Q2" + "\n"
        elif(tables_used_in_q1_only and not tables_used_in_q2_only):
            # If there is tables in q1 but there is no table in q2. We can say that those tables in Q1 is not in Q2
            diffString += "It seems like the "+current_node.node_type+" (Level "+str(current_node.level)+") for Query 2 did not use the tables ("+string_table_used_in_q1_but_not_in_q2+") used by the "+previous_node.node_type+" (Level "+str(previous_node.level)+") in Query 1 at all."+"\n"

        return diffString


    def insert_table_pairs(self, node1, node2, table_pairs):
        found = False
        for pair in table_pairs:
            # if found, append into the pair
            if node1.relation_name in pair[0]:
                found = True
                pair[0].append(node1)
                if node2 != None:
                    pair[1].append(node2)

        # if not found, create a new pair.
        if found == False:
            if node2 != None:
                table_pairs.append([[node1], [node2]])
            else:
                table_pairs.append([[node1], []])

        return table_pairs

