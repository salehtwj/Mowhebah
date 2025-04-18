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

@app.route('/profile')
def profile():
    talent_id = request.args.get('id')
    
    if not talent_id:
        return "لم يتم تحديد الموهوب", 400

    cursor.execute("SELECT * FROM talenters WHERE id = %s", (talent_id,))
    talent = cursor.fetchone()

    if not talent:
        return "الموهوب غير موجود", 404

    return render_template("profile.html", talent=talent)


@app.route("/login")
def login():
    return render_template("login.html")  

@app.route("/register")
def register():
    return render_template("register.html") 

@app.route('/create-profile', methods=['POST'])
def create_profile():
    if request.method == 'POST':
        # الحصول على البيانات من النموذج
        account_type = request.form['account_type']
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phone_number']
        sport_field = request.form['sport_field']
        other_sport = request.form.get('other_sport', '')
        position = request.form['position']
        skills = ','.join(request.form.getlist('skills[]'))
        height = request.form['height']
        password = request.form['password']
        city = request.form['city']

        # بيانات الكاشف (تكون موجودة فقط عند اختيار نوع الحساب "كاشف")
        scout_name = request.form.get('scout_name', '')
        organization = request.form.get('organization', '')
        experience = request.form.get('experience', '')
        scout_skills = ','.join(request.form.getlist('scout_skills[]'))

        # إذا كان نوع الحساب "موهوب"، نقوم بتخزين البيانات في جدول الموهوبين
        if account_type == "talent":
            sql = """
            INSERT INTO talenters (name, username, email, phone_number, sport_field, other_sport, position, skills, height, password, city)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, username, email, phone_number, sport_field, other_sport, position, skills, height, password, city)
            cursor.execute(sql, values)
        
        # إذا كان نوع الحساب "كاشف"، نقوم بتخزين البيانات في جدول الكاشفين
        elif account_type == "scout":
            sql = """
            INSERT INTO scouts (name, username, email, phone_number, sport_field, other_sport, position, skills, height, password, city, scout_name, organization, experience, scout_skills)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, username, email, phone_number, sport_field, other_sport, position, skills, height, password, city, scout_name, organization, experience, scout_skills)
            cursor.execute(sql, values)
        
        # حفظ البيانات في قاعدة البيانات
        db.commit()

        return redirect(url_for('login'))



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

    return jsonify({"reply": response_text, "best_candidates": candidates_data})  # إرسال البيانات إلى الـ Front-End



@app.route("/profiles")
def profiles():
    best_candidates = session.pop("best_candidates", None)
    print("Session Data:", session)  # طباعة الجلسة الأصلية
    print("Best Candidates after pop:", best_candidates)  # التحقق من قيمة best_candidates بعد pop


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
    app.run(debug=True, port=5002)
