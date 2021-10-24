from logging import debug
from flask import Flask,render_template,url_for,request
from flask_mongoengine import MongoEngine
from pywikihow import search_wikihow
import contextlib,io,os
from pymongo import MongoClient
import pandas as pd



app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://codesploit:codesploit@cluster0.xcehq.mongodb.net/test"

client = MongoClient("mongodb+srv://codesploit:codesploit@cluster0.xcehq.mongodb.net/test")
dbs = client['Cyberpreach']

class question():
    def __init__(self,question):
        self.question=dbs.quiz.find_one({"name":question})
        self.quiz=[]
    def fivequestion(self):
        self.quiz=self.question
        return self.quiz

@app.route('/',methods=['GET','POST'])
def index():                                     #index function
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        email = request.form.get("email")
        passw = request.form.get("pass")
        s=dbs.login.find_one({"email":email, "pass": passw})
        print(s)
        if(s):
            return render_template("index.html")
        else:
            print("invalid")

    return render_template('login.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if(request.method=="POST"):
        name= request.form.get("name")
        email=request.form.get("email")
        passw=request.form.get("pass")
        cpass=request.form.get("cpass")
        if(passw==cpass):
            x=dbs.login.insert_one({"name": name, "email": email, "pass": passw})
        if(x):
            return render_template("login.html")
    return render_template("signup.html")

@app.route('/learn',methods=['GET','POST'])
def learn():
    if(request.method=="POST"):
        try:
            find=request.form.get("searchkey")
            if(find!=""):
                resu=search_wikihow(find,1)
                cont = io.StringIO()
                with contextlib.redirect_stdout(cont):
                    resu[0].print()
                capt = cont.getvalue()
                print(capt)
                return render_template("learn.html",output=capt)
        except:
            print("bypass")

    return render_template("learn.html")



@app.route('/quiz/<quizfield>',methods=['GET','POST'])
def quiz(quizfield):
    Quiz= question(quizfield);
    if(request.method=="POST"):
        marks=0
        for ans in Quiz.fivequestion()["questions"]:
             if(ans['ans']==request.form[ans['name']]):
                 marks=marks+1
        print(marks)
        if(marks<7):
            return render_template("failure.html")
        else:
            return render_template("success.html")
    questions = Quiz.fivequestion()
    return render_template("quiz.html",questions=questions)

@app.route('/internet',methods=['GET','POST'])
def internet():
    return render_template("internet.html")


@app.route('/phone',methods=['GET','POST'])
def phone():
    if(request.method=="POST"):
        try:
            x=[]
            var = request.form.get("button")
            print(var)
            coll = dbs[var]
            cur = list(coll.find())
            print(cur[1])
            for i in cur:
                print(i)
            print(x)

            df = pd.DataFrame(cur)
            name_list = df["name"].tolist()
            des_list = df["des"].tolist()
            url_list = df["url"].tolist()
            print(len(name_list))
            return render_template("phone.html",len=len(name_list) ,output=name_list, out1=des_list ,out2 = url_list, out3=var )
        except:
            print("bypass")

    return render_template("phone.html")

@app.route('/video',methods=['GET','POST'])
def video():
    if(request.method=="POST"):
        try:
            var = request.form.get("link")
            col_name = request.form.get("colna")
            var1= request.form.get("vid")
            coll = dbs[col_name]
            cur = list(coll.find({"name":var1}))

            df = pd.DataFrame(cur)
            name_list = df["name"].tolist()
            des_list = df["des"].tolist()
            url_list = df["url"].tolist()

            print(cur)
            print(len(name_list))

            seark = des_list[0]
            resu=search_wikihow(seark,1)
            cont = io.StringIO()
            with contextlib.redirect_stdout(cont):
                resu[0].print()
            capt = cont.getvalue()
            print(capt)

            return render_template("video.html", output=name_list, out1=des_list , link=var, capture = capt)
        except:
            print("by2")

    return render_template("video.html")


if __name__=="__main__":
    app.run(debug=True)
