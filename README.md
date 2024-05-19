# LLM and Multi-Agent Collaboration for Demand Response
In this project, we leverage the multi-agent framework 'AutoGen' to create AI agents representing various stakeholders engaged in demand response, including operational, market, and consumer interests. These agents collaborate to formulate proposed solutions that align with the collective interests of all stakeholders and user preferences.

Demand response is a strategy that involves adjusting electricity usage in response to supply conditions or price signals to maintain grid stability and manage energy consumption.

AI Agents used:
1. **Utility Agent**: Analyzes data and proposes a demand response plan that ensures consumer load remains below a specified threshold during peak hours.
2. **Market Agent**: Revises the plan to maximize consumer savings while calculating the potential cost reductions through participation.
3. **Consumer Agent**: Evaluates the plan based on consumer comfort preferences and weather forecasts, rejecting modifications that would cause significant discomfort.
4. **Critical Evaluation Agent**: Assesses the proposed plan for potential flaws or limitations.
5. **Discussion Continuity Agent**: Summarizes the conversation and highlights areas for further collaboration to improve solution quality in subsequent discussion cycles.
6. **Executive Summary Agent**: Provides a concise and well- structured executive summary of agent conversation for the user.

![Demand Response Framework](DemandResponse_Framework.png)
