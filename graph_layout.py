import math
from collections import defaultdict

import networkx as nx
import plotly.graph_objects as go

from compounds import COMPOUNDS


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------
def build_graph(compounds=COMPOUNDS):
    g = nx.DiGraph()
    # Define the fields we expect to have
    required_fields = ["family", "structural_distance", "parent", "half_life", "legal_status_germany", "notes"]
    
    for c in compounds:
        # Create a dictionary of attributes
        attrs = {}
        for field in required_fields:
            # If the field is missing in the compound entry, set a default
            if field == "structural_distance":
                attrs[field] = c.get(field, 0)
            elif field == "notes":
                attrs[field] = c.get(field, "")
            else:
                attrs[field] = c.get(field, "N/A")
        
        # Add the node with all safe attributes
        g.add_node(c["name"], **attrs)
    
    # Add edges
    for c in compounds:
        parent = c.get("parent")
        if parent and parent in g:
            g.add_edge(parent, c["name"])
            
    return g

def list_families(compounds=COMPOUNDS):
    """Sorted unique family names. Used to build the global filter checklist
    and to assign deterministic angular sectors."""
    return sorted({c["family"] for c in compounds})


# ---------------------------------------------------------------------------
# Radial layout
# ---------------------------------------------------------------------------
def compute_radial_layout(
    compounds=COMPOUNDS,
    base_radius=1.0,
    ring_spacing=4.5,  # Increased to give more room between layers
    sector_fill=0.85,
):
    families = list_families(compounds)
    n_fam = len(families)
    sector_width = (2 * math.pi / n_fam) if n_fam else 2 * math.pi
    fam_index = {f: i for i, f in enumerate(families)}

    buckets = defaultdict(list)
    for c in sorted(compounds, key=lambda x: x["name"]):
        buckets[(c["family"], c["structural_distance"])].append(c["name"])

    pos = {}
    for (family, dist), names in buckets.items():
        center_angle = fam_index[family] * sector_width
        radius = base_radius + dist * ring_spacing
        n = len(names)
        
        # Calculate angular span based on number of nodes in this specific bucket
        span = sector_width * sector_fill
        
        if n == 1:
            angles = [center_angle]
        else:
            # Distribute nodes evenly across the sector
            step = span / n
            start = center_angle - (span / 2.0) + (step / 2.0)
            angles = [start + i * step for i in range(n)]

        for name, ang in zip(names, angles):
            pos[name] = (radius * math.cos(ang), radius * math.sin(ang))

    return pos
# ---------------------------------------------------------------------------
# Color mapping
# ---------------------------------------------------------------------------
# (distance, (r, g, b)) stops. Interpolated so fractional distances also work,
# though structural_distance is an int in practice.
COLOR_STOPS = [
    (0, (46, 204, 113)),   # green
    (1, (170, 214, 70)),   # yellow-green
    (2, (241, 196, 15)),   # amber
    (3, (230, 126, 34)),   # orange
    (4, (214, 48, 49)),    # red
    (5, (139, 0, 0)),      # deep crimson
]


def color_for_distance(d):
    """Map a structural distance to a hex color along COLOR_STOPS.
    Values are clamped to the [first, last] stop range."""
    lo, hi = COLOR_STOPS[0][0], COLOR_STOPS[-1][0]
    d = max(lo, min(d, hi))

    for (d0, c0), (d1, c1) in zip(COLOR_STOPS, COLOR_STOPS[1:]):
        if d0 <= d <= d1:
            t = 0.0 if d1 == d0 else (d - d0) / (d1 - d0)
            r, g, b = (round(a + (b - a) * t) for a, b in zip(c0, c1))
            return f"#{r:02x}{g:02x}{b:02x}"

    r, g, b = COLOR_STOPS[-1][1]
    return f"#{r:02x}{g:02x}{b:02x}"


def distance_legend():
    """(label, color) pairs for rendering a distance->color key in the UI."""
    labels = {
        0: "0  root",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5+  far from root",
    }
    return [(labels[d], color_for_distance(d)) for d, _ in COLOR_STOPS]


# ---------------------------------------------------------------------------
# Plotly traces / figure
# ---------------------------------------------------------------------------
def _visible(data, visible):
    return visible is None or data["family"] in visible


def build_edge_trace(graph, pos, visible=None):
    """Single Scatter holding all visible edges, broken by None gaps."""
    xs, ys = [], []
    for u, v in graph.edges():
        if not (_visible(graph.nodes[u], visible)
                and _visible(graph.nodes[v], visible)):
            continue
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        xs += [x0, x1, None]
        ys += [y0, y1, None]

    return go.Scatter(
        x=xs, y=ys, mode="lines",
        line=dict(width=1, color="rgba(160,160,160,0.35)"),
        hoverinfo="none", showlegend=False,
    )


def build_node_trace(graph, pos, visible=None):
    """Single node Scatter. customdata carries the metadata the Dash callback
    reads to populate the sidebar on hover/click."""
    xs, ys, colors, text, custom = [], [], [], [], []
    for name, data in graph.nodes(data=True):
        if not _visible(data, visible):
            continue
        x, y = pos[name]
        xs.append(x)
        ys.append(y)
        colors.append(color_for_distance(data["structural_distance"]))
        text.append(name)
        custom.append([
            data["family"],
            data["half_life"],
            data["legal_status_germany"],
            data["structural_distance"],
            data["notes"],
        ])

    return go.Scatter(
        x=xs, y=ys, mode="markers+text",
        text=text, textposition="top center",
        textfont=dict(color="#e0e0e0", size=10),
        marker=dict(size=16, color=colors,
                    line=dict(width=1.5, color="#111114")),
        customdata=custom,
hovertemplate=(
            "<b>%{text}</b>"
            "<br>Family: %{customdata[0]}"
            "<br>Half-life: %{customdata[1]}"
            "<br>Legal (DE): %{customdata[2]}"
            "<br>Struct. distance: %{customdata[3]}"
            "<br><i>Notes: %{customdata[4]}</i>"  # <--- THIS IS THE ONLY CHANGE
            "<extra></extra>"
        ),
        showlegend=False,
    )


def build_figure(visible_families=None, compounds=COMPOUNDS):
    """Assemble the full dark-mode radial figure.

    visible_families : iterable of family names to show, or None for all.
                       The Dash global-filter callback passes the checked
                       boxes here and returns build_figure(checked) to the
                       graph component.
    """
    graph = build_graph(compounds)
    pos = compute_radial_layout(compounds)
    visible = set(visible_families) if visible_families is not None else None

    edge = build_edge_trace(graph, pos, visible)
    node = build_node_trace(graph, pos, visible)

    fig = go.Figure(data=[edge, node])
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e0e10",
        plot_bgcolor="#0e0e10",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False),
        hoverlabel=dict(bgcolor="#1c1c1f", font_size=12),
        uirevision="constant",  # preserve zoom/pan across filter updates
    )
    return fig


if __name__ == "__main__":
    # Smoke test: layout covers every compound, no dangling parents.
    g = build_graph()
    p = compute_radial_layout()
    assert set(p) == set(g.nodes), "layout/node mismatch"
    print(f"nodes={g.number_of_nodes()} edges={g.number_of_edges()} "
          f"families={len(list_families())}")
    print("distance colors:", [c for _, c in distance_legend()])