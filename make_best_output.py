#!/usr/bin/env python3

import sys

if len(sys.argv) != 3:
    print("Uso: python make_output_best.py input.tsv output_best.tsv")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

best = {}

with open(input_file) as f:
    for line in f:

        line = line.strip()

        if not line:
            continue

        cols = line.split()

        if len(cols) < 5:
            continue

        q = cols[0]
        t = cols[1]
        pid = float(cols[2])
        length = int(cols[3])
        score = float(cols[4])

        # trata A-B e B-A como o mesmo par
        pair = tuple(sorted([q, t]))

        if pair not in best:
            best[pair] = (q, t, pid, length, score)

        else:
            _, _, old_pid, old_length, old_score = best[pair]

            # mantém o alinhamento de maior score
            if score > old_score:
                best[pair] = (q, t, pid, length, score)

with open(output_file, "w") as out:

    for pair in sorted(best):

        q, t, pid, length, score = best[pair]

        out.write(
            "%s\t%s\t%.2f\t%d\t%.1f\n"
            % (q, t, pid, length, score)
        )

print("Input alignments :", sum(1 for _ in open(input_file)))
print("Unique pairs     :", len(best))
print("Output file      :", output_file)