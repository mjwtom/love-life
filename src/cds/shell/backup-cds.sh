#!/usr/bin/env bash

BCE_HOME=${HOME}/coding/baidu/bce
CDS_TAR=cds.tar.xz

cd ${BCE_HOME}

tar -Jcvf ${CDS_TAR} cds

sz -y ${CDS_TAR}


