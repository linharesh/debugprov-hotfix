from graphviz import Graph

from execution_tree import ExecutionTree
from node import Node
from validity import Validity

class Visualization:

    PROVENANCE_COLOR = 'magenta2'
    PROV_PRUNED_NODE = 'grey64'

    def __init__(self, exec_tree: ExecutionTree):
        self.exec_tree = exec_tree
        self.graph = Graph('exec_tree', filename='exec_tree.gv')
        self.graph.attr('node', shape='box')

    def view_exec_tree(self):
        root_node = self.exec_tree.root_node
        self.graph.node(str(root_node.id), root_node.name, fillcolor='red', style='filled')
        self.navigate(root_node)
        self.graph.view()

    def view_exec_tree_prov(self, dependencies:list):
        root_node = self.exec_tree.root_node
        self.graph.node(str(root_node.id), root_node.name, fillcolor='red', style='filled')
        self.navigate(root_node)
        for d in dependencies: # this loop draws the provenance links between nodes
            if d.source.typeof == 'STARTER':
                self.graph.node(str(d.source.id), d.source.name, shape='none', fontcolor=self.PROVENANCE_COLOR, dir='forward')
                target_nodes = exec_tree.search_for_node_by_ccid(d.target.id)
                for tn in target_nodes:
                    self.graph.edge(str(d.source.id), str(tn.id), None, color=self.PROVENANCE_COLOR, dir='forward')
            else:
                source_nodes = exec_tree.search_for_node_by_ccid(d.source.id)
                target_nodes = exec_tree.search_for_node_by_ccid(d.target.id)
                for sn in source_nodes:
                    for tn in target_nodes:
                        self.graph.edge(str(sn.id), str(tn.id), None, color=self.PROVENANCE_COLOR, dir='forward')
        self.graph.view()

    def navigate(self, node:Node):
        chds = node.childrens

        for n in chds:
            self.graph.edge(str(node.id), str(n.id), None, dir='forward')
            if n.validity == Validity.INVALID:
                self.graph.node(str(n.id), str(n.name), fillcolor='red', style='filled')
            elif n.validity == Validity.VALID: 
                self.graph.node(str(n.id), str(n.name), fillcolor='green', style='filled')
            elif n.validity == Validity.UNKNOWN:  
                self.graph.node(str(n.id), str(n.name))
            # Uncomment this block to paint not-in-provenance removed nodes with grey
            #    if n.prov is None or n.prov is False:
            #        self.graph.node(str(n.id), str(n.name), fillcolor=self.PROV_PRUNED_NODE, style='filled')
            #    else:
            #        self.graph.node(str(n.id), str(n.name))

        if len(chds) > 0:
            g = Graph()
            for c in chds:
                g.node(str(c.id))
            g.graph_attr['rank']='same'
            self.graph.subgraph(g)

        for n in chds: 
            self.navigate(n)

    