"""
========================================================================
cellconpoment - showing reads conpoment of one bacteria cell by pieplot
========================================================================
"""
import sys
import matplotlib.pyplot as plt 


def pieplot(cell_id,labels,quants):
	plt.figure(figsize=(10,10), dpi=96)
	colors  = ["blue","red","coral","green","yellow","orange"]
	plt.pie(quants, colors=colors, labels=labels, autopct='%.2f%%', shadow=True)
	plt.title('cell{}'.format(cell_id), bbox={'facecolor':'0.8', 'pad':5})
	filename = "cell" +str(cell_id) + ".png"
	plt.savefig(filename)


def cellconpoment(barcode_count_file,kraken_output,kraken_report):
	barcode_list = [read.strip().split('_')[1] for read in kraken_output if read.startswith('C')]
	index_list = [read.strip().split('\t')[2] for read in kraken_output if read.startswith('C')]

	index_taxon = {}
	for line in kraken_report:
		index = line.strip().split('\t')[4]
		tax = line.strip().split('\t')[3]
		name = line.strip().split('\t')[5].strip()
		taxon = tax + "_" + name
		index_taxon[index] = taxon 

	cell_id = 1
	for line in barcode_count_file:
		barcode = line.strip().split('\t')[0]
		i = 0
		index_count = {}
		for barcode_id in barcode_list:
			if barcode == barcode_id:
				if index_list[i] in index_count:
					index_count[index_list[i]] = index_count[index_list[i]] + 1
				else:
					index_count[index_list[i]] = 1
			i = i+ 1
		index_count_list = sorted(index_count.items(),key = lambda x:x[1], reverse = True)

		barcode_index_taxon = []
		barcode_index_count = []
		for key,value in index_count_list:
			taxon = index_taxon[key]
			barcode_index_taxon.append(taxon)
			barcode_index_count.append(value)

		pieplot(cell_id, barcode_index_taxon, barcode_index_count)
		cell_id = cell_id + 1

if __name__=='__main__':
	f1 = open(sys.argv[1],'r')	###barcode_count.txt file
	barcode_count_file = f1.readlines()
	f1.close()
	f2 = open(sys.argv[2],'r')	###.output file
	kraken_output = f2.readlines()
	f2.close()
	f3 = open(sys.argv[3],'r')	###.report file
	kraken_report = f3.readlines()
	f3.close()
	cellconpoment(barcode_count_file,kraken_output,kraken_report)
