#!/usr/bin/env bash

set -e
set -x

#ruff crucial tests
black crucial tests --check
