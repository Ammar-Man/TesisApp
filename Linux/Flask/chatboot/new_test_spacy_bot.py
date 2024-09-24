import os
import random
import json
import torch
import torch.nn as nn
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
os.chdir(r'D:\2024\tesis robot app\Tesis Robot\Linux\Flask\chatboot')
# Hämta nuvarande arbetskatalog
current_directory = os.getcwd()
print(f'ntsbpy => Arbetskatalog: {current_directory}')
script_directory = os.path.dirname(os.path.abspath(__file__))
print(f'ntsbpy => Python-skriptets katalog: {script_directory}')




# Download punkt tokenizer (if it's not already downloaded)
nltk.download('punkt')

# Tokenization and stemming utilities
stemmer = PorterStemmer()

# Tokenize a sentence into words
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# Stem and lower a word
def stem(word):
    return stemmer.stem(word.lower())

# Create bag of words from a tokenized sentence
def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    return bag

# Neural network class
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out

# import sys
# sys.path.append('D:/2024/Arcada robot/ArcadaRobot/Linux/Flask/chatboot')

# Set device for PyTorch (GPU if available, otherwise CPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents file
with open("intents.json", 'r') as json_data:
    intents = json.load(json_data)

# Use current working directory to load the model
data_dir = os.getcwd()
FILE = os.path.join(data_dir, '.\chatdata.pth')
# D:\2024\tesis robot app\Tesis Robot\Linux\Flask\chatboot\chatdata.pth



# Load model data from .pth file
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

# Initialize and load the model
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()  # Set model to evaluation mode

# Define bot name
bot_name = "iris-NLP"

# Function to get a response from the bot
def get_response(msg):
    # Tokenize the input message
    sentence = tokenize(msg)
    
    # Convert sentence to bag of words
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    # Get model prediction
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # Get the probability of the predicted tag
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # Return a response if the probability is high enough
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent["responses"])

    return "I do not understand..."
# Main loop for chatbot interaction
# if __name__ == "__main__":
#     print(f"{bot_name}: Let's chat! (type 'quit' to exit)")
#     while True:
#         sentence = input("You: ")
#         if sentence.lower() == "quit":
#             break

#         response = get_response(sentence)
#         print(f"{bot_name}: {response}")

# response = get_response("hello who is deniis")
# print(response)
