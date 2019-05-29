import argparse
import os
import subprocess

CHROM_INDEX = 0
POS_INDEX = 1
REF_INDEX = 2
DEPTH_INDEX = 3
BASES_INDEX = 4

def get_base_tups(base_pieces, bases='ACGTN'):
    """Extract (base, count) tups from base pieces.
    
    base piece is a bam-readcount outputed base information that is in the following format
    as per bam-readcount documentation

    base:count:avg_mapping_quality:avg_basequality:avg_se_mapping_quality:num_plus_strand:num_minus_strand:avg_pos_as_fraction:avg_num_mismatches_as_fraction:avg_sum_mismatch_qualities:num_q2_containing_reads:avg_distance_to_q2_start_in_q2_reads:avg_clipped_length:avg_distance_to_effective_3p_end
    
    """
    base_count_dict = {}

    for piece in base_pieces:
        pieces = piece.split(':')
        
        base = pieces[0]
        if base in bases:
            count = pieces[1]
            base_count_dict[base] = int(count)
    
    base_count_tups = []
    for base in bases:
        base_count_tups.append((base, base_count_dict[base]))

    return base_count_tups

def get_vafs(ref, depth, base_tups):
    """Get vafs.
    
    returns list of vafs in the following order

    [reference_vaf, minor_vaf, base1_vaf, base_vaf, ...]
    """
    # take zero depth into account
    if depth == 0:
        base_vafs = [0.0] * len(base_tups)
        return [0.0, 0.0] + base_vafs

    reference_count = 0
    minor_count = 0
    base_vafs = []
    for base, count in base_tups:
        if base == ref:
            reference_count += count
        else:
            minor_count += count

        base_vafs.append(count / depth)

    vafs = []
    vafs.append(reference_count / depth)
    vafs.append(minor_count / depth)
    vafs += base_vafs

    return vafs

def get_vaf_line(bam_readcount_line, bases='ACGTN'):
    """Breaks down bam-readcount line into vaf line.

    bam-readcount line has the following format: chr    position    reference_base    depth    base:count:.....

    vaf line has the following format: <chrom>\t<pos>\t<ref>\t<depth>\t<ref_vaf>\t<minor_vaf>\t<base1_vaf>\t<base2_vaf>....\n    
    """
    pieces = bam_readcount_line.split('\t')
    chrom = pieces[CHROM_INDEX]
    pos = pieces[POS_INDEX]
    ref = pieces[REF_INDEX]
    depth = int(pieces[DEPTH_INDEX])
    base_pieces = pieces[BASES_INDEX:]
    
    base_tups = get_base_tups(base_pieces, bases=bases)

    vafs = get_vafs(ref, depth, base_tups)

    line = f'{chrom}\t{pos}\t{ref}\t{depth}\t'
    line += '\t'.join(['%.3f' % v for v in vafs]) + '\n'

    return line

def run_vaf_generation(input_readcount_fp, bases, output_fp, threads=1):
    """Generate vaf file.

    File has the following format: <chrom>\t<pos>\t<ref>\t<depth>\t<ref_vaf>\t<minor_vaf>\t<b1_vaf>\t<b2_vaf>....\n    
    """
    print('quartzite is generating vafs')
    
    f = open(input_readcount_fp)
    out_f = open(output_fp, 'w')

    bs = [b + '_VAF' for b in bases]
    out_f.write('CHROM\tPOS\tREF\tDEPTH\tREF_VAF\tMINOR_VAF\t' + '\t'.join(bs) + '\n')

    for line in f:
        out_f.write(get_vaf_line(line, bases=bases))

    f.close()
    out_f.close()

def main(args):
    run_vaf_generation(args.input_readcount, args.bases, args.output, threads=args.threads)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('input_readcount', type=str,
            help='input bam-readcount readcount file')

    parser.add_argument('--output', type=str,
            default='output.vaf', help='name given to output vaf file')
    parser.add_argument('--bases', type=str,
            default='ACGTN', help='Which bases to calculate vaf for. Default is ACGTN')
    parser.add_argument('--threads', type=int,
            default=1, help='DEAD parameter. Not currently used.')

    args = parser.parse_args()

    main(args)
