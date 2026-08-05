import streamlit as st
import time

# ============================================================
# INTERPOLATION SEARCH LAB — Single-file Streamlit Application
# ============================================================

st.set_page_config(
    page_title="Interpolation Search Lab",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------- CSS ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,.16), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(34,211,238,.12), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(139,92,246,.10), transparent 30%),
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
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .08em;
    margin-bottom: 18px;
}

.hero h1 {
    font-size: clamp(42px, 7vw, 78px);
    line-height: 1;
    margin: 0;
    font-weight: 800;
    letter-spacing: -0.05em;
    background: linear-gradient(90deg, #F8FAFC, #67E8F9, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 760px;
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

.info-card {
    min-height: 155px;
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 18px;
    padding: 21px;
}

.info-card .icon {
    font-size: 27px;
    margin-bottom: 10px;
}

.info-card h3 {
    margin: 0 0 8px;
    font-size: 17px;
}

.info-card p {
    color: #94A3B8;
    font-size: 14px;
    line-height: 1.65;
    margin: 0;
}

.formula {
    text-align: center;
    font-size: 25px;
    padding: 25px 10px;
    color: #E0F2FE;
    font-family: Georgia, serif;
    background: rgba(34,211,238,.045);
    border: 1px solid rgba(34,211,238,.16);
    border-radius: 18px;
}

.formula-note {
    text-align: center;
    color: #94A3B8;
    font-size: 13px;
    margin-top: 12px;
}

.complexity {
    text-align: center;
    padding: 22px 10px;
    border-radius: 18px;
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.09);
}

.complexity .value {
    color: #67E8F9;
    font-size: 25px;
    font-weight: 800;
}

.complexity .label {
    color: #94A3B8;
    font-size: 13px;
    margin-top: 5px;
}

.diagram {
    padding: 28px 12px 18px;
}

.diagram-title {
    text-align: center;
    color: #CBD5E1;
    font-size: 15px;
    margin-bottom: 22px;
}

.array-row {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
}

.array-cell {
    width: 65px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.12);
    color: #E2E8F0;
    font-weight: 700;
}

.array-cell.target {
    border-color: #67E8F9;
    background: rgba(34,211,238,.15);
    color: #67E8F9;
    box-shadow: 0 0 25px rgba(34,211,238,.16);
}

.array-cell.active {
    border-color: #A78BFA;
    background: rgba(139,92,246,.18);
    color: #DDD6FE;
    box-shadow: 0 0 25px rgba(139,92,246,.18);
}

.array-cell.found {
    border-color: #34D399;
    background: rgba(52,211,153,.18);
    color: #6EE7B7;
    box-shadow: 0 0 30px rgba(52,211,153,.20);
}

.index-row {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 7px;
    flex-wrap: wrap;
}

.index-cell {
    width: 65px;
    text-align: center;
    color: #64748B;
    font-size: 11px;
}

.marker-row {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 12px;
    flex-wrap: wrap;
}

.marker {
    width: 65px;
    text-align: center;
    color: #A78BFA;
    font-size: 11px;
    font-weight: 700;
}

.marker.target-marker {
    color: #67E8F9;
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

.footer {
    text-align: center;
    padding: 45px 0 10px;
    color: #64748B;
    font-size: 13px;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(103,232,249,.25);
    background: linear-gradient(135deg, rgba(34,211,238,.16), rgba(139,92,246,.16));
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

div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.12);
    color: #F8FAFC;
    border-radius: 12px;
}

div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.12);
    color: #F8FAFC;
    border-radius: 12px;
}

hr {
    border-color: rgba(255,255,255,.08);
}
</style>
""", unsafe_allow_html=True)


# ---------------------- Helper functions ---------------------

def parse_array(raw):
    """Convert space-separated input into a list of integers."""
    parts = raw.strip().split()

    if not parts:
        raise ValueError("Please enter at least one number.")

    try:
        return [int(x) for x in parts]
    except ValueError:
        raise ValueError("Please use only integers separated by spaces.")


def validate_array(arr):
    if len(arr) < 2:
        return False, "Please enter at least two values."

    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False, "The array must be sorted in non-decreasing order."

    return True, ""


def interpolation_search_steps(arr, target):
    """
    Return each state visited by interpolation search.
    Handles duplicate values safely.
    """
    steps = []
    low = 0
    high = len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:
        # If both endpoints have the same value, avoid division by zero.
        if arr[low] == arr[high]:
            comparisons += 1
            steps.append({
                "low": low,
                "high": high,
                "pos": low,
                "target": target,
                "comparisons": comparisons,
                "formula": f"arr[low] = arr[high] = {arr[low]}, so the position is checked directly."
            })

            if arr[low] == target:
                return steps, low

            return steps, -1

        pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])
        comparisons += 1

        formula = (
            f"pos = {low} + (({target} - {arr[low]}) × "
            f"({high} - {low})) / ({arr[high]} - {arr[low]}) = {pos}"
        )

        steps.append({
            "low": low,
            "high": high,
            "pos": pos,
            "target": target,
            "comparisons": comparisons,
            "formula": formula
        })

        if arr[pos] == target:
            return steps, pos

        if arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return steps, -1


def render_array(arr, low=None, high=None, pos=None, target=None, found=False):
    cells = ""

    for i, value in enumerate(arr):
        cls = "array-cell"

        if found and pos == i:
            cls += " found"
        elif pos == i:
            cls += " active"
        elif target == value:
            cls += " target"

        cells += f'<div class="{cls}">{value}</div>'

    indices = "".join(
        f'<div class="index-cell">{i}</div>' for i in range(len(arr))
    )

    markers = ""
    for i in range(len(arr)):
        label = ""
        css = "marker"

        if low == i:
            label = "LOW"
        if high == i:
            label = "HIGH" if not label else "LOW / HIGH"
        if pos == i:
            label = "POS" if not label else label + " / POS"

        if target == arr[i]:
            css += " target-marker"

        markers += f'<div class="{css}">{label}</div>'

    st.markdown(
        f"""
        <div class="diagram">
            <div class="array-row">{cells}</div>
            <div class="index-row">{indices}</div>
            <div class="marker-row">{markers}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------- Session state ------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "search_result" not in st.session_state:
    st.session_state.search_result = None

if "visualize" not in st.session_state:
    st.session_state.visualize = False

if "steps" not in st.session_state:
    st.session_state.steps = []

if "step_index" not in st.session_state:
    st.session_state.step_index = 0


# ---------------------- Navigation ----------------------------

if st.session_state.page == "home":

    # HERO
    st.markdown(
        """
        <div class="hero">
            <div class="badge">ALGORITHM VISUALIZATION LAB</div>
            <h1>Interpolation Search</h1>
            <p>
                Don't search everywhere. Predict where the answer is.
                Explore how interpolation search estimates the position of
                a target inside a sorted array.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # What is it?
    st.markdown('<div class="section-title">What is Interpolation Search?</div>',
                unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-subtitle">
        Interpolation Search is a searching algorithm designed for a
        <b>sorted array</b>. Instead of always checking the middle element
        like Binary Search, it estimates where the target is likely to be
        based on its value.
        <br><br>
        When the values are uniformly distributed, this prediction can make
        the search extremely fast.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="info-card">
                <div class="icon">📊</div>
                <h3>Sorted Data</h3>
                <p>
                The array must be sorted in ascending or non-decreasing order
                before interpolation search can be applied.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="info-card">
                <div class="icon">🎯</div>
                <h3>Predictive Search</h3>
                <p>
                It estimates the target's likely position instead of blindly
                checking the middle of the current range.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="info-card">
                <div class="icon">⚡</div>
                <h3>Fast on Uniform Data</h3>
                <p>
                With uniformly distributed values, the average complexity
                can reach O(log log n).
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Formula
    st.markdown('<div class="section-title">The Interpolation Formula</div>',
                unsafe_allow_html=True)

    st.markdown(
        """
        <div class="formula">
            pos = low +
            ((target − arr[low]) × (high − low))
            ÷ (arr[high] − arr[low])
        </div>
        <div class="formula-note">
            The formula estimates the most likely position of the target.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Complexity
    st.markdown('<div class="section-title">Time & Space Complexity</div>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    complexity_data = [
        ("O(1)", "Best Case"),
        ("O(log log n)", "Average Case"),
        ("O(n)", "Worst Case"),
        ("O(1)", "Space"),
    ]

    for col, (value, label) in zip((c1, c2, c3, c4), complexity_data):
        with col:
            st.markdown(
                f"""
                <div class="complexity">
                    <div class="value">{value}</div>
                    <div class="label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Diagram
    st.markdown('<div class="section-title">How Does It Predict?</div>',
                unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass diagram">
            <div class="diagram-title">
                Target = 80 &nbsp; • &nbsp; The algorithm predicts a position
                closer to the target value.
            </div>
        """,
        unsafe_allow_html=True
    )

    render_array(
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        low=0,
        high=9,
        pos=7,
        target=80
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # CTA
    st.markdown(
        """
        <div class="glass" style="text-align:center;">
            <div style="font-size:32px; font-weight:800;">
                Ready to see it in action?
            </div>
            <div class="muted" style="margin:10px 0 20px;">
                Build your own array and watch interpolation search find the target.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🔎 TRY INTERPOLATION SEARCH", use_container_width=True):
        st.session_state.page = "playground"
        st.session_state.search_result = None
        st.session_state.visualize = False
        st.rerun()

    st.markdown(
        '<div class="footer">Interpolation Search Lab • Built with Python & Streamlit</div>',
        unsafe_allow_html=True
    )


# ============================================================
# PLAYGROUND
# ============================================================

else:

    # Header
    left, right = st.columns([4, 1])

    with left:
        st.markdown(
            """
            <div style="padding:15px 0 5px;">
                <div class="badge">SEARCH PLAYGROUND</div>
                <h1 style="font-size:42px; margin:4px 0;">
                    Interpolation Search
                </h1>
                <div class="muted">
                    Enter a sorted array, choose your target, and run the search.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        if st.button("← Learn"):
            st.session_state.page = "home"
            st.session_state.search_result = None
            st.session_state.visualize = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Inputs
    st.markdown(
        """
        <div class="glass">
            <div class="section-title" style="margin-top:0;">
                Configure Your Search
            </div>
        """,
        unsafe_allow_html=True
    )

    array_input = st.text_input(
        "Sorted array",
        value="10 20 30 40 50 60 70 80 90 100",
        placeholder="Example: 10 20 30 40 50 60 70 80",
        help="Enter integers separated by spaces. The array must be sorted."
    )

    target_input = st.number_input(
        "Target value",
        value=70,
        step=1
    )

    b1, b2 = st.columns(2)

    with b1:
        find_clicked = st.button(
            "⚡ FIND OUTPUT",
            use_container_width=True
        )

    with b2:
        visualize_clicked = st.button(
            "▶ VISUALIZE SEARCH",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Process buttons
    if find_clicked or visualize_clicked:

        try:
            arr = parse_array(array_input)
            valid, message = validate_array(arr)

            if not valid:
                st.markdown(
                    f'<div class="error-box">⚠️ {message}</div>',
                    unsafe_allow_html=True
                )
                st.stop()

            target = int(target_input)
            steps, result = interpolation_search_steps(arr, target)

            st.session_state.steps = steps
            st.session_state.step_index = 0
            st.session_state.search_result = {
                "array": arr,
                "target": target,
                "result": result,
                "comparisons": len(steps),
            }
            st.session_state.visualize = visualize_clicked

        except ValueError as e:
            st.markdown(
                f'<div class="error-box">⚠️ {e}</div>',
                unsafe_allow_html=True
            )
            st.stop()

    # Result
    result_data = st.session_state.search_result

    if result_data and not st.session_state.visualize:

        arr = result_data["array"]
        target = result_data["target"]
        result = result_data["result"]
        comparisons = result_data["comparisons"]

        st.markdown("<br>", unsafe_allow_html=True)

        if result != -1:
            st.markdown(
                f"""
                <div class="success-box">
                    <div style="font-size:25px; font-weight:800;">
                        🎯 Target Found
                    </div>
                    <div class="muted" style="margin-top:7px;">
                        The target <b style="color:#6EE7B7;">{target}</b>
                        was found at index <b style="color:#6EE7B7;">
                        {result}</b>.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="error-box">
                    <div style="font-size:25px; font-weight:800;">
                        ❌ Target Not Found
                    </div>
                    <div class="muted" style="margin-top:7px;">
                        The value <b>{target}</b> does not exist in the array.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)

        metrics = [
            (str(target), "Target"),
            ("Found" if result != -1 else "Not Found", "Result"),
            (str(result) if result != -1 else "—", "Index"),
            (str(comparisons), "Comparisons"),
        ]

        for col, (value, label) in zip((m1, m2, m3, m4), metrics):
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
            <div class="glass">
                <b>Complexity note:</b>
                <span class="muted">
                Average-case performance is O(log log n) when values are
                suitably/uniformly distributed. The worst case is O(n).
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Visualization
    if result_data and st.session_state.visualize:

        arr = result_data["array"]
        target = result_data["target"]
        result = result_data["result"]
        steps = st.session_state.steps

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="section-title">🔬 Search Visualization</div>
            <div class="section-subtitle">
                Watch the algorithm estimate the target's position step by step.
            </div>
            """,
            unsafe_allow_html=True
        )

        # Replay visualization automatically
        if st.session_state.step_index < len(steps):

            current = steps[st.session_state.step_index]

            st.markdown('<div class="glass">', unsafe_allow_html=True)

            render_array(
                arr,
                low=current["low"],
                high=current["high"],
                pos=current["pos"],
                target=target,
                found=False
            )

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            left, right = st.columns([1.5, 1])

            with left:
                st.markdown(
                    f"""
                    <div class="step-box">
                        <h4>Step {st.session_state.step_index + 1}
                            of {len(steps)}</h4>
                        <div class="muted">
                            <b style="color:#CBD5E1;">Low:</b>
                            {current["low"]}
                            &nbsp;&nbsp;•&nbsp;&nbsp;
                            <b style="color:#CBD5E1;">High:</b>
                            {current["high"]}
                            &nbsp;&nbsp;•&nbsp;&nbsp;
                            <b style="color:#67E8F9;">Pos:</b>
                            {current["pos"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="step-box">
                        <h4>🧮 Position Calculation</h4>
                        <div style="color:#67E8F9; font-family:monospace;
                                    font-size:15px; line-height:1.8;">
                            {current["formula"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with right:
                st.markdown(
                    f"""
                    <div class="step-box">
                        <h4>Search Status</h4>
                        <div class="muted">
                            Target: <b>{target}</b><br>
                            Current value:
                            <b>{arr[current["pos"]]}</b><br>
                            Comparisons:
                            <b>{current["comparisons"]}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Auto progress
            time.sleep(0.8)
            st.session_state.step_index += 1
            st.rerun()

        else:

            # Finished visualization
            st.markdown('<div class="glass">', unsafe_allow_html=True)

            render_array(
                arr,
                low=None,
                high=None,
                pos=result if result != -1 else None,
                target=target,
                found=result != -1
            )

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if result != -1:
                st.markdown(
                    f"""
                    <div class="success-box">
                        <div style="font-size:28px; font-weight:800;">
                            🎯 Target Found!
                        </div>
                        <div class="muted" style="margin-top:8px;">
                            Interpolation Search found
                            <b style="color:#6EE7B7;">{target}</b>
                            at index
                            <b style="color:#6EE7B7;">{result}</b>
                            using <b>{len(steps)}</b> comparison(s).
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="error-box">
                        <div style="font-size:28px; font-weight:800;">
                            ❌ Target Not Found
                        </div>
                        <div class="muted" style="margin-top:8px;">
                            Interpolation Search completed after
                            <b>{len(steps)}</b> comparison(s), but
                            <b>{target}</b> was not found.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3)

            with m1:
                st.markdown(
                    f"""
                    <div class="metric">
                        <div class="metric-value">{len(steps)}</div>
                        <div class="metric-label">Iterations / Comparisons</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m2:
                st.markdown(
                    f"""
                    <div class="metric">
                        <div class="metric-value">
                            {"FOUND" if result != -1 else "NOT FOUND"}
                        </div>
                        <div class="metric-label">Final Result</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m3:
                st.markdown(
                    """
                    <div class="metric">
                        <div class="metric-value">O(1)</div>
                        <div class="metric-label">Auxiliary Space</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🔄 VISUALIZE AGAIN", use_container_width=True):
                st.session_state.step_index = 0
                st.rerun()

            if st.button("← NEW SEARCH", use_container_width=True):
                st.session_state.search_result = None
                st.session_state.visualize = False
                st.session_state.steps = []
                st.session_state.step_index = 0
                st.rerun()

    st.markdown(
        '<div class="footer">Interpolation Search Lab • Interactive Algorithm Learning</div>',
        unsafe_allow_html=True
    )