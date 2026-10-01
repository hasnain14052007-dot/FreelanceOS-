from crewai import Task
from agents import ProjectMetrics

def create_tasks(agents, job_description: str, tone: str, step_callback=None):
    """Creates the sequential tasks for the crew."""
    lead_scout, proposal_architect, project_manager, finance_officer = agents

    task1 = Task(
        description=f"Analyze this job:\n\n{job_description}\n\nDetermine a fit score (1-10), list any red flags, and declare a GO or NO-GO decision.",
        expected_output="A detailed analysis report including fit score, red flags, and a GO/NO-GO verdict.",
        agent=lead_scout,
        callback=step_callback
    )

    task2 = Task(
        description=f"Based on the analysis, write a proposal for the client. The tone should be: {tone}. Keep it strictly under 300 words.",
        expected_output="A clean, highly engaging proposal ready to be sent to the client.",
        agent=proposal_architect,
        callback=step_callback
    )

    task3 = Task(
        description="Draft a project plan. Create a markdown table of milestones, estimate total hours, and list 2-3 execution risks.",
        expected_output="A structured project plan with a milestone table, timeline, and risk assessment.",
        agent=project_manager,
        callback=step_callback
    )

    task4 = Task(
        description="Calculate a recommended fixed price in USD based on the estimated hours (assume $50/hr base, adjust for complexity). Outline a payment schedule (e.g., 50% upfront).",
        expected_output="Financial breakdown, payment terms, and the final structured metrics.",
        agent=finance_officer,
        output_pydantic=ProjectMetrics,
        callback=step_callback
    )

    return [task1, task2, task3, task4]