#!/usr/bin/env bash
mpirun -q -np 4 -hostfile hostfile --allow-run-as-root ./slime -no-hess -massive "${1}"
pkill slime_cloud
