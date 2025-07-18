# Personal Finance Buddy

**Personal Finance Buddy** is a modular, extensible LLM‑powered agentic toolkit that helps you plan, track, and optimize every aspect of your personal finances. Built on top of Google’s Agent Development Kit (ADK) and fastMCP Model Context Protocol servers, it brings together document ingestion, API integrations, and custom sub‑agents to deliver a seamless financial planning experience.

---

## Table of Contents

1. [Architecture & Components](#architecture--components)
2. [Key Features](#key-features)
3. [Tools & Integrations](#tools--integrations)
4. [Getting Started](#getting-started)
5. [Usage Examples](#usage-examples)
6. [Agent Workflow](#agent-workflow)
7. [Plans & Roadmap](#plans--roadmap)
8. [Contributing](#contributing)
9. [License](#license)

---

## Architecture & Components

### Core LLM Agent

* **LLM Backbone**: Orchestrates all sub‑agents via LangChain, managing context, memory, and routing queries to the right specialist.
* **Memory Store**: Vector database (e.g., Pinecone, FAISS) holding user‑specific and general financial knowledge.

### Sub‑Agents

1. **Tax Agent**: Interprets tax documents, estimates liabilities, suggests deductions.
2. **Investment Agent**: Analyzes market data, constructs optimized portfolios, runs scenario analyses.
3. **Budget Agent**: Tracks spending, categorizes transactions, sets saving goals.
4. **Credit Agent**: Monitors credit score changes, explains factors, suggests improvement strategies.
5. **Retirement Agent**: Simulates retirement savings, projects income streams, optimizes account allocations.
6. **Insurance Agent**: Reviews policies, benchmarks premiums, highlights coverage gaps.
7. **Goal Planning Agent**: Helps define financial goals, maps milestones, tracks progress.

### Orchestration

* **Google Agent Development Kit (ADK)**: Hosts and routes agent calls, provides web GUI for live testing, and exposes RESTful endpoints for programmatic access.
* **fastMCP Model Context Protocol Servers**: High‑throughput servers maintaining conversation state and agent contexts, enabling parallelism and low‑latency responses.

---

## Key Features

* **Document Ingestion**: Upload PDFs, bank statements, tax forms; parsed via OCR and fed into vector store.
* **API Integrations**: Real‑time data from Plaid, Alpha Vantage, IEX Cloud, Experian, IRS, NewsAPI, FRED, Numbeo, and more.
* **Vector Retrieval**: Uses RAG (Retrieval‑Augmented Generation) to ground agent answers in your own documents.
* **Automations**: Schedule reminders (e.g., quarterly tax reminders, monthly budget reviews) via built‑in scheduler.
* **Dynamic API Discovery**: Plans for self‑augmenting the toolset by scanning OpenAPI specs and auto‑registering new endpoints.

---

## Tools & Integrations

| Category               | Service / Library                | Purpose                               |
| ---------------------- | -------------------------------- | ------------------------------------- |
| Core Framework         | Google ADK                       | Agent orchestration, chains, memory   |
| Agent Hosting          | Google ADK                       | Sub‑agent lifecycle & API gateway     |
| Protocol Server        | fastMCP                          | Context management, low‑latency RPC   |
| Docs & RAG             | vector DB + LangChain            | Document retrieval & grounding        |
| Banking & Transactions | Plaid, Dwolla                    | Transaction history, balances         |
| Market Data            | Alpha Vantage, IEX Cloud, Finviz | Stock prices, fundamentals            |
| Credit Monitoring      | Experian API                     | Credit score, report details          |
| Tax Info               | IRS API, Taxee                   | Tax brackets, historic rules          |
| Macro & News           | NewsAPI, FRED, BEA               | Economic indicators, latest headlines |
| Cost of Living         | Numbeo, Teleport                 | Regional price indices, rent data     |

---

## Getting Started

### Prerequisites

* Python 3.10+
* [Google ADK](https://developers.google.com/agent-development-kit) installed
* fastMCP installed
* API keys for Plaid, Alpha Vantage, NewsAPI, Experian, etc.

### Installation

```bash
git clone https://github.com/your-org/personal-finance-buddy.git
cd personal-finance-buddy
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env` and populate:

   ```ini
   OPENAI_API_KEY=...
   PLAID_CLIENT_ID=...
   ALPHA_VANTAGE_KEY=...
   NEWSAPI_KEY=...
   EXPERIAN_API_KEY=...
   FRED_API_KEY=...
   ```
2. Start Google ADK web server:

   ```bash
   ```
adk web

````
3. python mcp/finance_servers/main_server.py
````

---

## Usage Examples

### Interactive Interface

Provided through ADK WEB and hosted on port 8000
```


---

## Agent Workflow

1. **User Query** arrives Web GUI, or API.
2. **Core LLM** inspects intent, routes to sub‑agent.
3. **Sub‑Agent** retrieves any required documents (via vector store) or fetches real‑time data (via API).
4. **Sub‑Agent** returns structured answer; Core LLM composes final response.
5. **Context Update**: Interaction is stored for future reference.

---

## Plans & Roadmap

* **Dynamic API Onboarding**: Auto‑parse OpenAPI specs, generate client wrappers, and register new endpoints without code changes.
* **Advanced Analytics**: Integrate lightweight ML models for anomaly detection, forecasting, and clustering of spending patterns.
* **Web Dashboard**: React/Tailwind UI with interactive charts, drill‑downs, and live notifications.
* **Trade Execution**: Experimental support for broker APIs (e.g., Alpaca, Interactive Brokers) to execute orders.
* **Mobile App**: Flutter/React Native companion for on‑the‑go access.
* **Community Plugins**: Marketplace for third‑party agent extensions and custom data connectors.

---

## Contributing

Contributions are welcome! Please review [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on raising issues and submitting pull requests.

---

## License

This project is licensed under the [MIT License](LICENSE).
