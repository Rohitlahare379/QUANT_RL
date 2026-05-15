from abc import ABC, abstractmethod
import logging
from orchestrator.context import SharedContext

class BaseAgent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"Agent.{agent_id}")

    @abstractmethod
    async def run(self, context: SharedContext) -> bool:
        """
        Run the agent's logic on the shared context.
        Returns True if successful, False otherwise.
        """
        pass

    def log_event(self, context: SharedContext, message: str):
        self.logger.info(message)
        if self.agent_id not in context.agent_outputs:
            from orchestrator.context import AgentOutput
            context.agent_outputs[self.agent_id] = AgentOutput(agent_id=self.agent_id, status="RUNNING", data={})
        context.agent_outputs[self.agent_id].logs.append(message)
