#!/usr/bin/env python3.3
import random
import datetime
import sys

how_many_grammars = 11
terminals_bound = 15
nonterminals_bound = 10
production_number_bound = 5
max_prod_length = 5

TERMINALS = 'abcdefghijklmnopqrstuvwxyz'
NONTERMINALS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x[1] not in seen and not seen_add(x[1])]


class Grammar:
    nonterminals = []
    terminals = []
    symbols = []
    productions = {}
    uid = 0

    def __init__(self):
        self.terminals = random.sample(TERMINALS, terminals_bound)
        self.nonterminals = random.sample(NONTERMINALS, nonterminals_bound)
        self.symbols = self.terminals + self.nonterminals
        self.generate_productions()
        self.uid = random.randint(0, 100000000)

    def generate_productions(self):
        for nt in self.nonterminals:
            self.productions[nt] = []
            for i in range(1, random.randint(1, production_number_bound)):
                self.productions[nt].append(self.generate_production())
        self.remove_duplicates_from_productions()

    def remove_duplicates_from_productions(self):
        for k, prods in self.productions.items():
            new_prods = list(zip(prods, map(self.stringify_production, prods)))
            new_prods = remove_duplicates(new_prods)
            new_prods = [x[0] for x in new_prods]

    def generate_production(self):
        prod_length = abs(int(random.gauss(1, 5)))
        return [random.choice(self.symbols) for _ in range(prod_length)]

    def __repr__(self):
        return "Grammar", self.uid

    def stringify_production(self, production):
        str_prod = ' '.join(production)
        if len(str_prod) == 0:
            str_prod = u"\u03B5"
        return str_prod

    def __str__(self):
        string_lines = []
        for nt in self.nonterminals:
            prods = map(self.stringify_production, self.productions[nt])
            prods = ' | '.join(prods)
            new_line = "{} -> {}".format(nt, prods)
            string_lines.append(new_line)
        return '\n'.join(string_lines)

    def stringify_production_char(self, char):
        if char.isupper():
            return "nt('{}')".format(char)
        return char

    def stringify_production_pl(self, production):
        return "[{}]".format(','.join(map(self.stringify_production_char, production)))

    def string_for_prolog(self):
        string_parts = []
        for nt in self.nonterminals:
            prods = "[{}]".format(','.join(map(self.stringify_production_pl, self.productions[nt])))
            str_part = "prod('{}',{})".format(nt, prods)
            string_parts.append(str_part)
        return "[{}]".format(','.join(string_parts))


def main():
    random.seed(datetime.datetime.utcnow())
    x = Grammar()
    print(x, file=sys.stderr)
    print(x.string_for_prolog())


if __name__ == "__main__":
    main()
