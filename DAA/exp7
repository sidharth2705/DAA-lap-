import streamlit as st
import time


# ---------------------------------------------------------
# N-QUEENS BACKTRACKING
# ---------------------------------------------------------

def solve_n_queens(n):
    solutions = []
    board = [-1] * n

    backtracks = 0
    placements = 0

    def is_safe(row, col):
        for previous_row in range(row):
            previous_col = board[previous_row]

            # Same column
            if previous_col == col:
                return False

            # Same diagonal
            if abs(previous_col - col) == abs(previous_row - row):
                return False

        return True

    def backtrack(row):
        nonlocal backtracks, placements

        # A complete solution has been found
        if row == n:
            solutions.append(board.copy())
            return

        placed = False

        for col in range(n):

            if is_safe(row, col):

                board[row] = col
                placements += 1
                placed = True

                # Try placing queen in the next row
                before = len(solutions)
                backtrack(row + 1)

                # Remove queen / undo choice
                board[row] = -1
                backtracks += 1

        return

    backtrack(0)

    return solutions, backtracks, placements


# ---------------------------------------------------------
# CONVERT SOLUTION INTO STRING
# ---------------------------------------------------------

def board_to_string(solution):
    n = len(solution)

    result = ""

    for row in range(n):
        for col in range(n):

            if solution[row] == col:
                result += "Q "
            else:
                result += ". "

        result += "\n"

    return result


# ---------------------------------------------------------
# STREAMLIT WEBSITE
# ---------------------------------------------------------

st.set_page_config(
    page_title="N-Queens Backtracking",
    page_icon="♛",
    layout="wide"
)

st.title("♛ N-Queens Problem using Backtracking")

st.write(
    """
    This website demonstrates the **N-Queens problem** using the
    **Backtracking technique** in Python.
    
    The program finds **all possible valid solutions** for the selected
    board size and counts the number of backtracks performed.
    """
)

st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("N-Queens Settings")

n = st.sidebar.selectbox(
    "Select Board Size (N)",
    [4, 6, 8]
)

execute = st.sidebar.button(
    "🚀 Execute Program",
    use_container_width=True
)


# ---------------------------------------------------------
# INFORMATION
# ---------------------------------------------------------

st.subheader("Problem")

st.write(
    f"""
    Place **{n} queens** on a **{n} × {n} chessboard** such that:

    - No two queens are in the same row.
    - No two queens are in the same column.
    - No two queens are on the same diagonal.

    The program uses **backtracking** to explore possible positions.
    """
)


# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------

if execute:

    start_time = time.perf_counter()

    solutions, backtracks, placements = solve_n_queens(n)

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    st.success("N-Queens problem solved successfully!")

    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    st.subheader("📊 Execution Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Board Size",
            f"{n} × {n}"
        )

    with col2:
        st.metric(
            "Total Solutions",
            len(solutions)
        )

    with col3:
        st.metric(
            "Backtracks",
            backtracks
        )

    with col4:
        st.metric(
            "Execution Time",
            f"{execution_time:.6f} sec"
        )

    st.write(
        f"**Queen placements attempted:** {placements}"
    )

    st.divider()

    # -----------------------------------------------------
    # DISPLAY ALL SOLUTIONS
    # -----------------------------------------------------

    st.subheader(
        f"♛ All Valid Solutions ({len(solutions)})"
    )

    for index, solution in enumerate(solutions, start=1):

        st.markdown(
            f"### Solution {index}"
        )

        # Display board using text
        board_string = board_to_string(solution)

        st.code(
            board_string,
            language="text"
        )

        # Display position representation
        positions = []

        for row, col in enumerate(solution):
            positions.append(
                f"Row {row + 1} → Column {col + 1}"
            )

        st.write(
            "**Queen Positions:** "
            + " | ".join(positions)
        )

        st.divider()


# ---------------------------------------------------------
# ALGORITHM EXPLANATION
# ---------------------------------------------------------

st.subheader("📚 Backtracking Algorithm")

st.code(
"""
BACKTRACK(row):

    if row == N:
        store the solution
        return

    for each column in the current row:

        if placing queen is safe:

            place queen

            BACKTRACK(row + 1)

            remove queen
""",
language="text"
)

st.write(
    """
    **Backtracking idea:**

    1. Start from the first row.
    2. Try placing a queen in every column.
    3. Check whether the position is safe.
    4. If safe, move to the next row.
    5. If no valid position exists, go back to the previous row.
    6. Remove the previously placed queen.
    7. Try another column.
    8. When all N rows contain queens, a valid solution is found.
    """
)


# ---------------------------------------------------------
# BACKTRACKING DEFINITION
# ---------------------------------------------------------

st.subheader("🔄 What is counted as a Backtrack?")

st.write(
    """
    In this implementation, a **backtrack is counted whenever the
    algorithm removes a previously placed queen after finishing the
    recursive exploration of that choice**.

    Therefore, the exact backtrack count depends on the implementation
    and counting convention used.
    """
)


# ---------------------------------------------------------
# COMPLEXITY
# ---------------------------------------------------------

st.subheader("⏱️ Complexity")

st.write(
    """
    The N-Queens backtracking algorithm has exponential/factorial
    search behavior. A commonly stated upper-bound estimate is:

    **Time Complexity: O(N!)**

    **Space Complexity: O(N)**

    The O(N) space is mainly used for the recursion stack and the
    array storing queen positions.
    """
)
