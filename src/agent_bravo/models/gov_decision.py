from pydantic import BaseModel, Field
from typing import Literal

class GovDecision(BaseModel):
    """A decision made by an AI governor. Implements functions for posting the decision to Discord. """
    opinion: str = Field(
        description="The opinion of the agent regarding the proposal."
    )
    reasoning: str = Field(
        description="The detailed reasoning behind the opinion."
    )
    vote: Literal[0, 1, 2] = Field(
        description="The vote of the agent (1 = for, 0 = against, 2 = abstain)."
    )

    def cast_vote(self):
        """Cast the vote on the proposal."""
        pass

    def post_opinion(self):
        """Post the opinion to the governance forum."""
        pass