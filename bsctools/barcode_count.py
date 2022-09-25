"""
======================================================
barcodecount - count kraken species identification 
======================================================

This script use the result of kraken calculation and the output file contains the species ident of each bacteria 
"""

import sys
import copy
from collections import defaultdict


def output_file_clean(file_header):
	output_filename = file_header + ".barcode_count.txt"
	f = open(output_filename,'w')
	f.seek(0)
	f.truncate()
	f.close()
	return(output_filename)


def barcodecount(kraken_output, kraken_report_mpa_new, file_header):
	barcode_reads_count = {}
	barcode_classified_count = {}
	map_index_tag = defaultdict(list)
	index_id = defaultdict(list)
	index_species = {}
	
	output_filename = output_file_clean(file_header)
	f = open(output_filename,'a')

	for line in kraken_output:
		###Count reads number of every barcode
		barcode = line.strip().split("_")[1]	
		if barcode in barcode_reads_count:
			barcode_reads_count[barcode] = barcode_reads_count[barcode] + 1 
		else:
			barcode_reads_count[barcode] = 1
		###Count classified reads number of every barcode and get the species index number of each read
		if line.startswith('C'):
			map_index_tag[barcode].append(int(line.strip().split()[2]))
			if barcode in barcode_classified_count:
				barcode_classified_count[barcode] = barcode_classified_count[barcode] + 1
			else:
				barcode_classified_count[barcode] = 1

	###Get the dict about the relation of index and species name also the index relation tree 
	for read in kraken_report_mpa_new:
		read = read.strip()
		species_name = read.split("\t")[1]
		index_relation = read.split("\t")[2]
		deepest_index = int(read.split("\t")[0])
		list_index_relation = [int(j) for j in index_relation.split("|")]
		index_id[deepest_index] = list_index_relation
		index_species[deepest_index] = species_name

	###The threshold of index reads number which would be count 
	if min(barcode_classified_count.values()) >=500:
		reads_num_threshold = float(10/min(barcode_classified_count.values()))
	else:
		reads_num_threshold = 0.02


	barcode_reads_count = sorted(barcode_reads_count.items(),key = lambda x:x[1], reverse = True)
	for key,value in barcode_reads_count:
		barcode_index_dict = {}
		barcode_index_sum = {}

		if key not in barcode_classified_count:
			f.write('{}\t{}\t0\t0\t0\tThis cell is Unindentified.\n'.format(key, value))
			continue
		else:
			###Count reads number of every index which is up to threshold in one cell
			for index in set(map_index_tag[key]):
				if map_index_tag[key].count(index)>= len(map_index_tag[key])*reads_num_threshold:
					barcode_index_dict[index] = map_index_tag[key].count(index)
			if barcode_index_dict == {}:
				f.write('{}\t{}\t{}\t0\t0\tUndefined_taxon\n'.format(key, value,barcode_classified_count[key]))
				continue

			###Delete index which isn't in report.mpa.newx file
			barcode_index_list = [int(i) for i in barcode_index_dict.keys()]
			for index in barcode_index_list:
				if index not in index_id:
					del barcode_index_dict[index]

			###Conut index reads based on index_relation_algorithm
			barcode_index_sum = copy.deepcopy(barcode_index_dict)
			for i in range(0,len(barcode_index_dict.keys())-1):
				for j in range(i+1,len(barcode_index_dict.keys())):
					test_index_i = list(barcode_index_dict.keys())[i]
					test_index_j = list(barcode_index_dict.keys())[j]
					if int(test_index_i) in index_id[test_index_j]:
						barcode_index_sum[test_index_j] = barcode_index_sum[test_index_j] + barcode_index_dict[test_index_i]
					elif int(test_index_j) in index_id[test_index_i]:
						barcode_index_sum[test_index_i] = barcode_index_sum[test_index_i] + barcode_index_dict[test_index_j]
			barcode_species_value = max(barcode_index_sum.values())
			barcode_species_index = max(barcode_index_sum, key = lambda x: barcode_index_sum[x])
			index_rate = barcode_species_value/len(map_index_tag[key])
			barcode_species_name = index_species[barcode_species_index]
			####write one cell result to output file 
			f.write('{}\t{}\t{}\t{}\t{:.4f}\t{}\n'.format(key, value,barcode_classified_count[key],barcode_species_index,index_rate,barcode_species_name))
	f.close()

	
if __name__=="__main__":
	##Input file: .output
	f1 = open(sys.argv[1], 'r')	
	kraken_output = f1.readlines()
	f1.close()
	##Input file: .report.mpa.newx
	f2 = open(sys.argv[2], 'r')
	kraken_report_mpa_new = f2.readlines()
	f2.close()
	##Output file header
	file_header = str(sys.argv[3])
	barcodecount(kraken_output, kraken_report_mpa_new,file_header)
