#!/usr/bin/env bash

set -e
set -x

#ruff basic tests
black basic tests --check
