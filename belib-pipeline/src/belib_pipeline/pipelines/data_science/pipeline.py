from kedro.pipeline import Pipeline, node
from .nodes import node_train_model, node_save_metrics

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=node_train_model,
                inputs="preprocessed_data",
                outputs="model_metrics",
                name="train_model_node",
            ),
            node(
                func=node_save_metrics,
                inputs="model_metrics",
                outputs=None,
                name="save_metrics_node",
            ),
        ]
    )
