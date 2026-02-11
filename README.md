# Agent Watchdog: Self-Healing Agentic Monitoring System
A real-time monitoring and anomaly detection system for distributed agents, with logging, health tracking, and automated alerting.

## Project Overview
Agent Watchdog is a self-healing monitoring system designed to detect, diagnose, and automatically resolve failures in a running Windows application.
The system continuously monitors application health, performs root cause analysis using logs and system telemetry, applies automated remediation actions, and escalates unresolved issues to developers.

This project demonstrates concepts in agentic AI systems, system observability, automated remediation, and AI-assisted operations (AIOps).

## Key Features
### 1. Real-Time Monitoring
   - Monitors process health and performance metrics
   - Detects crashes, hangs, and throughput degradation
   - Uses heartbeat logs to detect silent failures

### 2. Automated Diagnosis

   - Parses structured logs and Windows event data
   - Resolves crash symbols to source-level file and line numbers
   - Correlates performance metrics with failure patterns

### 3. Self-Healing Actions

   - Automatically restarts applications or services
   - Dynamically edits configuration parameters
   - Applies remediation strategies based on predefined rules and LLM decisions

### 4. Intelligent Escalation

   - Opens GitHub issues when automated recovery fails
   - Includes structured logs, root cause analysis, and suggested fixes
   - Provides build and reproduction instructions for developers

### 5. Learning & Adaptation

   - Logs remediation actions and outcomes
   - Analyzes historical effectiveness to improve future decisions

## System Architecture

**Application → Heartbeat Logger → Agent Watchdog → LLM Decision Engine → Remediation / Escalation**

- The target application emits structured logs and heartbeat signals.
- Agent Watchdog monitors system health and performance.
- An LLM determines remediation actions using structured prompts.
- Actions are executed automatically or escalated to developers.
- Historical outcomes are stored for learning and optimization.


## Project Structure
```
agent-watchdog/
│
├── agent_watchdog.py           # Main monitoring loop and remediation executor
├── deep_diag.py                # Diagnostic utilities and GitHub escalation logic
├── agent_diagnostics.py        # Log discovery, stall detection, and AI-generated diagnostic reports
├── deep_heal_prompt.txt        # LLM policy prompt for remediation decisions
├── brain.txt                   # Legacy prompt for basic restart logic
├── learn.py                    # Post-mortem learning and reboot scheduling
├── airport_config.yaml         # Application runtime configuration parameters
├── heartbeat_logger.py         # Heartbeat generator for stall detection
│
|
├── requirements.txt            # Python dependencies
└── README.md
```

## Technologies Used

- Python (psutil, subprocess, logging, JSON)
- Local LLM (Ollama / OpenAI-compatible API)
- GitHub API for automated escalation
- SQLite / JSON logging for historical learning
- Windows system telemetry & event logging

## How It Works

- The watchdog continuously monitors a target application (e.g., AirportDummy.exe).
- If a crash or stall is detected, recent logs and system signals are collected.
- An LLM analyzes the failure context and returns a structured remediation decision.
- The agent executes the action (restart, reconfigure, escalate, reboot).
- If unresolved, a detailed GitHub issue is automatically generated.


## Example Use Cases

- Automated recovery for critical Windows services
- AI-assisted DevOps troubleshooting
- Enterprise application uptime monitoring
- Self-healing infrastructure prototypes
- Intelligent SRE tooling experiments


## Future Improvements

- Multi-process orchestration and dependency graphs
- Cloud-based telemetry ingestion
- Reinforcement learning for remediation strategy optimization
- UI dashboard for live monitoring and incident tracking


## License

This project is for research and educational purposes.
Feel free to fork and extend.
