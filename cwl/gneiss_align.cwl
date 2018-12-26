class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: gneiss_align
baseCommand:
  - python
  - /gneiss/gneiss/gneiss.py
inputs:
  - id: genome_dir
    type: Directory
    inputBinding:
      position: 0
      prefix: '--genome-dir'
  - id: threads
    type: int?
    inputBinding:
      position: 0
      prefix: '--threads'
  - id: compressed_input
    type: boolean?
    inputBinding:
      position: 0
      prefix: '--compressed-input'
  - id: read_1_fastq
    type: File?
    inputBinding:
      position: 98
  - id: read_2_fastq
    type: File?
    inputBinding:
      position: 99
outputs:
  - id: output_bam
    type: File?
    outputBinding:
      glob: gneiss_outputs/Aligned.sortedByCoord.out.bam
label: gneiss_align
arguments:
  - position: 0
    prefix: '--output-dir'
    valueFrom: gneiss_outputs
requirements:
  - class: DockerRequirement
    dockerPull: estorrs/gneiss:0.0.1
