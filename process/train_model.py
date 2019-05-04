from model.open_nmt import OpenNMTModelRunner
from utils.pipeline import Pipeline

DEFAULT_TRAIN_CONFIG = {
    "features": True,
    "train": {
        "train_steps": 30000,
        "save_checkpoint_steps": 1000,
        "batch_size": 16,
        "word_vec_size": 300,
        "feat_vec_size": 300,
        "feat_merge": "sum",
        "layers": 3,
        "copy_attn": None,
        "position_encoding": None
    },
    "test": {

    }
}

TrainModelPipeline = Pipeline({"config": DEFAULT_TRAIN_CONFIG})
TrainModelPipeline.enqueue("model", "Initialize OpenNMT",
                           lambda f, x: OpenNMTModelRunner(x["pre-process"]["train"], x["pre-process"]["dev"]))
TrainModelPipeline.enqueue("expose", "Expose Train Data",
                           lambda f, x: f["model"].expose_train(), ext="txt")
TrainModelPipeline.enqueue("pre-process", "Pre-process Train and Dev",
                           lambda f, x: f["model"].pre_process(f["config"]["features"]))
TrainModelPipeline.enqueue("train", "Train model",
                           lambda f, x: f["model"].train(f["pre-process"], f["config"]["train"]))
TrainModelPipeline.enqueue("find-best", "Find best model", lambda f, x: f["model"].find_best(f["train"]))
TrainModelPipeline.enqueue("out", "Output a model instance", lambda f, x: f["find-best"])
