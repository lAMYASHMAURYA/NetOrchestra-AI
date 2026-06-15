# Project Synopsis: NetOrchestra AI (v3.0)

**An Asynchronous, Intent-Driven Infrastructure Automation & Security Cockpit**

## 1. Executive Summary

NetOrchestra AI is an enterprise-grade, lightweight infrastructure automation tool designed to bridge the gap between human intent and low-level network administration. By leveraging deterministic natural language parsing, the system translates high-level English instructions into immediate, kernel-level network configurations and diagnostics. Optimized for resource-constrained environments, the architecture operates with a **0% local RAM overhead** for AI inference, ensuring high-velocity performance on standard client hardware.

---

## 2. The Problem Statement

Modern network administration and cyber-incident response require deep command-line expertise (CLI) and rapid execution. During a network anomaly or a security breach (e.g., a malicious tracker or DDoS vector), manual intervention via standard administrative interfaces introduces critical latency. Furthermore, traditional monitoring tools carry heavy software footprints that drain system memory, causing significant performance degradation on low-spec endpoint nodes.

---

## 3. Our Solution: Technical Architecture

NetOrchestra AI decouples the management interface from the core operating system using a lightweight, asynchronous Full-Stack design:

* **The Tactical Cockpit (Frontend):** A high-end, responsive cyber-tactical user interface engineered using vanilla HTML5 and custom semantic CSS. It handles user inputs asynchronously via the browser's native **Fetch API**, eliminating page reloads and ensuring absolute visual fluidic stability.
* **The Orchestration Engine (Backend):** Powered by **FastAPI** and served via **Uvicorn**, this asynchronous Python layer acts as the central middleware. It features a high-performance string-mapping parser that extracts user intents and target variables (IP targets) instantly without utilizing heavy local machine-learning weights.
* **Security & Transport Enforcement (Kernel Layer):** * **Access Control Lists (ACL):** Triggers low-level `netsh advfirewall` processes to inject, modify, or purge outbound traffic rules directly within the Windows Advanced Firewall architecture.
* **Network Path Diagnostics:** Executes non-blocking diagnostic sub-processes to monitor core internet gateways ($8.8.8.8$) and local loopback nodes ($127.0.0.1$), capturing live operational latency metrics.



---

## 4. Technical Stack & Dependencies

| Layer | Technology / Framework | Functionality |
| --- | --- | --- |
| **Frontend** | HTML5 / Cyberpunk Custom CSS / JavaScript (ES6) | Asynchronous Command Entry & Live Log Stream |
| **Backend API** | Python 3.x / FastAPI / Uvicorn Server | High-velocity REST API & Intent Routing Engine |
| **Security Layer** | Windows Advanced Firewall Subprocess (`netsh`) | Real-time Core Access Control List (ACL) Manipulation |
| **Diagnostics** | ICMP Network Protocol (`ping`) | Live Latency and Node Operational Auditing |

---

## 5. Deployment & Quick Start Guide

To deploy the infrastructure controller locally under administrative privileges, execute the following sequence:

1. **Initialize the API Server:** Launch the host terminal as an Administrator and execute the core controller file to initialize the Uvicorn worker process on the local loopback interface:
```bash
python controller.py

```


*Output verification:* `INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`
2. **Access the Console:** Launch `index.html` via any modern web browser.
3. **Execute Infrastructure Commands:** Input native instructions into the command center interface:
* *Security Isolation:* `Block ip 192.168.1.99` (Returns HTTP status `200 OK` and enforces strict kernel-level traffic restriction).
* *Policy Clearance:* `Unblock ip 192.168.1.99` (Clears active security rules and purges firewall metadata).
* *Link Quality Audit:* `Check google internet` (Runs live latency metrics against global tier-1 DNS servers).
