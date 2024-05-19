from kedro.config import OmegaConfigLoader
from kedro.framework.hooks import _create_hook_manager
from kedro.framework.context import KedroContext
from kedro.framework.session.store import BaseSessionStore
from kedro.framework.startup import ProjectMetadata
from pathlib import Path

# Définissez les métadonnées du projet
project_metadata = ProjectMetadata(
    project_name="belib-pipeline",
    package_name="belib_pipeline",
    project_path=Path(__file__).parent.parent.parent,
    source_dir="src",
    kedro_init_version="0.19.5",
    tools=None,
    example_pipeline=None,
)

# Définir les configurations du projet
CONFIG_LOADER_CLASS = OmegaConfigLoader
CONFIG_LOADER_ARGS = {
    "globals_pattern": "*globals.yml",
    "globals_dict": {
        "project_name": project_metadata.project_name,
    },
}

SESSION_STORE_CLASS = BaseSessionStore
SESSION_STORE_ARGS = {
    "path": "./sessions"
}

CONTEXT_CLASS = KedroContext

HOOK_MANAGER = _create_hook_manager()
