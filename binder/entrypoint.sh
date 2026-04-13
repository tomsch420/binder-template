#!/bin/bash

set -e

# Launch ROS 2 into the shell environment used by background apps and Jupyter.
source "${ROS_PATH}/setup.bash"

start_rviz() {
    if [[ "${AUTO_START_RVIZ:-1}" != "1" ]]; then
        return
    fi

    export DISPLAY="${DISPLAY:-:1}"
    export RVIZ_CONFIG_FILE="${RVIZ_CONFIG_FILE:-/home/jovyan/.rviz2/default.rviz}"

    (
        for _ in $(seq 1 30); do
            if xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1; then
                exec rviz2 -d "${RVIZ_CONFIG_FILE}"
            fi
            sleep 2
        done

        echo "RViz startup skipped: display ${DISPLAY} did not become ready." >&2
    ) >/tmp/rviz2.log 2>&1 &
}

start_rviz

# The following line will allow the binderhub start Jupyterlab, should be at the end of the entrypoint.
# Do not modify it!
exec "$@"
