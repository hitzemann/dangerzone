#!/bin/sh

echo "Building container image"
docker build container --tag hitzeman/dangerzone

echo "Saving container image"
docker save hitzeman/dangerzone -o share/container.tar

echo "Compressing container image"
gzip -f share/container.tar

echo "Looking up the image id"
docker image ls hitzeman/dangerzone | grep "hitzeman/dangerzone" | tr -s ' ' | cut -d' ' -f3 > share/image-id.txt
