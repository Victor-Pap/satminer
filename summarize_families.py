#!/usr/bin/env python3

import csv
import sys

# --------------------------------------------------
# Verificar argumentos
# --------------------------------------------------

if len(sys.argv) != 2:
    print("Uso: python summarize_families.py arquivo.divsum")
    sys.exit(1)

divsum_file = sys.argv[1]

# --------------------------------------------------
# Ler arquivo divsum
# --------------------------------------------------

divsum = {}

with open(divsum_file) as f:
    for line in f:

        if line.startswith("Unspecified"):

            fields = line.split()

            repeat_name = fields[1]
            absLen = int(fields[2])
            kimura = float(fields[4])

            divsum[repeat_name] = {
                "absLen": absLen,
                "kimura": kimura
            }

print("Consensos encontrados:", len(divsum))

# --------------------------------------------------
# Função para processar famílias
# --------------------------------------------------

def process_families(family_file, output_file):

    out = []

    with open(family_file) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            parts = line.split("\t")

            if len(parts) < 3:
                continue

            family = parts[0]
            contigs = parts[2].split(",")

            total_absLen = 0
            weighted_div = 0
            valid_contigs = 0

            for contig in contigs:

                if contig not in divsum:
                    continue

                absLen = divsum[contig]["absLen"]
                kimura = divsum[contig]["kimura"]

                total_absLen += absLen
                weighted_div += absLen * kimura

                valid_contigs += 1

            if total_absLen > 0:
                mean_kimura = weighted_div / total_absLen
            else:
                mean_kimura = 0

            out.append([
                family,
                valid_contigs,
                total_absLen,
                round(mean_kimura, 3)
            ])

    out.sort(key=lambda x: x[2], reverse=True)

    with open(output_file, "w", newline="") as f:

        writer = csv.writer(f, delimiter="\t")

        writer.writerow([
            "Family",
            "N_variants",
            "Total_absLen",
            "Mean_Kimura"
        ])

        writer.writerows(out)

    print("Arquivo gerado:", output_file)

# --------------------------------------------------
# Executar
# --------------------------------------------------

process_families(
    "families95.txt",
    "family_summary.tsv"
)

process_families(
    "superfamilies80.txt",
    "superfamily_summary.tsv"
)