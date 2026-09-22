# 🛠️ AI-Powered Linux Troubleshooting Assistant

A retrieval-grounded AI assistant that helps analyze common Linux infrastructure issues and provides safe, structured troubleshooting guidance.

The application combines a curated Linux troubleshooting knowledge base with an external Large Language Model (LLM) to generate context-aware diagnostic recommendations through a responsive Streamlit interface.

> **Safety:** The assistant provides diagnostic guidance only. It does not execute commands or make changes to the target system.

---

## 🚀 Features

- AI-assisted Linux infrastructure troubleshooting
- Retrieval-based issue identification using keyword relevance scoring
- Curated troubleshooting knowledge base covering common Linux issues
- LLM-generated diagnostic guidance grounded with retrieved context
- Displays detected issue category, retrieval score, and matched indicators
- Safe diagnostic command recommendations
- Local knowledge-base fallback when the AI service is unavailable
- Responsive Streamlit web interface
- Environment-based API key management
- Automated unit tests for retrieval logic

---

## 🧠 How It Works

When a user describes a Linux problem, the application follows this workflow:

1. Accepts the Linux error message or problem description.
2. Compares the input against keywords in the local troubleshooting knowledge base.
3. Calculates a relevance score for each supported issue category.
4. Retrieves the most relevant troubleshooting context.
5. Sends the user problem and retrieved context to an LLM through OpenRouter.
6. Generates structured troubleshooting guidance.
7. Falls back to the local knowledge base if the external AI service is unavailable.

---

## 🏗️ Architecture

```text
                 ┌──────────────────────────────┐
                 │        Streamlit UI          │
                 │     User Problem Input       │
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │     Retrieval Engine         │
                 │  Keyword Relevance Scoring   │
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │ Linux Troubleshooting KB     │
                 │ Causes + Diagnostic Commands │
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │      LLM Integration         │
                 │        OpenRouter API        │
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │ Structured Troubleshooting   │
                 │        Guidance              │
                 └──────────────────────────────┘

                  AI unavailable
                         │
                         ▼
                 Local Knowledge Base
                       Fallback
```

---

## 🔎 Supported Troubleshooting Categories

The current knowledge base includes:

| Category | Example Problem |
|---|---|
| Disk Space | No space left on device |
| High CPU | CPU utilization reaching 100% |
| Memory | Cannot allocate memory / OOM |
| SSH Connectivity | SSH timeout or connection refused |
| Service Failure | Linux service failed to start |
| DNS Resolution | Temporary failure in name resolution |
| Permissions | Permission denied |
| Network Connectivity | No route to host |
| Read-Only Filesystem | Filesystem mounted read-only |
| High System Load | High load average / slow server |
| Application / Process | Application or process stopped |

The assistant can also send unmatched problems to the LLM with limited local context while clearly indicating that no direct knowledge-base match was found.

---

## 🤖 AI Response Structure

The LLM is instructed to return troubleshooting guidance using four sections:

```text
Issue Analysis:
Possible Causes:
Diagnostic Steps:
Recommended Next Step:
```

The prompt instructs the model to:

- Prefer retrieved troubleshooting context when available
- Avoid inventing command output
- Avoid claiming certainty without sufficient evidence
- Prefer safe, read-only diagnostic commands
- Never execute commands
- Avoid destructive commands
- Mention when administrator/root privileges may be required

---

## 🛡️ Safety Design

This project intentionally separates **diagnosis from execution**.

The assistant recommends commands such as:

```bash
df -h
free -h
systemctl status sshd
ip route
```

but never executes them automatically.

This reduces the risk of an AI-generated response making unintended changes to a Linux system.

The application also includes a local fallback mechanism so useful troubleshooting information can still be displayed when the external LLM service is unavailable.

---

## 🧰 Technology Stack

- **Python**
- **Streamlit**
- **OpenRouter API**
- **Large Language Models**
- **Requests**
- **python-dotenv**
- **truststore**
- **Pytest**
- **Linux troubleshooting knowledge base**

---

## 📁 Project Structure

```text
ai-linux-troubleshooting-assistant/
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── src/
│   ├── knowledge_base.py
│   ├── troubleshooter.py
│   └── llm_client.py
│
└── tests/
    └── test_troubleshooter.py
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd ai-linux-troubleshooting-assistant
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Configuration

The application uses OpenRouter for LLM access.

Create a `.env` file in the project root:

```text
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

An example configuration is provided in:

```text
.env.example
```

> Never commit your real `.env` file or API key to source control.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, typically:

```text
http://localhost:8501
```

---

## 🧪 Run Automated Tests

Run:

```bash
pytest -v
```

The unit tests validate the retrieval logic for several Linux troubleshooting scenarios and verify the behavior for an unknown issue.

---

## 💡 Example

### User Input

```text
SSH connection to my Linux server is timing out and I cannot connect on port 22.
```

### Retrieval

```text
Detected Category: SSH Connectivity Issue
Matched Indicators: port 22
```

The retrieved context is supplied to the LLM, which can then recommend diagnostics such as checking the SSH service, listening ports, network reachability, and firewall rules.

---

## 🔄 Fallback Handling

If the external AI service cannot be reached:

```text
LLM API unavailable
        ↓
Local troubleshooting knowledge retrieved
        ↓
Possible causes displayed
        ↓
Diagnostic commands displayed
```

This allows the application to retain basic troubleshooting capability even without an AI response.

---

## ⚠️ Limitations

- Retrieval currently uses keyword-based relevance scoring rather than semantic embeddings or a vector database.
- The knowledge base covers a defined set of Linux infrastructure scenarios.
- AI responses may still contain inaccurate recommendations and should be reviewed before use.
- The application does not inspect a real server or validate command output.
- The application intentionally does not execute remediation commands.
- LLM availability depends on the configured external API service.

---

## 🔮 Possible Future Enhancements

Potential improvements include:

- Semantic retrieval using embeddings
- Vector database integration
- Conversation history for multi-step troubleshooting
- Log-file analysis
- User-provided command-output analysis
- Expanded Linux and cloud troubleshooting knowledge
- Confidence indicators for retrieval results
- Optional integration with monitoring or incident-management platforms

---

## 🎯 Project Goal

This project explores how generative AI can support infrastructure engineers during Linux troubleshooting while maintaining a safety boundary between **AI-generated recommendations** and **actual system execution**.

It demonstrates the integration of:

- Linux infrastructure knowledge
- Python application development
- Retrieval-based context grounding
- LLM APIs
- Prompt engineering
- API failure handling
- Secure secret management
- Automated testing
- Streamlit application development

---

## 📄 Disclaimer

This project is intended for learning, demonstration, and troubleshooting assistance. Commands and AI-generated recommendations should be reviewed and validated before being used on production systems.

<img width="821" height="395" alt="image" src="https://github.com/user-attachments/assets/dfaf0f84-a084-437c-a9d1-32ab24e28178" />

<img width="833" height="414" alt="image" src="https://github.com/user-attachments/assets/3640528d-19b5-4a4f-9414-9e60e7e05f84" />

<img width="842" height="391" alt="image" src="https://github.com/user-attachments/assets/f9d18ee3-139a-4fdf-b727-99037ae93a89" />

<img width="812" height="370" alt="image" src="https://github.com/user-attachments/assets/f5569d30-2934-42dc-9d73-fc7979a5bde8" />



