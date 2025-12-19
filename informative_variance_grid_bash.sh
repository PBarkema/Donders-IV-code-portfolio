#!/bin/bash
# Author: P. Barkema
# Edited from P. Sulewski

#$ -N ikw_high_pass_test_causal_0.5Hz
#$ -pe default 7-19
#$ -l h_rt=00:15:00,mem=23G,h='!ramsauer.ikw.uni-osnabrueck.de' 
#$ -m beas 
#$ -q nbp.q 

## -N -> Name of the job
## -pe -> parallel environment number of slots/threads
## -m  -> receive job info to university mail
## -l h_rt -> walltime
## -q nbp.q  cluster computers

#obtain end time, output runtime
start_time=$(date +%y%m%d_%H%M)

#activate prepared python environment
source /net/store/nbp/projects/informative-variance/miniconda/bin/activate && conda activate  base

#go to working directory # where is your code?
cd /net/store/nbp/projects/informative-variance/

# setup grid job parameters
# missing:
# HVA: 18, 21-22, 27-28
# MVA: 27-30
# EVA: 2-10, 17-30
# qsub -N q_alignment_5sub -t 1-10 -pe default 7-19 -l h_rt=04:00:00,mem=23G,h='!ramsauer.ikw.uni-osnabrueck.de' -m beas -q nbp.q execute_cci.sh
#qsub -F -N z_alignment_LVC_1sub -t 1-30 -pe default 7-19 -l h_rt=02:00:00,mem=10G,h='!ramsauer.ikw.uni-osnabrueck.de -m beas -q nbp.q execute_cci.sh
# qsub -t 1-30 execute_cci.sh
gid=$SGE_TASK_ID
echo gid
echo $gid

# number of parallel slots/threads per job
echo NSLOTS
echo $NSLOTS

#ANALYSIS Parameters
#some additional parameters can be found in "Varionautics_source_estimates.py"
#################
ROIs_chunk_num=1												#Number of chunks to compute (for testing)
ROIs_chunk_size=1												#Number of ROIs per Node
distances='correlation' 								#submit as 'distance1,distance2,...'
analysis_id='cci_alignment_cloud_all_data'							#identifier of this analyisis
num_sub=15
num_sess=2
hemi_array=('both')												#( 'lh' 'rh' ) -> both
#TE1p,TE2p,FFC,VVC,VMV2,VMV3,PHA1,PHA2,PHA3
# LO1,LO2,LO3,V4t
labelset=('TE1p,TE2p,FFC,VVC,VMV2,VMV3,PHA1,PHA2,PHA3')
dsampling_freq=500												# Downsampling frequeny. Original data has 500hz
profile_memory=1												# activate memory profiler?
save_to='/net/store/nbp/projects/informative-variance' #where to save the results?
##################

# This will create
# subs = (1,1,2,2,3,3 ... 15,15) length = 30
# sessions = (1,2,1,2 [15 sets total]) length = 30
# so every subject will have two matching subjects, every partition is done.
subs=()
sessions=()
for sub in $(seq 1 $num_sub); do
	for sess in $(seq 1 $num_sess); do
		subs+=($sub)
		sessions+=($sess)	
	done
done

# chooses one task, based on ID
subID=${subs[gid-1]}
sessID=${sessions[gid-1]}

echo subs
echo $subs

echo sessID
echo $sessID
echo subID
echo $subID

syscall=$(printf 'python3 grid_cci.py %s %s %s %s %s %s %s %s %s' "$subID" "$sessID" "$dsampling_freq" "$hemi_array" "$labelset" "$distances" "$analysis_id"  "$save_to" "$NSLOTS" )

echo $syscall
eval $syscall

#obtain end time, output runtime
end_time=$(date +%y%m%d_%H%M)

echo started $start_time
echo ended   $end_time



