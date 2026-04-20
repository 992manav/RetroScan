import torch
import torch.nn as nn
import torch.optim as optim
import os
import random

# Hack: Append parent dir to path to import predictive logic
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predictive.lstm_model import PredictiveLSTM

def generate_synthetic_training_data(num_samples=1000):
    """
    Generates synthetic RA decay trajectories for training the LSTM model.
    """
    X, Y = [], []
    for _ in range(num_samples):
        # Start RA somewhere between 200 and 500
        start_ra = random.uniform(200, 500)
        # Decay rate
        decay_rate = random.uniform(0.5, 2.0)
        
        # Generate sequence of 5 past readings
        seq = []
        current = start_ra
        for _ in range(5):
            seq.append([current])
            current -= decay_rate
        
        # Failure occurs at 100
        days_to_fail = max(0, (current - 100) / decay_rate)
        
        X.append(seq)
        Y.append([days_to_fail])
        
    return torch.tensor(X, dtype=torch.float32), torch.tensor(Y, dtype=torch.float32)

def train_model():
    print("Generating synthetic data for PyTorch LSTM...")
    X, Y = generate_synthetic_training_data(2000)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = PredictiveLSTM(input_size=1, hidden_size=64, num_layers=2).to(device)
    
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    X, Y = X.to(device), Y.to(device)
    
    print("Beginning LSTM Training loop...")
    epochs = 100
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, Y)
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 20 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
            
    # Save Weights
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "weights"), exist_ok=True)
    save_path = os.path.join(os.path.dirname(__file__), "..", "weights", "lstm_model.pth")
    torch.save(model.state_dict(), save_path)
    print(f"Training Complete. Weights saved to {save_path}")

if __name__ == '__main__':
    train_model()
