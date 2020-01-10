class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: slate
baseCommand:
  - python
  - /slate/slate/slate.py
inputs:
  - id: threads
    type: int?
    inputBinding:
      position: 0
      prefix: '--threads'
  - id: min_base_quality
    type: int?
    inputBinding:
      position: 0
      prefix: '--min-base-quality'
  - id: min_mapping_quality
    type: int?
    inputBinding:
      position: 0
      prefix: '--min-mapping-quality'
  - id: input_bam
    type: File
    inputBinding:
      position: 99
  - id: positions
    type: File
    inputBinding:
      position: 0
      prefix: '--positions'
  - id: reference_fasta
    type: File
    inputBinding:
      position: 0
      prefix: '--fasta'
outputs:
  - id: readcount
    type: File?
    outputBinding:
      glob: output.readcount
  - id: filtered_bam
    type: File?
    outputBinding:
      glob: output.filtered.bam
label: slate
arguments:
  - position: 0
    prefix: '--readcount-output'
    valueFrom: output.readcount
  - position: 0
    prefix: '--filtered-bam-output'
    valueFrom: output.filtered.bam
requirements:
  - class: DockerRequirement
    dockerPull: 'estorrs/slate:0.0.2'
