import streamlit as st
import random
import time


# =========================================================
# RANDOMIZED QUICK SORT
# =========================================================

def randomized_quick_sort(arr):

    array = arr.copy()

    comparisons = 0
    swaps = 0
    recursive_calls = 0
    pivot_history = []

    # -----------------------------------------------------
    # Partition function
    # -----------------------------------------------------

    def partition(low, high):

        nonlocal comparisons
        nonlocal swaps

        # Select a random pivot
        random_index = random.randint(low, high)

        # Move random pivot to the end
        array[random_index], array[high] = (
            array[high],
            array[random_index]
        )

        swaps += 1

        pivot = array[high]

        pivot_history.append(pivot)

        i = low - 1

        # Partition the array
        for j in range(low, high):

            comparisons += 1

            if array[j] <= pivot:

                i += 1

                array[i], array[j] = (
                    array[j],
                    array[i]
                )

                swaps += 1

        # Place pivot in correct position
        array[i + 1], array[high] = (
            array[high],
            array[i + 1]
        )

        swaps += 1

        return i + 1

    # -----------------------------------------------------
    # Recursive Quick Sort
    # -----------------------------------------------------

    def quick_sort(low, high):

        nonlocal recursive_calls

        recursive_calls += 1

        if low < high:

            pivot_position = partition(
                low,
                high
            )

            # Sort left side
            quick_sort(
                low,
                pivot_position - 1
            )

            # Sort right side
            quick_sort(
                pivot_position + 1,
                high
            )

    # -----------------------------------------------------
    # Start sorting
    # -----------------------------------------------------

    if len(array) > 1:

        quick_sort(
            0,
            len(array) - 1
        )

    return (
        array,
        comparisons,
        swaps,
        recursive_calls,
        pivot_history
    )


# =========================================================
# NORMAL QUICK SORT
# =========================================================

def normal_quick_sort(arr):

    array = arr.copy()

    comparisons = 0
    swaps = 0

    def partition(low, high):

        nonlocal comparisons
        nonlocal swaps

        # Last element is always selected as pivot
        pivot = array[high]

        i = low - 1

        for j in range(low, high):

            comparisons += 1

            if array[j] <= pivot:

                i += 1

                array[i], array[j] = (
                    array[j],
                    array[i]
                )

                swaps += 1

        array[i + 1], array[high] = (
            array[high],
            array[i + 1]
        )

        swaps += 1

        return i + 1

    def quick_sort(low, high):

        if low < high:

            pivot_position = partition(
                low,
                high
            )

            quick_sort(
                low,
                pivot_position - 1
            )

            quick_sort(
                pivot_position + 1,
                high
            )

    if len(array) > 1:

        quick_sort(
            0,
            len(array) - 1
        )

    return array, comparisons, swaps


# =========================================================
# STREAMLIT PAGE
# =========================================================

st.set_page_config(
    page_title="Randomized Quick Sort",
    page_icon="⚡",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("⚡ Randomized Quick Sort")

st.subheader(
    "Improving Quick Sort Efficiency using Randomization"
)

st.write(
    """
    This website demonstrates **Randomized Quick Sort**.

    Instead of always selecting the first or last element as
    the pivot, the algorithm randomly selects a pivot.

    This helps reduce the possibility of repeatedly choosing
    a poor pivot and encountering the worst-case behavior of
    Quick Sort.
    """
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Quick Sort Settings")

input_method = st.sidebar.radio(
    "Choose Input Method",
    [
        "Enter Array",
        "Generate Random Array"
    ]
)


# =========================================================
# ENTER ARRAY
# =========================================================

if input_method == "Enter Array":

    array_input = st.sidebar.text_input(
        "Enter numbers separated by commas",
        value="45,23,78,12,56,9,34,67"
    )

    execute = st.sidebar.button(
        "🚀 Sort Array",
        use_container_width=True
    )


# =========================================================
# GENERATE RANDOM ARRAY
# =========================================================

else:

    array_size = st.sidebar.number_input(
        "Array Size",
        min_value=5,
        max_value=1000,
        value=20,
        step=5
    )

    min_value = st.sidebar.number_input(
        "Minimum Value",
        min_value=-10000,
        max_value=10000,
        value=1
    )

    max_value = st.sidebar.number_input(
        "Maximum Value",
        min_value=-10000,
        max_value=10000,
        value=100
    )

    generate = st.sidebar.button(
        "🎲 Generate Array",
        use_container_width=True
    )

    execute = st.sidebar.button(
        "🚀 Sort Array",
        use_container_width=True
    )

    if generate:

        if min_value > max_value:

            st.error(
                "Minimum value cannot be greater than maximum value."
            )

        else:

            st.session_state.random_array = [
                random.randint(
                    min_value,
                    max_value
                )
                for _ in range(array_size)
            ]

            st.success(
                "Random array generated!"
            )


# =========================================================
# GET ARRAY
# =========================================================

if input_method == "Enter Array":

    try:

        original_array = [
            int(x.strip())
            for x in array_input.split(",")
            if x.strip() != ""
        ]

    except ValueError:

        original_array = []

        st.error(
            "Please enter valid integers."
        )

else:

    original_array = st.session_state.get(
        "random_array",
        []
    )


# =========================================================
# DISPLAY ORIGINAL ARRAY
# =========================================================

if original_array:

    st.subheader("📥 Input Array")

    st.code(
        str(original_array),
        language="text"
    )


# =========================================================
# EXECUTION
# =========================================================

if execute and original_array:

    # -----------------------------------------------------
    # RANDOMIZED QUICK SORT
    # -----------------------------------------------------

    start_time = time.perf_counter()

    (
        randomized_result,
        randomized_comparisons,
        randomized_swaps,
        recursive_calls,
        pivot_history
    ) = randomized_quick_sort(
        original_array
    )

    end_time = time.perf_counter()

    randomized_time = (
        end_time - start_time
    )

    # -----------------------------------------------------
    # NORMAL QUICK SORT
    # -----------------------------------------------------

    start_time = time.perf_counter()

    (
        normal_result,
        normal_comparisons,
        normal_swaps
    ) = normal_quick_sort(
        original_array
    )

    end_time = time.perf_counter()

    normal_time = (
        end_time - start_time
    )

    # =====================================================
    # RESULT
    # =====================================================

    st.success(
        "Array sorted successfully!"
    )

    st.divider()

    # =====================================================
    # SORTED ARRAY
    # =====================================================

    st.subheader(
        "✅ Sorted Array"
    )

    st.code(
        str(randomized_result),
        language="text"
    )

    # =====================================================
    # RANDOMIZED QUICK SORT STATISTICS
    # =====================================================

    st.subheader(
        "📊 Randomized Quick Sort Statistics"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Comparisons",
            randomized_comparisons
        )

    with col2:

        st.metric(
            "Swaps",
            randomized_swaps
        )

    with col3:

        st.metric(
            "Recursive Calls",
            recursive_calls
        )

    with col4:

        st.metric(
            "Execution Time",
            f"{randomized_time:.6f}s"
        )

    st.divider()

    # =====================================================
    # PIVOT HISTORY
    # =====================================================

    st.subheader(
        "🎯 Randomly Selected Pivots"
    )

    st.write(
        " → ".join(
            str(pivot)
            for pivot in pivot_history
        )
    )

    st.divider()

    # =====================================================
    # NORMAL VS RANDOMIZED
    # =====================================================

    st.subheader(
        "⚖️ Normal Quick Sort vs Randomized Quick Sort"
    )

    comparison_data = {
        "": [
            "Comparisons",
            "Swaps",
            "Execution Time"
        ],

        "Normal Quick Sort": [
            normal_comparisons,
            normal_swaps,
            f"{normal_time:.6f}s"
        ],

        "Randomized Quick Sort": [
            randomized_comparisons,
            randomized_swaps,
            f"{randomized_time:.6f}s"
        ]
    }

    st.table(
        comparison_data
    )

    # =====================================================
    # VERIFICATION
    # =====================================================

    st.subheader(
        "🔎 Correctness Check"
    )

    if randomized_result == sorted(original_array):

        st.success(
            "✓ Randomized Quick Sort produced the correct result."
        )

    else:

        st.error(
            "✗ Sorting error detected."
        )


# =========================================================
# ALGORITHM
# =========================================================

st.divider()

st.subheader(
    "📚 Randomized Quick Sort Algorithm"
)

st.code(
"""
RANDOMIZED_QUICKSORT(A, low, high):

    if low < high:

        Choose a random index between low and high

        Exchange A[random_index] with A[high]

        pivot = A[high]

        Partition the array around pivot

        RANDOMIZED_QUICKSORT(A, low, pivot_position - 1)

        RANDOMIZED_QUICKSORT(A, pivot_position + 1, high)
""",
language="text"
)


# =========================================================
# HOW IT WORKS
# =========================================================

st.subheader(
    "🔍 How Randomized Quick Sort Works"
)

st.write(
    """
    **Step 1 — Select a random pivot**

    Instead of always choosing the first or last element,
    the algorithm randomly chooses an element.

    **Step 2 — Partition**

    Elements smaller than or equal to the pivot are placed
    on the left and larger elements are placed on the right.

    **Step 3 — Recursion**

    The same process is recursively applied to the left
    and right portions.

    **Step 4 — Continue**

    The process continues until the entire array is sorted.
    """
)


# =========================================================
# WHY RANDOMIZATION?
# =========================================================

st.subheader(
    "🎲 Why Use Randomization?"
)

st.write(
    """
    In ordinary Quick Sort, consistently selecting a poor pivot
    can produce highly unbalanced partitions.

    For example, if an already sorted array is processed and
    the last element is always selected as the pivot, the
    partitions can become:

        0 elements | Pivot | N-1 elements

    repeatedly.

    Randomized Quick Sort chooses the pivot randomly, reducing
    the dependence of the algorithm's behavior on the original
    ordering of the input.
    """
)


# =========================================================
# COMPLEXITY
# =========================================================

st.subheader(
    "⏱️ Complexity"
)

st.write(
    """
    **Best Case:**

    O(N log N)

    **Expected / Average Case:**

    O(N log N)

    **Worst Case:**

    O(N²)

    **Space Complexity:**

    O(log N) expected recursion depth.

    Randomization does not mathematically eliminate the O(N²)
    worst case, but it makes consistently poor pivot choices
    much less dependent on the input arrangement.
    """
)


# =========================================================
# EXAMPLE
# =========================================================

st.subheader(
    "📝 Example"
)

st.write(
    """
    Input:

        45, 23, 78, 12, 56, 9, 34

    The algorithm randomly selects a pivot, for example:

        Pivot = 56

    It partitions the array around 56 and recursively sorts
    both sides.

    The final result is:

        9, 12, 23, 34, 45, 56, 78
    """
)
