from knowledge_base import TROUBLESHOOTING_KB
from llm_client import generate_ai_response


def identify_issue(user_input):
    """
    Identify the most relevant Linux issue using
    keyword-based relevance scoring.
    """

    user_input = user_input.lower()

    best_issue_id = None
    best_issue_data = None
    best_score = 0
    best_matches = []

    for issue_id, issue_data in TROUBLESHOOTING_KB.items():

        matched_keywords = []

        for keyword in issue_data["keywords"]:
            if keyword in user_input:
                matched_keywords.append(keyword)

        score = len(matched_keywords)

        if score > best_score:
            best_score = score
            best_issue_id = issue_id
            best_issue_data = issue_data
            best_matches = matched_keywords

    return best_issue_id, best_issue_data, best_score, best_matches


def display_result(issue_data):
    """
    Display the local knowledge-base troubleshooting result.
    """

    print("\n--------------------------------")
    print("Linux Troubleshooting Assistant")
    print("--------------------------------")

    print(f"\nDetected Issue: {issue_data['name']}")

    print("\nPossible Causes:")
    for cause in issue_data["possible_causes"]:
        print(f"- {cause}")

    print("\nRecommended Diagnostic Commands:")
    for command in issue_data["diagnostic_commands"]:
        print(f"- {command}")

    print(
        "\nRecommendation: Review the diagnostic output "
        "before performing any remediation."
    )


def main():
    print("AI-Powered Linux Troubleshooting Assistant")
    print("------------------------------------------")

    user_input = input(
        "\nPaste a Linux error message or describe the problem:\n> "
    )

    issue_id, issue_data, score, matched_keywords = identify_issue(user_input)
    if issue_data:
      print(f"\nDetected Category: {issue_data['name']}")
      print(f"Retrieval Score: {score}")
      print(f"Matched Keywords: {', '.join(matched_keywords)}")

    try:
        print("\nAnalyzing the issue with AI...\n")

        response = generate_ai_response(user_input, issue_data)
        print(response)

    except Exception as error:
        print(f"\nAI API Error: {error}")

        print("\nAI service is currently unavailable.")
        print(
            "Falling back to the local troubleshooting "
            "knowledge base.\n"
        )

        if issue_data:
            display_result(issue_data)
        else:
            print(
                "The issue could not be identified from the "
                "current troubleshooting knowledge base."
            )


if __name__ == "__main__":
    main()