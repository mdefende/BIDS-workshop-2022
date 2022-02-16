#!/bin/bash
#
#SBATCH --job-name=S01-fmriprep
#SBATCH --output=/home/mdefende/Desktop/bids-test/D01/S01-fmriprep-out.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=medium
#SBATCH --time=50:00:00
#SBATCH --mem-per-cpu=5G
#SBATCH --mail-type=FAIL

# Users should only need to change the dataset_dir and the participant below to run this script.

# set the path to the dataset directory. This is the parent to the BIDS-formatted nifti directory.
dataset_dir=/home/mdefende/Desktop/bids-test/D01

# set the name of the participant
participant=sub-S01

# load the module
module load rc/fmriprep/20.2.3

# run fmriprep
fmriprep --work-dir $dataset_dir/workdir/ \
         --participant-label $participant \
         --output-spaces T1w \
         --fs-license-file $HOME/license.txt \
         --n-cpus 4 \
         --omp-nthreads 4 \
         --cifti-output 91k \
         $dataset_dir/nifti/ \
         $dataset_dir/nifti/derivatives \
         participant
