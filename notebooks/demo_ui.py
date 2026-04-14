import os

import ipywidgets as widgets
from IPython.display import HTML, Markdown, display


ROBOTS = ("hsrb", "stretch", "tiago", "g1", "justin", "armar7", "pr2")
ACTIONS = ("cut", "mix", "wipe")
ENVIRONMENTS = ("isr", "apartment", "kitchen")

CURRENT_DEMO_SELECTION = {}


def _style_label(value):
    return value.replace("_", " ").title()


def _inject_styles():
    display(
        HTML(
            """
            <style>
            .demo-shell {
                --demo-ink: #132238;
                --demo-muted: #5d7188;
                --demo-accent: #db5c32;
                --demo-accent-soft: #ffd8c8;
                --demo-card: rgba(255, 252, 247, 0.94);
                --demo-line: rgba(19, 34, 56, 0.14);
                font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
                color: var(--demo-ink);
                background:
                    radial-gradient(circle at top left, rgba(219, 92, 50, 0.28), transparent 28%),
                    radial-gradient(circle at top right, rgba(42, 134, 189, 0.18), transparent 32%),
                    linear-gradient(135deg, #f4efe6 0%, #e9f1f7 100%);
                border: 1px solid rgba(255,255,255,0.65);
                border-radius: 28px;
                box-shadow: 0 24px 60px rgba(23, 36, 58, 0.12);
                padding: 28px;
                overflow: hidden;
            }
            .demo-shell h1,
            .demo-shell h2,
            .demo-shell h3,
            .demo-shell p {
                margin: 0;
            }
            .demo-hero {
                display: grid;
                gap: 10px;
                margin-bottom: 20px;
            }
            .demo-kicker {
                display: inline-flex;
                width: fit-content;
                padding: 6px 12px;
                border-radius: 999px;
                background: rgba(19, 34, 56, 0.07);
                color: var(--demo-muted);
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }
            .demo-title {
                font-size: 34px;
                font-weight: 700;
                line-height: 1.05;
                letter-spacing: -0.03em;
                max-width: 12ch;
            }
            .demo-copy {
                max-width: 64ch;
                color: var(--demo-muted);
                line-height: 1.55;
                font-size: 15px;
            }
            .demo-grid {
                display: grid;
                grid-template-columns: minmax(0, 1.3fr) minmax(290px, 0.9fr);
                gap: 18px;
                align-items: start;
            }
            .demo-card {
                background: var(--demo-card);
                border: 1px solid var(--demo-line);
                border-radius: 22px;
                padding: 18px;
                backdrop-filter: blur(10px);
            }
            .demo-card-title {
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 6px;
            }
            .demo-card-copy {
                color: var(--demo-muted);
                font-size: 14px;
                line-height: 1.5;
                margin-bottom: 14px;
            }
            .demo-ui .widget-label {
                color: var(--demo-muted);
                font-size: 13px;
                font-weight: 600;
                min-width: 90px;
            }
            .demo-ui .widget-dropdown select,
            .demo-ui .widget-select select {
                border-radius: 14px;
                border: 1px solid var(--demo-line);
                box-shadow: none;
                background: rgba(255,255,255,0.86);
                font-size: 14px;
            }
            .demo-ui .widget-toggle-buttons {
                width: 100%;
            }
            .demo-ui .widget-toggle-buttons .widget-toggle-button {
                border-radius: 999px !important;
                border: 1px solid var(--demo-line) !important;
                margin-right: 8px;
                margin-bottom: 8px;
                background: rgba(255,255,255,0.76);
                color: var(--demo-ink);
                font-weight: 600;
                padding: 7px 15px;
                transition: transform 160ms ease, box-shadow 160ms ease, background 160ms ease;
            }
            .demo-ui .widget-toggle-buttons .widget-toggle-button.mod-active {
                background: linear-gradient(135deg, #db5c32 0%, #f18b47 100%);
                color: white;
                border-color: transparent !important;
                box-shadow: 0 10px 24px rgba(219, 92, 50, 0.28);
                transform: translateY(-1px);
            }
            .demo-start .widget-button {
                width: 100%;
                border: 0;
                border-radius: 16px;
                padding: 12px 18px;
                background: linear-gradient(135deg, #132238 0%, #2a4867 100%);
                color: white;
                font-weight: 700;
                letter-spacing: 0.01em;
                box-shadow: 0 14px 26px rgba(19, 34, 56, 0.22);
            }
            .demo-summary {
                display: grid;
                gap: 10px;
            }
            .demo-badge-grid {
                display: grid;
                gap: 10px;
            }
            .demo-badge {
                display: grid;
                gap: 4px;
                padding: 12px 14px;
                border-radius: 16px;
                background: rgba(255,255,255,0.72);
                border: 1px solid var(--demo-line);
            }
            .demo-badge-label {
                color: var(--demo-muted);
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }
            .demo-badge-value {
                font-size: 18px;
                font-weight: 700;
            }
            .demo-note {
                padding: 12px 14px;
                border-radius: 16px;
                background: var(--demo-accent-soft);
                color: #7f351b;
                font-size: 13px;
                line-height: 1.5;
            }
            @media (max-width: 900px) {
                .demo-grid {
                    grid-template-columns: 1fr;
                }
                .demo-title {
                    max-width: none;
                }
            }
            </style>
            """
        )
    )


def _selection_summary(selection):
    return f"""
    <div class="demo-summary">
      <div class="demo-badge-grid">
        <div class="demo-badge">
          <div class="demo-badge-label">Robot</div>
          <div class="demo-badge-value">{_style_label(selection['robot'])}</div>
        </div>
        <div class="demo-badge">
          <div class="demo-badge-label">Action</div>
          <div class="demo-badge-value">{_style_label(selection['action'])}</div>
        </div>
        <div class="demo-badge">
          <div class="demo-badge-label">Environment</div>
          <div class="demo-badge-value">{_style_label(selection['environment'])}</div>
        </div>
      </div>
      <div class="demo-note">
        This notebook is the single launch entrypoint. Change the stack here instead of
        relying on Binder URL params.
      </div>
    </div>
    """


def show_demo_ui(on_start=None):
    global CURRENT_DEMO_SELECTION

    _inject_styles()

    selection = {
        "robot": ROBOTS[-1],
        "action": ACTIONS[0],
        "environment": ENVIRONMENTS[0],
    }
    CURRENT_DEMO_SELECTION = selection.copy()

    header = widgets.HTML(
        value="""
        <div class="demo-hero">
          <div class="demo-kicker">Virtual Research Lab</div>
          <div class="demo-title">Compose a robotics demo run without leaving the notebook.</div>
          <div class="demo-copy">
            Pick the robot, choose an action, set the environment, then launch a shared
            demo backend. The UI is intentionally notebook-native so it stays stable on Binder.
          </div>
        </div>
        """
    )

    left_intro = widgets.HTML(
        value="""
        <div class="demo-card">
          <div class="demo-card-title">Scenario Builder</div>
          <div class="demo-card-copy">
            Use a broad robot catalog, keep actions explicit, and treat the environment as a first-class input.
          </div>
        </div>
        """
    )

    robot = widgets.Dropdown(
        options=[(_style_label(value), value) for value in ROBOTS],
        value=selection["robot"],
        description="Robot",
    )

    action = widgets.ToggleButtons(
        options=[(_style_label(value), value) for value in ACTIONS],
        value=selection["action"],
        description="Action",
    )

    environment = widgets.ToggleButtons(
        options=[(_style_label(value), value) for value in ENVIRONMENTS],
        value=selection["environment"],
        description="Env",
    )

    summary = widgets.HTML(value=_selection_summary(selection))
    start_button = widgets.Button(description="Start Demo", icon="play")
    output = widgets.Output()

    start_box = widgets.Box([start_button])
    start_box.add_class("demo-start")

    controls = widgets.VBox(
        [
            left_intro,
            robot,
            action,
            environment,
            start_box,
            output,
        ]
    )
    controls.add_class("demo-card")
    controls.add_class("demo-ui")

    aside = widgets.VBox(
        [
            widgets.HTML(
                value="""
                <div class="demo-card">
                  <div class="demo-card-title">Live Selection</div>
                  <div class="demo-card-copy">
                    The current stack updates as you click. Hook the launch button to your real runner later.
                  </div>
                </div>
                """
            ),
            summary,
        ]
    )
    aside.add_class("demo-card")

    def _update_selection(change):
        global CURRENT_DEMO_SELECTION
        selection[change["owner"].description.lower().replace("env", "environment")] = change["new"]
        CURRENT_DEMO_SELECTION = selection.copy()
        summary.value = _selection_summary(selection)

    robot.observe(_update_selection, names="value")
    action.observe(_update_selection, names="value")
    environment.observe(_update_selection, names="value")

    def _default_start(current_selection):
        with output:
            output.clear_output(wait=True)
            display(Markdown("### Demo Request"))
            print(current_selection)
            os.environ["DEMO_ROBOT"] = current_selection["robot"]
            os.environ["DEMO_ACTION"] = current_selection["action"]
            os.environ["DEMO_ENVIRONMENT"] = current_selection["environment"]
            print("Stored in environment as DEMO_ROBOT / DEMO_ACTION / DEMO_ENVIRONMENT")

    def _handle_start(_):
        callback = on_start or _default_start
        callback(selection.copy())

    start_button.on_click(_handle_start)

    grid = widgets.HBox(
        [controls, aside],
        layout=widgets.Layout(width="100%", align_items="stretch"),
    )
    grid.add_class("demo-grid")
    controls.layout = widgets.Layout(width="100%")
    aside.layout = widgets.Layout(width="100%")

    container = widgets.VBox([header, grid], layout=widgets.Layout(width="100%"))
    container.add_class("demo-shell")
    display(container)
