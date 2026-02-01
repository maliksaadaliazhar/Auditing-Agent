# 🕵️ AI Receipt Auditor (Agentic Workflow)

An intelligent agentic workflow that automates corporate expense auditing. It combines **Computer Vision** (LandingAI) with **Reasoning LLMs** (Gemini 2.5) to extract data, check compliance against corporate policies, and visually highlight violations.

> **🔴 Live Demo:** [Click here to test the App](https://auditing-agent.streamlit.app/)

## 🚀 Key Features
* **Visual Evidence:** Unlike standard auditors, this agent draws a **red bounding box** around the specific line item causing the violation.
* **Multi-Modal Pipeline:**  **Vision Agent:** Parses raw receipts (PDF/JPG/PNG) into structured JSON.
    * **Reasoning Agent:** Analyzes items against complex rules (e.g., "No alcohol," "No weekend expensing").
* **Grounding:** Solves LLM hallucinations by mapping the verdict back to the original pixel coordinates.

## 🛠️ Architecture

The system follows a 3-stage Pipeline:

1.  **The Eye (LandingAI):**  Extracts text and—crucially—the **bounding box coordinates** for every line item.
2.  **The Brain (Gemini 2.5 Flash):**  Receives the structured data.
    * identifies violating items (e.g., "Heineken" -> Alcohol).
3.  **The Painter (Custom Logic):**
    * Matches the LLM's identified items back to the Vision Agent's coordinates.
    * Annotates the image for the human reviewer.

## 📸 Usage

1.  **Upload a Receipt:** Supports JPG, PNG, and JPEG.
2.  **Automatic Analysis:** The agents run in the background.
3.  **Verdict:**
    * ✅ **Approved:** Shows the clean receipt.
    * ❌ **Fraud Detected:** Shows the specific policy broken (e.g., "Alcohol Detected") and highlights the item by using bounding boxes.


---
*Built as a prototype for exploring Agentic AI workflows in FinTech.*