# LangGraph Chatbot

A conversational AI chatbot built with **LangGraph**, **LangChain**, and **Streamlit**. The project focuses on building a practical chat experience with streamed responses, multiple conversations, and persistent chat history stored in **Microsoft SQL Server**.

Users will be able to start a conversation, return to an earlier one, and continue chatting with its previous context—or start a completely new conversation.

> **Project status:** This repository is under development. The feature checklist below can be updated as each capability is implemented.

## Features

- [ ] **Interactive chatbot UI** — a simple chat interface built with Streamlit.
- [ ] **Streaming responses** — display the assistant's response as it is generated instead of waiting for the full answer.
- [ ] **Multiple conversations** — create and manage separate chat sessions.
- [ ] **Persistent chat history** — store conversations and messages in Microsoft SQL Server.
- [ ] **Resume conversations** — load a previous conversation and continue from its saved context.
- [ ] **New conversation** — start a clean chat without mixing it with an existing conversation.
- [ ] **LangGraph workflow** — manage the chatbot's conversation flow and state using LangGraph.
- [ ] **LangChain integration** — connect the language model and supporting prompt/model components.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM orchestration | LangChain |
| Conversation workflow and state | LangGraph |
| Frontend | Streamlit |
| Database | Microsoft SQL Server |

The language model provider can be configured according to the model/API you choose for the implementation.

## How It Works

At a high level, a chat request follows this flow:

1. The user selects an existing conversation or creates a new one in the Streamlit interface.
2. The application loads the selected conversation's saved messages from SQL Server.
3. The user's message is passed to the LangGraph workflow along with the relevant conversation state.
4. The chatbot generates a response, which is streamed to the Streamlit UI.
5. The user and assistant messages are persisted in SQL Server so the conversation can be resumed later.

Each conversation should have its own unique identifier (for example, a `conversation_id` or LangGraph `thread_id`). This keeps the history and state of different chats separate.



## Prerequisites

Before running the application, make sure you have:

- Python installed (use a version supported by the dependencies in `requirements.txt`).
- Access to a Microsoft SQL Server instance.
- The required SQL Server ODBC driver if your Python database library uses ODBC.
- Credentials or an API key for the language model provider configured by the project.
- Git installed to clone the repository.

## Getting Started

### 1. Clone the repository

```bash
git clone <REPOSITORY_URL>
cd langgraph-chatbot
```

Replace `<REPOSITORY_URL>` with the SSH or HTTPS URL of your GitHub repository.

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template. Add the configuration required by your selected model provider and SQL Server setup.

Example template:

```env
# Language model provider
LLM_API_KEY=your_api_key
LLM_MODEL=your_model_name

# SQL Server
SQLSERVER_CONNECTION_STRING=your_sql_server_connection_string
```

Use the exact variable names expected by the application. Do not commit `.env` or real credentials to GitHub.

### 5. Set up the database

Create a database for the application in SQL Server (for example, `LangGraphChatbot`). Run the SQL schema or migrations provided by the project once they are added.

The persistence layer is intended to store, at minimum:

- Conversation metadata, such as conversation ID, title, and created/updated timestamps.
- Message data, such as conversation ID, role, content, and timestamp.
- Any additional checkpoint or graph state required by the chosen LangGraph persistence approach.

### 6. Start the application

```bash
streamlit run app.py
```

Streamlit will print the local URL in the terminal. Open that URL in your browser to use the chatbot.

## Conversation Persistence

Conversation history and LangGraph execution state are related, but they are not necessarily the same thing:

- **Chat history** contains the messages shown to the user.
- **Graph state/checkpoints** preserve the state needed by the LangGraph workflow to continue a conversation.

The application should associate both with a stable conversation/thread identifier. SQL Server will be the durable store for the application's conversation data. The specific checkpoint integration should match the persistence adapter implemented in this repository; do not assume that a generic LangGraph checkpointer automatically supports SQL Server.

## Development Roadmap

Potential improvements for later versions include:

- [ ] Rename, delete, and search conversations.
- [ ] Support configurable LLM providers and models.
- [ ] Add user authentication and user-specific conversation ownership.
- [ ] Add conversation titles generated from the first few messages.
- [ ] Add retry, error handling, and request logging.
- [ ] Add document-based chat using retrieval-augmented generation (RAG).
- [ ] Add unit tests for graph logic and persistence operations.
- [ ] Add Docker support and deployment instructions.

## Security Notes

- Keep API keys, database passwords, and other secrets in environment variables or a secret manager.
- Never commit `.env`, credentials, or production connection strings.
- Use parameterized database queries or a safe ORM/database layer.
- If authentication is added, ensure users can access only their own conversations.

## Contributing

Contributions and suggestions are welcome. For substantial changes, open an issue first to discuss the proposed feature or design. Keep changes focused and add tests where practical.

## License

A license has not been specified yet. Add a `LICENSE` file and update this section before distributing or reusing the project publicly.
