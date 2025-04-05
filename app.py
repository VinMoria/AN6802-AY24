from flask import Flask, request, render_template
import sqlite3
import datetime
import google.generativeai as genai
import os
import wikipedia

api = os.getenv("gemini_api_key")
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=api)
telegram_api = os.getenv("telegram_api")
# print(telegram_api)

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
        conn = sqlite3.connect("user.db")
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

    conn = sqlite3.connect("user.db")
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

    conn = sqlite3.connect("user.db")
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
    return render_template("FAQ1.html", r=r_text)


@app.route("/FAQ_input", methods=["POST", "GET"])
def FAQ_input():
    q = request.form["q"]
    # r = model.generate_content(q)
    r = wikipedia.summary(q)
    # r_text = r.candidates[0].content.parts[0].text
    return render_template("FAQinput.html", r=r)


@app.route("/start_bot", methods=["POST", "GET"])
def start_bot():
    import time, requests
    from threading import Thread

    def run_bot():
        url = f"https://api.telegram.org/bot{telegram_api}/"
        updates = url + "getUpdates"
        flag = ""
        prompt = "Please enter the inflation rate (type exit to break)"
        error_msg = "Please enter a number"

        r = requests.get(updates)
        r = r.json()
        chat = r["result"][-1]["message"]["chat"]["id"]

        while True:

            msg = url + f"sendMessage?chat_id={chat}&text={prompt}"
            requests.get(msg)
            time.sleep(5)
            r = requests.get(updates)
            r = r.json()
            r = r["result"][-1]["message"]["text"]

            if flag != r:
                flag = r
                if r.isnumeric():
                    r = f"The predicted interest rate is {float(r) + 1.5}"
                    msg = url + f"sendMessage?chat_id={chat}&text={r}"
                    requests.get(msg)
                else:
                    if r == "exit":
                        msg = url + f"sendMessage?chat_id={chat}&text=Bye~"
                        requests.get(msg)
                        print("Bot Exit")
                        break
                    else:
                        msg = url + f"sendMessage?chat_id={chat}&text={error_msg}"
                        requests.get(msg)
            print(r)
            time.sleep(8)

    # 启动后台线程运行机器人逻辑
    Thread(target=run_bot).start()

    # 返回一个简单的响应给客户端
    return "success"


if __name__ == "__main__":
    app.run(debug=True)
