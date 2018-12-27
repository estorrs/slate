#!/bin/bash

CWL="cwl/slate.cwl"
YAML="cwl/tests/slate_config.yaml"

mkdir -p cwl/tests/test_results
RABIX_ARGS="--basedir cwl/tests/test_results"

rabix $RABIX_ARGS $CWL $YAML
