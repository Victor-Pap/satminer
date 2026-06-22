#!/usr/bin/env python3

import sys
from collections import defaultdict

if len(sys.argv) != 4:
    print("Uso: python build_families.py output_best.tsv identidade_minima arquivo_saida")
    sys.exit(1)

tsv = sys.argv[1]
cutoff = float(sys.argv[2])
outfile = sys.argv[3]

graph = defaultdict(set)
all_nodes = set()

with open(tsv) as f:
    for line in f:
        cols = line.strip().split()

        if len(cols) < 5:
            continue

        q = cols[0]
        t = cols[1]
        ident = float(cols[2])

        all_nodes.add(q)
        all_nodes.add(t)

        if ident >= cutoff:
            graph[q].add(t)
            graph[t].add(q)

visited = set()
families = []

for node in sorted(all_nodes):

    if node in visited:
        continue

    stack = [node]
    component = []

    while stack:
        n = stack.pop()

        if n in visited:
            continue

        visited.add(n)
        component.append(n)

        for neigh in graph[n]:
            if neigh not in visited:
                stack.append(neigh)

    families.append(sorted(component))

families.sort(key=len, reverse=True)

with open(outfile, "w") as out:

    for i, fam in enumerate(families, start=1):
        out.write(
            "Family_%d\t%d\t%s\n" %
            (i, len(fam), ",".join(fam))
        )

print("Families:", len(families))
print("Output:", outfile)