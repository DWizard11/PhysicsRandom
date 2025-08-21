from flask import Flask, render_template
import json 
import random 
### FUNCTION DEFINITIONS ###
def parse_data(): 
    with open("h2_physics_equations.json", "r", encoding='utf-8') as file: 
        eqn = json.load(file) 
        random.shuffle(eqn)
        
    with open("idkwhat.txt", "r", encoding='utf-8') as file: 
        data = []
        for line in file: 
            try: 
                data.append(line.rstrip())
            except: 
                continue
    random.shuffle(data)
    return data

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
def definition(): 
    usr = input("Type a key word to search for definition (or press enter to reveal def)")
    print()
    if usr == "q": 
        break 
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
        
### WEBSITE IMPLEMENTATION  
app = Flask(__name__)

@app.route("/") 
def home(): 
    return render_template("index.html")


if __name__ == "__main__": 
    app.run()