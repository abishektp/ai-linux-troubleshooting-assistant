import truststore

truststore.inject_into_ssl()

import os
import requests

from dotenv import load_dotenv


load_dotenv()

MODEL_NAME = "openrouter/free"


def generate_ai_response(user_problem, issue_data=None):
    """
    Generate Linux troubleshooting guidance using
    a free LLM through OpenRouter.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY was not found. Check the .env file."
        )

    if issue_data:
        causes = "\n".join(
            f"- {cause}"
            for cause in issue_data["possible_causes"]
        )

        commands = "\n".join(
            f"- {command}"
            for command in issue_data["diagnostic_commands"]
        )

        trusted_context = f"""
Issue Category:
{issue_data["name"]}

Known Possible Causes:
{causes}

Approved Diagnostic Commands:
{commands}
"""
    else:
        trusted_context = """
No matching issue was found in the local troubleshooting
knowledge base. Analyze the problem carefully and clearly
state any uncertainty.
"""

    prompt = f"""
You are an AI Linux infrastructure troubleshooting assistant.

User Problem:
{user_problem}

Trusted Troubleshooting Context:
{trusted_context}

Analyze the problem and provide a concise troubleshooting response.

Use exactly these sections:

Issue Analysis:
Possible Causes:
Diagnostic Steps:
Recommended Next Step:

Rules:
- Prefer the trusted troubleshooting context when available.
- Do not invent command output.
- Do not claim certainty without sufficient evidence.
- Prefer safe, read-only diagnostic commands.
- Do not execute commands.
- Do not recommend destructive commands such as rm -rf.
- Mention when administrator/root privileges may be required.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]