"""
Spamlyser Pro Models Package
This package contains all the model-related functionality for SMS threat detection.
"""

from .batch_processor import BatchProcessor
from .calibration import ConfidenceCalibrator
from .custom_rules_manager import (
    check_custom_rules,
    load_custom_rules,
    save_custom_rules,
)
from .encrypted_report import ReportEncryptor
from .export_feature import export_results_button
from .message_categorizer import MessageCategorizer
from .model_comparator import agreement_score, compare_predictions
from .sender_reputation import SenderReputation
from .rule_engine import (
    check_compound_rules,
    evaluate_compound_rule,
    evaluate_condition,
    validate_compound_rules,
)
from .simple_explainer import SPAM_KEYWORDS, SimpleExplainer
from .storage_manager import StorageManager, default_json_validator
from .threat_analyzer import (
    THREAT_CATEGORIES,
    classify_threat_type,
    get_threat_specific_advice,
)
from .webhook_notifier import WebhookNotifier
from .word_analyzer import WordAnalyzer

__all__ = [
    "SPAM_KEYWORDS",
    "THREAT_CATEGORIES",
    "BatchProcessor",
    "ConfidenceCalibrator",
    "MessageCategorizer",
    "ReportEncryptor",
    "SenderReputation",
    "SimpleExplainer",
    "StorageManager",
    "WebhookNotifier",
    "WordAnalyzer",
    "agreement_score",
    "check_custom_rules",
    "check_compound_rules",
    "classify_threat_type",
    "compare_predictions",
    "default_json_validator",
    "evaluate_compound_rule",
    "evaluate_condition",
    "export_results_button",
    "get_threat_specific_advice",
    "load_custom_rules",
    "save_custom_rules",
    "validate_compound_rules",
]
