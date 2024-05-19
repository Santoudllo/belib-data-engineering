from kedro.pipeline import Pipeline, node
from belib_pipeline.pipelines.data_processing.nodes import fetch_data, rename_columns, preprocess_data
from belib_pipeline.pipelines.data_science.nodes import node_train_model, node_save_metrics

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=fetch_data,
                inputs=None,
                outputs="raw_data",
                name="fetch_data_node",
            ),
            node(
                func=rename_columns,
                inputs="raw_data",
                outputs="renamed_data",
                name="rename_columns_node",
            ),
            node(
                func=preprocess_data,
                inputs="renamed_data",
                outputs="preprocessed_data",
                name="preprocess_data_node",
            ),
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
