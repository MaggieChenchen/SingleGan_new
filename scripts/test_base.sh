MODE='base'
# dataset details
CLASS=$1  #apple2orange summer2winter_yosemite horse2zebra
TIME_DIR=$2    # e.g. 2018_10_15_10_48_56
EPOCH='latest'
HOW_MANY=9500
LOAD_SIZE=256
FINE_SIZE=256
INPUT_NC=3


# training
GPU_ID=0
NAME=${MODE}_${CLASS}
# command
CUDA_VISIBLE_DEVICES=${GPU_ID} python ./test.py \
  --dataroot ./datasets${CLASS} \
  --checkpoints_dir ./checkpoints \
  --time_dir 2020_10_15_13_16_04${TIME_DIR} \
  --name ${NAME} \
  --mode ${MODE} \
  --loadSize ${LOAD_SIZE} \
  --fineSize ${FINE_SIZE} \
  --input_nc ${INPUT_NC} \
  --how_many ${HOW_MANY} \
  --which_epoch ${EPOCH} \
  --is_flip 0 \
  --batchSize 1 \
  --ngf 64
  




  
