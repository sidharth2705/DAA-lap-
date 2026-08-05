import streamlit as st
import time

# ============================================================
# STRING MATCHING LAB
# Naive Search • Rabin-Karp • KMP
# Single-file Streamlit application
# ============================================================

st.set_page_config(
    page_title="String Matching Lab",
    page_icon="🔎",
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
        radial-gradient(circle at 8% 10%, rgba(99,102,241,.16), transparent 28%),
        radial-gradient(circle at 92% 15%, rgba(34,211,238,.11), transparent 27%),
        radial-gradient(circle at 50% 90%, rgba(139,92,246,.10), transparent 32%),
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
    background: linear-gradient(90deg, #F8FAFC, #67E8F9, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 790px;
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
    min-height: 290px;
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
    font-size: 21px;
}

.algorithm-card p {
    color: #94A3B8;
    font-size: 14px;
    line-height: 1.65;
    min-height: 72px;
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
    font-family: Georgia, serif;
    background: rgba(34,211,238,.045);
    border: 1px solid rgba(34,211,238,.16);
    border-radius: 18px;
}

.compare-table {
    width: 100%;
    border-collapse: collapse;
    overflow: hidden;
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

.array-wrap {
    overflow-x: auto;
    padding: 22px 5px;
}

.string-row {
    display: flex;
    justify-content: center;
    min-width: max-content;
}

.char-cell {
    width: 48px;
    height: 52px;
    margin: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.10);
    color: #E2E8F0;
    font-size: 18px;
    font-weight: 800;
}

.char-cell.match {
    background: rgba(52,211,153,.15);
    border-color: rgba(52,211,153,.55);
    color: #6EE7B7;
}

.char-cell.mismatch {
    background: rgba(248,113,113,.15);
    border-color: rgba(248,113,113,.55);
    color: #FCA5A5;
}

.char-cell.window {
    background: rgba(139,92,246,.12);
    border-color: rgba(167,139,250,.45);
}

.pattern-row {
    display: flex;
    justify-content: center;
    min-width: max-content;
    margin-top: 7px;
}

.pattern-cell {
    width: 48px;
    height: 44px;
    margin: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba(99,102,241,.12);
    border: 1px solid rgba(129,140,248,.35);
    color: #C4B5FD;
    font-weight: 800;
}

.pattern-cell.match {
    background: rgba(52,211,153,.15);
    border-color: rgba(52,211,153,.55);
    color: #6EE7B7;
}

.index-row {
    display: flex;
    justify-content: center;
    min-width: max-content;
}

.index-cell {
    width: 48px;
    margin: 3px;
    text-align: center;
    color: #64748B;
    font-size: 10px;
}

.hash-card {
    text-align: center;
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 16px;
    padding: 18px;
}

.hash-value {
    font-size: 27px;
    font-weight: 800;
    color: #67E8F9;
    margin-top: 6px;
}

.lps-cell {
    width: 52px;
    height: 48px;
    margin: 3px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba(99,102,241,.10);
    border: 1px solid rgba(129,140,248,.30);
}

.lps-value {
    color: #67E8F9;
    font-weight: 800;
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

hr {
    border-color: rgba(255,255,255,.08);
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# ALGORITHMS
# ============================================================

def naive_search(text, pattern):
    """Naive string matching. Returns matches, comparisons, and steps."""
    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0
    steps = []

    if m == 0:
        return [0], 0, steps

    for i in range(n - m + 1):
        matched = True
        compared_positions = []

        for j in range(m):
            comparisons += 1
            compared_positions.append(j)

            if text[i + j] != pattern[j]:
                matched = False
                steps.append({
                    "start": i,
                    "compare_index": j,
                    "text_index": i + j,
                    "pattern_index": j,
                    "match": False,
                    "message": (
                        f"Mismatch: text[{i+j}] = '{text[i+j]}' "
                        f"but pattern[{j}] = '{pattern[j]}'. Shift by 1."
                    ),
                    "comparisons": comparisons,
                })
                break

            steps.append({
                "start": i,
                "compare_index": j,
                "text_index": i + j,
                "pattern_index": j,
                "match": True,
                "message": (
                    f"Match: '{text[i+j]}' = '{pattern[j]}'. "
                    f"Continue comparing."
                ),
                "comparisons": comparisons,
            })

        if matched:
            matches.append(i)
            steps.append({
                "start": i,
                "compare_index": m - 1,
                "text_index": i + m - 1,
                "pattern_index": m - 1,
                "match": True,
                "found": True,
                "message": f"Pattern found at index {i}.",
                "comparisons": comparisons,
            })

    return matches, comparisons, steps


def rolling_hash(s, base=256, mod=1000000007):
    h = 0
    for ch in s:
        h = (h * base + ord(ch)) % mod
    return h


def rabin_karp_search(text, pattern):
    """Rabin-Karp using a rolling hash."""
    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0
    steps = []

    if m == 0:
        return [0], 0, steps

    if m > n:
        return [], 0, steps

    base = 256
    mod = 1000000007

    pattern_hash = rolling_hash(pattern, base, mod)
    window_hash = rolling_hash(text[:m], base, mod)

    high_power = pow(base, m - 1, mod)

    for i in range(n - m + 1):
        hash_equal = window_hash == pattern_hash

        if hash_equal:
            # Verify characters because equal hashes can theoretically collide.
            actual_match = True
            for j in range(m):
                comparisons += 1
                if text[i + j] != pattern[j]:
                    actual_match = False
                    steps.append({
                        "start": i,
                        "hash_equal": True,
                        "verified": False,
                        "compare_index": j,
                        "message": (
                            f"Hash match at window {i}, but character verification "
                            f"failed at position {j}."
                        ),
                        "comparisons": comparisons,
                        "window_hash": window_hash,
                        "pattern_hash": pattern_hash,
                    })
                    break

            if actual_match:
                matches.append(i)
                steps.append({
                    "start": i,
                    "hash_equal": True,
                    "verified": True,
                    "found": True,
                    "compare_index": m - 1,
                    "message": f"Hash match verified. Pattern found at index {i}.",
                    "comparisons": comparisons,
                    "window_hash": window_hash,
                    "pattern_hash": pattern_hash,
                })
        else:
            steps.append({
                "start": i,
                "hash_equal": False,
                "verified": False,
                "message": (
                    f"Hash mismatch at window {i}. "
                    f"Slide the window by one position."
                ),
                "comparisons": comparisons,
                "window_hash": window_hash,
                "pattern_hash": pattern_hash,
            })

        if i < n - m:
            window_hash = (
                (window_hash - ord(text[i]) * high_power) * base
                + ord(text[i + m])
            ) % mod

    return matches, comparisons, steps


def build_lps(pattern):
    """Build the KMP LPS array."""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    steps = []

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            steps.append({
                "i": i,
                "length": length,
                "value": lps[i],
                "match": True,
                "message": (
                    f"pattern[{i}] = pattern[{length-1}]. "
                    f"LPS[{i}] becomes {lps[i]}."
                ),
            })
            i += 1
        elif length != 0:
            old = length
            length = lps[length - 1]
            steps.append({
                "i": i,
                "length": length,
                "value": lps[i],
                "match": False,
                "message": (
                    f"Mismatch. Jump from prefix length {old} "
                    f"to LPS[{old-1}] = {length}."
                ),
            })
        else:
            lps[i] = 0
            steps.append({
                "i": i,
                "length": 0,
                "value": 0,
                "match": False,
                "message": f"No matching prefix. LPS[{i}] = 0.",
            })
            i += 1

    return lps, steps


def kmp_search(text, pattern):
    """KMP string matching."""
    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0
    steps = []

    if m == 0:
        return [0], 0, [], [0]

    lps, lps_steps = build_lps(pattern)

    i = 0
    j = 0

    while i < n:
        comparisons += 1

        if text[i] == pattern[j]:
            steps.append({
                "text_index": i,
                "pattern_index": j,
                "match": True,
                "message": (
                    f"Match: text[{i}] = '{text[i]}' and "
                    f"pattern[{j}] = '{pattern[j]}'."
                ),
                "comparisons": comparisons,
                "lps": lps,
            })
            i += 1
            j += 1

            if j == m:
                start = i - m
                matches.append(start)
                steps.append({
                    "text_index": i - 1,
                    "pattern_index": j - 1,
                    "match": True,
                    "found": True,
                    "message": f"Pattern found at index {start}.",
                    "comparisons": comparisons,
                    "lps": lps,
                })
                j = lps[j - 1]
        else:
            steps.append({
                "text_index": i,
                "pattern_index": j,
                "match": False,
                "message": (
                    f"Mismatch: text[{i}] = '{text[i]}' and "
                    f"pattern[{j}] = '{pattern[j]}'."
                ),
                "comparisons": comparisons,
                "lps": lps,
            })

            if j != 0:
                old_j = j
                j = lps[j - 1]
                steps.append({
                    "text_index": i,
                    "pattern_index": j,
                    "match": False,
                    "jump": True,
                    "message": (
                        f"KMP uses LPS: jump pattern index from "
                        f"{old_j} to {j} without moving the text index."
                    ),
                    "comparisons": comparisons,
                    "lps": lps,
                })
            else:
                i += 1

    return matches, comparisons, steps, lps


# ============================================================
# RENDERING HELPERS
# ============================================================

def render_text_pattern(text, pattern, start=None, compare_index=None,
                        text_index=None, found=False):
    """Render text and pattern as aligned character cards."""
    n = len(text)
    m = len(pattern)

    text_html = ""
    index_html = ""
    pattern_html = ""

    for i, ch in enumerate(text):
        cls = "char-cell"

        if found and start is not None and start <= i < start + m:
            cls += " match"
        elif text_index == i:
            cls += "match" if compare_index is not None else "window"
        elif start is not None and start <= i < start + m:
            cls += "window"

        display = "&nbsp;" if ch == " " else ch
        text_html += f'<div class="{cls}">{display}</div>'
        index_html += f'<div class="index-cell">{i}</div>'

    if start is not None:
        for j in range(n):
            if start <= j < start + m:
                p_idx = j - start
                pch = pattern[p_idx]
                cls = "pattern-cell"

                if found:
                    cls += " match"
                elif text_index == j:
                    cls += "match" if compare_index is not None else ""
                elif compare_index == p_idx:
                    cls += "match"

                pattern_html += f'<div class="{cls}">{pch}</div>'
            else:
                pattern_html += '<div style="width:54px;"></div>'
    else:
        pattern_html = "".join(
            f'<div class="pattern-cell">{ch}</div>' for ch in pattern
        )

    st.markdown(
        f"""
        <div class="glass array-wrap">
            <div style="color:#94A3B8; font-size:12px; margin:0 0 8px 5px;">
                TEXT
            </div>
            <div class="string-row">{text_html}</div>
            <div class="index-row">{index_html}</div>
            <div style="height:10px;"></div>
            <div style="color:#94A3B8; font-size:12px; margin:0 0 8px 5px;">
                PATTERN
            </div>
            <div class="pattern-row">{pattern_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_lps(pattern, lps, active=None):
    chars = ""
    values = ""

    for i, ch in enumerate(pattern):
        cls = "lps-cell"
        if active == i:
            cls += " match"

        chars += f'<div class="{cls}">{ch}</div>'
        values += (
            f'<div class="lps-cell">'
            f'<span class="lps-value">{lps[i]}</span></div>'
        )

    st.markdown(
        f"""
        <div class="glass">
            <div style="color:#94A3B8; font-size:12px; margin-bottom:8px;">
                PATTERN
            </div>
            <div style="display:flex; justify-content:center; min-width:max-content;">
                {chars}
            </div>
            <div style="color:#94A3B8; font-size:12px; margin:12px 0 8px;">
                LPS TABLE
            </div>
            <div style="display:flex; justify-content:center; min-width:max-content;">
                {values}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def reset_search():
    st.session_state.result = None
    st.session_state.visualizing = False
    st.session_state.algorithm = None
    st.session_state.step_index = 0


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "result" not in st.session_state:
    st.session_state.result = None

if "visualizing" not in st.session_state:
    st.session_state.visualizing = False

if "algorithm" not in st.session_state:
    st.session_state.algorithm = None

if "step_index" not in st.session_state:
    st.session_state.step_index = 0


# ============================================================
# PAGE 1 — HOME / LEARN
# ============================================================

if st.session_state.page == "home":

    st.markdown(
        """
        <div class="hero">
            <div class="badge">ALGORITHM VISUALIZATION LAB</div>
            <h1>String Matching</h1>
            <p>
                Three algorithms. One pattern. Discover how Naive Search,
                Rabin-Karp, and KMP solve the same problem in completely
                different ways.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass">
            <div class="section-title">What is String Matching?</div>
            <div class="section-subtitle">
                String matching is the process of finding where a smaller
                <b>pattern</b> occurs inside a larger <b>text</b>.
                Search engines, text editors, DNA analysis, plagiarism
                detection, and many other systems use string matching ideas.
            </div>

            <div style="text-align:center; padding:15px;">
                <div style="color:#94A3B8; font-size:12px;">TEXT</div>
                <div style="font-size:24px; font-weight:800;
                            color:#E2E8F0; margin:8px;">
                    A B A B D A B A C A B
                </div>
                <div style="color:#94A3B8; font-size:12px; margin-top:18px;">
                    PATTERN
                </div>
                <div style="font-size:24px; font-weight:800;
                            color:#67E8F9; margin:8px;">
                    A B A
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Meet the Three Algorithms</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    cards = [
        (
            c1,
            "01",
            "Naive Search",
            "Compare the pattern against every possible position in the text. "
            "Simple and easy to understand, but it may repeat many comparisons.",
            "O(nm)",
            "O(1)",
            "Direct comparison"
        ),
        (
            c2,
            "02",
            "Rabin-Karp",
            "Use a rolling hash to compare the pattern with each text window. "
            "Only verify characters when the hashes match.",
            "O(nm)",
            "O(1)",
            "Rolling hash"
        ),
        (
            c3,
            "03",
            "Knuth-Morris-Pratt",
            "Build an LPS table so the pattern can jump over characters that "
            "have already been matched.",
            "O(n + m)",
            "O(m)",
            "LPS / prefix table"
        ),
    ]

    for col, number, name, description, worst, space, idea in cards:
        with col:
            st.markdown(
                f"""
                <div class="algorithm-card">
                    <div class="number">ALGORITHM {number}</div>
                    <h3>{name}</h3>
                    <p>{description}</p>
                    <div class="complexity-line">
                        Worst Case: <span>{worst}</span>
                    </div>
                    <div class="complexity-line">
                        Space: <span>{space}</span>
                    </div>
                    <div class="complexity-line">
                        Core Idea: <span>{idea}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Complexity Comparison</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass">
            <table class="compare-table">
                <tr>
                    <th>Algorithm</th>
                    <th>Best Case</th>
                    <th>Average Case</th>
                    <th>Worst Case</th>
                    <th>Extra Space</th>
                </tr>
                <tr>
                    <td>Naive</td>
                    <td>O(n)</td>
                    <td>O(nm)</td>
                    <td>O(nm)</td>
                    <td>O(1)</td>
                </tr>
                <tr>
                    <td>Rabin-Karp</td>
                    <td>O(n + m)</td>
                    <td>O(n + m)</td>
                    <td>O(nm)</td>
                    <td>O(1)</td>
                </tr>
                <tr>
                    <td>KMP</td>
                    <td>O(n + m)</td>
                    <td>O(n + m)</td>
                    <td>O(n + m)</td>
                    <td>O(m)</td>
                </tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # KMP formula / LPS concept
    st.markdown(
        '<div class="section-title">The KMP Secret: LPS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass">
            <div class="section-subtitle">
                KMP uses an <b>LPS (Longest Proper Prefix which is also a Suffix)</b>
                table. It tells KMP how far the pattern can jump after a mismatch.
            </div>
        """,
        unsafe_allow_html=True
    )

    render_lps("ABABAC", [0, 0, 1, 2, 3, 0])

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass" style="text-align:center;">
            <div style="font-size:30px; font-weight:800;">
                Ready to compare them?
            </div>
            <div class="muted" style="margin:10px 0 20px;">
                Enter your own text and pattern, then watch all three algorithms
                search through the same input.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🔎 TRY STRING MATCHING", use_container_width=True):
        st.session_state.page = "playground"
        reset_search()
        st.rerun()

    st.markdown(
        '<div class="footer">String Matching Lab • Naive • Rabin-Karp • KMP</div>',
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
                <div class="badge">STRING PLAYGROUND</div>
                <h1 style="font-size:42px; margin:4px 0;">
                    Search & Compare
                </h1>
                <div class="muted">
                    Give all three algorithms the same text and pattern.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with top2:
        if st.button("← Learn"):
            st.session_state.page = "home"
            reset_search()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    text = st.text_input(
        "Text",
        value="ABABDABACDABABCABAB",
        placeholder="Enter the text to search inside..."
    )

    pattern = st.text_input(
        "Pattern",
        value="ABABCABAB",
        placeholder="Enter the pattern to search for..."
    )

    b1, b2 = st.columns(2)

    with b1:
        find_clicked = st.button("⚡ FIND OUTPUT", use_container_width=True)

    with b2:
        visualize_clicked = st.button("▶ VISUALIZE", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------- Run search --------------------

    if find_clicked or visualize_clicked:

        if not text:
            st.markdown(
                '<div class="error-box">⚠️ Please enter a text.</div>',
                unsafe_allow_html=True
            )
            st.stop()

        if not pattern:
            st.markdown(
                '<div class="error-box">⚠️ Please enter a pattern.</div>',
                unsafe_allow_html=True
            )
            st.stop()

        if len(pattern) > len(text):
            st.markdown(
                '<div class="warning-box">⚠️ The pattern is longer than the text, '
                'so it cannot be found.</div>',
                unsafe_allow_html=True
            )

        naive_matches, naive_comparisons, naive_steps = naive_search(
            text, pattern
        )

        rk_matches, rk_comparisons, rk_steps = rabin_karp_search(
            text, pattern
        )

        kmp_matches, kmp_comparisons, kmp_steps, lps = kmp_search(
            text, pattern
        )

        st.session_state.result = {
            "text": text,
            "pattern": pattern,
            "naive": {
                "matches": naive_matches,
                "comparisons": naive_comparisons,
                "steps": naive_steps,
            },
            "rabin": {
                "matches": rk_matches,
                "comparisons": rk_comparisons,
                "steps": rk_steps,
                "pattern_hash": rolling_hash(pattern),
            },
            "kmp": {
                "matches": kmp_matches,
                "comparisons": kmp_comparisons,
                "steps": kmp_steps,
                "lps": lps,
            },
        }

        st.session_state.visualizing = visualize_clicked
        st.session_state.algorithm = "Naive"
        st.session_state.step_index = 0

    # ------------------------- Results ------------------------

    data = st.session_state.result

    if data and not st.session_state.visualizing:

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">Search Results</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(3)

        result_rows = [
            ("Naive", data["naive"]),
            ("Rabin-Karp", data["rabin"]),
            ("KMP", data["kmp"]),
        ]

        for col, (name, result_data) in zip(cols, result_rows):
            with col:
                matches = result_data["matches"]
                comparisons = result_data["comparisons"]

                if matches:
                    result_text = "Found"
                    detail = ", ".join(map(str, matches))
                    box_class = "success-box"
                    icon = "✓"
                else:
                    result_text = "Not Found"
                    detail = "—"
                    box_class = "error-box"
                    icon = "✕"

                st.markdown(
                    f"""
                    <div class="{box_class}">
                        <div style="font-size:12px; color:#94A3B8;">
                            {name.upper()}
                        </div>
                        <div style="font-size:25px; font-weight:800; margin-top:5px;">
                            {icon} {result_text}
                        </div>
                        <div class="muted" style="margin-top:8px;">
                            Index: <b>{detail}</b><br>
                            Comparisons: <b>{comparisons}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # Metrics
        m1, m2, m3, m4 = st.columns(4)

        total_naive = data["naive"]["comparisons"]
        total_rk = data["rabin"]["comparisons"]
        total_kmp = data["kmp"]["comparisons"]

        fastest = min(
            [
                ("Naive", total_naive),
                ("Rabin-Karp", total_rk),
                ("KMP", total_kmp),
            ],
            key=lambda x: x[1]
        )

        metrics = [
            (str(len(data["text"])), "Text Length"),
            (str(len(data["pattern"])), "Pattern Length"),
            (str(fastest[1]), f"Fewest Comparisons • {fastest[0]}"),
            (str(len(data["kmp"]["matches"])), "Occurrences"),
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

        # Comparison bars using simple HTML
        max_comp = max(total_naive, total_rk, total_kmp, 1)

        st.markdown(
            """
            <div class="glass">
                <div style="font-size:20px; font-weight:800; margin-bottom:18px;">
                    Comparison Count
                </div>
            """,
            unsafe_allow_html=True
        )

        for name, value, cls in [
            ("Naive", total_naive, "rgba(248,113,113,.70)"),
            ("Rabin-Karp", total_rk, "rgba(167,139,250,.75)"),
            ("KMP", total_kmp, "rgba(103,232,249,.75)"),
        ]:
            width = max(4, int((value / max_comp) * 100))
            st.markdown(
                f"""
                <div style="margin:13px 0;">
                    <div style="display:flex; justify-content:space-between;
                                font-size:13px; color:#CBD5E1; margin-bottom:6px;">
                        <span>{name}</span><b>{value}</b>
                    </div>
                    <div style="height:10px; border-radius:99px;
                                background:rgba(255,255,255,.06);">
                        <div style="height:10px; width:{width}%;
                                    border-radius:99px; background:{cls};"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("▶ VISUALIZE AN ALGORITHM", use_container_width=True):
            st.session_state.visualizing = True
            st.session_state.algorithm = "Naive"
            st.session_state.step_index = 0
            st.rerun()

    # ----------------------- Visualization -------------------

    if data and st.session_state.visualizing:

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="section-title">🔬 Algorithm Visualization</div>
            <div class="section-subtitle">
                Choose an algorithm and watch its search strategy step by step.
            </div>
            """,
            unsafe_allow_html=True
        )

        algorithm = st.selectbox(
            "Select algorithm",
            ["Naive", "Rabin-Karp", "KMP"],
            index=["Naive", "Rabin-Karp", "KMP"].index(
                st.session_state.algorithm
            )
        )

        if algorithm != st.session_state.algorithm:
            st.session_state.algorithm = algorithm
            st.session_state.step_index = 0
            st.rerun()

        text = data["text"]
        pattern = data["pattern"]

        # ----------- NAIVE VISUALIZATION ----------------------

        if algorithm == "Naive":

            steps = data["naive"]["steps"]

            if not steps:
                st.info("No visualization steps are available.")
            elif st.session_state.step_index < len(steps):

                step = steps[st.session_state.step_index]
                start = step["start"]

                render_text_pattern(
                    text,
                    pattern,
                    start=start,
                    compare_index=step["compare_index"],
                    text_index=step["text_index"],
                    found=step.get("found", False)
                )

                left, right = st.columns([1.5, 1])

                with left:
                    st.markdown(
                        f"""
                        <div class="step-box">
                            <h4>
                                Step {st.session_state.step_index + 1}
                                of {len(steps)}
                            </h4>
                            <div class="muted">
                                Comparing text index
                                <b style="color:#67E8F9;">
                                {step["text_index"]}</b>
                                with pattern index
                                <b style="color:#A78BFA;">
                                {step["pattern_index"]}</b>.
                            </div>
                            <div style="margin-top:10px;">
                                {step["message"]}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with right:
                    st.markdown(
                        f"""
                        <div class="step-box">
                            <h4>Naive Strategy</h4>
                            <div class="muted">
                                Shift: <b>+1</b><br>
                                Comparisons: <b>{step["comparisons"]}</b><br>
                                Current window: <b>{start}</b>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                time.sleep(0.65)
                st.session_state.step_index += 1
                st.rerun()

            else:
                matches = data["naive"]["matches"]
                st.markdown(
                    f"""
                    <div class="success-box">
                        <div style="font-size:27px; font-weight:800;">
                            {"🎯 Pattern Found" if matches else "❌ Pattern Not Found"}
                        </div>
                        <div class="muted" style="margin-top:8px;">
                            Naive Search completed with
                            <b>{data["naive"]["comparisons"]}</b>
                            character comparison(s).
                            {"Occurrences: " + ", ".join(map(str, matches))
                             if matches else ""}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ----------- RABIN-KARP VISUALIZATION -----------------

        elif algorithm == "Rabin-Karp":

            steps = data["rabin"]["steps"]

            if not steps:
                st.info("No visualization steps are available.")
            elif st.session_state.step_index < len(steps):

                step = steps[st.session_state.step_index]
                start = step["start"]

                render_text_pattern(
                    text,
                    pattern,
                    start=start,
                    compare_index=None,
                    text_index=None,
                    found=step.get("found", False)
                )

                h1, h2 = st.columns(2)

                with h1:
                    st.markdown(
                        f"""
                        <div class="hash-card">
                            <div class="muted">PATTERN HASH</div>
                            <div class="hash-value">
                                {step["pattern_hash"]}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with h2:
                    st.markdown(
                        f"""
                        <div class="hash-card">
                            <div class="muted">WINDOW HASH</div>
                            <div class="hash-value">
                                {step["window_hash"]}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f"""
                    <div class="step-box">
                        <h4>
                            Step {st.session_state.step_index + 1}
                            of {len(steps)}
                        </h4>
                        <div>
                            {step["message"]}
                        </div>
                        <div class="muted" style="margin-top:8px;">
                            Window start: <b>{start}</b>
                            &nbsp; • &nbsp;
                            Character comparisons:
                            <b>{step["comparisons"]}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                time.sleep(0.75)
                st.session_state.step_index += 1
                st.rerun()

            else:
                matches = data["rabin"]["matches"]
                st.markdown(
                    f"""
                    <div class="success-box">
                        <div style="font-size:27px; font-weight:800;">
                            {"🎯 Pattern Found" if matches else "❌ Pattern Not Found"}
                        </div>
                        <div class="muted" style="margin-top:8px;">
                            Rabin-Karp completed with
                            <b>{data["rabin"]["comparisons"]}</b>
                            character verification comparison(s).
                            {"Occurrences: " + ", ".join(map(str, matches))
                             if matches else ""}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ---------------- KMP VISUALIZATION ------------------

        else:

            steps = data["kmp"]["steps"]
            lps = data["kmp"]["lps"]

            if not steps:
                st.info("No visualization steps are available.")
            elif st.session_state.step_index < len(steps):

                step = steps[st.session_state.step_index]
                ti = step["text_index"]
                pi = step["pattern_index"]

                start = max(0, ti - pi)

                render_lps(
                    pattern,
                    lps,
                    active=min(pi, len(lps) - 1)
                )

                render_text_pattern(
                    text,
                    pattern,
                    start=start,
                    compare_index=pi,
                    text_index=ti,
                    found=step.get("found", False)
                )

                st.markdown(
                    f"""
                    <div class="step-box">
                        <h4>
                            Step {st.session_state.step_index + 1}
                            of {len(steps)}
                        </h4>
                        <div>
                            {step["message"]}
                        </div>
                        <div class="muted" style="margin-top:9px;">
                            Text index: <b>{ti}</b>
                            &nbsp; • &nbsp;
                            Pattern index: <b>{pi}</b>
                            &nbsp; • &nbsp;
                            Comparisons: <b>{step["comparisons"]}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if step.get("jump"):
                    st.markdown(
                        """
                        <div class="warning-box" style="margin-top:14px;">
                            🧠 KMP is using the LPS table instead of restarting
                            the pattern from the beginning.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                time.sleep(0.72)
                st.session_state.step_index += 1
                st.rerun()

            else:
                matches = data["kmp"]["matches"]

                render_lps(pattern, lps)

                st.markdown(
                    f"""
                    <div class="success-box" style="margin-top:18px;">
                        <div style="font-size:27px; font-weight:800;">
                            {"🎯 Pattern Found" if matches else "❌ Pattern Not Found"}
                        </div>
                        <div class="muted" style="margin-top:8px;">
                            KMP completed with
                            <b>{data["kmp"]["comparisons"]}</b>
                            character comparison(s).
                            {"Occurrences: " + ", ".join(map(str, matches))
                             if matches else ""}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Visualization controls
        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            if st.button("🔄 REPLAY", use_container_width=True):
                st.session_state.step_index = 0
                st.rerun()

        with c2:
            if st.button("📊 VIEW COMPARISON", use_container_width=True):
                st.session_state.visualizing = False
                st.rerun()

    st.markdown(
        '<div class="footer">String Matching Lab • Built with Python & Streamlit</div>',
        unsafe_allow_html=True
    )