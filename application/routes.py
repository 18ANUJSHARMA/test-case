from application import app
from flask import render_template
from flask import  render_template, request, session, redirect ,url_for


import sys
from audio import generate_audio
from character import charcter_select2,create_new_ai_character2
import json

#conversation_history = []  # Initialize conversation history
with open('users.json', 'r') as f:
    users = json.load(f)

@app.route("/")
#app.secret_key = '123'  # Replace with a strong, unique key

# Load user data from JSON file




#@app.route("/index")
def index():
   # return "<h1>hello harsh</h1>"
    return render_template("index.html" , login=False)

@app.route("/home")
def home():
   # if 'username' not in session:
       # return redirect(url_for('login'))
   # return "<h1>hello harsh</h1>"
    return render_template("home.html" , index=True)


@app.route("/login",methods=['GET','POST']) # for linking new routes
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists and password is correct
        if username in users and users[username]['password'] == password:
            # Successful login
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

@app.route("/characters") # for linking new routes
def characters():
    #conversation_history=[]
    characterData =  charcter_select2.list_subfolders()
    #[{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]
   # print(courseData[0])
    return render_template("characters.html" ,characterData=characterData , characters=True )



@app.route("/createnew", methods=["GET", "POST"])
def create_new():
  if request.method == "POST":
    character_name = request.form["characterName"]
    background_option = request.form["backgroundOption"]
    if background_option == "write":
      background_text = request.form["backgroundText"]
    else:
      background_text = create_new_ai_character2.background_character_prompt(character_name)  # Generate automatically

    try:
      create_new_ai_character2.create_new_ai_character(character_name,background_text)
      return render_template("create_new.html", success_message="Character created successfully!")
    except Exception as e:
      return render_template("create_new.html", error_message=str(e))
  else:
    return render_template("create_new.html")









@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        if username in users:
            return render_template('register.html', error='Username already exists.')

        # Add new user to JSON file
        users[username] = {'password': password}
        with open('users.json', 'w') as f:
            json.dump(users, f)

        return redirect(url_for('login'))

    return render_template('register.html')



from audio import speech_to_text
speech_to_text = speech_to_text.SpeechToText()

from character_responce import ai_palm_response
import sys
from audio import generate_audio


conversation_history=[]
@app.route('/<character_name>',methods=['GET', 'POST'])
def character_page(character_name):
    from character_responce import ai_palm_response
    
    background=charcter_select2.read_data_in_subfolder(character_name)
    background2=charcter_select2.read_data_in_subfolder(character_name)[0]
    
    #selected_character = background
    
 

    if request.method == 'POST':
        speech = request.form['speech']
        ai_response = ai_palm_response.AIResponse("AIzaSyDiqEPDpI47Qd4Je3I3chb5-z2ZQyKu3gk", background=background2)

        if speech.lower() == "disconnect call":
            sys.exit(0)
        elif speech.lower() == "what is your name":
            response = "I am " + character_name
        else:
            prompt = f"Stay in your character. Answer the question as a human as per your character {character_name}. Question: "
            response = ai_response.generate_res(prompt + speech)
            #generate_audio.generate(response)
        conversation_history.append({'user_speech': speech, 'ai_response': response})
        return render_template('character_interaction.html',name=character_name,selected_character=background, speech=speech, response=response, ai_response=ai_response,background=background ,  conversation_history=conversation_history)

    return render_template('character_interaction.html',name=character_name,selected_character=character_name,background=background)

    
   # return render_template('character_interaction.html',name=character_name,background=background)




'''
from character_responce import ai_palm_response
import sys
from audio import generate_audio
@app.route('/conversation', methods=['GET', 'POST'])
def conversation():
   

    selected_character = session['selected_character']

    if request.method == 'POST':
        speech = request.form['speech']
        ai_response = ai_palm_response.AIResponse("AIzaSyDiqEPDpI47Qd4Je3I3chb5-z2ZQyKu3gk", background=selected_character)

        if speech.lower() == "disconnect call":
            sys.exit(0)
        elif speech.lower() == "what is your name":
            response = "I am " + selected_character
        else:
            prompt = "Stay in your character. Answer the question as a human as per your character {0}. Question: ".format(selected_character)
            response = ai_response.generate_res(prompt + speech)
            generate_audio.generate(response)
        return render_template('conversation.html', selected_character=selected_character, speech=speech, response=response, ai_response=ai_response)

    # If it's a GET request, render the conversation page
    return render_template('conversation.html', selected_character=selected_character)'''