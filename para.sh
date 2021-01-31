#!/bin/bash
#SBATCH -t 25:00:00
#SBATCH -n 1

module load 2020
module load ecCodes/2.18.0-foss-2020a-Python-3.8.2

for (( i=0; i<=23 ; i++ )) ; do
(
  python batcher.py 23 $i 1
) &
done
wait
