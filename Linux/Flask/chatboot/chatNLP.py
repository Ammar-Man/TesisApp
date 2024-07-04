import spacy
from nltk.metrics import jaccard_distance

# Ladda spaCy-modellen
nlp = spacy.load("en_core_web_sm")

# Dokumentet att söka igenom
document = """
Hello to, my name is Snow from TechLabs.

The RobotLab is where we run workshops and trials of implementations on our humanoid robots.

Dennis  is an IT-Lecturer at Arcada UAS where he teaches full stack web programming and data managing, visualization and engineering.

Krista  is a PhD trainer, project manager and researcher at the Department of Business Management. 

Kuvaja-Adolfsson is an IT Engineer and previous practical nurse from Sweden with a new found passion in IT. 
Christopher is an IT Engineer and previous practical nurse from Sweden with a new found passion in IT. 

Arcada is a multi-professional University of Applied Sciences in Finland.

Thank you for asking robot, I m just a computer program, so I don't have feelings, but I'm here and ready to help you with any questions or information you might need. 
 
Ammar is the maker of this application.
"""

# Klass för att lösa läsning och förståelse med spaCy
class ReadingComprehensionSolverSpacy:
    def __init__(self, corpus) -> None:
        self.nlp = spacy.load('en_core_web_sm')
        self.set_corpus(corpus)

    def __str__(self) -> str:
        return "spaCy"
    
    def set_corpus(self, document) -> None:
        self.document = document
        self.sentences = [sent.text for sent in self.nlp(document).sents]
        self.document_parts = self._split_document()

    def _split_document(self):
        # Dela upp dokumentet i 9 delar
        parts = []
        total_len = len(self.sentences)
        part_size = total_len // 9
        for i in range(9):
            start_idx = i * part_size
            end_idx = (i + 1) * part_size if i < 8 else total_len
            parts.append(" ".join(self.sentences[start_idx:end_idx]))
        return parts
    
    def preprocess(self, text) -> list:
        return [token.lemma_.lower().strip() for token in self.nlp(text) if not token.is_stop and not token.is_punct and not token.is_space]
    
    def solve(self, question) -> str:
        # Process the question
        question_tokens = self.preprocess(question)

        # Score the similarity between the question and each part of the document
        scores = []
        for part in self.document_parts:
            part_tokens = self.preprocess(part)
            score = 1 - jaccard_distance(set(part_tokens), set(question_tokens))
            scores.append(score)
        
        # The part with the highest similarity
        top_index = scores.index(max(scores))
        top_part = self.document_parts[top_index]
        return top_part


rcs = ReadingComprehensionSolverSpacy(document)

def askRobot(questions):
    best_match_question = None
    best_match_text = None
    max_similarity = -1
    
    for question in questions:
        # Hitta bästa matchningen för frågan
        match_text = rcs.solve(question)
        # Jämför likheten mellan frågan och matchningen
        question_tokens = rcs.preprocess(question)
        match_tokens = rcs.preprocess(match_text)
        similarity = 1 - jaccard_distance(set(match_tokens), set(question_tokens))
        
        # Uppdatera bästa matchningen om det är en bättre matchning
        if similarity > max_similarity:
            max_similarity = similarity
            best_match_question = question
            best_match_text = match_text
    
    return best_match_question, best_match_text

# # Exempel på hur du kan använda funktionen
# questions = ["Who is the maker?", "What is Arcada?"]
# best_question, best_match = askRobot(questions)
# print(f"Best matching question: {best_question}")
# print(f"Corresponding text: {best_match}")
