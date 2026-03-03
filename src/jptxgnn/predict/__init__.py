"""老藥新用預測模組"""

from .repurposing import (
    load_drug_disease_relations,
    find_repurposing_candidates,
    generate_repurposing_report,
)

from .prepare_for_txgnn import (
    load_txgnn_nodes,
    build_drugbank_to_node_index,
    build_disease_node_mappings,
    prepare_drug_list_for_txgnn,
    get_drug_node_mapping_stats,
    export_for_colab,
)

from .process_txgnn_results import (
    load_txgnn_predictions,
    filter_by_score_threshold,
    merge_with_kg_candidates,
    generate_txgnn_report,
    export_high_confidence_predictions,
    compare_with_existing_indications,
)

from .txgnn_model import (
    TxGNNPredictor,
    CheckpointManager,
    detect_device,
    check_dependencies,
    download_pretrained_model,
    download_kg_data,
    run_taiwan_drug_prediction,
)

__all__ = [
    # Knowledge Graph based
    "load_drug_disease_relations",
    "find_repurposing_candidates",
    "generate_repurposing_report",
    # TxGNN preparation
    "load_txgnn_nodes",
    "build_drugbank_to_node_index",
    "build_disease_node_mappings",
    "prepare_drug_list_for_txgnn",
    "get_drug_node_mapping_stats",
    "export_for_colab",
    # TxGNN results processing
    "load_txgnn_predictions",
    "filter_by_score_threshold",
    "merge_with_kg_candidates",
    "generate_txgnn_report",
    "export_high_confidence_predictions",
    "compare_with_existing_indications",
    # TxGNN Deep Learning Model
    "TxGNNPredictor",
    "CheckpointManager",
    "detect_device",
    "check_dependencies",
    "download_pretrained_model",
    "download_kg_data",
    "run_taiwan_drug_prediction",
]
