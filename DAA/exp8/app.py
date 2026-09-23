import streamlit as st
import time
import math

# ---------------------------------------------------------
# TSP USING BRANCH AND BOUND
# ---------------------------------------------------------

def tsp_branch_and_bound(cost_matrix):

    n = len(cost_matrix)

    # Best solution found
    best_cost = float("inf")
    best_path = []

    # Statistics
    nodes_explored = 0
    branches_pruned = 0

    # -----------------------------------------------------
    # Calculate initial lower bound
    # -----------------------------------------------------

    def calculate_initial_bound():

        bound = 0

        for i in range(n):

            first = float("inf")
            second = float("inf")

            for j in range(n):

                if i != j:

                    if cost_matrix[i][j] < first:
                        second = first
                        first = cost_matrix[i][j]

                    elif cost_matrix[i][j] < second:
                        second = cost_matrix[i][j]

            bound += first + second

        return math.ceil(bound / 2)

    # -----------------------------------------------------
    # Recursive Branch and Bound
    # -----------------------------------------------------

    def branch_and_bound(
        current_path,
        visited,
        current_cost,
        bound
    ):

        nonlocal best_cost
        nonlocal best_path
        nonlocal nodes_explored
        nonlocal branches_pruned

        nodes_explored += 1

        # -------------------------------------------------
        # All cities have been visited
        # -------------------------------------------------

        if len(current_path) == n:

            last_city = current_path[-1]
            first_city = current_path[0]

            return_cost = cost_matrix[last_city][first_city]

            total_cost = current_cost + return_cost

            if total_cost < best_cost:

                best_cost = total_cost

                best_path = current_path.copy()

                best_path.append(first_city)

            return

        # -------------------------------------------------
        # Try every unvisited city
        # -------------------------------------------------

        current_city = current_path[-1]

        for next_city in range(n):

            if not visited[next_city]:

                new_cost = (
                    current_cost
                    + cost_matrix[current_city][next_city]
                )

                # Simple lower-bound calculation
                new_bound = bound

                # Reduce bound using minimum outgoing edge
                min_edge = float("inf")

                for city in range(n):

                    if city != next_city and not visited[city]:

                        if cost_matrix[next_city][city] < min_edge:
                            min_edge = cost_matrix[next_city][city]

                if min_edge != float("inf"):
                    new_bound += min_edge

                # -------------------------------------------------
                # Branching decision
                # -------------------------------------------------

                if new_cost + new_bound < best_cost:

                    visited[next_city] = True
                    current_path.append(next_city)

                    branch_and_bound(
                        current_path,
                        visited,
                        new_cost,
                        new_bound
                    )

                    current_path.pop()
                    visited[next_city] = False

                else:

                    branches_pruned += 1

    # ---------------------------------------------------------
    # Start the algorithm from city 0
    # ---------------------------------------------------------

    initial_bound = calculate_initial_bound()

    visited = [False] * n

    visited[0] = True

    branch_and_bound(
        [0],
        visited,
        0,
        initial_bound
    )

    return (
        best_path,
        best_cost,
        nodes_explored,
        branches_pruned
    )


# ---------------------------------------------------------
# FORMAT PATH
# ---------------------------------------------------------

def format_path(path):

    return " → ".join(
        f"City {city + 1}"
        for city in path
    )


# ---------------------------------------------------------
# STREAMLIT PAGE
# ---------------------------------------------------------

st.set_page_config(
    page_title="TSP Branch and Bound",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Travelling Salesman Problem")
st.subheader("Using Branch and Bound")

st.write(
    """
    This website solves the **Travelling Salesman Problem (TSP)**
    using the **Branch and Bound technique**.

    The objective is to find the minimum-cost tour that:

    - Starts from a city
    - Visits every city exactly once
    - Returns to the starting city
    - Has minimum possible total cost
    """
)

st.divider()


# ---------------------------------------------------------
# CITY INPUT
# ---------------------------------------------------------

st.sidebar.header("TSP Settings")

num_cities = st.sidebar.number_input(
    "Number of Cities",
    min_value=3,
    max_value=8,
    value=4,
    step=1
)

st.sidebar.write(
    "Enter the cost/distance matrix below."
)


# ---------------------------------------------------------
# DEFAULT MATRIX
# ---------------------------------------------------------

default_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]


# ---------------------------------------------------------
# CREATE MATRIX
# ---------------------------------------------------------

if num_cities == 4:

    matrix = default_matrix

else:

    matrix = []

    for i in range(num_cities):

        row = []

        for j in range(num_cities):

            if i == j:
                row.append(0)

            else:
                row.append(10)

        matrix.append(row)


# ---------------------------------------------------------
# MATRIX INPUT
# ---------------------------------------------------------

st.subheader("📊 Cost / Distance Matrix")

st.write(
    "The value at row i, column j represents the cost of travelling "
    "from City i to City j."
)

edited_matrix = []

for i in range(num_cities):

    cols = st.columns(num_cities)

    row = []

    for j in range(num_cities):

        value = cols[j].number_input(
            f"C{i + 1},{j + 1}",
            min_value=0,
            value=int(matrix[i][j]),
            step=1,
            key=f"city_{i}_{j}"
        )

        row.append(value)

    edited_matrix.append(row)


# ---------------------------------------------------------
# EXECUTE BUTTON
# ---------------------------------------------------------

execute = st.button(
    "🚀 Find Optimal Path",
    use_container_width=True
)


# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------

if execute:

    # Check diagonal
    valid = True

    for i in range(num_cities):

        if edited_matrix[i][i] != 0:

            st.error(
                f"Diagonal value C{i + 1},{i + 1} must be 0."
            )

            valid = False

    if valid:

        start_time = time.perf_counter()

        (
            best_path,
            best_cost,
            nodes_explored,
            branches_pruned
        ) = tsp_branch_and_bound(
            edited_matrix
        )

        end_time = time.perf_counter()

        execution_time = end_time - start_time

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        st.success(
            "Optimal tour found successfully!"
        )

        st.divider()

        # -------------------------------------------------
        # STATISTICS
        # -------------------------------------------------

        st.subheader("📊 Execution Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Number of Cities",
                num_cities
            )

        with col2:

            st.metric(
                "Minimum Cost",
                best_cost
            )

        with col3:

            st.metric(
                "Nodes Explored",
                nodes_explored
            )

        with col4:

            st.metric(
                "Branches Pruned",
                branches_pruned
            )

        st.write(
            f"**Execution Time:** {execution_time:.6f} seconds"
        )

        st.divider()

        # -------------------------------------------------
        # OPTIMAL PATH
        # -------------------------------------------------

        st.subheader("🏆 Optimal Path")

        st.success(
            format_path(best_path)
        )

        st.write(
            f"### Minimum Tour Cost = {best_cost}"
        )

        st.divider()

        # -------------------------------------------------
        # PATH DETAILS
        # -------------------------------------------------

        st.subheader("🛣️ Path Details")

        for i in range(len(best_path) - 1):

            from_city = best_path[i]
            to_city = best_path[i + 1]

            travel_cost = edited_matrix[
                from_city
            ][
                to_city
            ]

            st.write(
                f"City {from_city + 1} → "
                f"City {to_city + 1} "
                f"= {travel_cost}"
            )

        st.write(
            f"**Total Cost = {best_cost}**"
        )


# ---------------------------------------------------------
# ALGORITHM
# ---------------------------------------------------------

st.divider()

st.subheader("📚 Branch and Bound Algorithm")

st.code(
"""
TSP_BRANCH_AND_BOUND():

    Calculate initial lower bound

    Start from City 1

    Mark City 1 as visited

    Branch and Bound:

        If all cities are visited:

            Add cost of returning to City 1

            Update minimum cost

        Otherwise:

            For every unvisited city:

                Calculate new cost

                Calculate lower bound

                If:

                    new_cost + lower_bound
                    < best_cost

                Then:

                    Visit the city

                    Recursively explore

                    Backtrack

                Else:

                    Prune the branch
""",
language="text"
)


# ---------------------------------------------------------
# EXPLANATION
# ---------------------------------------------------------

st.subheader("🔍 How Branch and Bound Works")

st.write(
    """
    **1. Branch**

    The algorithm creates different possible paths by selecting
    an unvisited city.

    **2. Bound**

    For every partial path, a lower bound on the possible final
    tour cost is calculated.

    **3. Compare**

    The lower bound is compared with the best complete solution
    found so far.

    **4. Prune**

    If the lower bound is already greater than or equal to the
    current best cost, that branch cannot produce a better answer.

    Therefore, the branch is discarded.

    **5. Continue**

    The remaining promising branches are explored until the
    optimal tour is found.
    """
)


# ---------------------------------------------------------
# COMPLEXITY
# ---------------------------------------------------------

st.subheader("⏱️ Complexity")

st.write(
    """
    **Worst-case time complexity:** O(N!)

    The Branch and Bound method can still have factorial
    worst-case complexity because it may need to explore many
    possible tours.

    However, the bounding function can prune a large number
    of branches in practice.

    **Space complexity:** O(N)

    The recursive search stores the current path and visited
    cities.
    """
)
