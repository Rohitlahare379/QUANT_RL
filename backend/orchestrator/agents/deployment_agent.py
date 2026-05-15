from orchestrator.agents.base import BaseAgent
from orchestrator.context import SharedContext
import asyncio

class DeploymentAgent(BaseAgent):
    def __init__(self):
        super().__init__("DeploymentDecision")

    async def run(self, context: SharedContext) -> bool:
        self.log_event(context, "Synthesizing all agent outputs for deployment decision...")
        
        if not context.regime_analysis or not context.robustness_results:
            self.log_event(context, "Error: Missing upstream agent data.")
            context.deployment_decision = "REJECT"
            context.decision_reasoning = "Insufficient data for decision."
            return False
            
        await asyncio.sleep(1)
        
        # Simple decision logic for now
        suitability = context.regime_analysis.get("suitability_score", 0)
        robustness = context.robustness_results.get("robustness_score", 0)
        
        if suitability > 70 and robustness > 80:
            context.deployment_decision = "DEPLOY"
            context.decision_reasoning = f"High suitability ({suitability}) and robustness ({robustness})."
        elif suitability > 50 and robustness > 60:
            context.deployment_decision = "VALIDATION_REQUIRED"
            context.decision_reasoning = "Moderate scores. Further paper trading required."
        else:
            context.deployment_decision = "REJECT"
            context.decision_reasoning = f"Fails robustness or suitability thresholds."
            
        self.log_event(context, f"Decision: {context.deployment_decision}. Reason: {context.decision_reasoning}")
        return True
