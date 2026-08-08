"""Entry point discovery for Bench Pro modules."""

from dataclasses import dataclass
from importlib import metadata
import logging
from typing import Any

from benchpro_core.module_host.contracts import BENCHPRO_ENTRY_POINT_GROUP

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DiscoveredModule:
    name: str
    entry_point: Any
    distribution: str | None = None


def _distribution_name(entry_point: Any) -> str | None:
    dist = getattr(entry_point, "dist", None)
    if dist is None:
        return None
    metadata_obj = getattr(dist, "metadata", {})
    return metadata_obj.get("Name") if hasattr(metadata_obj, "get") else None


def discover_modules(group: str = BENCHPRO_ENTRY_POINT_GROUP) -> list[DiscoveredModule]:
    """Discover module entry points without importing or instantiating them."""
    entry_points = metadata.entry_points()
    selected = entry_points.select(group=group) if hasattr(entry_points, "select") else entry_points.get(group, [])

    modules = [
        DiscoveredModule(
            name=entry_point.name,
            entry_point=entry_point,
            distribution=_distribution_name(entry_point),
        )
        for entry_point in sorted(selected, key=lambda entry_point: entry_point.name)
    ]
    logger.info("Discovered %d module entry point(s)", len(modules))
    return modules
