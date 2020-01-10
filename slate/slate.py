import argparse
import os
import subprocess

import quartzite

parser = argparse.ArgumentParser()

parser.add_argument('input_bam', type=str,
        help='input bam fp')

positions_group = parser.add_argument_group('positions_group')
positions_group.add_argument('--positions', type=str,
        help='fp to .bed or .tsv to use with bam readcount. format: <chrom>:<start-pos>:<end-pos>')

fasta_group = parser.add_argument_group('fasta_group')
fasta_group.add_argument('--fasta', type=str,
        help='reference fasta to use with bam-readcount')

parser.add_argument('--min-base-quality', type=int,
		default=0, help='Only count bases with greater base quality than given value.')
parser.add_argument('--min-mapping-quality', type=int,
		default=0, help='Only count reads with greater mapping quality than given value.')

parser.add_argument('--readcount-output', type=str,
        default='output.readcount', help='fp to be used for readcount output')
parser.add_argument('--vaf-output', type=str,
        default=None, help='If present, will output a vaf file in addition to readcount output.')
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
            '-@', str(threads),
            '-L', positions_fp,
            '-o', output_fp,
            bam_fp]

    print('slate is executing filtering step')
    print(f'slate is executing the following command: {" ".join(tool_args)}')
    print(subprocess.check_output(tool_args).decode('utf-8'))

def run_readcount_step(filtered_bam_fp, positions_fp, reference_fasta, output_fp,
		min_base_quality=0, min_mapping_quality=0):
    """run bam readcount step"""
    tool_args = ['bam-readcount',
        '-w', '1',
        '-f', reference_fasta,
        '-l', positions_fp,
        '-q', str(min_mapping_quality),
        '-b', str(min_base_quality),
        filtered_bam_fp]

    print('slate is executing bam readcount step')
    print(f'slate is executing the following command: {" ".join(tool_args)}')
    f = open(output_fp, 'w')
    subprocess.call(tool_args, stdout=f)
    print(f'slate is piping stdout to: {output_fp}')
    f.close()

def main():
    check_arguments()

    if not os.path.exists(args.input_bam + '.bai'):
        index_bam(args.input_bam)
    run_filter_step(args.input_bam, args.positions, args.filtered_bam_output, threads=args.threads)
    index_bam(args.filtered_bam_output)
    run_readcount_step(args.filtered_bam_output, args.positions, args.fasta, args.readcount_output,
    		    min_base_quality=args.min_base_quality, min_mapping_quality=args.min_mapping_quality)

    # convert to vaf if necissary
    if args.vaf_output is not None:
        quartzite.run_vaf_generation(args.readcount_output, 'ACGTN', args.vaf_output, 1)

if __name__ == '__main__':
    main()
