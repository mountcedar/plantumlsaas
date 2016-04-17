#!/usr/bin/env bash

cd ..
pwd
echo "removing dist dir..."
rm -rf dist
echo "recreate dist dir..."
mkdir dist
echo "archive plantumlsaas"
git archive --format=tar HEAD plantumlsaas | tar -C dist -xf -
cd -
