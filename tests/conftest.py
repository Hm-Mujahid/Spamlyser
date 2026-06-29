import sys
from unittest.mock import MagicMock

# 1. Mock optional heavy / UI dependencies before any package code loads
sys.modules["torch"] = MagicMock()
sys.modules["torch"].cuda = MagicMock()
sys.modules["torch"].cuda.is_available.return_value = False

sys.modules["transformers"] = MagicMock()
sys.modules["transformers"].AutoTokenizer = MagicMock()
sys.modules["transformers"].AutoModelForSequenceClassification = MagicMock()

sys.modules["streamlit"] = MagicMock()
sys.modules["lime"] = MagicMock()
sys.modules["lime.lime_text"] = MagicMock()
sys.modules["fpdf"] = MagicMock()
sys.modules["plotly"] = MagicMock()
sys.modules["plotly.express"] = MagicMock()
sys.modules["plotly.graph_objects"] = MagicMock()
sys.modules["sklearn"] = MagicMock()
sys.modules["sentencepiece"] = MagicMock()
sys.modules["datasets"] = MagicMock()

# Setup a default mock pipeline that returns structured scores for tests
mock_pipeline = MagicMock()
mock_pipeline.return_value = [{"label": "SPAM", "score": 0.95}]
sys.modules["transformers"].pipeline.return_value = mock_pipeline

# 2. Prevent models/model_init.py verification from calling Hugging Face on import
import models.model_init

models.model_init.MODEL_STATUS = True
models.model_init.MODEL_ERROR_MESSAGE = ""
models.model_init.MODEL_WARNINGS = []
models.model_init.verify_model_availability = MagicMock(return_value=(True, "", []))
