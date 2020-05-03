#!/bin/bash

for src in $(ls *.py); do
    pylint -j 0 -f colorized --errors-only $src || exit 1
done

for src in $(ls *.py); do
    pylint -j 0 -f colorized --disable=C0114 --disable=C0116 $src || exit 1
done
