# AI-Driven Local Log Analysis System 

This project is a real-time log monitoring and analysis tool designed for DevOps environments. It uses a local LLM (TinyLlama) via Ollama to analyze system errors instantly without sending data to the cloud.

## Key Features
- **Real-time Monitoring:** Watches all `.log` files in the directory.
- **Spam Filter:** Prevents redundant AI analysis for repeated errors.
- **Local AI:** Secure and private analysis using TinyLlama.
- **Automated Reporting:** Archives all solutions in `reports/solutions.txt`.

## How to Run
1. Install dependencies: `task setup`
2. Start the system: `task run`
3. Simulate an error: `task error`
