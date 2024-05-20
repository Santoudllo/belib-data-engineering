from kedro.pipeline import Pipeline
from belib_pipeline.pipelines.data_processing.pipeline import create_pipeline as data_processing_pipeline
from belib_pipeline.pipelines.data_science.pipeline import create_pipeline as data_science_pipeline

def register_pipelines() -> dict:
    data_processing = data_processing_pipeline()
    data_science = data_science_pipeline()

    return {
        "__default__": data_processing + data_science,
        "data_processing": data_processing,
        "data_science": data_science,
    }
