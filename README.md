# 🤖 Invoice Processing Agent – Multi‑Agent System with Google Gemini

This project is a multi‑agent invoice processing system built as a capstone for the **Kaggle Agents Intensive**. It automates reading, validating, routing, and optimizing invoice payments using **Google Gemini** models, with optional Excel export and support for **handwritten invoices**.

---

## 🎯 Project Overview

### Problem

Manual invoice processing in Accounts Payable (AP) is:

- Slow (often 30–45 minutes per invoice).
- Error‑prone (typos, missed fields, duplicate payments).
- Costly (missed early‑payment discounts, overpayments).
- Hard to scale as invoice volume grows.

### Solution

This project implements an **AI‑powered multi‑agent system** that:

- Accepts PDF or image invoices.
- Uses Google Gemini to extract structured invoice data.
- Validates data quality and detects potential duplicates.
- Routes invoices to the right approver based on business rules.
- Optimizes payment timing to capture early‑payment discounts.
- Handles exceptions (new vendor, high‑amount, suspicious invoices).
- Optionally **exports invoice details to Excel** for finance systems.

Track: **Enterprise Agents** – intelligent agents for business workflows.

---

## 🧠 Agent Architecture

The system is organized as 6 cooperating agents in the `agents/` folder:

1. **InvoiceOrchestrator (`orchestrator.py`)**  
   - Entry point for processing an invoice.  
   - Coordinates all other agents in sequence and returns a final result.

2. **InvoiceCaptureAgent (`capture_agent.py`)**  
   - Uses Gemini to extract structured fields from:
     - PDF invoices.
     - Image invoices (including handwritten) using Gemini Vision.
   - Fields include invoice number, vendor, dates, amounts, currency, tax, terms, and line items.

3. **ValidationAgent (`validation_agent.py`)**  
   - Validates extracted data:
     - Required fields present.
     - Date and amount sanity checks.
     - Basic duplicate / anomaly checks (can be extended).

4. **RoutingAgent (`routing_agent.py`)**  
   - Decides who should approve the invoice:
     - Small amounts → auto‑approve or team lead.
     - Medium amounts → department manager.
     - Large amounts → finance leadership.
   - Returns approver role, urgency/priority, and suggested SLA.

5. **OptimizationAgent (`optimizer_agent.py`)**  
   - Analyzes payment terms (e.g., “2/10 Net 30”).  
   - Computes potential early‑payment savings and recommends optimal payment dates.

6. **ExceptionHandlerAgent (`exception_handler.py`)**  
   - Handles flagged issues:
     - New or unknown vendors.
     - High‑amount invoices.
     - Validation failures.
   - Produces structured exception records for human review.

All agents use **Google Gemini** via the official `google-generativeai` Python SDK.

---

## 🧱 Tech Stack

- **Language:** Python 3.11+
- **AI:** Google Gemini (via `google-generativeai`)
- **API Framework:** FastAPI + Uvicorn
- **Data / Export:** pandas, openpyxl
- **Images / Handwriting:** Pillow (PIL)
- **Other:** python‑dotenv, logging

---

## 🔌 Gemini Integration

The project uses the **direct Gemini API** (not ADK) for reliability and production‑style control:

- Configured via `google.generativeai.configure(api_key=...)`.
- Models created with `genai.GenerativeModel(model_name)`.
- Content generated with `model.generate_content(...)`.
- Vision (handwritten invoices) supported by passing images and prompts together.

---

## 📂 Project Structure

invoice-agent/
├── agents/
│ ├── init.py
│ ├── orchestrator.py # Main orchestrator agent
│ ├── capture_agent.py # Capture/extraction agent (PDF + handwritten)
│ ├── validation_agent.py # Validation agent
│ ├── routing_agent.py # Routing/approval agent
│ ├── optimizer_agent.py # Payment optimization agent
│ └── exception_handler.py # Exception handling agent
├── api/
│ ├── init.py
│ └── main.py # FastAPI app and HTTP endpoints
├── utils/
│ └── excel_exporter.py # Excel export utilities (pandas + openpyxl)
├── tests/
│ ├── sample_invoices/ # Sample PDF/image invoices for testing
│ ├── test_agents.py # Tests individual agents
│ ├── test_end_to_end.py # End‑to‑end processing test + Excel export
│ └── test_handwritten.py # Test for handwritten invoice extraction
├── .env.example # Template for environment variables
├── requirements.txt # Python dependencies
├── README.md # This file
└── (optional helper scripts like start-api.sh, test-api-endpoints.sh)

