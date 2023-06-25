#!/usr/bin/env bash

set -e
set -x

#ruff foundational tests
black foundational tests --check
