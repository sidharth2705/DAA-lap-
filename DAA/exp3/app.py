import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import re
import time

# ============================================================
# MST LAB — Kruskal's & Prim's Algorithms
# Single-file Streamlit application
# ============================================================

st.set_page_config(
    page_title="MST Algorithm Lab",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------- CSS -----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 10%, rgba(34,211,238,.13), transparent 28%),
        radial-gradient(circle at 92% 15%, rgba(99,102,241,.15), transparent 28%),
        radial-gradient(circle at 50% 90%, rgba(52,211,153,.08), transparent 32%),
        #070B14;
    color: #F8FAFC;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.hero {
    text-align: center;
    padding: 55px 20px 35px;
}

.badge {
    display: inline-block;
    padding: 7px 15px;
    border: 1px solid rgba(103,232,249,.30);
    border-radius: 999px;
    background: rgba(34,211,238,.08);
    color: #67E8F9;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .09em;
    margin-bottom: 18px;
}

.hero h1 {
    font-size: clamp(42px, 7vw, 76px);
    line-height: 1;
    margin: 0;
    font-weight: 800;
    letter-spacing: -0.05em;
    background: linear-gradient(90deg, #F8FAFC, #67E8F9, #A78BFA, #6EE7B7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 820px;
    margin: 22px auto 0;
    color: #AAB5C7;
    font-size: 18px;
    line-height: 1.7;
}

.glass {
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.11);
    border-radius: 22px;
    padding: 25px;
    box-shadow: 0 18px 60px rgba(0,0,0,.18);
    backdrop-filter: blur(16px);
}

.section-title {
    font-size: 27px;
    font-weight: 800;
    margin: 12px 0 10px;
}

.section-subtitle {
    color: #94A3B8;
    line-height: 1.7;
    margin-bottom: 22px;
}

.algorithm-card {
    min-height: 330px;
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 19px;
    padding: 22px;
}

.algorithm-card .number {
    color: #67E8F9;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .1em;
}

.algorithm-card h3 {
    margin: 8px 0 10px;
    font-size: 22px;
}

.algorithm-card p {
    color: #94A3B8;
    font-size: 14px;
    line-height: 1.65;
    min-height: 105px;
}

.complexity-line {
    padding: 8px 0;
    color: #CBD5E1;
    font-size: 13px;
}

.complexity-line span {
    color: #67E8F9;
    font-weight: 800;
}

.formula {
    text-align: center;
    font-size: 21px;
    padding: 22px;
    color: #E0F2FE;
    background: rgba(34,211,238,.045);
    border: 1px solid rgba(34,211,238,.16);
    border-radius: 18px;
}

.compare-table {
    width: 100%;
    border-collapse: collapse;
}

.compare-table th {
    color: #67E8F9;
    text-align: left;
    padding: 14px;
    border-bottom: 1px solid rgba(255,255,255,.1);
}

.compare-table td {
    color: #CBD5E1;
    padding: 14px;
    border-bottom: 1px solid rgba(255,255,255,.06);
}

.metric {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 16px;
    padding: 17px;
    text-align: center;
}

.metric-value {
    font-size: 24px;
    font-weight: 800;
    color: #67E8F9;
}

.metric-label {
    color: #94A3B8;
    font-size: 12px;
    margin-top: 4px;
}

.success-box {
    padding: 22px;
    border-radius: 18px;
    background: rgba(52,211,153,.08);
    border: 1px solid rgba(52,211,153,.25);
}

.error-box {
    padding: 22px;
    border-radius: 18px;
    background: rgba(248,113,113,.08);
    border: 1px solid rgba(248,113,113,.25);
}

.warning-box {
    padding: 18px;
    border-radius: 16px;
    background: rgba(251,191,36,.07);
    border: 1px solid rgba(251,191,36,.22);
    color: #FCD34D;
}

.step-box {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 16px;
    padding: 18px;
    margin-top: 14px;
}

.step-box h4 {
    margin: 0 0 10px;
}

.muted {
    color: #94A3B8;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(103,232,249,.25);
    background: linear-gradient(135deg, rgba(34,211,238,.16), rgba(99,102,241,.16));
    color: #F8FAFC;
    font-weight: 700;
    min-height: 46px;
    transition: all .2s ease;
}

div.stButton > button:hover {
    border-color: rgba(103,232,249,.60);
    transform: translateY(-1px);
    box-shadow: 0 8px 28px rgba(34,211,238,.10);
}

div[data-testid="stTextInput"] input,
textarea {
    background: rgba(255,255,255,.055) !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    color: #F8FAFC !important;
    border-radius: 12px !important;
}

div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,.055);
    border-radius: 12px;
}

.footer {
    text-align: center;
    padding: 45px 0 10px;
    color: #64748B;
    font-size: 13px;
}

.choice-card {
    min-height: 235px;
    text-align: center;
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 22px;
    padding: 28px 22px;
}

.choice-icon {
    font-size: 48px;
    margin-bottom: 10px;
}

.choice-card h3 {
    font-size: 23px;
    margin: 5px 0 9px;
}

.choice-card p {
    color: #94A3B8;
    font-size: 14px;
    line-height: 1.6;
}

.edge-pill {
    display: inline-block;
    padding: 7px 11px;
    margin: 4px;
    border-radius: 999px;
    background: rgba(99,102,241,.10);
    border: 1px solid rgba(129,140,248,.25);
    color: #C4B5FD;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# GRAPH PARSING
# ============================================================

def parse_edges(edge_text):
    """
    Accepts:
        A-B-4, A-C-2, B-C-1
    or:
        A B 4, A C 2, B C 1
    Also accepts one edge per line.
    """
    cleaned = edge_text.replace(";", ",").replace("\n", ",")
    parts = [p.strip() for p in cleaned.split(",") if p.strip()]
    edges = []

    for part in parts:
        tokens = [x for x in re.split(r"\s*[-:]\s*|\s+", part.strip()) if x]

        if len(tokens) != 3:
            raise ValueError(
                f"Could not read '{part}'. Use format A-B-4 or A B 4."
            )

        u, v, w_raw = tokens

        if u == v:
            raise ValueError(f"Self-loop '{u}-{v}' is not allowed.")

        try:
            w = float(w_raw)
        except ValueError:
            raise ValueError(f"Weight '{w_raw}' is not a number.")

        if w < 0:
            raise ValueError("This implementation expects non-negative edge weights.")

        edges.append((u, v, w))

    if not edges:
        raise ValueError("Please enter at least one edge.")

    # Remove exact duplicate undirected edges, keeping the first.
    seen = set()
    unique = []
    for u, v, w in edges:
        key = tuple(sorted((u, v)))
        if key not in seen:
            seen.add(key)
            unique.append((u, v, w))

    return unique


def build_graph(edges):
    G = nx.Graph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G


# ============================================================
# KRUSKAL
# ============================================================

class DSU:
    def __init__(self, nodes):
        self.parent = {x: x for x in nodes}
        self.rank = {x: 0 for x in nodes}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False

        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra

        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1

        return True


def kruskal_algorithm(G):
    nodes = list(G.nodes())
    edges = sorted(
        [(u, v, data["weight"]) for u, v, data in G.edges(data=True)],
        key=lambda x: (x[2], str(x[0]), str(x[1]))
    )

    dsu = DSU(nodes)
    mst = []
    total = 0
    steps = []

    for u, v, w in edges:
        creates_cycle = dsu.find(u) == dsu.find(v)

        if creates_cycle:
            action = "REJECT"
            message = (
                f"Edge {u} — {v} ({fmt_weight(w)}) would create a cycle, "
                f"so Kruskal rejects it."
            )
        else:
            dsu.union(u, v)
            mst.append((u, v, w))
            total += w
            action = "ACCEPT"
            message = (
                f"Edge {u} — {v} ({fmt_weight(w)}) is the smallest available "
                f"safe edge, so Kruskal adds it to the MST."
            )

        steps.append({
            "u": u,
            "v": v,
            "w": w,
            "action": action,
            "message": message,
            "mst": list(mst),
            "total": total,
        })

        if len(mst) == len(nodes) - 1:
            break

    return mst, total, steps


# ============================================================
# PRIM
# ============================================================

def prim_algorithm(G, start):
    if start not in G.nodes:
        start = list(G.nodes())[0]

    visited = {start}
    mst = []
    total = 0
    steps = []

    # Add an initial step so the starting vertex is visible.
    steps.append({
        "u": None,
        "v": start,
        "w": None,
        "action": "START",
        "message": f"Prim starts from vertex {start}.",
        "mst": [],
        "total": 0,
        "visited": set(visited),
        "frontier": sorted(
            [(start, v, G[start][v]["weight"]) for v in G.neighbors(start)],
            key=lambda x: x[2]
        ),
    })

    while len(visited) < len(G.nodes):
        candidates = []

        for u in visited:
            for v in G.neighbors(u):
                if v not in visited:
                    candidates.append((u, v, G[u][v]["weight"]))

        if not candidates:
            break

        u, v, w = min(
            candidates,
            key=lambda x: (x[2], str(x[0]), str(x[1]))
        )

        visited.add(v)
        mst.append((u, v, w))
        total += w

        frontier = []
        for a in visited:
            for b in G.neighbors(a):
                if b not in visited:
                    frontier.append((a, b, G[a][b]["weight"]))

        steps.append({
            "u": u,
            "v": v,
            "w": w,
            "action": "ACCEPT",
            "message": (
                f"Prim selects the minimum-weight edge crossing from the "
                f"visited set to an unvisited vertex: {u} — {v} "
                f"({fmt_weight(w)})."
            ),
            "mst": list(mst),
            "total": total,
            "visited": set(visited),
            "frontier": sorted(frontier, key=lambda x: x[2]),
        })

    return mst, total, steps


# ============================================================
# HELPERS
# ============================================================

def fmt_weight(w):
    if w is None:
        return ""
    return str(int(w)) if float(w).is_integer() else f"{w:g}"


def normalize_edge(u, v):
    return frozenset((u, v))


def make_positions(G):
    # Fixed seed gives a stable, clean layout.
    return nx.spring_layout(G, seed=14, k=1.25)


def render_graph(G, mst_edges=None, active_edge=None,
                 visited=None, frontier=None, title=None):
    """
    Interactive Plotly graph.
    MST edges are green; active edge is cyan; other edges are muted.
    """
    mst_edges = mst_edges or []
    visited = visited or set()
    frontier = frontier or []

    pos = make_positions(G)
    mst_set = {normalize_edge(u, v) for u, v, _ in mst_edges}
    active_set = normalize_edge(*active_edge[:2]) if active_edge else None
    frontier_set = {
        normalize_edge(u, v) for u, v, _ in frontier
    }

    fig = go.Figure()

    # Edges
    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_key = normalize_edge(u, v)

        if active_set == edge_key:
            line_color = "#67E8F9"
            width = 6
        elif edge_key in mst_set:
            line_color = "#34D399"
            width = 5
        elif edge_key in frontier_set:
            line_color = "#A78BFA"
            width = 4
        else:
            line_color = "rgba(148,163,184,.35)"
            width = 2

        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode="lines",
            line=dict(color=line_color, width=width),
            hoverinfo="none",
            showlegend=False
        ))

        # Edge weight at midpoint
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        fig.add_trace(go.Scatter(
            x=[xm],
            y=[ym],
            mode="text",
            text=[fmt_weight(data["weight"])],
            textfont=dict(size=13, color="#CBD5E1"),
            hoverinfo="none",
            showlegend=False
        ))

    # Nodes
    xs, ys, texts, colors, sizes = [], [], [], [], []

    for node in G.nodes():
        x, y = pos[node]
        xs.append(x)
        ys.append(y)
        texts.append(str(node))

        if node in visited:
            colors.append("#34D399")
        else:
            colors.append("#818CF8")

        sizes.append(32 if node in visited else 27)

    fig.add_trace(go.Scatter(
        x=xs,
        y=ys,
        mode="markers+text",
        text=texts,
        textposition="middle center",
        textfont=dict(size=14, color="#FFFFFF", family="Inter"),
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=2, color="rgba(255,255,255,.35)")
        ),
        hovertemplate="Vertex %{text}<extra></extra>",
        showlegend=False
    ))

    fig.update_layout(
        title=title,
        height=540,
        margin=dict(l=10, r=10, t=45, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        font=dict(color="#F8FAFC", family="Inter")
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def result_edges_html(edges):
    if not edges:
        return '<span class="muted">No edges selected.</span>'

    return "".join(
        f'<span class="edge-pill">{u} — {v} : {fmt_weight(w)}</span>'
        for u, v, w in edges
    )


def validate_connected(G):
    if len(G.nodes()) == 0:
        return False
    return nx.is_connected(G)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "result" not in st.session_state:
    st.session_state.result = None

if "selected_algorithm" not in st.session_state:
    st.session_state.selected_algorithm = None

if "visualizing" not in st.session_state:
    st.session_state.visualizing = False

if "step_index" not in st.session_state:
    st.session_state.step_index = 0


def reset_state():
    st.session_state.result = None
    st.session_state.selected_algorithm = None
    st.session_state.visualizing = False
    st.session_state.step_index = 0


# ============================================================
# PAGE 1 — ABOUT
# ============================================================

if st.session_state.page == "home":

    st.markdown(
        """
        <div class="hero">
            <div class="badge">ALGORITHM VISUALIZATION LAB</div>
            <h1>Minimum Spanning Tree</h1>
            <p>
                Build the minimum-cost network using two classic greedy
                algorithms — <b>Kruskal's</b> and <b>Prim's</b>.
                Learn, compare, and watch every edge selection happen.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass">
            <div class="section-title">What is a Minimum Spanning Tree?</div>
            <div class="section-subtitle">
                A <b>Minimum Spanning Tree (MST)</b> of a connected, weighted,
                undirected graph is a spanning tree whose total edge weight
                is as small as possible.
                It connects every vertex with exactly <b>V − 1 edges</b>
                and contains <b>no cycles</b>.
            </div>
            <div class="formula">
                MST → connects all vertices + no cycle + minimum total weight
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Algorithm cards
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="algorithm-card">
                <div class="number">ALGORITHM 01</div>
                <h3>🌐 Kruskal's Algorithm</h3>
                <p>
                    Kruskal's algorithm treats the graph as a collection of
                    edges. It sorts all edges from smallest to largest and
                    repeatedly chooses the next cheapest edge that does not
                    create a cycle.
                </p>
                <div class="complexity-line">
                    Strategy: <span>Edge-based greedy</span>
                </div>
                <div class="complexity-line">
                    Main tool: <span>Union-Find / Disjoint Set</span>
                </div>
                <div class="complexity-line">
                    Typical complexity: <span>O(E log E)</span>
                </div>
                <div class="complexity-line">
                    Key rule: <span>Reject edges that form a cycle</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="algorithm-card">
                <div class="number">ALGORITHM 02</div>
                <h3>🔵 Prim's Algorithm</h3>
                <p>
                    Prim's algorithm starts from one vertex and grows a single
                    tree. At each step it chooses the cheapest edge connecting
                    a visited vertex to an unvisited vertex.
                </p>
                <div class="complexity-line">
                    Strategy: <span>Vertex/tree-based greedy</span>
                </div>
                <div class="complexity-line">
                    Main idea: <span>Grow one connected tree</span>
                </div>
                <div class="complexity-line">
                    Complexity with a binary heap: <span>O(E log V)</span>
                </div>
                <div class="complexity-line">
                    Key rule: <span>Choose the cheapest frontier edge</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">How They Think Differently</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass">
            <table class="compare-table">
                <tr>
                    <th>Feature</th>
                    <th>Kruskal's</th>
                    <th>Prim's</th>
                </tr>
                <tr>
                    <td>Starts with</td>
                    <td>All edges</td>
                    <td>One starting vertex</td>
                </tr>
                <tr>
                    <td>Grows</td>
                    <td>A forest that becomes one tree</td>
                    <td>One connected tree</td>
                </tr>
                <tr>
                    <td>Selection</td>
                    <td>Smallest remaining edge</td>
                    <td>Smallest edge leaving the visited set</td>
                </tr>
                <tr>
                    <td>Cycle handling</td>
                    <td>Union-Find checks cycles</td>
                    <td>Visited/unvisited sets prevent cycles</td>
                </tr>
                <tr>
                    <td>Typical complexity</td>
                    <td>O(E log E)</td>
                    <td>O(E log V) with binary heap</td>
                </tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass">
            <div class="section-title">The Greedy Idea</div>
            <div class="section-subtitle">
                Both algorithms are greedy: they make the best locally safe
                choice at every step while preserving the possibility of
                forming a valid minimum spanning tree.
            </div>

            <div style="text-align:center; font-size:19px; line-height:2.1;">
                <span style="color:#67E8F9;">Choose a cheap edge</span>
                &nbsp;→&nbsp;
                <span style="color:#A78BFA;">Keep the tree valid</span>
                &nbsp;→&nbsp;
                <span style="color:#6EE7B7;">Repeat until V − 1 edges</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Try section — TWO OPTIONS
    st.markdown(
        """
        <div style="text-align:center;">
            <div class="section-title">Try an Algorithm</div>
            <div class="section-subtitle">
                Choose which MST algorithm you want to implement and visualize.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    o1, o2 = st.columns(2)

    with o1:
        st.markdown(
            """
            <div class="choice-card">
                <div class="choice-icon">🌐</div>
                <h3>Kruskal's Algorithm</h3>
                <p>
                    Sort edges → choose the cheapest safe edge →
                    use Union-Find to avoid cycles.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("TRY KRUSKAL'S →", key="try_kruskal", use_container_width=True):
            st.session_state.page = "playground"
            st.session_state.selected_algorithm = "Kruskal's"
            reset_state()
            st.session_state.selected_algorithm = "Kruskal's"
            st.rerun()

    with o2:
        st.markdown(
            """
            <div class="choice-card">
                <div class="choice-icon">🔵</div>
                <h3>Prim's Algorithm</h3>
                <p>
                    Start from a vertex → choose the cheapest frontier edge →
                    grow one connected tree.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("TRY PRIM'S →", key="try_prim", use_container_width=True):
            st.session_state.page = "playground"
            st.session_state.selected_algorithm = "Prim's"
            reset_state()
            st.session_state.selected_algorithm = "Prim's"
            st.rerun()

    st.markdown(
        '<div class="footer">MST Lab • Kruskal\'s • Prim\'s • Greedy Algorithms</div>',
        unsafe_allow_html=True
    )


# ============================================================
# PAGE 2 — PLAYGROUND
# ============================================================

else:

    top1, top2 = st.columns([4, 1])

    with top1:
        st.markdown(
            """
            <div style="padding:15px 0 5px;">
                <div class="badge">MST PLAYGROUND</div>
                <h1 style="font-size:42px; margin:4px 0;">
                    Build the MST
                </h1>
                <div class="muted">
                    Enter a weighted undirected graph and watch the selected
                    algorithm construct its minimum spanning tree.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with top2:
        if st.button("← About MST"):
            st.session_state.page = "home"
            reset_state()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    selected = st.radio(
        "Choose implementation",
        ["Kruskal's", "Prim's"],
        index=0 if st.session_state.selected_algorithm == "Kruskal's" else 1,
        horizontal=True,
    )

    st.session_state.selected_algorithm = selected

    edge_input = st.text_area(
        "Weighted edges",
        value="A-B-4, A-C-2, B-C-1, B-D-5, C-D-8, C-E-10, D-E-2, D-F-6, E-F-3",
        height=115,
        help="Use A-B-4, A-C-2, B-C-1. Separate edges with commas or new lines."
    )

    st.markdown(
        """
        <div class="muted" style="font-size:12px; margin-top:-8px;">
            Format: <b>A-B-4, A-C-2, B-C-1</b> &nbsp;•&nbsp;
            First two values are vertices, third is weight.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Prim start vertex
    try:
        preview_edges = parse_edges(edge_input)
        preview_nodes = sorted(
            set([u for u, _, _ in preview_edges] +
                [v for _, v, _ in preview_edges]),
            key=str
        )
    except Exception:
        preview_nodes = []

    if selected == "Prim's":
        if preview_nodes:
            default_start = preview_nodes[0]
            start_vertex = st.selectbox(
                "Starting vertex for Prim's",
                preview_nodes,
                index=0,
            )
        else:
            start_vertex = None
    else:
        start_vertex = None

    b1, b2 = st.columns(2)

    with b1:
        output_clicked = st.button(
            "⚡ FIND MST",
            use_container_width=True
        )

    with b2:
        visualize_clicked = st.button(
            "▶ VISUALIZE",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------ Execute -------------------------

    if output_clicked or visualize_clicked:

        try:
            edges = parse_edges(edge_input)
            G = build_graph(edges)

            if not validate_connected(G):
                st.markdown(
                    """
                    <div class="error-box">
                        ❌ The graph is disconnected. An MST exists only for
                        a connected graph.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.stop()

            if selected == "Kruskal's":
                mst, total, steps = kruskal_algorithm(G)
                extra = {}
            else:
                if start_vertex is None:
                    start_vertex = list(G.nodes())[0]
                mst, total, steps = prim_algorithm(G, start_vertex)
                extra = {"start": start_vertex}

            st.session_state.result = {
                "edges": edges,
                "graph": G,
                "mst": mst,
                "total": total,
                "steps": steps,
                "algorithm": selected,
                "extra": extra,
            }

            st.session_state.visualizing = visualize_clicked
            st.session_state.step_index = 0

        except Exception as e:
            st.markdown(
                f"""
                <div class="error-box">
                    ❌ <b>Input Error</b><br><br>{str(e)}
                </div>
                """,
                unsafe_allow_html=True
            )
            st.stop()

    data = st.session_state.result

    # -------------------------- OUTPUT ------------------------

    if data and not st.session_state.visualizing:

        st.markdown("<br>", unsafe_allow_html=True)

        G = data["graph"]
        mst = data["mst"]
        total = data["total"]

        st.markdown(
            f"""
            <div class="section-title">
                {data["algorithm"]} — Minimum Spanning Tree
            </div>
            """,
            unsafe_allow_html=True
        )

        render_graph(G, mst_edges=mst, title="Final Minimum Spanning Tree")

        c1, c2, c3, c4 = st.columns(4)

        metrics = [
            (str(len(G.nodes())), "Vertices"),
            (str(len(G.edges())), "Input Edges"),
            (str(len(mst)), "MST Edges"),
            (fmt_weight(total), "Total MST Weight"),
        ]

        for col, (value, label) in zip((c1, c2, c3, c4), metrics):
            with col:
                st.markdown(
                    f"""
                    <div class="metric">
                        <div class="metric-value">{value}</div>
                        <div class="metric-label">{label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="success-box">
                <div style="font-size:27px; font-weight:800;">
                    🎯 MST Complete
                </div>
                <div class="muted" style="margin-top:8px;">
                    {data["algorithm"]} selected <b>{len(mst)}</b> edges
                    with a minimum total weight of <b>{fmt_weight(total)}</b>.
                </div>
                <div style="margin-top:14px;">
                    {result_edges_html(mst)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("▶ VISUALIZE STEP BY STEP", use_container_width=True):
            st.session_state.visualizing = True
            st.session_state.step_index = 0
            st.rerun()

    # ---------------------- VISUALIZATION ---------------------

    if data and st.session_state.visualizing:

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="section-title">
                🔬 {data["algorithm"]} Visualization
            </div>
            <div class="section-subtitle">
                Watch the algorithm make one greedy decision at a time.
                Green edges are already part of the MST.
            </div>
            """,
            unsafe_allow_html=True
        )

        G = data["graph"]
        steps = data["steps"]

        if st.session_state.step_index < len(steps):

            step = steps[st.session_state.step_index]

            active = None
            if step["u"] is not None:
                active = (step["u"], step["v"], step["w"])

            if data["algorithm"] == "Prim's":
                visited = step.get("visited", set())
                frontier = step.get("frontier", [])
            else:
                visited = set()
                frontier = []

            render_graph(
                G,
                mst_edges=step["mst"],
                active_edge=active,
                visited=visited,
                frontier=frontier,
                title=f"Step {st.session_state.step_index + 1} of {len(steps)}"
            )

            left, right = st.columns([1.5, 1])

            with left:
                action = step["action"]

                if action == "ACCEPT":
                    color_message = (
                        f'<div class="success-box">'
                        f'<b>✓ {action}</b><br><br>'
                        f'{step["message"]}'
                        f'</div>'
                    )
                elif action == "REJECT":
                    color_message = (
                        f'<div class="error-box">'
                        f'<b>✕ {action}</b><br><br>'
                        f'{step["message"]}'
                        f'</div>'
                    )
                else:
                    color_message = (
                        f'<div class="warning-box">'
                        f'<b>▶ START</b><br><br>'
                        f'{step["message"]}'
                        f'</div>'
                    )

                st.markdown(color_message, unsafe_allow_html=True)

            with right:
                if data["algorithm"] == "Kruskal's":
                    strategy = """
                    <b>Kruskal's Rule</b><br>
                    Sort edges by weight and take the cheapest edge
                    that does not create a cycle.
                    """
                else:
                    strategy = """
                    <b>Prim's Rule</b><br>
                    From the visited set, choose the cheapest edge
                    leading to an unvisited vertex.
                    """

                st.markdown(
                    f"""
                    <div class="step-box">
                        <h4>Step {st.session_state.step_index + 1}</h4>
                        <div class="muted">
                            MST edges: <b>{len(step["mst"])}</b><br>
                            Current total: <b>{fmt_weight(step["total"])}</b>
                        </div>
                        <hr style="border-color:rgba(255,255,255,.08);">
                        {strategy}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if data["algorithm"] == "Kruskal's":
                st.markdown(
                    """
                    <div class="step-box">
                        <h4>🧩 Union-Find / Disjoint Set</h4>
                        <div class="muted">
                            Kruskal accepts an edge only when its two endpoints
                            belong to different components. If both endpoints
                            already have the same representative, adding the
                            edge would create a cycle, so it is rejected.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="step-box">
                        <h4>🌱 Growing the Tree</h4>
                        <div class="muted">
                            Prim keeps one connected tree. The highlighted
                            frontier edges connect the visited vertices to
                            vertices that have not been visited yet.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            time.sleep(0.85)
            st.session_state.step_index += 1
            st.rerun()

        else:
            render_graph(
                G,
                mst_edges=data["mst"],
                visited=set(G.nodes()) if data["algorithm"] == "Prim's" else set(),
                title="MST Completed"
            )

            st.markdown(
                f"""
                <div class="success-box">
                    <div style="font-size:29px; font-weight:800;">
                        🎯 Minimum Spanning Tree Complete
                    </div>
                    <div class="muted" style="margin-top:8px;">
                        Algorithm: <b>{data["algorithm"]}</b><br>
                        MST edges: <b>{len(data["mst"])}</b><br>
                        Total weight: <b>{fmt_weight(data["total"])}</b>
                    </div>
                    <div style="margin-top:15px;">
                        {result_edges_html(data["mst"])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("🔄 REPLAY", use_container_width=True):
                st.session_state.step_index = 0
                st.rerun()

        with c2:
            if st.button("📊 VIEW OUTPUT", use_container_width=True):
                st.session_state.visualizing = False
                st.rerun()

        with c3:
            if st.button("← CHANGE ALGORITHM", use_container_width=True):
                st.session_state.page = "home"
                reset_state()
                st.rerun()

    st.markdown(
        '<div class="footer">MST Lab • Built with Python, Streamlit, NetworkX & Plotly</div>',
        unsafe_allow_html=True
    )