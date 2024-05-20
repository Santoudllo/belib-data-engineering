from kedro.framework.context import KedroContext
from kedro.config import OmegaConfigLoader
from kedro.framework.hooks import _create_hook_manager
from kedro.framework.session.store import BaseSessionStore

class ProjectContext(KedroContext):
    project_name = "belib-pipeline"
    project_version = "0.1"
    package_name = "belib_pipeline"
    hooks = _create_hook_manager()

    def _get_config_loader(self, conf_paths):
        return OmegaConfigLoader(conf_paths)

# Configuration du projet
def configure_project(package_name: str) -> None:
    from kedro.framework.context import KedroContext
    context = KedroContext(package_name=package_name)
    context.bootstrap()
