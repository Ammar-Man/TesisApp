# chat.py
import os
import random
import json
import torch
from model import NeuralNet  # Assuming you have model.py file for the NeuralNet class
from nltk_utils import bag_of_words, tokenize  # Your custom functions

# Set device for torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents JSON file
with open("intents.json", 'r') as json_data:
    intents = json.load(json_data)

# Use current working directory
data_dir = os.getcwd()

# Path to the .pth file
FILE = os.path.join(data_dir, 'chatdata.pth')

# Load the saved model data
data = torch.load(FILE)

# Extract the required data from the loaded model
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

# Initialize the model and load the saved state dict (weights)
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()  # Set the model to evaluation mode

# Define the bot's name
bot_name = "iris-NLP"

# Function to get the bot's response
def get_response(msg):
    # Tokenize the input message
    sentence = tokenize(msg)
    
    # Convert the sentence into bag of words format
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    # Get the model's output
    output = model(X)
    
    # Get the predicted tag with the highest probability
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # Calculate probabilities for the prediction
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # Return the appropriate response if the confidence is high enough
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent['tag']:
                return random.choice(intent['responses'])

    return "I do not understand..."

# Main loop to keep the chatbot running
if __name__ == "__main__":
    print(f"{bot_name}: Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence.lower() == "quit":
            break

        response = get_response(sentence)
        print(f"{bot_name}: {response}")
