from kedro.pipeline import Pipeline, node
from .nodes import fetch_data, rename_columns, preprocess_data

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
        ]
    )
