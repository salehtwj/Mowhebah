from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from langchain_rag import query_rag  
from chat_utils import ChatUtils
from video_analyzer import analyze_video 
import pymysql
import uuid
import os

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': "mawhebh",
    'charset': 'utf8mb4'  # لضمان دعم اللغة العربية
}

UPLOAD_FOLDER = 'challenges_videos'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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


@app.route("/analyze_video", methods=["POST"])
def analyze_video_endpoint():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400
   
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({"error": "No video selected"}), 400
    
    # Get the challenge text
    challenge = request.form.get('challenge', '')
   
    # Generate a unique filename to prevent collisions
    filename = str(uuid.uuid4()) + os.path.splitext(video_file.filename)[1]
    video_path = os.path.join(UPLOAD_FOLDER, filename)
   
    # Save the file temporarily
    video_file.save(video_path)
   
    try:
        # Analyze the video with challenge context
        analysis_result = analyze_video(video_path, challenge)
       
        # Clean up the temporary file
        os.remove(video_path)
       
        return jsonify({"result": analysis_result})
    except Exception as e:
        # Clean up in case of error
        if os.path.exists(video_path):
            os.remove(video_path)
            print(e)
        return jsonify({"error": str(e)}), 500

@app.route("/about")
def about():
    return render_template("about.html")  

@app.route("/contact")
def contact():
    return render_template("contact.html")  


@app.route("/profiles")
def profiles():
    # Simply render the template, data will be loaded via API
    return render_template("profiles.html")

@app.route("/api/profiles")
def api_profiles():
    best_candidates = session.get("best_candidates", None)
    
    if best_candidates:
        data = best_candidates
        print('best_candidates used:', data)
    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM talenters")
        rows = cursor.fetchall()
        
        # Data will be handled by JavaScript
        data = rows
        print('Database query executed, rows:', len(rows))
    
    return jsonify(data)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json["message"]
        # Call your RAG function to get response and candidates
        response_text, best_candidates = query_rag(user_message, 0.5)
        
        # Fetch candidates data if IDs are returned
        if best_candidates and len(best_candidates) > 0:
            format_strings = ','.join(['%s'] * len(best_candidates))
            query = f"SELECT * FROM talenters WHERE id IN ({format_strings})"
            cursor = db.cursor()
            cursor.execute(query, tuple(best_candidates))
            candidates_data = cursor.fetchall()
            # Store in session for later use
            session["best_candidates"] = candidates_data
        else:
            candidates_data = []
            session["best_candidates"] = None
            
        # Return both text response and candidates data
        return jsonify({
            "reply": response_text, 
            "best_candidates": candidates_data
        })
        
    except Exception as e:
        print("Error in chat endpoint:", str(e))
        return jsonify({
            "reply": "عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى.",
            "best_candidates": []
        }), 500

# Route for the development page
@app.route("/development")
def development():
    """صفحة التطوير مع المساعدين"""
    return render_template("development.html")

@app.route("/chat/career", methods=["POST"])
def chat_career():
    """Career development chatbot endpoint"""
    try:
        user_message = request.json["message"]
        
        # Process the career-related message
        response = ChatUtils.process_chat(user_message, context="career")
        
        # Fallback responses if API fails or for common keywords
        if not response or len(response) < 10:
            career_responses = {
                "مهارات": "لتطوير مهاراتك المهنية، أنصحك بالتركيز على التعلم المستمر والمشاركة في دورات تدريبية متخصصة. هل هناك مهارة محددة تريد التركيز عليها؟",
                "وظيفة": "للحصول على وظيفة أفضل، يجب تحديث سيرتك الذاتية وتطوير شبكة علاقاتك المهنية. هل تحتاج مساعدة في تحسين سيرتك الذاتية؟",
                "ترقية": "للحصول على ترقية، عليك إثبات قيمتك من خلال تحقيق نتائج ملموسة وحل مشكلات حقيقية في عملك. هل تواجه تحديات معينة في هذا المجال؟",
                "سيرة ذاتية": "لإعداد سيرة ذاتية احترافية، ركز على إبراز إنجازاتك بدلًا من مجرد وصف مهامك. هل تحتاج نموذجًا للسيرة الذاتية؟",
                "مقابلة": "للنجاح في المقابلات الشخصية، عليك البحث عن الشركة وتحضير إجابات لأسئلة المقابلة الشائعة. هل تريد نصائح محددة للمقابلات؟"
            }
            
            response = "شكراً على تواصلك مع مساعد التطوير المهني. يمكنني مساعدتك في تطوير مهاراتك، تحسين سيرتك الذاتية، والتحضير للمقابلات. كيف يمكنني مساعدتك تحديداً؟"
            
            for keyword, reply in career_responses.items():
                if keyword in user_message:
                    response = reply
                    break
        
        return jsonify({"reply": response})
    except Exception as e:
        app.logger.error(f"Error in career chat: {str(e)}")
        return jsonify({"reply": "عذراً، حدث خطأ أثناء معالجة طلبك. هل يمكنك إعادة صياغة سؤالك؟"})

@app.route("/chat/health", methods=["POST"])
def chat_health():
    """Occupational health chatbot endpoint"""
    try:
        user_message = request.json["message"]
        
        # Process the health-related message
        response = ChatUtils.process_chat(user_message, context="health")
        
        # Fallback responses if API fails or for common keywords
        if not response or len(response) < 10:
            health_responses = {
                "إرهاق": "يبدو أنك تعاني من الإرهاق المهني. أنصحك بأخذ فترات راحة منتظمة وممارسة تمارين الاسترخاء. هل ترغب في معرفة تقنيات للتعامل مع الضغط؟",
                "ضغط": "إدارة الضغط النفسي مهمة جداً للصحة المهنية. جرب تقنيات التنفس العميق والتأمل، وحدد أولوياتك بشكل واضح. هل ترغب في معرفة المزيد من تقنيات إدارة الضغط؟",
                "توازن": "التوازن بين العمل والحياة ضروري لصحتك. حاول وضع حدود واضحة للعمل، وخصص وقتاً للاسترخاء والعائلة والهوايات. هل تواجه صعوبة في تحقيق هذا التوازن؟",
                "جلوس": "الجلوس لفترات طويلة يضر بصحتك. حاول الوقوف والتحرك كل 30 دقيقة، وتأكد من ضبط مكتبك بشكل مريح. هل ترغب في نصائح أكثر حول بيئة العمل المريحة؟",
                "نوم": "النوم الجيد أساسي للصحة المهنية. حاول النوم 7-8 ساعات يومياً، وتجنب الشاشات قبل النوم بساعة على الأقل. هل تواجه مشكلات في النوم؟"
            }
            
            response = "شكراً على تواصلك مع مساعد الصحة المهنية. يمكنني مساعدتك في تحسين صحتك النفسية والجسدية في بيئة العمل. كيف يمكنني مساعدتك تحديداً؟"
            
            for keyword, reply in health_responses.items():
                if keyword in user_message:
                    response = reply
                    break
        
        return jsonify({"reply": response})
    except Exception as e:
        app.logger.error(f"Error in health chat: {str(e)}")
        return jsonify({"reply": "عذراً، واجهنا مشكلة في الاستجابة لاستفسارك. هل يمكنك المحاولة مرة أخرى؟"})



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



if __name__ == "__main__":
    app.run(debug=True , port=5001)