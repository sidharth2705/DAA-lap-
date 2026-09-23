import streamlit as st
import time


# =========================================================
# FIRST FIT DECREASING BIN PACKING
# =========================================================

def first_fit_decreasing(items, capacity):

    # Sort items in decreasing order
    sorted_items = sorted(items, reverse=True)

    # Store bins
    bins = []

    # Count placements
    placements = 0

    # Count rejected attempts
    rejected_attempts = 0

    # -----------------------------------------------------
    # Place every item
    # -----------------------------------------------------

    for item in sorted_items:

        placed = False

        # Try existing bins first
        for bin_data in bins:

            # Check whether item fits
            if bin_data["remaining"] >= item:

                bin_data["items"].append(item)

                bin_data["remaining"] -= item

                placements += 1

                placed = True

                break

            else:
                rejected_attempts += 1

        # -------------------------------------------------
        # If item does not fit in any existing bin
        # create a new bin
        # -------------------------------------------------

        if not placed:

            new_bin = {
                "items": [item],
                "remaining": capacity - item
            }

            bins.append(new_bin)

            placements += 1

    return bins, sorted_items, placements, rejected_attempts


# =========================================================
# BIN UTILIZATION
# =========================================================

def calculate_utilization(bin_data, capacity):

    used = sum(bin_data["items"])

    utilization = (used / capacity) * 100

    return used, utilization


# =========================================================
# STREAMLIT WEBSITE
# =========================================================

st.set_page_config(
    page_title="Bin Packing Approximation",
    page_icon="📦",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📦 Efficient Bin Packing")
st.subheader("Using First Fit Decreasing Approximation Algorithm")

st.write(
    """
    This website solves the **Bin Packing Problem** using the
    **First Fit Decreasing (FFD)** approximation algorithm.

    The objective is to pack all items into the minimum possible
    number of bins while respecting the capacity of each bin.
    """
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Bin Packing Settings")

capacity = st.sidebar.number_input(
    "Bin Capacity",
    min_value=1,
    max_value=1000,
    value=10,
    step=1
)

st.sidebar.write(
    "Enter item sizes separated by commas."
)

items_input = st.sidebar.text_input(
    "Item Sizes",
    value="7,5,6,4,2,3,8,1"
)


# =========================================================
# EXECUTE BUTTON
# =========================================================

execute = st.sidebar.button(
    "🚀 Pack Items",
    use_container_width=True
)


# =========================================================
# MAIN EXPLANATION
# =========================================================

st.subheader("📚 Problem")

st.write(
    f"""
    Each bin has a fixed capacity of **{capacity}**.

    The goal is to place all items into bins such that:

    - No bin exceeds its capacity.
    - The number of bins used is minimized.
    - Larger items are considered first.
    """
)


# =========================================================
# EXECUTION
# =========================================================

if execute:

    try:

        # -------------------------------------------------
        # Convert input into list
        # -------------------------------------------------

        items = [
            int(x.strip())
            for x in items_input.split(",")
            if x.strip() != ""
        ]

        # -------------------------------------------------
        # Validate items
        # -------------------------------------------------

        if len(items) == 0:

            st.error(
                "Please enter at least one item."
            )

        elif any(item <= 0 for item in items):

            st.error(
                "Item sizes must be greater than 0."
            )

        elif any(item > capacity for item in items):

            invalid_items = [
                item for item in items
                if item > capacity
            ]

            st.error(
                f"These items are larger than the bin capacity: "
                f"{invalid_items}"
            )

        else:

            # -------------------------------------------------
            # Start timer
            # -------------------------------------------------

            start_time = time.perf_counter()

            # -------------------------------------------------
            # Execute FFD
            # -------------------------------------------------

            (
                bins,
                sorted_items,
                placements,
                rejected_attempts
            ) = first_fit_decreasing(
                items,
                capacity
            )

            # -------------------------------------------------
            # End timer
            # -------------------------------------------------

            end_time = time.perf_counter()

            execution_time = end_time - start_time

            # =================================================
            # SUCCESS
            # =================================================

            st.success(
                "All items have been packed successfully!"
            )

            st.divider()

            # =================================================
            # STATISTICS
            # =================================================

            st.subheader("📊 Execution Statistics")

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Total Items",
                    len(items)
                )

            with col2:

                st.metric(
                    "Bins Used",
                    len(bins)
                )

            with col3:

                st.metric(
                    "Bin Capacity",
                    capacity
                )

            with col4:

                st.metric(
                    "Execution Time",
                    f"{execution_time:.6f}s"
                )

            st.write(
                f"**Item placements:** {placements}"
            )

            st.write(
                f"**Rejected bin attempts:** "
                f"{rejected_attempts}"
            )

            st.divider()

            # =================================================
            # SORTED ITEMS
            # =================================================

            st.subheader("🔽 Items in Decreasing Order")

            st.write(
                " → ".join(
                    str(item)
                    for item in sorted_items
                )
            )

            st.divider()

            # =================================================
            # BIN DETAILS
            # =================================================

            st.subheader("📦 Bin Allocation")

            total_used = 0

            for index, bin_data in enumerate(bins):

                used, utilization = calculate_utilization(
                    bin_data,
                    capacity
                )

                remaining = bin_data["remaining"]

                total_used += used

                st.markdown(
                    f"### Bin {index + 1}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        "**Items:** "
                        + " + ".join(
                            str(item)
                            for item in bin_data["items"]
                        )
                    )

                with col2:

                    st.write(
                        f"**Used:** {used} / {capacity}"
                    )

                with col3:

                    st.write(
                        f"**Remaining:** {remaining}"
                    )

                st.progress(
                    min(utilization / 100, 1.0)
                )

                st.write(
                    f"**Utilization:** "
                    f"{utilization:.2f}%"
                )

                st.divider()

            # =================================================
            # OVERALL UTILIZATION
            # =================================================

            st.subheader("📈 Overall Packing Efficiency")

            total_capacity = len(bins) * capacity

            overall_utilization = (
                total_used / total_capacity
            ) * 100

            st.metric(
                "Overall Bin Utilization",
                f"{overall_utilization:.2f}%"
            )

            st.write(
                f"Total item size = **{total_used}**"
            )

            st.write(
                f"Total available capacity = "
                f"**{total_capacity}**"
            )


    except ValueError:

        st.error(
            "Invalid input! Please enter item sizes like: "
            "7,5,6,4,2,3,8,1"
        )


# =========================================================
# ALGORITHM
# =========================================================

st.divider()

st.subheader("📚 First Fit Decreasing Algorithm")

st.code(
"""
FIRST_FIT_DECREASING(items, capacity):

    Sort all items in decreasing order

    Create an empty list of bins

    For each item:

        For each existing bin:

            If item fits in the bin:

                Place item in that bin

                Update remaining capacity

                Move to next item

        If item does not fit in any bin:

            Create a new bin

            Place item inside it

    Return all bins
""",
language="text"
)


# =========================================================
# HOW IT WORKS
# =========================================================

st.subheader("🔍 How the Algorithm Works")

st.write(
    """
    **Step 1 — Sort**

    All items are sorted from largest to smallest.

    **Step 2 — First Fit**

    Starting with the first bin, the algorithm searches for
    the first bin where the current item fits.

    **Step 3 — Create a Bin**

    If the item does not fit into any existing bin, a new bin
    is created.

    **Step 4 — Continue**

    The process continues until every item has been placed.

    This is called **First Fit Decreasing (FFD)** because the
    items are sorted in decreasing order before applying
    First Fit.
    """
)


# =========================================================
# APPROXIMATION CONCEPT
# =========================================================

st.subheader("🎯 Why is it an Approximation Algorithm?")

st.write(
    """
    Finding the absolute minimum number of bins for the general
    Bin Packing Problem is computationally difficult.

    Instead of checking every possible arrangement, FFD uses a
    fast strategy to obtain a good packing.

    Therefore, FFD is an **approximation algorithm** rather than
    an exact algorithm.
    """
)


# =========================================================
# COMPLEXITY
# =========================================================

st.subheader("⏱️ Complexity")

st.write(
    """
    Let **N** be the number of items.

    **Sorting:**

    O(N log N)

    **First Fit:**

    O(N²) in the straightforward implementation used here.

    Therefore, the overall worst-case complexity is:

    **O(N²)**

    Space complexity:

    **O(N)**

    because the bins and their item allocations are stored.
    """
)


# =========================================================
# EXAMPLE
# =========================================================

st.subheader("📝 Example")

st.write(
    """
    Suppose:

    **Bin Capacity = 10**

    **Items = 7, 5, 6, 4, 2, 3, 8, 1**

    After sorting:

    **8, 7, 6, 5, 4, 3, 2, 1**

    The algorithm then tries to place each item into the first
    available bin where it fits.
    """
)
