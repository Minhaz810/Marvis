from __future__ import annotations

import asyncio
import importlib.util
import os
from types import ModuleType

from config.database import AsyncSessionLocal


def _load_seed(filename: str) -> ModuleType:
    """Load a seed module by filename from the same directory."""
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(filename, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load seed file: {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


async def run() -> None:
    """Run all seeds in dependency order."""
    providers_seed = _load_seed("llm_providers.seed.py")
    models_seed = _load_seed("llm_models.seed.py")

    async with AsyncSessionLocal() as db:
        await providers_seed.seed_llm_providers(db)
        await models_seed.seed_llm_models(db)


if __name__ == "__main__":
    asyncio.run(run())
