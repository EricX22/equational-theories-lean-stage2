#!/bin/bash
# DEPRECATED — superseded by overnight.sh, which does this and then harvests +
# classifies new laws, retries the stubborn ones, and writes the merged corpus.
#
#   nohup bash paper/scripts/overnight.sh > /dev/null 2>&1 &
#   tail -f paper/results/overnight.log
exec bash "$(dirname "$0")/overnight.sh" "$@"
