import os
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/", methods=["GET", "POST"])
def home():
    workout = None

    if request.method == "POST":
        muscle = request.form.get("muscle")
        level = request.form.get("level")
        time = request.form.get("time")
        goal = request.form.get("goal")
        place = request.form.get("place")
        equipment = request.form.get("equipment")

        prompt = f"""
Skapa ett träningspass på svenska.

Information:
Muskelgrupp: {muscle}
Nivå: {level}
Tid: {time} minuter
Mål: {goal}
Plats: {place}
Utrustning: {equipment}

Regler:
- Anpassa passet efter tiden
- Anpassa övningar efter plats och utrustning
- Skriv först en kort uppvärmning
- Skriv sedan 4 till 6 övningar

Formatet ska vara exakt så här:

UPPVÄRMNING
Kort uppvärmning (1–2 meningar)

ÖVNINGAR

1. Namn på övning
Set: antal
Reps: antal
Vila: sekunder

2. Namn på övning
Set: antal
Reps: antal
Vila: sekunder

3. Namn på övning
Set: antal
Reps: antal
Vila: sekunder

4. Namn på övning
Set: antal
Reps: antal
Vila: sekunder

TIPS
Ett kort tips på slutet.
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        workout = response.output_text

    return render_template("index.html", workout=workout)

   
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
