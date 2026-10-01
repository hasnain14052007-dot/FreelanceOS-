from crewai import Crew, Process
from agents import create_agents
from tasks import create_tasks

class FreelanceCopilot:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def run_analysis(self, job_description: str, tone: str, step_callback=None):
        """Runs the crew. Handles fallbacks and limits automatically."""
        if not self.api_key:
            raise ValueError("API Key is missing.")
            
        if len(job_description) > 4000:
            raise ValueError("Job description exceeds the 4000 character limit.")

        try:
            return self._execute_crew(job_description, tone, step_callback, fallback=False)
        except Exception as e:
            error_str = str(e).lower()
            if "429" in error_str or "quota" in error_str:
                raise RuntimeError("Rate limit hit or free quota exhausted. Please wait 60 seconds or use your own API key.")
            elif "404" in error_str or "not found" in error_str:
                # Attempt fallback to lite model
                try:
                    return self._execute_crew(job_description, tone, step_callback, fallback=True)
                except Exception as fallback_err:
                    raise RuntimeError("Failed to connect to AI models. Please verify your API key.")
            else:
                # Sanitize unknown errors to avoid leaking tracebacks/keys
                raise RuntimeError("An unexpected error occurred during processing. Please try again.")

    def _execute_crew(self, job_description: str, tone: str, step_callback, fallback: bool):
        agents = create_agents(self.api_key, fallback=fallback)
        tasks = create_tasks(agents, job_description, tone, step_callback)

        crew = Crew(
            agents=list(agents),
            tasks=tasks,
            process=Process.sequential,
            verbose=False, # Secure: prevents logging prompts/keys
            max_rpm=8
        )

        result = crew.kickoff()
        
        # Extract the structured Pydantic output from the final task
        metrics = tasks[-1].output.pydantic
        
        return {
            "metrics": metrics,
            "analysis": tasks[0].output.raw,
            "proposal": tasks[1].output.raw,
            "plan": tasks[2].output.raw,
        }