from typing import List


class ConversationManager:

    def __init__(self):

        self.role_keywords = [
            "developer",
            "engineer",
            "manager",
            "leader",
            "executive",
            "director",
            "graduate",
            "sales",
            "customer",
            "agent",
            "analyst",
            "consultant",
            "scientist",
            "administrator",
            "specialist",
            "intern"
        ]

        self.purpose_keywords = [
            "hire",
            "hiring",
            "selection",
            "screening",
            "recruitment",
            "development",
            "training"
        ]

    # -----------------------------------------
    # Check if enough information is provided
    # -----------------------------------------
    def analyze(self, history: List[dict]):

        conversation = " ".join(
            message["content"].lower()
            for message in history
            if message["role"] == "user"
        )

        # If user is refining an existing request,
        # don't ask for clarification again.
        refinement_keywords = [
            "also",
            "include",
            "add",
            "another",
            "along with",
            "personality",
            "cognitive",
            "behavioral"
        ]

        is_refinement = any(
            word in conversation
            for word in refinement_keywords
        )

        if is_refinement:
            return {
                "status": "recommend"
            }

        has_role = any(
            keyword in conversation
            for keyword in self.role_keywords
        )

        has_purpose = any(
            keyword in conversation
            for keyword in self.purpose_keywords
        )

        if not has_role:
            return {
                "status": "clarify",
                "reply": "What role are you hiring for?"
            }

        if not has_purpose:
            return {
                "status": "clarify",
                "reply": "Is this for hiring, selection, employee development, or training?"
            }

        return {
            "status": "recommend"
        }
    # -----------------------------------------
    # Detect Out-of-Scope Queries
    # -----------------------------------------
    def is_out_of_scope(self, history: List[dict]):

        conversation = " ".join(
            message["content"].lower()
            for message in history
            if message["role"] == "user"
        )

        allowed_keywords = [
            "assessment",
            "assessments",
            "test",
            "tests",
            "developer",
            "engineer",
            "manager",
            "leader",
            "executive",
            "director",
            "graduate",
            "sales",
            "customer",
            "agent",
            "analyst",
            "consultant",
            "scientist",
            "administrator",
            "specialist",
            "intern",
            "java",
            "python",
            "sql",
            "role",
            "roles",
            "hire",
            "hiring",
            "selection",
            "screening",
            "recruitment",
            "training",
            "development",
            "candidate",
            "compare",
            "comparison",
            "vs",
            "versus",
            "difference",
            "better"
        ]

        return not any(
            keyword in conversation
            for keyword in allowed_keywords
        )

    # -----------------------------------------
    # Detect Comparison Requests
    # -----------------------------------------
    def is_compare_request(self, history: List[dict]):

        conversation = " ".join(
            message["content"].lower()
            for message in history
            if message["role"] == "user"
        )

        compare_keywords = [
            "compare",
            "comparison",
            "vs",
            "versus",
            "difference",
            "better"
        ]

        return any(
            keyword in conversation
            for keyword in compare_keywords
        )