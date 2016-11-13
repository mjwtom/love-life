#!/usr/bin/env bash

# install the protobuf
echo entering the downloads directory
cd ${HOME}/downloads/
echo run git clone command
git clone https://github.com/google/protobuf.git
cd protobuf
./configure --prefix=${HOME}/install/protobuf

#
