import streamlit as st

from core.usage import get_usage_status
from core.rules import make_decision

from core.database import (initialize_database,save_ticket,get_all_tickets)

from core.llm import analyze_ticket


st.set_page_config(
    page_title="AI Support Ticket Decision Engine",
    page_icon="🎫",
    layout="wide"
)

initialize_database()

st.title("🎫 AI Support Ticket Decision Engine")

usage = get_usage_status()

st.sidebar.header("AI Usage")

st.sidebar.metric(
    "Tokens Used",
    f"{usage['total_tokens']:,}"
)

st.sidebar.metric(
    "AI Requests",
    usage["total_requests"]
)

st.sidebar.progress(
    min(usage["percentage"] / 100, 1.0)
)

if usage["status"] == "normal":

    st.sidebar.success(
        f"Usage: {usage['percentage']:.2f}%"
    )

elif usage["status"] == "warning":

    st.sidebar.warning(
        f"Usage approaching safety limit: "
        f"{usage['percentage']:.2f}%"
    )

else:

    st.sidebar.error(
        "AI requests are temporarily disabled."
    )

st.write(
    "Automatically classify support tickets, apply business rules, "
    "and recommend the appropriate action."
)


st.subheader("Create Support Ticket")

customer_name = st.text_input("Customer Name")

customer_email = st.text_input("Customer Email")

previous_contacts = st.number_input(
    "Previous Support Contacts",
    min_value=0,
    max_value=20,
    value=0,
    step=1
)

ticket_text = st.text_area(
    "Customer Issue",
    height=180,
    placeholder=(
        "Example: I was charged twice for my subscription "
        "and nobody has responded to my previous request."
    )
)

analyze_tab, dashboard_tab = st.tabs( [ 
    "🎫 Analyze Ticket", 
    "📊 Operations Dashboard" 
    ] 
)

if st.button("Analyze Ticket", type="primary"):

    if not customer_name or not ticket_text:
        st.warning("Please provide the customer name and issue.")

    else:

        with st.spinner("Analyzing ticket..."):

            try:
                analysis = analyze_ticket(ticket_text)
                decision = make_decision(
                    category=analysis["category"],
                    urgency=analysis["urgency"],
                    sentiment=analysis["sentiment"],
                    previous_contacts=previous_contacts
                )
                ticket_id = save_ticket(
                    customer_name=customer_name,
                    customer_email=customer_email,
                    ticket_text=ticket_text,
                    previous_contacts=previous_contacts,
                    analysis=analysis,
                    decision=decision
                )

                st.success("Ticket analyzed successfully!")

            
            # AI Analysis Results

                st.divider()
                st.subheader("AI Analysis")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Category",
                        analysis["category"]
                    )

                with col2:
                    st.metric(
                        "Sentiment",
                        analysis["sentiment"]
                    )

                with col3:
                    st.metric(
                        "Urgency",
                        analysis["urgency"]
                    )


                st.write(
                    f"**Subcategory:** "
                    f"{analysis['subcategory']}"
                )

                st.write(
                    f"**Summary:** "
                    f"{analysis['summary']}"
                )

                # Business Decision

                st.divider()

                st.subheader("Business Decision")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Priority",
                        decision["priority"]
                    )

                with col2:
                    st.metric(
                        "Assigned Team",
                        decision["team"]
                    )

                with col3:
                    st.metric(
                        "Escalated",
                        "Yes"
                        if decision["escalated"]
                        else "No"
                    )

                with col4:
                    st.metric(
                        "Action",
                        decision["action"]
                    )


                # ------------------------------------------
                # Decision Explanation
                # ------------------------------------------

                st.info(
                    f"**Decision Reason:** "
                    f"{decision['reason']}"
                )

                st.success(
                   f"Ticket #{ticket_id} saved successfully."
                )


            except Exception as e:
                st.error(
                    f"Unable to analyze ticket: {e}"
                )

with dashboard_tab:

    st.subheader("Support Operations Dashboard")

    tickets = get_all_tickets()


    # ----------------------------------------------
    # No Tickets
    # ----------------------------------------------

    if not tickets:

        st.info(
            "No tickets have been analyzed yet."
        )


    else:

        # Convert SQLite rows into dictionaries
        tickets = [
            dict(ticket)
            for ticket in tickets
        ]


        # ------------------------------------------
        # KPI Calculations
        # ------------------------------------------

        total_tickets = len(tickets)

        critical_tickets = sum(
            1
            for ticket in tickets
            if ticket["priority"] == "Critical"
        )

        escalated_tickets = sum(
            1
            for ticket in tickets
            if ticket["escalated"] == 1
        )

        high_priority_tickets = sum(
            1
            for ticket in tickets
            if ticket["priority"] == "High"
        )


        # KPI Cards


        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Tickets",
                total_tickets
            )

        with col2:

            st.metric(
                "Critical",
                critical_tickets
            )

        with col3:

            st.metric(
                "High Priority",
                high_priority_tickets
            )

        with col4:

            st.metric(
                "Escalated",
                escalated_tickets
            )


        st.divider()

# Analytics-------------------------------------------------------------------------

        left, right = st.columns(2)


# Tickets by Category------------------------------------------

        with left:

            st.subheader("Tickets by Category")

            category_counts = {}

            for ticket in tickets:

                category = ticket["category"]

                category_counts[category] = (
                    category_counts.get(category, 0) + 1
                )

            st.bar_chart(
                category_counts
            )

# Tickets by Priority---------------------------------------------------------------

        with right:

            st.subheader("Tickets by Priority")

            priority_counts = {}

            for ticket in tickets:

                priority = ticket["priority"]

                priority_counts[priority] = (
                    priority_counts.get(priority, 0) + 1
                )

            st.bar_chart(
                priority_counts
            )


        st.divider()


# Ticket History--------------------------------------------------------------------------------


        st.subheader("Recent Ticket History")

        for ticket in tickets:

            with st.expander(
                f"#{ticket['id']} | "
                f"{ticket['priority']} | "
                f"{ticket['category']} | "
                f"{ticket['customer_name']}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Customer:** "
                        f"{ticket['customer_name']}"
                    )

                    st.write(
                        f"**Email:** "
                        f"{ticket['customer_email']}"
                    )

                    st.write(
                        f"**Category:** "
                        f"{ticket['category']}"
                    )

                    st.write(
                        f"**Subcategory:** "
                        f"{ticket['subcategory']}"
                    )

                    st.write(
                        f"**Sentiment:** "
                        f"{ticket['sentiment']}"
                    )

                    st.write(
                        f"**Urgency:** "
                        f"{ticket['urgency']}"
                    )


                with col2:

                    st.write(
                        f"**Priority:** "
                        f"{ticket['priority']}"
                    )

                    st.write(
                        f"**Assigned Team:** "
                        f"{ticket['assigned_team']}"
                    )

                    st.write(
                        f"**Action:** "
                        f"{ticket['action']}"
                    )

                    st.write(
                        f"**Escalated:** "
                        f"{'Yes' if ticket['escalated'] else 'No'}"
                    )

                    st.write(
                        f"**Previous Contacts:** "
                        f"{ticket['previous_contacts']}"
                    )


                st.write("**Customer Issue:**")

                st.write(
                    ticket["ticket_text"]
                )


                st.write("**AI Summary:**")

                st.write(
                    ticket["summary"]
                )


                st.info(
                    f"**Decision Reason:** "
                    f"{ticket['decision_reason']}"
                )

                st.caption(
                    f"Created: {ticket['created_at']}"
                )