from belib_pipeline.pipelines.data_processing import pipeline as data_processing_pipeline
from belib_pipeline.pipelines.data_science import pipeline as data_science_pipeline

def register_pipelines():
    return {
        "__default__": data_processing_pipeline.create_pipeline() + data_science_pipeline.create_pipeline(),
        "data_processing": data_processing_pipeline.create_pipeline(),
        "data_science": data_science_pipeline.create_pipeline(),
    }
