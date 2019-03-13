from debugprov.navgiation_strategy import NavigationStrategy
from debugprov.node import Node
from debugprov.validity import Validity
from debugprov.execution_tree import ExecutionTree

class DivideAndQuery(NavigationStrategy):

    def navigate(self):
        self.recursive_navigate(self.exec_tree.root_node)
        return self.exec_tree

    def find_best_guess(self, node:Node, w_2:float):
        if node.weight <= w_2 and node.validity is Validity.UNKNOWN:
            if (self.best_guess is None):
                self.best_guess = node
            elif node.weight > self.best_guess.weight:
                self.best_guess = node
        for c in node.childrens:
            if c.validity is not Validity.VALID:
                self.find_best_guess(c, w_2)

    def weight(self, node: Node):
        summ = 0
        for c in node.childrens:
            if c.validity is Validity.UNKNOWN or c.validity is Validity.INVALID:
                summ += 1 + self.weight(c)
            elif c.validity is Validity.NOT_IN_PROV:
                summ += self.weight(c)
        node.weight = summ
        return summ

    def recursive_navigate(self, node: Node):
        self.weight(node)
        self.best_guess = None
        self.find_best_guess(node, (node.weight/2))
        if self.best_guess is not None:
            self.evaluate(self.best_guess)
            if self.best_guess.validity is Validity.VALID:
                if self.best_guess.parent.has_childrens_with_validity(Validity.UNKNOWN):
                    self.recursive_navigate(node)
                else:
                    self.exec_tree.buggy_node = self.best_guess.parent
                    self.finish_navigation()
            elif self.best_guess.validity is Validity.INVALID:
                if self.best_guess.has_childrens_with_validity(Validity.UNKNOWN):
                    self.recursive_navigate(node)
                else:
                    self.exec_tree.buggy_node = self.best_guess
                    self.finish_navigation()


            