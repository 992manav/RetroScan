import torch
import torch.nn as nn
import os
import random

class PredictiveLSTM(nn.Module):
    """
    A real PyTorch LSTM Model designed for Time-Series evaluation of Retroreflectivity.
    Predicts remaining useful days based on a sequence of historical RA measurements.
    """
    def __init__(self, input_size=1, hidden_size=64, num_layers=2):
        super(PredictiveLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM Layer
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        # Fully Connected Layer to project to 'Days to Failure'
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x is expected to be [batch, sequence_length, features]
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, _ = self.lstm(x, (h0, c0))
        # Take the output of the last time step
        out = out[:, -1, :] 
        out = self.fc(out)
        return out


class PredictiveController:
    """
    Controller module wrapping the PyTorch model for production pipeline ingestion.
    """
    def __init__(self, model_path="weights/lstm_model.pth"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = PredictiveLSTM().to(self.device)
        
        # In a real environment, we load weights here
        if os.path.exists(model_path):
            print(f"[Predictive Engine] Loading PyTorch weights from {model_path}")
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()
        else:
            print(f"[Predictive Engine] No LSTM weights found at {model_path}. Running with untrained weights / fallback simulator.")
            self.trained = False
        
        self.history_buffer = {}  # Store recent readings per GPS segment ID

    def predict_days_to_failure(self, current_ra, object_type, failure_threshold, gps_segment_id="0001"):
        """
        Uses standard sequence modeling. Pad history into [1, seq_len, 1] tensor.
        """
        if current_ra <= failure_threshold:
            return 0
            
        # Maintain a dummy history buffer of the last 5 readings for sequence modeling
        if gps_segment_id not in self.history_buffer:
            self.history_buffer[gps_segment_id] = [current_ra] * 5
        
        self.history_buffer[gps_segment_id].pop(0)
        self.history_buffer[gps_segment_id].append(current_ra)
        
        seq = self.history_buffer[gps_segment_id]
        
        # Convert to tensor
        input_tensor = torch.tensor(seq, dtype=torch.float32).unsqueeze(0).unsqueeze(-1).to(self.device)
        
        with torch.no_grad():
            output = self.model(input_tensor)
            days = output.item()
            
        # Due to untrained weights producing random numbers, we enforce a sane clamp
        # for demonstrative purposes unless a model is properly trained.
        if days < 0 or days > 10000: 
            # Fallback mathematical simulation if PyTorch LSTM isn't trained
            rate = {'ROAD_MARKING': 0.8, 'SIGN_BOARD': 0.2, 'ROAD_STUD': 0.5}.get(object_type.replace(' ', '_'), 0.5)
            days = (current_ra - failure_threshold) / rate
            
        return max(0, int(days))
