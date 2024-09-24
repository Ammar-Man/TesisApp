import spacy
import json
import os

# Ladda spaCy-modellen
nlp = spacy.load("en_core_web_sm")

# Filväg till intents.json
intents_file_path = r"D:/2024/tesis robot app/Tesis Robot/Linux/Flask/spacy_nltk_treings_modol/intents.json"

# Funktion för att ladda intents.json eller skapa en ny om den inte finns
def load_intents():
    if os.path.exists(intents_file_path):
        with open(intents_file_path, 'r') as file:
            intents = json.load(file)
    else:
        intents = {"intents": []}  # Skapa en tom intents-struktur om filen inte finns
    return intents

# Funktion för att spara intents.json
def save_intents(intents):
    with open(intents_file_path, 'w') as file:
        json.dump(intents, file, indent=4)

# Funktion för att generera en tag baserat på frågan
def generate_tag(question):
    doc = nlp(question)
    lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return "_".join(lemmas[:3])  # Använd de tre första lemmorna för att generera en tag

# Funktion för att kontrollera om en tag redan finns
def tag_exists(tag, intents):
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return True
    return False

# Funktion för att skapa ett nytt intent och lägga till det i intents.json
def add_intent(question, answer):
    intents = load_intents()
    
    # Generera en tag för frågan
    tag = generate_tag(question)
    
    # Kontrollera om taggen redan finns
    if tag_exists(tag, intents):
        print(f"Tag '{tag}' already exists. Please use a different question.")
        return  # Avbryt om taggen redan finns
    
    # Skapa ett nytt intent
    new_intent = {
        "tag": tag,
        "patterns": [question],
        "responses": [answer]
    }
    
    # Lägg till det nya intentet i intents-listan
    intents["intents"].append(new_intent)
    
    # Spara tillbaka till intents.json
    save_intents(intents)
    
    print(f"New intent added with tag: {tag}")

# Exempel på användning
if __name__ == "__main__":
    question = "Who is Christa Tigerstedt?"
    answer = "Christa Tigerstedt is Principal Lecturer in Business Administration Project researcher at Arcada in the following projects: CASSIOPEIA, MäRI, AFORA, AI Driven Nordic Health and Welfare Fields: human-centric AI driven systems, social robots, HRI"
    
    # Lägg till frågan och svaret som ett nytt intent
    add_intent(question, answer)

    # Testa med samma fråga för att se om taggen redan finns
    question_duplicate = "What is robot lab"
    add_intent(question_duplicate, answer)
