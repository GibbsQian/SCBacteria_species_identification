'''
=========================================================
inanno - single cell bacteria species identification
=========================================================

This tool mainly do three parts work: 
    1) Count index result of each read in one cell and based on "overlap index algorithm"
     to determine the final result of one cell.This method can both calculate 16S and NCBI 
     refseq mapping result from kraken2.
    2) Compare 16S and NCBI refseq species identification result and finally determine 
     the index result.
    3) Based on kraken2 index anotation for every read, we can count reads index component of 
    cells which you are interested in and display it in pieplot format.
'''

description = '''
Method:

    Count reads index result to determine the final result of every cell:

        bsctools inanno --module barcode_count --kraken-output [kraken output file] --kraken-treated-report [treated kraken report] --prefix [output header name]

    Compare 16S and NCBI refseq species identification result:

        bsctools inanno --module index_compare --refseq-result [refseq.barcode_count.txt] --amplicon-result [16S.barcode_count.txt] --prefix [output header name]

    Count reads index conpoment of cells:

        bsctools inanno --module count_component --barcode-count [file with selected barocde index] --kraken-output [kraken output file] --kraken-report [kraken report]

    Note: The "barcode count" model need kraken output file and report file after treaded. It must be treated by "kreport2mpa.py" and "go_perl_newx.TXT" step by step.
        To konw the detailed step, please read the analysis pipeline.
 
'''

import re
import os
import sys
import argparse
from bsctools import barcode_count
from bsctools import index_compare
from bsctools import bscpieplot


def main(argv):
    """script main

    parser command line options in sys.argv, unless *argv* is given
    """

    if argv is None:
        argv = sys.argv

    if argv[0] != "inanno" and argv[0] != "inanno.py":
        print("Please input appropriate tool name!\nspindent closed")
        
        return 

    parser = argparse.ArgumentParser(
                                    usage = globals()["__doc__"],
                                    description = description,
                                    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-p', '--prefix', type = str, help=
                        "output name header of 'barcode count' or 'index compare' model")

    group = parser.add_argument_group("inanno-specific options")

    group.add_argument('-m', '--module', choices = ['barcode_count','index_compare','count_component'], required = True, help=
                        "choose the model to analysis single cell bacteria data:\n"
                        "barcode_count: count reads index result to determine the final result of every cell\n"
                        "index_compare: compare 16S and NCBI refseq species identification result\n"
                        "count_component: count reads index conpoment of cells\n")
                                                                            
    group.add_argument('-ko', '--kraken-output', type = str, default = None, help=
                        "Please give the output of 'kraken2 --output' filename")

    group.add_argument('-kr', '--kraken-report', type = str, default = None, help=
                        "Please give the output of 'kraken2 --report' filename")   
                                                                       
    group.add_argument('-ktr', '--kraken-treated-report', type = str, default = None, help=
                        "The output of 'kraken2 --report' file, and then treated by \"kreport2mpa.py\" and \n"
                        "\"go_perl_newx.TXT\" step by step.")

    group.add_argument('-r', '--refseq-result' ,type = str, help =
                        "please give the 'barcode count' output which aligned to NCBI refseq dataset by kraken2")

    group.add_argument('-s', '--amplicon-result' ,type = str, default = None, help =
                        "please give the 'barcode count' output which aligned to 16S dataset by kraken2")

    group.add_argument('-bc', '--barcode-count', type = str, default = None, help=
                        "Please give the \"...barcode_count.txt\" filename or a few barcode info lines from it \n"
                        "to draw the cell reads component pieplot")

    args = parser.parse_args()

    if args.module == "barcode_count":
        f1 = open(args.kraken_output,'r')
        kraken_output = f1.readlines()
        f1.close()
        f2 = open(args.kraken_treated_report,'r')
        kraken_report_mpa_new = f2.readlines()
        f2.close()
        file_header = args.prefix
        barcode_count.barcodecount(kraken_output, kraken_report_mpa_new,file_header)
        

    elif args.module == "index_compare":
        f1 = open(args.refseq_result,'r')
        refseq_result = f1.readlines()
        f1.close()
        f2 = open(args.amplicon_result,'r')
        silva_result = f2.readlines()
        f2.close()
        file_header = args.prefix
        index_compare.taxoncompare(refseq_result,silva_result,file_header)

    elif args.module == "count_component":
        f1 = open(args.barcode_count,'r')
        barcode_count_file = f1.readlines()
        f1.close()
        f2 = open(args.kraken_output,'r')
        kraken_output =f2.readlines()
        f2.close()
        f3 = open(args.kraken_report,'r')
        kraken_report = f3.readlines()
        f3.close()
        bscpieplot.cellconpoment(barcode_count_file,kraken_output,kraken_report)



if __name__ == '__main__':
    sys.exit(main(sys.argv))