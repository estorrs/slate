import os
import subprocess

import pytest

TEST_DATA_DIR = 'tests/data/'
TEST_FASTA_REFERENCE = TEST_DATA_DIR + 'test_ref.fa'
TEST_POSITIONS = TEST_DATA_DIR + 'positions.bed'
TEST_INPUT_BAM = TEST_DATA_DIR + 'test.bam'

TEST_FILTERED_BAM = TEST_DATA_DIR + 'test.filtered.bam'
TEST_READCOUNT = TEST_DATA_DIR + 'test.readcount'


def test_basic_run():
    tool_args = ['python', 'slate/slate.py',
            '--threads', '2',
            '--positions', TEST_POSITIONS,
            '--filtered-bam-output', TEST_FILTERED_BAM,
            '--readcount-output', TEST_READCOUNT,
            '--fasta', TEST_FASTA_REFERENCE,
            TEST_INPUT_BAM]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    assert True

def test_min_mapping_quality():
    tool_args = ['python', 'slate/slate.py',
            '--threads', '2',
            '--positions', TEST_POSITIONS,
            '--filtered-bam-output', TEST_FILTERED_BAM,
            '--readcount-output', TEST_READCOUNT,
            '--min-mapping-quality', '20',
            '--min-base-quality', '25',
            '--fasta', TEST_FASTA_REFERENCE,
            TEST_INPUT_BAM]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    assert True

def test_vaf_output():
    tool_args = ['python', 'slate/slate.py',
            '--positions', TEST_POSITIONS,
            '--filtered-bam-output', TEST_FILTERED_BAM,
            '--readcount-output', TEST_READCOUNT,
            '--vaf-output', 'output.vaf',
            '--fasta', TEST_FASTA_REFERENCE,
            TEST_INPUT_BAM]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    assert True
