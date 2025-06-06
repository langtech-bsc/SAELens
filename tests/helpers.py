import copy
from typing import Any, TypedDict

from transformer_lens import HookedTransformer

from sae_lens.config import LanguageModelSAERunnerConfig

TINYSTORIES_MODEL = "tiny-stories-1M"
TINYSTORIES_DATASET = "roneneldan/TinyStories"
NEEL_NANDA_C4_10K_DATASET = "NeelNanda/c4-10k"

ALL_ARCHITECTURES = ["standard", "gated", "jumprelu", "topk"]


class LanguageModelSAERunnerConfigDict(TypedDict, total=False):
    model_name: str
    hook_name: str
    hook_layer: int
    hook_head_index: int | None
    dataset_path: str
    dataset_trust_remote_code: bool
    streaming: bool
    is_dataset_tokenized: bool
    use_cached_activations: bool
    d_in: int
    l1_coefficient: float
    lp_norm: float
    lr: float
    train_batch_size_tokens: int
    context_size: int
    feature_sampling_window: int
    dead_feature_threshold: float
    dead_feature_window: int
    n_batches_in_buffer: int
    training_tokens: int
    store_batch_size_prompts: int
    log_to_wandb: bool
    wandb_project: str
    wandb_entity: str
    wandb_log_frequency: int
    device: str
    seed: int
    checkpoint_path: str
    dtype: str
    prepend_bos: bool
    normalize_activations: str


def build_sae_cfg(**kwargs: Any) -> LanguageModelSAERunnerConfig:
    """
    Helper to create a mock instance of LanguageModelSAERunnerConfig.
    """
    mock_config_dict: LanguageModelSAERunnerConfigDict = {
        "model_name": TINYSTORIES_MODEL,
        "hook_name": "blocks.0.hook_mlp_out",
        "hook_layer": 0,
        "hook_head_index": None,
        # use a small, non-streaming dataset for testing. Huggingface gives too many requests errors otherwise.
        "dataset_path": NEEL_NANDA_C4_10K_DATASET,
        "streaming": False,
        "dataset_trust_remote_code": True,
        "is_dataset_tokenized": False,
        "use_cached_activations": False,
        "d_in": 64,
        "l1_coefficient": 2e-3,
        "lp_norm": 1,
        "lr": 2e-4,
        "train_batch_size_tokens": 4,
        "context_size": 6,
        "feature_sampling_window": 50,
        "dead_feature_threshold": 1e-7,
        "dead_feature_window": 1000,
        "n_batches_in_buffer": 2,
        "training_tokens": 1_000_000,
        "store_batch_size_prompts": 4,
        "log_to_wandb": False,
        "wandb_project": "test_project",
        "wandb_entity": "test_entity",
        "wandb_log_frequency": 10,
        "device": "cpu",
        "seed": 24,
        "checkpoint_path": "test/checkpoints",
        "dtype": "float32",
        "prepend_bos": True,
        "normalize_activations": "none",
    }

    for key, value in kwargs.items():
        mock_config_dict[key] = value

    mock_config = LanguageModelSAERunnerConfig(**mock_config_dict)

    # reset checkpoint path (as we add an id to each each time)
    mock_config.checkpoint_path = kwargs.get("checkpoint_path", "test/checkpoints")

    return mock_config


MODEL_CACHE: dict[str, HookedTransformer] = {}


def load_model_cached(model_name: str) -> HookedTransformer:
    """
    helper to avoid unnecessarily loading the same model multiple times.
    NOTE: if the model gets modified in tests this will not work.
    """
    if model_name not in MODEL_CACHE:
        MODEL_CACHE[model_name] = HookedTransformer.from_pretrained(
            model_name, device="cpu"
        )
    # we copy here to prevent sharing state across tests
    return copy.deepcopy(MODEL_CACHE[model_name])
