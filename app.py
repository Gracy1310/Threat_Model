
from flask import Flask, render_template, request
import re
import secrets
import string

app = Flask(__name__)


def check_password_strength(password):
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add an uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add a lowercase letter.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Add a number.")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        suggestions.append("Add a special character.")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, suggestions


def generate_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(characters) for _ in range(14))


@app.route("/", methods=["GET", "POST"])
def home():
    strength = None
    suggestions = []
    password = ""

    if request.method == "POST":
        password = request.form.get("password", "")

        if len(password) > 128:
            strength = "Invalid"
            suggestions = ["Password must not exceed 128 characters."]
        elif password:
            strength, suggestions = check_password_strength(password)
        else:
            suggestions = ["Please enter a password."]

    generated_password = generate_password()

    return render_template(
        "index.html",
        strength=strength,
        suggestions=suggestions,
        password=password,
        generated_password=generated_password
    )


if __name__ == "__main__":
    app.run(debug=True)
