from flask import Flask, request, render_template
import sqlite3
import datetime
import google.generativeai as genai
import os
import wikipedia

api = os.getenv('gemini_api_key')
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=api)

flag = 1

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    global flag
    if flag == 1:
        user_name = request.form.get("q")

        t = datetime.datetime.now()
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("insert into user (name, timestamp) values (?,?)", (user_name, t))
        conn.commit()
        c.close()
        conn.close()
        flag = 0

    return render_template("main.html")

# @app.route("/foodexp", methods=["GET", "POST"])
# def foodexp():
#     return render_template("foodexp.html")

@app.route("/foodexp1", methods=["GET", "POST"])
def foodexp1():
    return render_template("foodexp1.html")

@app.route("/foodexp2", methods=["GET", "POST"])
def foodexp2():
    return render_template("foodexp2.html")

@app.route("/ethical_test", methods=["GET", "POST"])
def ethical_test():
    return render_template("ethical_test.html")

@app.route("/test_result", methods=["POST", "GET"])
def test_result():
    answer = request.form.get("answer")
    if answer == "false":
        return render_template("pass.html")
    elif answer == "true":
        return render_template("fail.html")

# @app.route("/foodexp_pred", methods=["POST", "GET"])
# def food_exp():
#     q = request.form.get("q")
#     r = 0.4851 * float(q) + 147.4
#     return render_template("foodexp_pred.html", r=r)

@app.route("/userLog", methods=["POST", "GET"])
def userLog():

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from user")
    r = ""
    for row in c.fetchall():
        r += str(row) + "\n"
    print(r)
    c.close()
    conn.close()

    return render_template("userLog.html", r=r)

@app.route("/deleteLog", methods=["POST", "GET"])
def deleteLog():

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close()
    return render_template("deleteLog.html")

@app.route("/FAQ", methods=["POST", "GET"])
def FAQ():
    return render_template("FAQ.html")

@app.route("/FAQ1", methods=["POST", "GET"])
def FAQ1():
    r = model.generate_content("Factors for Profit")
    r_text = r.candidates[0].content.parts[0].text
    return(render_template("FAQ1.html", r=r_text))

@app.route("/FAQ_input", methods=["POST", "GET"])
def FAQ_input():
    q = request.form['q']
    # r = model.generate_content(q)
    r = wikipedia.summary(q)
    # r_text = r.candidates[0].content.parts[0].text
    return(render_template("FAQinput.html", r=r))

if __name__ == "__main__":
    app.run(debug=True)
