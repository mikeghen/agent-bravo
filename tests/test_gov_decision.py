import pytest
from pydantic import ValidationError
from agent_bravo.models.gov_decision import GovDecision

def test_valid_gov_decision_votes():
    """Test that valid votes (0, 1, 2) create a valid GovDecision."""
    for vote in [0, 1, 2]:
        decision = GovDecision(
            opinion="The proposal is well thought out.",
            reasoning="After reviewing all considerations, this seems balanced.",
            vote=vote,
        )
        assert decision.vote == vote
        assert decision.opinion == "The proposal is well thought out."
        assert decision.reasoning == "After reviewing all considerations, this seems balanced."

@pytest.mark.parametrize("invalid_vote", [-1, 3, 10, "1", 1.5, None])
def test_invalid_gov_decision_votes(invalid_vote):
    """Test that any vote not in (0, 1, 2) raises a ValidationError."""
    with pytest.raises(ValidationError):
        GovDecision(
            opinion="The proposal is off-balance.",
            reasoning="Based on our criteria, this should not be accepted.",
            vote=invalid_vote,
        ) 