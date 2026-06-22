#!/usr/bin/python

import sys
from Bio import SeqIO
from subprocess import call

print "Usage: rm_homology.py FastaFile"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce FASTA file: ")

data = SeqIO.parse(open(file), "fasta")
seq_dict = {}
seq_list = []

for s in data:
    seq_dict[str(s.id)] = str(s.seq)
    seq_list.append(str(s.id))

w = open(file+"homology", "w")
w.close()

for seq in seq_list:
    tmp_list = [x for x in seq_list if x != seq]
    tmp_out = "EMPTY"

    w = open("output", "a")
    w.write(seq+":\n")
    w.close()

    while True:
        
        tmp_query = open("tmp_query.fas", "w")
        tmp_db = open("tmp_db.fas", "w")

        tmp_query.write(">%s\n%s\n" % (seq, seq_dict[seq]))
        tmp_query.close()

        for tmp in tmp_list:
            tmp_db.write(">%s\n%s\n" % (tmp, seq_dict[tmp]))
        tmp_db.close()

        call("RepeatMasker -nolow -no_is -s -engine rmblast -lib tmp_db.fas tmp_query.fas", shell=True)

        tmp_out = open("tmp_query.fas.out").readlines()

        if len(tmp_out) <= 3:
            break
            
        print tmp_out

        call("rm -r tmp_query.fas.*", shell=True)

        if len(tmp_out) > 1:

            removed = 0

            for line in tmp_out[3:]:

                info = line.split()

                if len(info) < 11:
                    continue

                score = float(info[0])
                div = float(info[1])

                identity = 100.0 - div

                query = info[4]

                q_begin = int(info[5])
                q_end   = int(info[6])

                name = info[9]

                hit_len = q_end - q_begin + 1

                w = open("output.tsv", "a")

                w.write("%s\t%s\t%.2f\t%d\t%.1f\n" %
                            (query,
                             name,
                             identity,
                             hit_len,
                             score))

                w.close()
                try:
                    tmp_list.remove(name)
                    removed += 1
                except:
                    pass

            if removed == 0:
                print "No new contigs removed"
                break

        if len(tmp_list) == 0:
            break

        print "Remaining:", len(tmp_list)