"""Structural Truth Gate for Phase 2A."""

from __future__ import annotations

import copy
from typing import Mapping

from app.db.types import AssetStatus
from app.gates.types import GateDecision, GateResult, GateSection
from app.repositories.assets import AssetSnapshot
from app.schemas.enums import PresentationLayer, ProductionType, TruthDependency, UsageRole
from app.schemas.jobs import CreateVideoJobRequest, ReferenceAsset

FORBIDDEN_AI_PROOF_TYPES = {
    "suction",
    "dirt_intake",
    "before_after",
    "transparent_bin",
    "human_efficacy",
    "sterilization",
    "safety",
    "measurable_performance",
}
PROTECTED_PROOF_TYPES = {
    "identity",
    "structure",
    "accessory",
    "compatibility",
    "attachment_performance",
    "function",
    "result",
}
AI_PRESENTATION_LAYERS = {
    PresentationLayer.AI_VISUALIZATION,
    PresentationLayer.AI_ENVIRONMENT,
    PresentationLayer.STOCK_CONTEXT,
    PresentationLayer.TEXT_CLAIM,
}


def evaluate_truth_gate(
    request: CreateVideoJobRequest,
    assets_by_id: Mapping[str, AssetSnapshot],
) -> GateSection:
    """Evaluate structural truth rules without inspecting media semantics."""

    _ = copy.deepcopy(request.model_dump(mode="json"))
    decisions: list[GateDecision] = []

    if (
        request.production_type == ProductionType.AI_GENERATION
        and request.truth_dependency == TruthDependency.high
    ):
        decisions.append(
            _decision(
                code="TRUTH_GATE_BLOCKED",
                message="High truth dependency cannot be assigned to pure AI generation.",
                field="truth_dependency",
            )
        )
        return GateSection(result=GateResult.BLOCK, decisions=decisions)

    if request.production_type != ProductionType.AI_GENERATION:
        return GateSection(result=GateResult.ALLOW, decisions=decisions)

    for index, proof in enumerate(request.proof_needs):
        proof_type = proof.proof_type.value
        if (
            proof_type in FORBIDDEN_AI_PROOF_TYPES
            and proof.presentation_layer != PresentationLayer.REAL_CAPTURE
        ):
            decisions.append(
                _decision(
                    code="AI_PROOF_NOT_ALLOWED",
                    message=f"AI presentation cannot carry {proof_type} proof.",
                    field=f"proof_needs.{index}.presentation_layer",
                )
            )
            return GateSection(result=GateResult.BLOCK, decisions=decisions)

        if proof_type in PROTECTED_PROOF_TYPES and not _has_real_proof_binding(
            proof_need_id=proof.proof_need_id,
            proof_type=proof_type,
            reference_assets=request.reference_assets,
            assets_by_id=assets_by_id,
        ):
            decisions.append(
                _decision(
                    code="TRUTH_GATE_BLOCKED",
                    message=f"{proof_type} proof requires a READY real proof asset binding.",
                    field=f"proof_needs.{index}",
                )
            )
            return GateSection(result=GateResult.BLOCK, decisions=decisions)

    return GateSection(
        result=GateResult.ALLOW,
        decisions=decisions,
        details={
            "structural_truth_only": True,
            "semantic_truth_verified": False,
            "client_facts_upgraded": False,
        },
    )


def _has_real_proof_binding(
    *,
    proof_need_id: str,
    proof_type: str,
    reference_assets: list[ReferenceAsset],
    assets_by_id: Mapping[str, AssetSnapshot],
) -> bool:
    for reference in reference_assets:
        if reference.usage_role not in {
            UsageRole.PROOF_EVIDENCE,
            UsageRole.PRODUCT_IDENTITY,
        }:
            continue
        if not reference.required_for_truth_gate:
            continue
        if proof_need_id not in reference.linked_proof_need_ids:
            continue
        asset = assets_by_id.get(reference.asset_id)
        if asset is None or asset.status != AssetStatus.READY:
            continue
        if proof_type in {"identity", "structure", "accessory"}:
            locks = reference.preservation_locks
            if proof_type == "identity" and not locks.lock_identity:
                continue
            if proof_type == "structure" and not locks.lock_structure:
                continue
            if proof_type == "accessory" and not (
                locks.lock_identity or locks.lock_structure
            ):
                continue
        return True
    return False


def _decision(*, code: str, message: str, field: str) -> GateDecision:
    return GateDecision(
        gate_name="truth_gate",
        result=GateResult.BLOCK,
        code=code,
        message=message,
        field=field,
        required_action="Use real proof evidence or reduce the proof burden.",
        details={"semantic_truth_verified": False},
    )
