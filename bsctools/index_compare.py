"""
=====================================================================
taxoncompare - combine 16S and refseq species identification result
=====================================================================
"""

import sys
import re

def output_file_clean(file_header):
	output_filename = file_header + ".combine_annotation.txt"
	f = open(output_filename,'w')
	f.seek(0)
	f.truncate()
	f.close()
	return(output_filename)

def taxoncompare(refseq_result,silva_result,file_header):
    barcode_species = {}

    for i in range(0,len(refseq_result)):
        barcode = refseq_result[i].strip().split("\t")[0]
        rate1 = float(refseq_result[i].strip().split("\t")[4])
        rate2 = float(silva_result[i].strip().split("\t")[4])
        index1 = refseq_result[i].strip().split("\t")[5]
        index1_list = index1.split("|")
        index2 = silva_result[i].strip().split("\t")[5]
        if int(silva_result[i].strip().split("\t")[3]) > 4:
            index2 = re.findall(r"(.+\|[a-z]_[a-zA-Z0-9]+)",index2)[0]
            index2_list = index2.split("|")
        else:
            index2_list = [index2]

        if rate1 >= 0.95:
            barcode_species[barcode] = index1
        elif len(index1_list)>= len(index2_list) and index2_list[len(index2_list)-1] == index1_list[len(index2_list)-1]:
            barcode_species[barcode] = index1
        else:
            if rate1 >= rate2:
                barcode_species[barcode] = index1
            else:
                barcode_species[barcode] = index2
    
    output_filename = output_file_clean(file_header)
    f = open(output_filename,'a')
    for k,v in barcode_species.items():
        f.write("{}\t{}\n".format(k,v))
    f.close()


if __name__ =="__main__":
    ###refseq.barcode_count.txt
    f1 = open(sys.argv[1],'r')
    refseq_result = f1.readlines()
    f1.close()
    ###silva.barcode_count.txt
    f2 = open(sys.argv[2],'r')
    silva_result = f2.readlines()
    f2.close()
    ##Output file header
    file_header = str(sys.argv[3])
    taxoncompare(refseq_result,silva_result,file_header)