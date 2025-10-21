import streamlit as st
import pandas as pd

st.set_page_config(page_title="💰 Personal Expense Tracker", layout="centered")

# Initialize session state (to persist data while app runs)
if "expenses" not in st.session_state:
    st.session_state.expenses = []
if "budget" not in st.session_state:
    st.session_state.budget = 0.0

categories = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Others"]

st.title("💰 Personal Expense Tracker")

menu = ["Add New Expense", "View All Expenses", "Category Summary", "Set / Check Budget", "Search Expenses"]
choice = st.sidebar.radio("📋 Menu", menu)

# --- ADD NEW EXPENSE ---
if choice == "Add New Expense":
    st.subheader("➕ Add New Expense")
    category = st.selectbox("Select Category", categories)
    amount = st.number_input("Enter Amount (₹)", min_value=0.0, step=10.0)
    desc = st.text_input("Enter Description")
    if st.button("Add Expense"):
        expense = {"Category": category, "Amount": amount, "Description": desc}
        st.session_state.expenses.append(expense)
        st.success("✅ Expense Added Successfully!")

# --- VIEW ALL EXPENSES ---
elif choice == "View All Expenses":
    st.subheader("📊 All Expenses")
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df, use_container_width=True)
        total = df["Amount"].sum()
        st.info(f"**Total Expenses:** ₹{total}")
        st.write(f"**Total Entries:** {len(df)}")
    else:
        st.warning("No expenses recorded yet!")

# --- CATEGORY SUMMARY ---
elif choice == "Category Summary":
    st.subheader("📈 Category Summary")
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        summary = df.groupby("Category")["Amount"].sum().reset_index()
        st.bar_chart(summary.set_index("Category"))
        for _, row in summary.iterrows():
            st.write(f"**{row['Category']}**: ₹{row['Amount']}")
        st.info(f"**Total:** ₹{summary['Amount'].sum()}")
    else:
        st.warning("No expenses recorded yet!")

# --- SET / CHECK BUDGET ---
elif choice == "Set / Check Budget":
    st.subheader("💵 Budget Management")
    budget = st.number_input("Enter or Update Your Budget (₹)", min_value=0.0, step=100.0, value=st.session_state.budget)
    if st.button("Save Budget"):
        st.session_state.budget = budget
        st.success(f"Budget set to ₹{budget}")

    if st.session_state.expenses:
        total_expenses = sum(exp["Amount"] for exp in st.session_state.expenses)
        if st.session_state.budget > 0:
            remaining = st.session_state.budget - total_expenses
            if remaining >= 0:
                st.success(f"🟢 You can still spend ₹{remaining}")
            else:
                st.error(f"🔴 Over budget by ₹{abs(remaining)}!")
    else:
        st.info("No expenses recorded yet to compare with budget.")

# --- SEARCH EXPENSES ---
elif choice == "Search Expenses":
    st.subheader("🔍 Search Expenses")
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        search_type = st.selectbox("Search by", ["Category", "Description", "Amount"])
        query = st.text_input(f"Enter {search_type}")
        if st.button("Search"):
            if search_type == "Amount":
                try:
                    query = float(query)
                    result = df[df["Amount"] == query]
                except ValueError:
                    st.error("Please enter a valid number.")
                    result = pd.DataFrame()
            else:
                result = df[df[search_type].str.contains(query, case=False, na=False)]
            if not result.empty:
                st.dataframe(result, use_container_width=True)
            else:
                st.warning("No matching records found.")
    else:
        st.warning("No expenses recorded yet!")

st.markdown("---")
st.caption("✨ Created with ❤️ By Mrinank")
