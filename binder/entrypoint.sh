#!/bin/bash

set -e

source "${ROS_PATH}/setup.bash"

import_workspace() {
    local workspace_file="${JUPYTER_WORKSPACE_FILE:-/home/repo/binder/auto-d.jupyterlab-workspace}"

    if [[ ! -f "${workspace_file}" ]]; then
        return
    fi

    jupyter lab workspaces import "${workspace_file}" >/tmp/jupyter-workspace-import.log 2>&1 || \
        echo "Workspace import failed; see /tmp/jupyter-workspace-import.log" >&2
}

start_rviz() {
    if [[ "${AUTO_START_RVIZ:-1}" != "1" ]]; then
        return
    fi

    export DISPLAY="${RVIZ_DISPLAY:-${DISPLAY:-:1}}"
    export RVIZ_CONFIG_FILE="${RVIZ_CONFIG_FILE:-/home/jovyan/.rviz2/default.rviz}"
    export LIBGL_ALWAYS_SOFTWARE="${LIBGL_ALWAYS_SOFTWARE:-1}"
    export QT_X11_NO_MITSHM="${QT_X11_NO_MITSHM:-1}"

    (
        while true; do
            if xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1; then
                echo "Starting RViz on display ${DISPLAY}" >&2
                exec rviz2 -d "${RVIZ_CONFIG_FILE}"
            fi
            echo "Waiting for display ${DISPLAY} before starting RViz" >&2
            sleep 2
        done
    ) >/tmp/rviz2.log 2>&1 &
}

import_workspace
start_rviz

exec "$@"
