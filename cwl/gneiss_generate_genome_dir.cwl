class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: gneiss_align
baseCommand:
  - python
  - /gneiss/gneiss/generate_genome_dir.py
inputs:
  - id: threads
    type: int?
    inputBinding:
      position: 0
      prefix: '--threads'
  - id: reference_fasta
    type: File
    inputBinding:
      position: 0
      prefix: '--reference-fasta'
  - id: gtf
    type: File?
    inputBinding:
      position: 0
      prefix: '--gtf'
outputs:
  - id: output_genome_dir
    type: Directory?
    outputBinding:
      glob: genome_dir
label: gneiss_align
arguments:
  - position: 99
    valueFrom: genome_dir
requirements:
  - class: DockerRequirement
    dockerPull: estorrs/gneiss:0.0.1
