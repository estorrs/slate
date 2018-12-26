import argparse
import os
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument('input_bam', type=str,
        help='input bam fp')

# readcount_output_group = parser.add_argument_group('readcount_output_group')
# readcount_output_group.add_argument('--readcount-output', type=str,
#         help='fp to be used for readcount output')
# 
# filtered_output_group = parser.add_argument_group('filtered_output_group')
# filtered_output_group.add_argument('--filtered-bam-output', type=str,
#         help='fp to be used for the intermediary filtered bam')

positions_group = parser.add_argument_group('positions_group')
positions_group.add_argument('--positions', type=str,
        help='fp to .bed or .tsv to use with bam readcount. format: <chrom>:<start-pos>:<end-pos>')

fasta_group = parser.add_argument_group('fasta_group')
fasta_group.add_argument('--fasta', type=str,
        help='reference fasta to use with bam-readcount')

parser.add_argument('--readcount-output', type=str,
        default='output.readcount', help='fp to be used for readcount output')
parser.add_argument('--filtered-bam-output', type=str,
        default='output.filtered.bam', help='fp to be used for the intermediary filtered bam')
parser.add_argument('--threads', type=int,
        default=1, help='how many processes to allow samtools to use')

args = parser.parse_args()

def check_arguments():
    if args.positions is None:
        raise ValueError('Must specify position file with --positions')

    if args.fasta is None:
        raise ValueError('Must specify reference fasta with --fasta')

def index_bam(bam_fp):
    """index the given bam.
    
    note: no threads option because I'm fairly sure that setting the number of threads with
        indexing in this samtools version is unstable
    """
    tool_args = ['samtools', 'index', bam_fp]
    
    print(f'slate is executing the following command: {" ".join(tool_args)}')
    print(subprocess.check_output(tool_args).decode('utf-8'))

def run_filter_step(bam_fp, positions_fp, output_fp, threads=1):
    """run bam filter step"""
    tool_args = ['samtools', 'view', '-h',
            '-@', threads,
            '-R', positions_fp,
            '-o', output_fp,
            bam_fp

    print(f'slate is executing filtering step')
    print(f'slate is executing the following command: {" ".join(tool_args)}')
    print(subprocess.check_output(tool_args).decode('utf-8'))

def run_readcount_step(filtered_bam_fp, positions_fp, reference_fasta, output_fp):
    """run bam readcount step"""
    tool_args = ['bam-readcount',
        '-w', 1,
        '-f', reference_fasta,
        '-l', positions_fp,
        filtered_bam_fp]

    print(f'slate is executing bam readcount step')
    print(f'slate is executing the following command: {" ".join(tool_args)}')
    f = open(output_fp, 'w')
    print(subprocess.check_output(tool_args, stdout=f).decode('utf-8'))
    print(f'slate is piping stdout to: {output_fp}')
    f.close()

def main():
    check_arguments()

    index_bam(args.input_bam)
    run_filter_step(args.input_bam, args.positions, args.filtered_bam_output, threads=args.threads)
    index_bam(args.filtered_bam_output)
    run_readcount_step(args.filtered_bam_output, args.positions, args.fasta, args.readcount_output)

if __name__ == '__main__':
    main()
