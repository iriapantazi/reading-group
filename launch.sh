PROJECT_NAME="reading-group"

: ${STORAGE:="$HOME/storage"}
: ${HF_CACHE:="$HOME/.cache/huggingface"}

DOCKER_ARGS="-t -i --rm --gpus=all --shm-size=4g --ulimit memlock=-1 --ulimit stack=67108864 "

# Keep cached Hugging Face datasets even when restarting the container
hf_cache_volume="$HF_CACHE:/root/.cache/huggingface"
DOCKER_ARGS+=" -v $hf_cache_volume "
# Keep PDF or other files in the storage directory
storage_volume="$STORAGE:/storage"
DOCKER_ARGS+=" -v $storage_volume "
DOCKER_ARGS+=" -e HF_TOKEN=$HF_TOKEN "

# Mount the storage directory
# DOCKER_ARGS+=" -v $STORAGE "

docker run $DOCKER_ARGS -v $PWD:/workspace/reading-group "$PROJECT_NAME" sh -c bash
