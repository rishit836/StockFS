from flask import Flask,request,render_template
import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import style
import yfinance as yf
import pandas as pd
import seaborn as sns


app = Flask(__name__)
global login
login =False
def save_stock_graph(ticker="TSLA"):
    start = "2023-01-01"
    end = '2023-12-30'
    ticker_data = yf.download(ticker,start,end)
    df = pd.DataFrame(ticker_data)
    sns.relplot(data=df['Close'],kind="line",label=ticker)
    plt.savefig("static/plot/"+str(ticker)+".png")
    sns.relplot(data=df['Volume'],kind="line",label=ticker)

    
    plt.savefig("static/plot/1.png")


@app.route('/',methods=('GET','POST'))
def main():
    ticker=""
    graph=True
    value,labels=0,0
    if request.method == "POST":
        ticker = request.form['value']

        save_stock_graph(ticker=ticker)
        graph = False


    return render_template("index.html",graph=graph,ticker=ticker.upper(),path="static/plot/"+str(ticker)+".png")

@app.route("/pm",methods=('GET','POST'))
def pm():
    global login
    if request.method == "POST":
        username = request.form['email']
        password = request.form['pass']
        with open('static/userdata.csv', mode="r") as f1:
            data = f1.readlines()
            for row in data:
                name, pas = row.split(',')
                pas = pas.strip()
                if username == name:
                    if password == pas:
                        login = True
                        print("log")
                    else:
                        login = False
                else:
                    login = False
    return render_template("pm.html",login=login)

@app.route("/signup",methods=('GET','POST'))
def signup():
    succ=False
    if  request.method == "POST":
        username = request.form['email']
        password = request.form['pass']
        insert_data = '\n' + str(username) + ',' + str(password)
        with open('static/userdata.csv', mode="a") as f:
            f.write(insert_data)
        succ=True

    return render_template("signup.html",succ=succ)


if __name__ == "__main__":
    app.run(debug=True)
    # save_stock_graph()