"""Structured gate result types."""

from __future__ import annotations

from dataclasses import dataclass, field as dataclass_field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class GateResult(str, Enum):
    ALLOW = "ALLOW"
    WARN = "WARN"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class GateDecision:
    gate_name: str
    result: GateResult
    code: Optional[str]
    message: str
    field: Optional[str] = None
    required_action: Optional[str] = None
    details: dict[str, Any] = dataclass_field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "gate_name": self.gate_name,
            "result": self.result.value,
            "code": self.code,
            "message": self.message,
            "field": self.field,
            "required_action": self.required_action,
            "details": self.details,
        }


@dataclass(frozen=True)
class GateSection:
    result: GateResult
    decisions: list[GateDecision] = dataclass_field(default_factory=list)
    details: dict[str, Any] = dataclass_field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "result": self.result.value,
            "decisions": [decision.to_json() for decision in self.decisions],
            "details": self.details,
        }


@dataclass(frozen=True)
class GateEvaluation:
    truth_gate: GateSection
    hybrid_gate: GateSection
    allowed: bool
    evaluated_at: datetime
    truth_rule_version: str

    def to_json(self) -> dict[str, Any]:
        return {
            "truth_rule_version": self.truth_rule_version,
            "allowed": self.allowed,
            "evaluated_at": self.evaluated_at.isoformat(),
            "truth_gate": self.truth_gate.to_json(),
            "hybrid_gate": self.hybrid_gate.to_json(),
        }
