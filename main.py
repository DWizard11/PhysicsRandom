from flask import Flask, render_template, url_for, request, redirect, session
import json 
import random 
import os 
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_SECRET_KEY"))

### FUNCTION DEFINITIONS ###
def parse_data(): 
    """Reads and parse the definition qn bank """
    with open("h2_definition.json", "r", encoding='utf-8') as file: 
        eqn = json.load(file) 
    '''
    with open("idkwhat.txt", "r", encoding='utf-8') as file: 
        data = []
        for line in file: 
            try: 
                data.append(line.rstrip())
            except: 
                continue
    random.shuffle(data)
    '''
    return eqn

def get_answer(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly A-Level H2 Physics Teacher, teaching in Singapore and teaching a Junior College 2 Student by giving feedback to them about some questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        reply = response.choices[0].message.content
    except:
        reply = "Sorry, the OpenAI quota has been exceeded. Please try again later."
    return reply


### VARIABLE DEFINITIONS ###
qn_bank = parse_data()

topic_list = []
for topic, value in qn_bank.items(): 
    topic_list.append(topic)
topic_list.append("Ask Me Random")
answered_qns = []

### WEBSITE IMPLEMENTATION  ###
app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY') 

@app.route("/", methods=["POST", "GET"]) 
def home(): 
    # process definitions 
    topic = "" 
    session["answered_qns"] = []
    firstTime = True 
    if topic == "": 
        firstTime = True 
    return render_template("index.html", firstTime=firstTime, topic_list=topic_list, qn_bank=qn_bank)

@app.route("/definition", methods=["POST", "GET"])
def definition(): 
    if request.method == "POST": 
        topic = request.form.get("topic") 
        if topic == "Ask Me Random": 
            topic = random.choice(topic_list) 
            
        question_set = random.choice(qn_bank[topic]["definitions"])
        question = question_set["question"]
        session["question_set"] = question_set
        session["question"] = question 
        session["topic"] = topic 
        session["correct_answer"] = question_set["answer"]
        
        
        return render_template("definition.html", topic=topic, question=question)

    # next question 
    question_set = session.get("question_set")
    answered_qns = session.get("answered_qns")
    answered_qns.append(question_set)
    topic = session.get("topic")

    if len(answered_qns) == len(qn_bank[topic]["definitions"]): 
        answered_qns = []
        
    new_question_set = random.choice(qn_bank[topic]["definitions"])
    while new_question_set in answered_qns: 
        new_question_set = random.choice(qn_bank[topic]["definitions"])
        
    question = new_question_set["question"]
    session["question_set"] = new_question_set
    session["question"] = question 
    session["topic"] = topic 
    session["correct_answer"] = question_set["answer"]
    session["answered_qns"] = answered_qns 
    
    return render_template("definition.html", topic=topic, question=question)

@app.route("/answer", methods=["POST", "GET"])
def answer(): 
    if request.method == "POST": 
        answer = request.form.get("answer")
        try: 
            question = session.get("question") 
            topic = session.get("topic")
            correct_answer = session.get("correct_answer")
        except: 
            question = None
            topic = None 
            correct_answer = None
        # add in answer handling 
        '''
        if question is not None or correct_answer is not None: 
            prompt = f
                With regard to the H2 Physics GCE A Level Syllabus, this is the question: {question}, 
                can you check if this answer: {answer} is correct with accordance to this question? Please give feedback.
                For reference, this is the model answer: {correct_answer}
            
            reply = get_answer(prompt)
        else: 
            print("invalid") 
            prompt = "" 
        '''
        
        return render_template("answer.html", question=question, topic=topic, correct_answer=correct_answer, answer=answer)



    
if __name__ == "__main__": 
    app.run(debug=True, port=5000)





'''
def normalise(s):
    # crude normalisation: strip spaces, lowercase, collapse multiple equals signs formatting
    s = s.strip().lower()
    s = re.sub(r"\s+", "", s)
    # convert some unicode symbols to ascii approximations
    s = s.replace("Δ", "delta").replace("λ", "lambda")
    return s

def eqn(): 
    for i, q in enumerate(eqn, 1):
        print(f"\nQ{i}. Subject: {q['prompt']}")
        print(f"   Topic: {q['topic']}")
        user = input("   Type the equation (or press Enter to reveal): ")
        if not user.strip():
            print(f"   ▶ Answer: {q['equation']}")
            continue
        if normalise(user) == normalise(q["equation"]):
            print("   ✓ Correct!")
            score += 1
        if user == "e": 
            break 
        else:
            print("   ✗ Not quite.")
            print(f"   ▶ Answer: {q['equation']}")


temp = []
count = 0 
data = []

if data == []: 
    data = parse_data()
def definition(usr): 
    if usr == "q": 
        return 
    if usr == "r": 
        count = 0 
        print("Count reset.")
        print(f"Number of Times: ", count) 
    elif usr != "": 
        found = False 
        for char in data: 
            if char.lower().startswith(usr.lower()): 
                found = True 
                print(char)
        if found is False: 
            print("Definition not found.")
    else: 
        count += 1
        rand = random.choice(data).rstrip()
        while rand in temp: 
            rand = random.choice(data).rstrip()
        print(rand)
        temp.append(rand)
        if len(temp) >= 15: 
            temp = [] 
        print(f"Number of Times: ", count) 
'''