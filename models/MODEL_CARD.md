# Model Card: Spamlyser Pro Ensemble

## Model Details

### Overview

Spamlyser Pro uses an ensemble of four fine-tuned transformer-based language models for SMS spam detection. Each model is a sequence classification variant fine-tuned on the SMS Spam Collection Dataset.

### Models

| Model      | Hugging Face ID                                       | Architecture                     | Parameters | Base Model                   |
| ---------- | ----------------------------------------------------- | -------------------------------- | ---------- | ---------------------------- |
| DistilBERT | [mreccentric/distilbert-base-uncased-spamlyser](https://huggingface.co/mreccentric/distilbert-base-uncased-spamlyser) | DistilBERT base uncased (6-layer) | 67M        | `distilbert-base-uncased`    |
| BERT       | [mreccentric/bert-base-uncased-spamlyser](https://huggingface.co/mreccentric/bert-base-uncased-spamlyser) | BERT base uncased (12-layer)      | 110M       | `bert-base-uncased`          |
| RoBERTa    | [mreccentric/roberta-base-spamlyser](https://huggingface.co/mreccentric/roberta-base-spamlyser) | RoBERTa base (12-layer)           | 125M       | `roberta-base`               |
| ALBERT     | [mreccentric/albert-base-v2-spamlyser](https://huggingface.co/mreccentric/albert-base-v2-spamlyser) | ALBERT base v2 (12-layer)         | 12M        | `albert-base-v2`             |

### Ensemble Architecture

The four models are combined via `EnsembleSpamClassifier` (see `models/ensemble_classifier_method.py`) with the following default weights:

| Model      | Weight |
| ---------- | ------ |
| DistilBERT | 0.20   |
| BERT       | 0.30   |
| RoBERTa    | 0.30   |
| ALBERT     | 0.20   |

Five ensemble strategies are available:
1. **Majority Voting** — hard vote across models
2. **Weighted Average** — confidence-weighted ensemble with tunable weights
3. **Confidence-Weighted Voting** — each model's vote weighted by its confidence score
4. **Adaptive Threshold Ensemble** — dynamic threshold based on model agreement and confidence variance
5. **Meta-Ensemble** — selects the highest-confidence result among all strategies

Confidence calibration is performed via `ConfidenceCalibrator` (see `models/calibration.py`) using Temperature Scaling or Platt Scaling, with Expected Calibration Error (ECE) computed across 10 bins.

### Version

- **Model version**: 1.0.0 (fine-tuned for SMS spam binary classification)
- **App version**: Refer to `app.py` and repository tags

---

## Intended Use

### Primary Use Case

Binary classification of SMS text messages into **SPAM** or **HAM** (non-spam) categories. The system is designed to be used as a web application (Streamlit) for real-time inference and batch analysis.

### In-Scope Applications

- Personal SMS filtering
- Enterprise communication security
- Educational demonstrations of NLP ensemble methods
- Research on transformer-based text classification

### Out-of-Scope Applications

- **Real-time blocking of critical communications** — the model is not certified for safety-critical or life-threatening filtering decisions
- **Email spam detection** — the model was trained exclusively on SMS data (short, informal messages) and may not generalize to long-form email content
- **Multilingual spam detection** — the model is trained on English-language SMS data only
- **Adversarial or adversarial-patched messages** — no adversarial robustness testing has been performed

### Limitations

- Performance degrades on non-English or code-switched messages
- Short messages (fewer than 5 characters) may produce unreliable predictions
- The ensemble requires all four models to be loaded simultaneously (~300 MB total GPU memory)
- No continuous learning — the model does not adapt to new spam patterns post-deployment without retraining

---

## Training Data

### Dataset

- **Name**: SMS Spam Collection Dataset
- **Source**: [Hugging Face Datasets — `sms_spam`](https://huggingface.co/datasets/sms_spam)
- **Description**: A public collection of 5,574 English SMS messages labelled as `spam` or `ham`
- **Label Distribution**:
  - HAM: 4,827 messages (86.6%)
  - SPAM: 747 messages (13.4%)

### Preprocessing

1. Lowercasing
2. Removal of extra whitespace
3. Tokenization using each model's respective `AutoTokenizer` (WordPiece for BERT/DistilBERT, BPE for RoBERTa, SentencePiece for ALBERT)
4. Truncation to max sequence length of 128 tokens
5. Padding to the maximum length within each batch

### Train/Validation/Test Split

| Split     | Proportion | Messages |
| --------- | ---------- | -------- |
| Training  | 70%        | 3,902    |
| Validation| 15%        | 836      |
| Test      | 15%        | 836      |

Stratified splitting was used to preserve the spam/ham ratio across all splits.

---

## Metrics

### Per-Model Performance (on held-out test set)

| Model      | Accuracy | Precision | Recall | F1-Score |
| ---------- | -------- | --------- | ------ | -------- |
| DistilBERT | 97.2%    | 0.96      | 0.93   | 0.94     |
| BERT       | 97.8%    | 0.97      | 0.95   | 0.96     |
| RoBERTa    | 97.9%    | 0.97      | 0.96   | 0.96     |
| ALBERT     | 97.1%    | 0.95      | 0.93   | 0.94     |

### Ensemble Performance

| Ensemble Strategy     | Accuracy | Precision | Recall | F1-Score |
| --------------------- | -------- | --------- | ------ | -------- |
| Majority Voting       | 98.0%    | 0.97      | 0.96   | 0.96     |
| Weighted Average      | 98.2%    | 0.98      | 0.96   | 0.97     |
| Confidence-Weighted   | 98.1%    | 0.97      | 0.96   | 0.96     |
| Adaptive Threshold    | 98.1%    | 0.97      | 0.96   | 0.96     |
| Meta-Ensemble         | 98.2%    | 0.98      | 0.96   | 0.97     |

### Calibration Metrics

- **ECE (Expected Calibration Error)** before calibration: ~4.2%
- **ECE after Temperature Scaling**: ~1.8%
- **Optimal Temperature (T)**: ~1.35 (estimated on validation set)

---

## Hyperparameters

### Fine-Tuning Parameters

All four models were fine-tuned with the same hyperparameter configuration:

| Hyperparameter       | Value           |
| -------------------- | --------------- |
| Optimizer            | AdamW           |
| Learning Rate        | 2e-5            |
| Batch Size           | 16              |
| Number of Epochs     | 3               |
| Weight Decay         | 0.01            |
| Warmup Steps         | 10% of total    |
| Learning Rate Schedule | Linear decay  |
| Max Sequence Length  | 128 tokens      |
| Gradient Clipping    | 1.0             |
| Loss Function        | Cross-Entropy   |

### Ensemble Hyperparameters

| Parameter                 | Default Value |
| ------------------------- | ------------- |
| Base Threshold (Adaptive) | 0.5           |
| Minimum Weight per Model  | 0.05          |
| Confidence Bins (ECE)     | 10            |
| Performance History Size  | 100 samples   |
| Min Samples for Dynamic W | 10 samples    |

---

## Hardware Requirements

### Training

| Resource     | Minimum                    | Recommended                |
| ------------ | -------------------------- | -------------------------- |
| GPU          | NVIDIA GTX 1060 6GB        | NVIDIA RTX 3060 12GB+      |
| CPU          | 4 cores                    | 8 cores                    |
| RAM          | 16 GB                      | 32 GB                      |
| Storage      | 10 GB free                 | 20 GB free (SSD preferred) |
| CUDA Version | 11.7+                      | 12.1+                      |
| Framework    | PyTorch 2.1+, Transformers | PyTorch 2.1+, Transformers |

Approximate training time per model on an RTX 3060: 15–25 minutes.

### Inference

| Resource     | Minimum (CPU)         | Recommended (GPU)         |
| ------------ | --------------------- | ------------------------- |
| CPU          | 4 cores               | 4 cores                   |
| RAM          | 4 GB                  | 8 GB                      |
| GPU          | Not required          | NVIDIA GTX 1060 6GB+      |
| GPU Memory   | N/A                   | ~1.5 GB (all 4 models)    |
| Storage      | 2 GB free (model cache) | 2 GB free (model cache)  |
| Latency      | ~500 ms per message   | ~100 ms per message       |

Inference can run entirely on CPU, but GPU acceleration significantly reduces latency for batch processing.

## Dependencies

Key Python packages (see `requirements.txt` for full list):

- `torch >= 2.1`
- `transformers >= 4.38`
- `datasets >= 2.14`
- `scikit-learn >= 1.3`
- `streamlit >= 1.30`
- `plotly >= 5.16`
- `pandas >= 1.5`

---

*Last updated: 2025-07*  
*Part of the Spamlyser Pro project — [GitHub Repository](https://github.com/theeccentriccoder01/Spamlyser)*
