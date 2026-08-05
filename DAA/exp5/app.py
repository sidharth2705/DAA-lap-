import streamlit as st
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="Min-Max Divide & Conquer Lab",
    page_icon="🔀",
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
    font-size:62px;margin:0;font-weight:800;
    background:linear-gradient(90deg,#F8FAFC,#67E8F9,#A78BFA,#6EE7B7);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.hero p{max-width:800px;margin:20px auto;color:#AAB5C7;font-size:18px;line-height:1.7}
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
</style>
""", unsafe_allow_html=True)


def parse_array(text):
    values = [x.strip() for x in text.replace(",", " ").split() if x.strip()]
    if not values:
        raise ValueError("Please enter at least one integer.")
    try:
        return [int(x) for x in values]
    except ValueError:
        raise ValueError("Please enter only integer values.")


def minmax_dc(arr, left, right, steps, depth=0):
    # Record the current recursive call.
    steps.append({
        "type": "CALL",
        "left": left,
        "right": right,
        "depth": depth,
        "array": arr[left:right + 1],
        "message": f"Divide: examining indices {left} to {right}."
    })

    # One element.
    if left == right:
        steps.append({
            "type": "BASE",
            "left": left,
            "right": right,
            "depth": depth,
            "array": arr[left:right + 1],
            "min": arr[left],
            "max": arr[left],
            "message": f"Base case: only {arr[left]} is present, so MIN = MAX = {arr[left]}."
        })
        return arr[left], arr[left]

    # Two elements.
    if right == left + 1:
        if arr[left] < arr[right]:
            mn, mx = arr[left], arr[right]
        else:
            mn, mx = arr[right], arr[left]

        steps.append({
            "type": "BASE2",
            "left": left,
            "right": right,
            "depth": depth,
            "array": arr[left:right + 1],
            "min": mn,
            "max": mx,
            "message": (
                f"Two-element case: compare {arr[left]} and {arr[right]} "
                f"→ MIN = {mn}, MAX = {mx}."
            )
        })
        return mn, mx

    mid = (left + right) // 2

    steps.append({
        "type": "SPLIT",
        "left": left,
        "right": right,
        "mid": mid,
        "depth": depth,
        "array": arr[left:right + 1],
        "message": (
            f"Split at index {mid}: "
            f"[{left}..{mid}] and [{mid + 1}..{right}]."
        )
    })

    left_min, left_max = minmax_dc(arr, left, mid, steps, depth + 1)
    right_min, right_max = minmax_dc(arr, mid + 1, right, steps, depth + 1)

    final_min = min(left_min, right_min)
    final_max = max(left_max, right_max)

    steps.append({
        "type": "COMBINE",
        "left": left,
        "right": right,
        "depth": depth,
        "array": arr[left:right + 1],
        "left_min": left_min,
        "left_max": left_max,
        "right_min": right_min,
        "right_max": right_max,
        "min": final_min,
        "max": final_max,
        "message": (
            f"Combine: compare MIN({left_min}, {right_min}) = {final_min}; "
            f"MAX({left_max}, {right_max}) = {final_max}."
        )
    })

    return final_min, final_max


def make_visual(arr, current_step):
    fig = go.Figure()

    for i, value in enumerate(arr):
        is_active = current_step["left"] <= i <= current_step["right"]

        if current_step["type"] == "COMBINE":
            if value == current_step.get("min"):
                marker_color = "#34D399"
                size = 42
            elif value == current_step.get("max"):
                marker_color = "#F59E0B"
                size = 42
            elif is_active:
                marker_color = "#818CF8"
                size = 34
            else:
                marker_color = "rgba(100,116,139,.35)"
                size = 28

        elif current_step["type"] in ("BASE", "BASE2"):
            if is_active:
                marker_color = "#34D399"
                size = 42
            else:
                marker_color = "rgba(100,116,139,.35)"
                size = 28

        else:
            marker_color = "#67E8F9" if is_active else "rgba(100,116,139,.35)"
            size = 36 if is_active else 28

        fig.add_trace(
            go.Scatter(
                x=[i],
                y=[value],
                mode="markers+text",
                text=[str(value)],
                textposition="top center",
                textfont=dict(size=14, color="white"),
                marker=dict(
                    size=size,
                    color=marker_color,
                    line=dict(width=2, color="rgba(255,255,255,.35)")
                ),
                hovertemplate=f"Index: {i}<br>Value: {value}<extra></extra>",
                showlegend=False
            )
        )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=45, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=f"Current Recursive Range: [{current_step['left']} ... {current_step['right']}]",
        xaxis=dict(
            title="Array Index",
            dtick=1,
            gridcolor="rgba(148,163,184,.08)",
            zeroline=False
        ),
        yaxis=dict(
            title="Value",
            gridcolor="rgba(148,163,184,.08)",
            zeroline=False
        ),
        font=dict(color="#CBD5E1")
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


# ---------------- HOME PAGE ----------------

if st.session_state.page == "home":

    st.markdown("""
    <div class="hero">
        <div class="badge">DIVIDE & CONQUER LAB</div>
        <h1>Min-Max Finder</h1>
        <p>
            Find the minimum and maximum values of an array using the
            Divide and Conquer technique — and watch the recursive process
            happen step by step.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="title">What is the Min-Max Problem?</div>
        <div class="muted">
            Given an array of numbers, the goal is to find both the smallest
            value (MIN) and the largest value (MAX). Instead of scanning the
            array in a straightforward way, Divide and Conquer repeatedly
            divides the array into smaller parts, solves each part, and then
            combines their results.
        </div>

        <div class="formula">
            <b>Divide</b> → Split the array into two halves<br>
            <b>Conquer</b> → Find MIN and MAX in each half<br>
            <b>Combine</b> → Compare the two MIN values and two MAX values
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="card">
            <div class="badge">DIVIDE</div>
            <h3>🔀 Split the Array</h3>
            <p class="muted">
                The array is recursively divided into two smaller subarrays
                until each subarray contains one or two elements.
            </p>
            <p>
                <b>Left half</b> → solve recursively<br>
                <b>Right half</b> → solve recursively
            </p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
            <div class="badge">COMBINE</div>
            <h3>⚡ Merge the Results</h3>
            <p class="muted">
                After both halves are solved, compare their results.
                The smaller of the two minimums becomes the final MIN,
                while the larger of the two maximums becomes the final MAX.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="title">Algorithm Logic</div>
        <div class="muted" style="font-size:17px">
            1. If there is one element, it is both MIN and MAX.<br>
            2. If there are two elements, compare them once.<br>
            3. Otherwise, find the middle index.<br>
            4. Recursively find MIN and MAX of the left half.<br>
            5. Recursively find MIN and MAX of the right half.<br>
            6. Compare the two minimums and two maximums.<br>
            7. Return the final MIN and MAX.
        </div>

        <div class="formula">
            <b>MIN = min(leftMin, rightMin)</b>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <b>MAX = max(leftMax, rightMax)</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="metric">
            <div class="metric-value">O(n)</div>
            <div class="metric-label">TIME COMPLEXITY</div>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="metric">
            <div class="metric-value">O(log n)</div>
            <div class="metric-label">RECURSION DEPTH</div>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="metric">
            <div class="metric-value">O(n)</div>
            <div class="metric-label">SPACE COMPLEXITY</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="title">Why Divide and Conquer?</div>
        <div class="muted">
            The important idea is not that the asymptotic time becomes better
            than O(n). Finding both MIN and MAX still requires examining the
            input values. The technique is useful because it demonstrates the
            classic Divide → Conquer → Combine strategy and provides a clear
            recursive solution.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    x, y, z = st.columns([1, 2, 1])

    with y:
        st.markdown("""
        <div class="card" style="text-align:center">
            <div style="font-size:48px">🔀</div>
            <h2>Try Min-Max</h2>
            <p class="muted">
                Enter your own array and visualize every recursive
                divide and combine operation.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("TRY MIN-MAX →", use_container_width=True):
            st.session_state.page = "play"
            st.rerun()

    st.markdown(
        '<div class="footer">Min-Max Lab • Divide and Conquer • DAA</div>',
        unsafe_allow_html=True
    )


# ---------------- PLAYGROUND PAGE ----------------

else:

    c1, c2 = st.columns([4, 1])

    with c1:
        st.markdown(
            '<div class="badge">MIN-MAX PLAYGROUND</div>'
            '<h1 style="font-size:42px">Find Minimum & Maximum</h1>'
            '<div class="muted">'
            'Enter an array and apply Divide and Conquer.'
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

    array_input = st.text_input(
        "Enter array",
        value="38 12 45 7 23 91 4 56 18 73"
    )

    st.markdown(
        '<div class="muted" style="font-size:12px">'
        'Format: <b>38 12 45 7 23</b> or '
        '<b>38, 12, 45, 7, 23</b>'
        '</div>',
        unsafe_allow_html=True
    )

    p, q = st.columns(2)

    with p:
        find_button = st.button(
            "⚡ FIND MIN & MAX",
            use_container_width=True
        )

    with q:
        visualize_button = st.button(
            "▶ VISUALIZE",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    if find_button or visualize_button:

        try:
            arr = parse_array(array_input)

            if len(arr) > 100:
                raise ValueError("Please use an array with at most 100 elements for visualization.")

            steps = []
            minimum, maximum = minmax_dc(
                arr, 0, len(arr) - 1, steps
            )

            st.session_state.data = {
                "array": arr,
                "min": minimum,
                "max": maximum,
                "steps": steps
            }

            st.session_state.visual = visualize_button
            st.session_state.step = 0

        except Exception as ex:
            st.markdown(
                f'<div class="error">❌ <b>Input Error</b><br><br>{ex}</div>',
                unsafe_allow_html=True
            )

    data = st.session_state.data

    # ---------------- OUTPUT ----------------

    if data and not st.session_state.visual:

        arr = data["array"]

        st.markdown(
            '<div class="title">Min-Max Result</div>',
            unsafe_allow_html=True
        )

        a, b, c, d = st.columns(4)

        with a:
            st.markdown(
                f'<div class="metric"><div class="metric-value">'
                f'{data["min"]}</div><div class="metric-label">MINIMUM</div></div>',
                unsafe_allow_html=True
            )

        with b:
            st.markdown(
                f'<div class="metric"><div class="metric-value">'
                f'{data["max"]}</div><div class="metric-label">MAXIMUM</div></div>',
                unsafe_allow_html=True
            )

        with c:
            st.markdown(
                f'<div class="metric"><div class="metric-value">'
                f'{len(arr)}</div><div class="metric-label">ARRAY SIZE</div></div>',
                unsafe_allow_html=True
            )

        with d:
            st.markdown(
                f'<div class="metric"><div class="metric-value">'
                f'{len(data["steps"])}</div><div class="metric-label">RECURSIVE STEPS</div></div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f'<div class="success">'
            f'<h2>🎯 Result Found</h2>'
            f'<div class="muted">'
            f'For the given array, the <b>minimum value is {data["min"]}</b> '
            f'and the <b>maximum value is {data["max"]}</b>.'
            f'</div></div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        fig = go.Figure()

        for i, value in enumerate(arr):
            if value == data["min"]:
                marker_color = "#34D399"
                size = 42
            elif value == data["max"]:
                marker_color = "#F59E0B"
                size = 42
            else:
                marker_color = "#818CF8"
                size = 30

            fig.add_trace(
                go.Scatter(
                    x=[i],
                    y=[value],
                    mode="markers+text",
                    text=[str(value)],
                    textposition="top center",
                    textfont=dict(color="white"),
                    marker=dict(
                        size=size,
                        color=marker_color,
                        line=dict(
                            width=2,
                            color="rgba(255,255,255,.35)"
                        )
                    ),
                    showlegend=False
                )
            )

        fig.update_layout(
            title="Array Values",
            height=420,
            margin=dict(l=20, r=20, t=50, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Index",
                dtick=1,
                gridcolor="rgba(148,163,184,.08)"
            ),
            yaxis=dict(
                title="Value",
                gridcolor="rgba(148,163,184,.08)"
            ),
            font=dict(color="#CBD5E1")
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "▶ VISUALIZE STEP BY STEP",
            use_container_width=True
        ):
            st.session_state.visual = True
            st.session_state.step = 0
            st.rerun()

    # ---------------- VISUALIZATION ----------------

    if data and st.session_state.visual:

        steps = data["steps"]
        arr = data["array"]
        index = st.session_state.step

        st.markdown(
            '<div class="title">🔬 Divide & Conquer Visualization</div>'
            '<div class="muted">'
            'Watch the algorithm divide the array recursively and then '
            'combine the MIN and MAX values.'
            '</div>',
            unsafe_allow_html=True
        )

        if index < len(steps):

            current = steps[index]

            fig = make_visual(arr, current)
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

            if current["type"] in ("COMBINE", "BASE", "BASE2"):
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

            if current["type"] == "COMBINE":

                st.markdown(
                    f"""
                    <div class="step">
                        <h4>🔗 Combine Results</h4>
                        <p class="muted">
                            Left half → MIN = <b>{current["left_min"]}</b>,
                            MAX = <b>{current["left_max"]}</b><br>
                            Right half → MIN = <b>{current["right_min"]}</b>,
                            MAX = <b>{current["right_max"]}</b>
                        </p>
                        <div class="formula">
                            MIN = min({current["left_min"]}, {current["right_min"]})
                            = <b>{current["min"]}</b>
                            <br><br>
                            MAX = max({current["left_max"]}, {current["right_max"]})
                            = <b>{current["max"]}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    f"""
                    <div class="step">
                        <h4>Current Recursive Range</h4>
                        <div class="muted">
                            Indices:
                            <b>{current["left"]}</b>
                            to
                            <b>{current["right"]}</b>
                            <br>
                            Values:
                            <b>{current["array"]}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.progress(
                min((index + 1) / len(steps), 1.0),
                text=f"Step {index + 1} of {len(steps)}"
            )

            # Automatic animation.
            time.sleep(0.65)
            st.session_state.step += 1
            st.rerun()

        else:

            st.markdown(
                f'<div class="success">'
                f'<h2>🎯 Divide & Conquer Complete</h2>'
                f'<div class="muted">'
                f'Final MIN = <b>{data["min"]}</b><br>'
                f'Final MAX = <b>{data["max"]}</b>'
                f'</div></div>',
                unsafe_allow_html=True
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
                if st.button("← CHANGE ARRAY", use_container_width=True):
                    st.session_state.data = None
                    st.session_state.visual = False
                    st.session_state.step = 0
                    st.rerun()

    st.markdown(
        '<div class="footer">'
        'Min-Max Lab • Python • Streamlit • Divide and Conquer'
        '</div>',
        unsafe_allow_html=True
    )