import streamlit as st
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="Matrix Chain Multiplication Lab",
    page_icon="🔗",
    layout="wide"
)

st.markdown("""
<style>
.stApp{
    background:
    radial-gradient(circle at 10% 10%, rgba(34,211,238,.12), transparent 28%),
    radial-gradient(circle at 90% 15%, rgba(139,92,246,.14), transparent 28%),
    #070B14;
    color:#F8FAFC;
}
.block-container{max-width:1200px;padding-top:2rem}
.hero{text-align:center;padding:55px 20px 35px}
.hero h1{
    font-size:58px;margin:0;font-weight:800;
    background:linear-gradient(90deg,#F8FAFC,#67E8F9,#A78BFA,#6EE7B7);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.hero p{max-width:820px;margin:20px auto;color:#AAB5C7;font-size:18px;line-height:1.7}
.badge{
    display:inline-block;padding:7px 15px;border:1px solid rgba(103,232,249,.3);
    border-radius:999px;background:rgba(34,211,238,.08);
    color:#67E8F9;font-size:12px;font-weight:800;letter-spacing:.09em
}
.glass,.card,.step{
    background:rgba(255,255,255,.055);
    border:1px solid rgba(255,255,255,.11);
    border-radius:22px;padding:25px;
    box-shadow:0 18px 60px rgba(0,0,0,.18)
}
.card{min-height:285px}
.title{font-size:28px;font-weight:800;margin:15px 0 10px}
.muted{color:#94A3B8;line-height:1.7}
.formula{
    text-align:center;font-size:19px;padding:22px;margin-top:20px;
    color:#E0F2FE;background:rgba(34,211,238,.05);
    border:1px solid rgba(34,211,238,.16);border-radius:18px
}
.metric{
    background:rgba(255,255,255,.045);
    border:1px solid rgba(255,255,255,.09);
    border-radius:16px;padding:17px;text-align:center
}
.metric-value{font-size:24px;font-weight:800;color:#67E8F9}
.metric-label{color:#94A3B8;font-size:12px}
.success{
    padding:22px;border-radius:18px;background:rgba(52,211,153,.08);
    border:1px solid rgba(52,211,153,.25)
}
.warning{
    padding:18px;border-radius:16px;background:rgba(251,191,36,.07);
    border:1px solid rgba(251,191,36,.22);color:#FCD34D
}
.error{
    padding:22px;border-radius:18px;background:rgba(248,113,113,.08);
    border:1px solid rgba(248,113,113,.25)
}
div.stButton>button{
    width:100%;border-radius:12px;
    border:1px solid rgba(103,232,249,.25);
    background:linear-gradient(135deg,rgba(34,211,238,.16),rgba(99,102,241,.16));
    color:#F8FAFC;font-weight:700;min-height:46px
}
.footer{text-align:center;padding:40px;color:#64748B}
.matrix{
    display:inline-flex;align-items:center;justify-content:center;
    font-size:24px;font-weight:800;color:#E0F2FE;
    padding:16px 25px;border:1px solid rgba(103,232,249,.25);
    border-radius:15px;background:rgba(34,211,238,.06);
    margin:5px
}
table{width:100%;border-collapse:collapse}
th{color:#67E8F9;text-align:center;padding:12px;border-bottom:1px solid rgba(255,255,255,.1)}
td{text-align:center;color:#CBD5E1;padding:12px;border-bottom:1px solid rgba(255,255,255,.06)}
.highlight{background:rgba(103,232,249,.15);border-radius:8px}
</style>
""", unsafe_allow_html=True)


INF = float("inf")


def parse_dimensions(text):
    values = [x.strip() for x in text.replace(",", " ").split() if x.strip()]

    if len(values) < 2:
        raise ValueError(
            "Enter at least 2 dimensions. Example: 10 20 30 40."
        )

    try:
        p = [int(x) for x in values]
    except ValueError:
        raise ValueError("Dimensions must be positive integers.")

    if any(x <= 0 for x in p):
        raise ValueError("All matrix dimensions must be positive.")

    if len(p) > 9:
        raise ValueError(
            "Please use at most 9 dimensions (8 matrices) "
            "so the DP table and visualization remain clear."
        )

    return p


def matrix_names(n):
    return [f"A{i}" for i in range(1, n + 1)]


def matrix_chain_dp(p):
    n = len(p) - 1

    m = [[0] * (n + 1) for _ in range(n + 1)]
    split = [[0] * (n + 1) for _ in range(n + 1)]
    steps = []

    # Length is the number of matrices in the subchain.
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            m[i][j] = INF
            best_k = None

            steps.append({
                "type": "CELL",
                "i": i,
                "j": j,
                "length": length,
                "m": [row[:] for row in m],
                "split": [row[:] for row in split],
                "message": (
                    f"Compute M[{i},{j}] for matrices A{i} through A{j}. "
                    f"Try every possible split k."
                )
            })

            for k in range(i, j):
                cost = (
                    m[i][k]
                    + m[k + 1][j]
                    + p[i - 1] * p[k] * p[j]
                )

                improved = cost < m[i][j]

                if improved:
                    m[i][j] = cost
                    split[i][j] = k
                    best_k = k

                steps.append({
                    "type": "TRY",
                    "i": i,
                    "j": j,
                    "k": k,
                    "length": length,
                    "candidate": cost,
                    "best": None if m[i][j] == INF else m[i][j],
                    "improved": improved,
                    "m": [row[:] for row in m],
                    "split": [row[:] for row in split],
                    "message": (
                        f"Split k={k}: "
                        f"M[{i},{k}] + M[{k + 1},{j}] + "
                        f"p[{i - 1}]×p[{k}]×p[{j}] = {cost}."
                        + (
                            f" New best = {cost}."
                            if improved
                            else " Not better than the current best."
                        )
                    )
                })

            steps.append({
                "type": "FINAL",
                "i": i,
                "j": j,
                "length": length,
                "m": [row[:] for row in m],
                "split": [row[:] for row in split],
                "message": (
                    f"M[{i},{j}] finalized as {m[i][j]} "
                    f"using split k={best_k}."
                )
            })

    return m, split, steps


def optimal_parenthesization(split, i, j):
    if i == j:
        return f"A{i}"

    k = split[i][j]

    if k == 0:
        return f"A{i}...A{j}"

    left = optimal_parenthesization(split, i, k)
    right = optimal_parenthesization(split, k + 1, j)

    return f"({left} × {right})"


def draw_dp_heatmap(m, current_i=None, current_j=None):
    n = len(m) - 1

    labels = []
    values = []

    for i in range(1, n + 1):
        row_labels = []
        row_values = []

        for j in range(1, n + 1):
            row_labels.append(f"M[{i},{j}]")

            if j < i:
                row_values.append(None)
            elif i == j:
                row_values.append(0)
            elif m[i][j] == INF:
                row_values.append(None)
            else:
                row_values.append(m[i][j])

        labels.append(row_labels)
        values.append(row_values)

    fig = go.Figure(
        data=go.Heatmap(
            z=values,
            x=[f"j={j}" for j in range(1, n + 1)],
            y=[f"i={i}" for i in range(1, n + 1)],
            text=labels,
            texttemplate="%{text}<br>%{z}",
            hovertemplate="%{text}<br>Cost: %{z}<extra></extra>",
            colorscale="Viridis",
            colorbar=dict(title="Cost")
        )
    )

    if current_i is not None and current_j is not None:
        fig.add_shape(
            type="rect",
            x0=current_j - 1.45,
            x1=current_j - 0.55,
            y0=current_i - 1.45,
            y1=current_i - 0.55,
            line=dict(color="#67E8F9", width=4),
            fillcolor="rgba(0,0,0,0)"
        )

    fig.update_layout(
        title="Dynamic Programming Cost Table M",
        height=500,
        margin=dict(l=50, r=30, t=60, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1"),
        xaxis=dict(side="top"),
        yaxis=dict(autorange="reversed")
    )

    return fig


if "page" not in st.session_state:
    st.session_state.page = "home"

if "data" not in st.session_state:
    st.session_state.data = None

if "visual" not in st.session_state:
    st.session_state.visual = False

if "step" not in st.session_state:
    st.session_state.step = 0


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.markdown("""
    <div class="hero">
        <div class="badge">DYNAMIC PROGRAMMING LAB</div>
        <h1>Matrix Chain Multiplication</h1>
        <p>
            Find the optimal parenthesization of a matrix chain and minimize
            the total number of scalar multiplications using Dynamic Programming.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="title">What is Matrix Chain Multiplication?</div>
        <div class="muted">
            Matrix Chain Multiplication is an optimization problem where we
            are given a sequence of matrices and need to determine the best
            order in which to multiply them. Matrix multiplication is
            associative, so different parenthesizations produce the same
            final matrix, but they can require very different numbers of
            scalar multiplications.
        </div>

        <div class="formula">
            <b>Goal:</b> Find the parenthesization with the minimum multiplication cost.
            <br><br>
            A<sub>1</sub> × A<sub>2</sub> × ... × A<sub>n</sub>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="card">
            <div class="badge">WHY OPTIMIZE?</div>
            <h3>🔗 Same Result, Different Cost</h3>
            <p class="muted">
                Matrix multiplication is associative:
                (A × B) × C gives the same result as
                A × (B × C). However, the number of scalar
                multiplications can be dramatically different.
            </p>
            <p>
                <b>Objective:</b> Minimize computation cost.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
            <div class="badge">DP IDEA</div>
            <h3>🧠 Store Optimal Subproblems</h3>
            <p class="muted">
                The algorithm computes the optimal cost for shorter matrix
                chains first and stores those results in a DP table.
                Larger chains reuse these already-computed values.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="title">The DP Recurrence</div>
        <div class="formula">
            m[i,j] = min<sub>i ≤ k &lt; j</sub>
            { m[i,k] + m[k+1,j] + p<sub>i-1</sub> × p<sub>k</sub> × p<sub>j</sub> }
        </div>
        <div class="muted" style="margin-top:20px">
            <b>m[i,j]</b> = minimum cost of multiplying A<sub>i</sub> through A<sub>j</sub><br>
            <b>k</b> = position where the chain is split<br>
            <b>p</b> = array containing matrix dimensions
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="title">How the Algorithm Works</div>
        <div class="muted" style="font-size:17px">
            1. Set the cost of a single matrix to 0.<br>
            2. Start with chains containing two matrices.<br>
            3. Try every possible split point k.<br>
            4. Calculate the cost for each split.<br>
            5. Keep the minimum cost.<br>
            6. Increase the chain length and repeat.<br>
            7. The final answer is stored in M[1,n].
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="metric">
            <div class="metric-value">O(n³)</div>
            <div class="metric-label">TIME COMPLEXITY</div>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="metric">
            <div class="metric-value">O(n²)</div>
            <div class="metric-label">SPACE COMPLEXITY</div>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="metric">
            <div class="metric-value">DP</div>
            <div class="metric-label">TECHNIQUE</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="title">Example</div>
        <div class="muted">
            Suppose the dimensions are:
        </div>
        <div class="formula">
            p = [10, 20, 30, 40]
        </div>
        <div class="muted">
            This represents:
            <b>A1 = 10×20</b>,
            <b>A2 = 20×30</b>,
            <b>A3 = 30×40</b>.
            The algorithm determines whether
            (A1 × A2) × A3 or A1 × (A2 × A3)
            requires fewer scalar multiplications.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    x, y, z = st.columns([1, 2, 1])

    with y:
        st.markdown("""
        <div class="card" style="text-align:center">
            <div style="font-size:48px">🔗</div>
            <h2>Try Matrix Chain</h2>
            <p class="muted">
                Enter matrix dimensions, calculate the optimal cost,
                and visualize the DP table step by step.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("TRY MATRIX CHAIN →", use_container_width=True):
            st.session_state.page = "play"
            st.rerun()

    st.markdown(
        '<div class="footer">'
        'Matrix Chain Multiplication Lab • Dynamic Programming • DAA'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# PLAYGROUND
# ============================================================

else:

    c1, c2 = st.columns([4, 1])

    with c1:
        st.markdown(
            '<div class="badge">MATRIX CHAIN PLAYGROUND</div>'
            '<h1 style="font-size:42px">Optimal Cost Computation</h1>'
            '<div class="muted">'
            'Enter the dimension array p and find the optimal multiplication order.'
            '</div>',
            unsafe_allow_html=True
        )

    with c2:
        if st.button("← ABOUT"):
            st.session_state.page = "home"
            st.session_state.data = None
            st.session_state.visual = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    dimension_input = st.text_input(
        "Enter matrix dimensions p",
        value="10 20 30 40"
    )

    st.markdown(
        '<div class="muted" style="font-size:12px">'
        'For n matrices, enter n+1 dimensions. '
        'Example: <b>10 20 30 40</b> means '
        'A1=10×20, A2=20×30, A3=30×40.'
        '</div>',
        unsafe_allow_html=True
    )

    try:
        preview_p = parse_dimensions(dimension_input)
        preview_n = len(preview_p) - 1
        preview_names = matrix_names(preview_n)

        matrices_html = ""

        for i in range(preview_n):
            matrices_html += (
                f'<span class="matrix">'
                f'{preview_names[i]} = {preview_p[i]}×{preview_p[i + 1]}'
                f'</span>'
            )

        st.markdown(
            f'<div style="margin-top:20px">{matrices_html}</div>',
            unsafe_allow_html=True
        )

    except Exception:
        pass

    pcol, qcol = st.columns(2)

    with pcol:
        find_button = st.button(
            "⚡ FIND OPTIMAL COST",
            use_container_width=True
        )

    with qcol:
        visualize_button = st.button(
            "▶ VISUALIZE DP",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    if find_button or visualize_button:

        try:
            p = parse_dimensions(dimension_input)

            m, split, steps = matrix_chain_dp(p)

            n = len(p) - 1
            optimal_cost = m[1][n]
            parenthesization = optimal_parenthesization(
                split, 1, n
            )

            st.session_state.data = {
                "p": p,
                "m": m,
                "split": split,
                "steps": steps,
                "cost": optimal_cost,
                "parenthesization": parenthesization
            }

            st.session_state.visual = visualize_button
            st.session_state.step = 0

        except Exception as ex:

            st.markdown(
                f'<div class="error">'
                f'❌ <b>Input Error</b><br><br>{ex}'
                f'</div>',
                unsafe_allow_html=True
            )

    data = st.session_state.data

    # ========================================================
    # OUTPUT
    # ========================================================

    if data and not st.session_state.visual:

        n = len(data["p"]) - 1

        st.markdown(
            '<div class="title">Optimal Result</div>',
            unsafe_allow_html=True
        )

        a, b, c = st.columns(3)

        with a:
            st.markdown(
                f'<div class="metric">'
                f'<div class="metric-value">{data["cost"]:,}</div>'
                f'<div class="metric-label">MINIMUM SCALAR MULTIPLICATIONS</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with b:
            st.markdown(
                f'<div class="metric">'
                f'<div class="metric-value">{n}</div>'
                f'<div class="metric-label">NUMBER OF MATRICES</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with c:
            st.markdown(
                f'<div class="metric">'
                f'<div class="metric-value">O(n³)</div>'
                f'<div class="metric-label">TIME COMPLEXITY</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f'<div class="success">'
            f'<h2>🎯 Optimal Parenthesization</h2>'
            f'<div class="formula">'
            f'{data["parenthesization"]}'
            f'</div>'
            f'<p class="muted">'
            f'This ordering requires only '
            f'<b>{data["cost"]:,}</b> scalar multiplications.'
            f'</p>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.plotly_chart(
            draw_dp_heatmap(data["m"]),
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Display final DP table as HTML.
        m = data["m"]

        header = "<tr><th>i \\ j</th>"
        for j in range(1, n + 1):
            header += f"<th>{j}</th>"
        header += "</tr>"

        rows = ""

        for i in range(1, n + 1):

            rows += f"<tr><th>{i}</th>"

            for j in range(1, n + 1):

                if j < i:
                    value = "—"
                else:
                    value = str(m[i][j])

                rows += f"<td>{value}</td>"

            rows += "</tr>"

        st.markdown(
            f'<div class="glass">'
            f'<div class="title">Final DP Cost Table M</div>'
            f'<table>{header}{rows}</table>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "▶ VISUALIZE DP STEP BY STEP",
            use_container_width=True
        ):
            st.session_state.visual = True
            st.session_state.step = 0
            st.rerun()

    # ========================================================
    # VISUALIZATION
    # ========================================================

    if data and st.session_state.visual:

        steps = data["steps"]
        index = st.session_state.step

        st.markdown(
            '<div class="title">🔬 DP Table Visualization</div>'
            '<div class="muted">'
            'Watch the algorithm fill the DP table by increasing chain length '
            'and testing every possible split.'
            '</div>',
            unsafe_allow_html=True
        )

        if index < len(steps):

            current = steps[index]

            current_i = current.get("i")
            current_j = current.get("j")

            st.plotly_chart(
                draw_dp_heatmap(
                    current["m"],
                    current_i,
                    current_j
                ),
                use_container_width=True,
                config={"displayModeBar": False}
            )

            if current["type"] in ("FINAL",):
                box_class = "success"
            else:
                box_class = "warning"

            st.markdown(
                f'<div class="{box_class}">'
                f'<b>{current["type"]}</b><br><br>'
                f'{current["message"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            if current["type"] == "TRY":

                candidate = current["candidate"]
                best = current["best"]

                st.markdown(
                    f"""
                    <div class="step">
                        <h4>🧮 Split Evaluation</h4>
                        <div class="formula">
                            Candidate Cost = <b>{candidate:,}</b>
                            <br>
                            Current Best =
                            <b>{best:,}</b>
                        </div>
                        <p class="muted">
                            Split position:
                            <b>k = {current["k"]}</b>
                            <br>
                            {"✅ This split gives a better cost." if current["improved"]
                             else "❌ This split does not improve the current best."}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif current["type"] == "CELL":

                st.markdown(
                    f"""
                    <div class="step">
                        <h4>📦 New DP Cell</h4>
                        <p class="muted">
                            We are calculating <b>M[{current["i"]},{current["j"]}]</b>.
                            Every split from
                            <b>k={current["i"]}</b> to
                            <b>k={current["j"] - 1}</b>
                            will be tested.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif current["type"] == "FINAL":

                st.markdown(
                    f"""
                    <div class="step">
                        <h4>✅ Cell Finalized</h4>
                        <div class="formula">
                            M[{current["i"]},{current["j"]}]
                            =
                            <b>{current["m"][current["i"]][current["j"]]:,}</b>
                        </div>
                        <p class="muted">
                            The minimum cost among all possible split points
                            has been stored in this DP cell.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.progress(
                min((index + 1) / len(steps), 1.0),
                text=f"Step {index + 1} of {len(steps)}"
            )

            time.sleep(0.65)
            st.session_state.step += 1
            st.rerun()

        else:

            st.markdown(
                f'<div class="success">'
                f'<h2>🎯 Dynamic Programming Complete</h2>'
                f'<div class="muted">'
                f'Minimum scalar multiplications: '
                f'<b>{data["cost"]:,}</b><br><br>'
                f'Optimal order: '
                f'<b>{data["parenthesization"]}</b>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            st.plotly_chart(
                draw_dp_heatmap(data["m"]),
                use_container_width=True,
                config={"displayModeBar": False}
            )

            a, b, c = st.columns(3)

            with a:
                if st.button("🔄 REPLAY", use_container_width=True):
                    st.session_state.step = 0
                    st.rerun()

            with b:
                if st.button("📊 VIEW OUTPUT", use_container_width=True):
                    st.session_state.visual = False
                    st.rerun()

            with c:
                if st.button("← CHANGE INPUT", use_container_width=True):
                    st.session_state.data = None
                    st.session_state.visual = False
                    st.session_state.step = 0
                    st.rerun()

    st.markdown(
        '<div class="footer">'
        'Matrix Chain Multiplication Lab • Python • Streamlit • Dynamic Programming'
        '</div>',
        unsafe_allow_html=True
    )