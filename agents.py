import os
from crewai import Agent, LLM
from pydantic import BaseModel, Field

# --- Structured Output Models ---
class ProjectMetrics(BaseModel):
    fit_score: int = Field(description="Fit score from 1 to 10")
    decision: str = Field(description="GO or NO-GO")
    estimated_hours: int = Field(description="Estimated total hours to complete")
    recommended_price: float = Field(description="Recommended price in USD")
    red_flags: list[str] = Field(description="List of identified red flags")

def get_llm(api_key: str, model_name: str = "gemini/gemini-3.5-flash"):
    """Returns the CrewAI LLM instance."""
    return LLM(model=model_name, api_key=api_key, temperature=0.4)

def create_agents(api_key: str, fallback: bool = False):
    """Initializes the 4 agents with the provided API key."""
    # Use fallback to lite model if requested
    model = "gemini/gemini-3.5-flash-lite" if fallback else "gemini/gemini-3.5-flash"
    llm = get_llm(api_key, model)

    lead_scout = Agent(
        role="Lead Scout",
        goal="Analyze the job description for fit, red flags, and viability.",
        backstory="Expert at vetting freelance clients and projects to prevent scope creep and bad deals.",
        verbose=False,
        llm=llm,
        allow_delegation=False
    )

    proposal_architect = Agent(
        role="Proposal Architect",
        goal="Write a highly converting, concise proposal under 300 words tailored to the specific tone.",
        backstory="A master copywriter who knows how to hook clients quickly and highlight relevant value.",
        verbose=False,
        llm=llm,
        allow_delegation=False
    )

    project_manager = Agent(
        role="Project Manager",
        goal="Break the project down into clear milestones, a realistic timeline, and identify execution risks.",
        backstory="Seasoned technical PM who ensures projects are delivered on time without overwhelming the developer.",
        verbose=False,
        llm=llm,
        allow_delegation=False
    )

    finance_officer = Agent(
        role="Finance Officer",
        goal="Determine fair pricing, outline a payment schedule, draft an invoice summary, and finalize structured metrics.",
        backstory="Strict but fair financial advisor who ensures the freelancer gets paid what they are worth.",
        verbose=False,
        llm=llm,
        allow_delegation=False
    )

    return lead_scout, proposal_architect, project_manager, finance_officer