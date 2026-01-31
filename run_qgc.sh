#!/bin/bash
# Wrapper to launch QGroundControl with BOTH system and Qt library paths
export LD_LIBRARY_PATH=/mnt/data/projects/QGC_Extracted/Qt/libs:/mnt/data/projects/QGC_Extracted/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
/mnt/data/projects/QGC_Extracted/AppRun "$@"
