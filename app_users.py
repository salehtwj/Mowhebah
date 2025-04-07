from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from langchain_rag import query_rag  
from chat_utils import ChatUtils
from video_analyzer import analyze_video 
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



# # did not test it needed to rewrite
# @app.route("/posts", methods=["GET", "POST"])
# def posts():
#     if request.method == "POST":
#         if 'video' not in request.files:
#             return render_template("post2.html", error="الرجاء رفع ملف الفيديو.")

#         video = request.files['video']
#         if video.filename == "":
#             return render_template("post2.html", error="لم يتم اختيار أي ملف.")

#         upload_folder = "static/uploads"
#         os.makedirs(upload_folder, exist_ok=True)
#         video_path = os.path.join(upload_folder, video.filename)
#         video.save(video_path)

#         try:
#             analysis_result = analyze_video(video_path)
#             return render_template("post2.html", analysis=analysis_result)
#         except Exception as e:
#             return render_template("post2.html", error=f"حدث خطأ أثناء تحليل الفيديو: {e}")

#     return render_template("post2.html")


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


if __name__ == "__main__":
    app.run(debug=True)