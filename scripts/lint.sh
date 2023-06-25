#!/usr/bin/env bash

set -e
set -x

#ruff basics tests
black basics tests --check
