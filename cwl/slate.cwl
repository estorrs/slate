class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: gneiss_align
baseCommand:
  - python
  - /slate/slate/slate.py
inputs:
  - id: threads
    type: int?
    inputBinding:
      position: 0
      prefix: '--threads'
  - id: input_bam
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
    dockerPull: estorrs/slate:0.0.1
