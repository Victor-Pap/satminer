#!/usr/bin/env python3

import re
import csv
import sys
from collections import defaultdict

# --------------------------------------------------
# Argumentos
# --------------------------------------------------

if len(sys.argv) != 4:
    print("Uso:")
    print("python align_to_landscape.py align_file families95.txt output.csv")
    sys.exit(1)

align_file = sys.argv[1]
families_file = sys.argv[2]
output_file = sys.argv[3]

# --------------------------------------------------
# Ler famílias
# --------------------------------------------------

contig2family = {}

with open(families_file) as f:
    for line in f:

        parts = line.strip().split("\t")

        if len(parts) < 3:
            continue

        family = parts[0]

        contigs = parts[2].split(",")

        for c in contigs:
            contig2family[c] = family

print("Contigs associados:", len(contig2family))

# --------------------------------------------------
# Ler align
# --------------------------------------------------

landscape = defaultdict(int)

with open(align_file) as f:
    lines = f.readlines()

for line in lines:

    line = line.strip()

    m = re.match(
        r'^\s*\d+\s+([\d\.]+)\s+[\d\.]+\s+[\d\.]+\s+\S+\s+(\d+)\s+(\d+)\s+\S+\s+[C]?\s*(CL\S+?)#',
        line
    )

    if not m:
        continue

    kimura = float(m.group(1))

    start = int(m.group(2))
    end = int(m.group(3))

    contig = m.group(4)

    hit_len = abs(end - start) + 1

    family = contig2family.get(contig)

    if family:

        bin_div = int(round(kimura))

        if bin_div > 50:
            bin_div = 50

        landscape[(family, bin_div)] += hit_len

# --------------------------------------------------
# Salvar CSV
# --------------------------------------------------

with open(output_file, "w") as out:

    writer = csv.writer(out)

    writer.writerow([
        "Family",
        "Divergence",
        "Abundance"
    ])

    for (family, div), abundance in sorted(landscape.items()):
        writer.writerow([
            family,
            div,
            abundance
        ])

print("Arquivo salvo:", output_file)
print("Linhas:", len(landscape))