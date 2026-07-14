"""Structural HYBRID Gate for Phase 2A."""

from __future__ import annotations

from typing import Mapping, Optional

from app.db.types import AssetStatus
from app.gates.types import GateDecision, GateResult, GateSection
from app.repositories.assets import AssetSnapshot
from app.schemas.enums import ProductionType, UsageRole
from app.schemas.jobs import CreateVideoJobRequest, ReferenceAsset

REAL_LAYER_PROOF_TYPES = {
    "suction",
    "dirt_intake",
    "before_after",
    "transparent_bin",
    "human_efficacy",
    "sterilization",
    "safety",
    "measurable_performance",
    "function",
    "result",
    "attachment_performance",
}
REAL_LAYER_ROLES = {
    UsageRole.PROOF_EVIDENCE,
    UsageRole.PRODUCT_IDENTITY,
    UsageRole.FIRST_FRAME,
    UsageRole.SOURCE_CLIP,
}
ALLOWED_AI_ROLES = {"environment", "atmosphere", "transition", "non_proof_hook"}
PROHIBITED_AI_PROOF_ROLES = {
    "core_product_proof",
    "before_after",
    "measurable_performance",
}
REQUIRED_REWRITE_LOCKS = {
    "product_shape",
    "logo",
    "controls",
    "accessory_set",
    "proof_result",
}


def evaluate_hybrid_gate(
    request: CreateVideoJobRequest,
    assets_by_id: Mapping[str, AssetSnapshot],
) -> GateSection:
    if request.production_type != ProductionType.HYBRID:
        return GateSection(
            result=GateResult.ALLOW,
            details={"applicable": False},
        )

    layers = request.hybrid_layers
    if layers is None:
        return _blocked("HYBRID requires hybrid_layers.", "hybrid_layers")
    if layers.real_layer is None:
        return _blocked("HYBRID requires real_layer.", "hybrid_layers.real_layer")
    if layers.ai_layer is None:
        return _blocked("HYBRID requires ai_layer.", "hybrid_layers.ai_layer")
    if layers.real_layer.required is not True:
        return _blocked("real_layer.required must be true.", "hybrid_layers.real_layer.required")
    if layers.ai_layer.required is not True:
        return _blocked("ai_layer.required must be true.", "hybrid_layers.ai_layer.required")
    if not layers.ai_must_not_rewrite:
        return _blocked(
            "ai_must_not_rewrite must not be empty.",
            "hybrid_layers.ai_must_not_rewrite",
        )

    allowed_roles = set(layers.ai_layer.allowed_roles)
    disallowed_roles = sorted(allowed_roles - ALLOWED_AI_ROLES)
    if disallowed_roles:
        return _blocked(
            "ai_layer.allowed_roles contains proof or unsupported roles.",
            "hybrid_layers.ai_layer.allowed_roles",
            details={"disallowed_roles": disallowed_roles},
        )
    prohibited_overlap = sorted(allowed_roles & PROHIBITED_AI_PROOF_ROLES)
    if prohibited_overlap:
        return _blocked(
            "AI layer cannot be allowed to carry product proof.",
            "hybrid_layers.ai_layer.allowed_roles",
            details={"disallowed_roles": prohibited_overlap},
        )

    missing_locks = sorted(REQUIRED_REWRITE_LOCKS - set(layers.ai_must_not_rewrite))
    if missing_locks:
        return _blocked(
            "HYBRID proof jobs must lock all proof-related fields.",
            "hybrid_layers.ai_must_not_rewrite",
            details={"missing_rewrite_locks": missing_locks},
        )

    references_by_id = {reference.asset_id: reference for reference in request.reference_assets}
    for index, proof in enumerate(request.proof_needs):
        if proof.proof_type.value not in REAL_LAYER_PROOF_TYPES:
            continue
        if proof.proof_need_id not in layers.real_layer.carries_proof_need_ids:
            return _blocked(
                "Proof need must be carried by real_layer.",
                f"proof_needs.{index}",
            )
        if not _has_real_layer_asset(
            proof_need_id=proof.proof_need_id,
            reference_asset_ids=layers.real_layer.reference_asset_ids,
            references_by_id=references_by_id,
            assets_by_id=assets_by_id,
        ):
            return _blocked(
                "Proof need requires a READY real layer reference asset.",
                f"proof_needs.{index}",
            )

    return GateSection(
        result=GateResult.ALLOW,
        details={
            "applicable": True,
            "real_layer_carries_proof": True,
            "ai_layer_presentation_only": True,
            "semantic_truth_verified": False,
        },
    )


def _has_real_layer_asset(
    *,
    proof_need_id: str,
    reference_asset_ids: list[str],
    references_by_id: Mapping[str, ReferenceAsset],
    assets_by_id: Mapping[str, AssetSnapshot],
) -> bool:
    for asset_id in reference_asset_ids:
        reference = references_by_id.get(asset_id)
        if reference is None:
            continue
        if reference.usage_role not in REAL_LAYER_ROLES:
            continue
        if proof_need_id not in reference.linked_proof_need_ids:
            continue
        asset = assets_by_id.get(asset_id)
        if asset is None or asset.status != AssetStatus.READY:
            continue
        return True
    return False


def _blocked(
    message: str,
    field: str,
    *,
    details: Optional[dict[str, object]] = None,
) -> GateSection:
    return GateSection(
        result=GateResult.BLOCK,
        decisions=[
            GateDecision(
                gate_name="hybrid_gate",
                result=GateResult.BLOCK,
                code="HYBRID_GATE_BLOCKED",
                message=message,
                field=field,
                required_action="Move proof to the real layer and restrict AI to presentation.",
                details=details or {"semantic_truth_verified": False},
            )
        ],
    )
