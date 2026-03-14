# AI Model Design: Literacy Classification

## 1. Objective
To instantly classify a user's digital literacy level in real-time, providing deterministic signals that trigger an interface layout adaptation to "Easy Mode".

## 2. Algorithmic Approach
Deep learning implies considerable compute resources and complex API setups which fall out of budget and violate local hackathon performance scaling. We adopt simple ML.
- **Algorithm**: Multi-class Logistic Regression
- **Library Package**: `scikit-learn`
- **Output Classes**: Low, Medium, High

## 3. Input Features (Telemetry Data)
The model depends on a 1D vector mapped directly from DOM events:
1. `typing_speed`: Measured in characters per minute (CPM).
2. `error_rate`: Proportion of Backspace/Delete strokes versus normal alpha-numerical inputs. 
3. `pause_time`: Average millisecond delay between navigating the focus of one input field to the next.

## 4. Training Strategy (Synthetic Pipeline)
Because real behavioral user data for Indian citizens is unavailable natively within 48 hours for training:
- **Synthetic Data Generation**: We will write a deterministic script using `numpy` and `pandas` generating artificial populations (e.g., 3,000 samples). 
- **Profiles**:
  - *Low Literacy Segment*: High average pause_time, high error_rate, low typing_speed.
  - *High Literacy Segment*: Low pause_time, nominal error_rate, standard typing_speed limit.
- **Persistence**: Train the Logistic Regression locally and persist it to disk using `joblib`. The Flask API will load the `joblib` file purely for inference (O(1) time complexity per request).
