import queue
import json

class Node(object):
    def __init__(self, node_type, relation_name, schema, alias, group_key, sort_key, join_type, index_name,
                 hash_cond, table_filter, index_cond, merge_cond, recheck_cond, join_filter, subplan_name, actual_rows,
                 actual_time):
        self.node_type = node_type
        self.children = []
        self.relation_name = relation_name
        self.schema = schema
        self.alias = alias
        self.group_key = group_key
        self.sort_key = sort_key
        self.join_type = join_type
        self.index_name = index_name
        self.hash_cond = hash_cond
        self.table_filter = table_filter
        self.index_cond = index_cond
        self.merge_cond = merge_cond
        self.recheck_cond = recheck_cond
        self.join_filter = join_filter
        self.subplan_name = subplan_name
        self.actual_rows = actual_rows
        self.actual_time = actual_time

    def add_children(self, child):
        self.children.append(child)

    def set_output_name(self, output_name):
        if "T" == output_name[0] and output_name[1:].isdigit():
            self.output_name = int(output_name[1:])
        else:
            self.output_name = output_name

    def get_output_name(self):
        if str(self.output_name).isdigit():
            return "T" + str(self.output_name)
        else:
            return self.output_name

    def set_step(self, step):
        self.step = step


# Phase 1
def parse_json(json_string):
    q = queue.Queue()
    q_node = queue.Queue()
    json_obj = json.loads(json_string)
    plan = json_obj[0]['Plan']
    q.put(plan)
    q_node.put(None)

    while not q.empty():
        current_plan = q.get()
        parent_node = q_node.get()

        relation_name = schema = alias = group_key = sort_key = join_type = index_name = hash_cond = table_filter \
            = index_cond = merge_cond = recheck_cond = join_filter = subplan_name = actual_rows = actual_time = None
        if 'Relation Name' in current_plan:
            relation_name = current_plan['Relation Name']
        if 'Schema' in current_plan:
            schema = current_plan['Schema']
        if 'Alias' in current_plan:
            alias = current_plan['Alias']
        if 'Group Key' in current_plan:
            group_key = current_plan['Group Key']
        if 'Sort Key' in current_plan:
            sort_key = current_plan['Sort Key']
        if 'Join Type' in current_plan:
            join_type = current_plan['Join Type']
        if 'Index Name' in current_plan:
            index_name = current_plan['Index Name']
        if 'Hash Cond' in current_plan:
            hash_cond = current_plan['Hash Cond']
        if 'Filter' in current_plan:
            table_filter = current_plan['Filter']
        if 'Index Cond' in current_plan:
            index_cond = current_plan['Index Cond']
        if 'Merge Cond' in current_plan:
            merge_cond = current_plan['Merge Cond']
        if 'Recheck Cond' in current_plan:
            recheck_cond = current_plan['Recheck Cond']
        if 'Join Filter' in current_plan:
            join_filter = current_plan['Join Filter']
        if 'Actual Rows' in current_plan:
            actual_rows = current_plan['Actual Rows']
        if 'Actual Total Time' in current_plan:
            actual_time = current_plan['Actual Total Time']
        if 'Subplan Name' in current_plan:
            if "returns" in current_plan['Subplan Name']:
                name = current_plan['Subplan Name']
                subplan_name = name[name.index("$"):-1]
            else:
                subplan_name = current_plan['Subplan Name']

        current_node = Node(current_plan['Node Type'], relation_name, schema, alias, group_key, sort_key, join_type,
                            index_name, hash_cond, table_filter, index_cond, merge_cond, recheck_cond, join_filter,
                            subplan_name, actual_rows, actual_time)

        if "Limit" == current_node.node_type:
            current_node.plan_rows = current_plan['Plan Rows']

        if "Scan" in current_node.node_type:
            if "Index" in current_node.node_type:
                if relation_name:
                    current_node.set_output_name(relation_name + " with index " + index_name)
            elif "Subquery" in current_node.node_type:
                current_node.set_output_name(alias)
            else:
                current_node.set_output_name(relation_name)

        if parent_node is not None:
            parent_node.add_children(current_node)
        else:
            head_node = current_node

        if 'Plans' in current_plan:
            for item in current_plan['Plans']:
                # push child plans into queue
                q.put(item)
                # push parent for each child into queue
                q_node.put(current_node)

    return head_node


def convert_tree_string(node):
    if len(node.children) == 0:
        print(node.node_type)
        return node.node_type

    lstr = "("

    for n in node.children:
        print(node.node_type)
        lstr += convert_tree_string(n) + ","

    lstr = lstr[:-1]

    lstr += ")%s" % node.node_type
    print(lstr)
    return lstr
