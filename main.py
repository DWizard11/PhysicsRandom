from flask import Flask, render_template, url_for, request, redirect, session
import json 
import random 
import os 

### FUNCTION DEFINITIONS ###
def parse_data(): 
    """Reads and parse the definition qn bank """
    with open("h2_definition.json", "r", encoding='utf-8') as file: 
        eqn = json.load(file) 
        
    return eqn

### VARIABLE DEFINITIONS ###
qn_bank = parse_data()

topic_list = []
for topic, value in qn_bank.items(): 
    topic_list.append(topic)

answered_qns = []

### WEBSITE IMPLEMENTATION  ###
app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY') 

@app.route("/", methods=["GET", "POST"])
def home():
    session["answered_qns"] = []

    # check if there's a search result stored
    results = session.pop("result", None)
    query = session.pop("query", None)

    # if you want to know if it came from search at all
    searched = session.pop("searched", False)

    return render_template(
        "index.html",
        topic_list=["Ask Me Random"] + topic_list,
        qn_bank=qn_bank,
        results=results,
        query=query,
    )


@app.route("/definition", methods=["POST", "GET"])
def definition(): 
    if request.method == "POST": 
        topic = request.form.get("topic") 
        if topic == "Ask Me Random": 
            topic = random.choice(topic_list)
            random_qn = True 
        else: 
            random_qn = False 

        # Decide question type
        type_qn = random.choice(["definitions", "equations"])
        if not qn_bank[topic].get("equations"): 
            type_qn = "definitions"
        if not qn_bank[topic].get("definitions"): 
            type_qn = "equations"

        # Pick first question
        question_set = random.choice(qn_bank[topic][type_qn])
        session["question_set"] = question_set
        session["question"] = question_set["question"]
        session["topic"] = topic 
        session["correct_answer"] = question_set["answer"]
        session["answered_qns"] = [question_set]  # start fresh
        session["random_qn"] = random_qn 
        return render_template("definition.html", topic=topic, question=question_set["question"])

    else: 
        # GET: next question
        random_qn = session.get("random_qn", False) 
        if random_qn is True: 
            topic = random.choice(topic_list)
        else: 
            topic = session.get("topic", random.choice(topic_list))
        answered_qns = session.get("answered_qns", [])
    
        all_qns = []
        for key in ["definitions", "equations"]:
            all_qns.extend(qn_bank[topic].get(key, []))
    
        # If everything answered, reset
        if len(answered_qns) >= len(all_qns): 
            answered_qns = []
    
        # Choose new qn not answered yet
        remaining = [q for q in all_qns if q not in answered_qns]
        if not remaining:
            return "No questions available for this topic."
    
        new_question_set = random.choice(remaining)
    
        answered_qns.append(new_question_set)
        session["answered_qns"] = answered_qns
        session["question_set"] = new_question_set
        session["question"] = new_question_set["question"]
        session["correct_answer"] = new_question_set["answer"]
        session["topic"] = topic

        return render_template("definition.html", topic=topic, question=new_question_set["question"])

@app.route("/answer", methods=["POST", "GET"])
def answer(): 
    if request.method == "POST": 
        answer = request.form.get("answer")
        try: 
            question = session.get("question", None) 
            topic = session.get("topic", None)
            correct_answer = session.get("correct_answer", None)
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

@app.route("/search")
def search(): 
    query = request.args.get("query") 
    if query == "": 
        session["result"] = None
        session["query"] = None
        return redirect("/")
    result = []
    # query definition
    for topic, values in qn_bank.items(): 
        # go thru the definitions and equations 
        definitions = values["definitions"] 
        if definitions != []: 
            for item in definitions: 
                if query.lower() in topic.lower(): 
                    result.append(item) 
                elif query.lower() in item["question"].lower(): 
                    result.append(item)
                     
                    
        # check equation 
        equation = values["equations"] 
        if equation != []: 
            for item in equation: 
                if query.lower() in topic.lower(): 
                    result.append(item)
                elif query.lower() in item["question"].lower(): 
                    result.append(item) 

    if result == []: 
        print("NOT FOUND")
        result = "Not found" 
    else: 
        print(result)
    session["result"] = result
    session["query"] = query
    session["searched"] = True
    return redirect("/")
        
    

    
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