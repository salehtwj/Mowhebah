from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from langchain_rag import query_rag  
import pymysql

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': "mawhebh",
    'charset': 'utf8mb4'  # لضمان دعم اللغة العربية
}

db = pymysql.connect(**db_config)
cursor = db.cursor(pymysql.cursors.DictCursor)  # استخدام DictCursor لإرجاع النتائج كمصفوفة قواميس

app = Flask(__name__)

app.secret_key = "eb47fec502f8d3381a55371832deaf390a8a76ee3dd8f41ad784dd2bde7855da"

@app.route("/")
def index():
    return render_template("index.html")  

@app.route("/posts")
def posts():
    return render_template("post2.html")  

@app.route("/about")
def about():
    return render_template("about.html")  

@app.route("/contact")
def contact():
    return render_template("contact.html")  


# اخر تحديث وصلت له
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    # إعادة تعيين المرشحين السابقين قبل استرجاع بيانات جديدة
    session["best_candidates"] = None 

    response_text, best_candidates = query_rag(user_message, 0.5)  # استرجاع القيمتين

    # جلب بيانات الموهوبين من قاعدة البيانات
    if best_candidates:
        format_strings = ','.join(['%s'] * len(best_candidates))  # إنشاء placeholders للـ SQL
        query = f"SELECT * FROM talenters WHERE id IN ({format_strings})"
        cursor.execute(query, tuple(best_candidates))
        candidates_data = cursor.fetchall()
    else:
        candidates_data = []

    session["best_candidates"] = candidates_data  
    # print(f"theis is the shape : {candidates_data.shape}")

    return jsonify({"reply": response_text, "best_candidates": candidates_data})  # إرسال البيانات إلى الـ Front-End



@app.route("/profiles")
def profiles():
    best_candidates = session.pop("best_candidates", None)
   
    if best_candidates:
        data = best_candidates  # استخدام المرشحين الجدد
        print('best_candidates!!!!!', data)

    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM talenters") 
        data = cursor.fetchall()  # جلب جميع الملفات في الحالة العادية
        print('هذا الشرط تنفذ!!!!!!', data)

    return render_template("profiles.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)