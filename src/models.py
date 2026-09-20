from pydantic import BaseModel
from typing import List, Dict, Optional


class PolicyContext(BaseModel):
    allowed_actions: List[str]
    disallowed_actions: List[str]
    required_points: List[str]


class Case(BaseModel):
    case_id: str
    user_message: str
    assistant_response: str
    policy_context: PolicyContext


class RuleCheck(BaseModel):
    case_id: str
    sensitive_info_detected: bool
    absolute_guarantee_detected: bool
    required_points_covered: bool
    response_length: int


class LLMEvaluation(BaseModel):
    case_id: str
    policy_adherence: str
    customer_helpfulness: str
    risk_level: str
    reasoning: List[str]
    policy_violations: List[str]
    recommended_fix: str


class FinalScore(BaseModel):
    case_id: str
    score: int
    status: str
    explanation: str
