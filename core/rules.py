def calculate_priority(urgency, sentiment, previous_contacts):

    """
    Determine ticket priority using deterministic business rules.
    """

    if urgency == "High" and sentiment == "Negative":
        priority = "Critical"

    elif urgency == "High":
        priority = "High"

    elif urgency == "Medium":
        priority = "Medium"

    else:
        priority = "Low"

    # Increase priority if the customer has contacted support before
    if previous_contacts >= 2:

        if priority == "Low":
            priority = "Medium"

        elif priority == "Medium":
            priority = "High"

        elif priority == "High":
            priority = "Critical"

    return priority


def assign_team(category):

    """
    Route the ticket to the appropriate team.
    """

    team_mapping = {
        "Billing": "Payments Team",
        "Technical": "Technical Support",
        "Account": "Account Support",
        "Shipping": "Logistics Team",
        "Product": "Product Support",
        "Other": "General Support"
    }

    return team_mapping.get(
        category,
        "General Support"
    )


def determine_action(priority):

    """
    Determine the operational action.
    """

    action_mapping = {
        "Critical": "Immediate senior review",
        "High": "Priority support queue",
        "Medium": "Standard support queue",
        "Low": "Normal support queue"
    }

    return action_mapping.get(
        priority,
        "Standard support queue"
    )


def should_escalate(priority, sentiment):

    """
    Determine whether the ticket should be escalated.
    """

    if priority == "Critical":
        return True

    if priority == "High" and sentiment == "Negative":
        return True

    return False


def generate_reason(
    category,
    urgency,
    sentiment,
    priority,
    previous_contacts,
    escalated
):
    
    """
    Generate a human-readable explanation
    for the business decision.
    """

    reasons = []

    if urgency == "High":
        reasons.append("high urgency")

    if sentiment == "Negative":
        reasons.append("negative customer sentiment")

    if previous_contacts >= 1:
        reasons.append(
            f"{previous_contacts} previous support contact(s)"
        )

    if category == "Billing":
        reasons.append("billing-related issue")

    if category == "Technical":
        reasons.append("technical issue")

    if escalated:
        reasons.append("escalation criteria met")

    if not reasons:
        return "Standard ticket requiring normal support handling."

    return "Decision based on " + ", ".join(reasons) + "."


def make_decision(
    category,
    urgency,
    sentiment,
    previous_contacts
):
    """
    Main decision-engine function.
    """

    priority = calculate_priority(
        urgency=urgency,
        sentiment=sentiment,
        previous_contacts=previous_contacts
    )

    team = assign_team(category)

    action = determine_action(priority)

    escalated = should_escalate(
        priority=priority,
        sentiment=sentiment
    )

    reason = generate_reason(
        category=category,
        urgency=urgency,
        sentiment=sentiment,
        priority=priority,
        previous_contacts=previous_contacts,
        escalated=escalated
    )

    return {
        "priority": priority,
        "team": team,
        "action": action,
        "escalated": escalated,
        "reason": reason
    }