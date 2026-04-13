import os

from IPython import get_ipython
from IPython.display import HTML, display
from sidecar import Sidecar
import ipywidgets as widgets


def display_desktop(anchor="split-right"):
    try:
        jupyterhub_user = os.environ["JUPYTERHUB_USER"]
        domain_name = os.environ["BINDER_LAUNCH_HOST"].replace("binder", "jupyter")
    except KeyError:
        jupyterhub_user = None
        domain_name = "http://localhost:8888"

    url_prefix = f"{domain_name}/user/{jupyterhub_user}" if jupyterhub_user is not None else ""
    remote_desktop_url = f"{url_prefix}/desktop"

    display(
        widgets.HTML(
            value=(
                f'<a href="{remote_desktop_url}" class="jupyter-button" '
                'style="color: #fff;background-color: #1976d2;" target="_blank">'
                "Open Desktop in new Tab</a>"
            ),
        )
    )

    sc = Sidecar(title="Desktop", anchor=anchor)
    with sc:
        display(
            HTML(
                f"""
                <style>
                body.p-mod-override-cursor div.iframe-widget {{
                    position: relative;
                    pointer-events: none;
                }}

                body.p-mod-override-cursor div.iframe-widget:before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: transparent;
                }}
                </style>
                <div class="iframe-widget" style="width: calc(100% + 10px);height:100%;">
                    <iframe src="{remote_desktop_url}" width="100%" height="100%"></iframe>
                </div>
                """
            )
        )


def _auto_open_desktop():
    if os.environ.get("AUTO_OPEN_DESKTOP", "0") != "1":
        return

    shell = get_ipython()
    if shell is None or shell.__class__.__name__ != "ZMQInteractiveShell":
        return

    if os.environ.get("_AUTO_DESKTOP_ALREADY_OPENED") == "1":
        return

    os.environ["_AUTO_DESKTOP_ALREADY_OPENED"] = "1"
    display_desktop(anchor=os.environ.get("AUTO_OPEN_DESKTOP_ANCHOR", "split-right"))


_auto_open_desktop()
