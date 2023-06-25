#!/usr/bin/env bash

set -e
set -x

#ruff basal tests
black basal tests --check
