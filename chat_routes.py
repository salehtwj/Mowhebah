# from flask import jsonify, request
# from chat_utils import ChatUtils

# def register_chat_routes(app):
#     """
#     Register chat-related routes with the Flask application
#     """
    
#     @app.route("/chat/career", methods=["POST"])
#     def chat_career():
#         """Career development chatbot endpoint"""
#         try:
#             user_message = request.json["message"]
            
#             # Process the career-related message
#             response = ChatUtils.process_chat(user_message, context="career")
            
#             # Fallback responses if API fails or for common keywords
#             if not response or len(response) < 10:
#                 career_responses = {
#                     "مهارات": "لتطوير مهاراتك المهنية، أنصحك بالتركيز على التعلم المستمر والمشاركة في دورات تدريبية متخصصة. هل هناك مهارة محددة تريد التركيز عليها؟",
#                     "وظيفة": "للحصول على وظيفة أفضل، يجب تحديث سيرتك الذاتية وتطوير شبكة علاقاتك المهنية. هل تحتاج مساعدة في تحسين سيرتك الذاتية؟",
#                     "ترقية": "للحصول على ترقية، عليك إثبات قيمتك من خلال تحقيق نتائج ملموسة وحل مشكلات حقيقية في عملك. هل تواجه تحديات معينة في هذا المجال؟",
#                     "سيرة ذاتية": "لإعداد سيرة ذاتية احترافية، ركز على إبراز إنجازاتك بدلًا من مجرد وصف مهامك. هل تحتاج نموذجًا للسيرة الذاتية؟",
#                     "مقابلة": "للنجاح في المقابلات الشخصية، عليك البحث عن الشركة وتحضير إجابات لأسئلة المقابلة الشائعة. هل تريد نصائح محددة للمقابلات؟"
#                 }
                
#                 response = "شكراً على تواصلك مع مساعد التطوير المهني. يمكنني مساعدتك في تطوير مهاراتك، تحسين سيرتك الذاتية، والتحضير للمقابلات. كيف يمكنني مساعدتك تحديداً؟"
                
#                 for keyword, reply in career_responses.items():
#                     if keyword in user_message:
#                         response = reply
#                         break
            
#             return jsonify({"reply": response})
#         except Exception as e:
#             app.logger.error(f"Error in career chat: {str(e)}")
#             return jsonify({"reply": "عذراً، حدث خطأ أثناء معالجة طلبك. هل يمكنك إعادة صياغة سؤالك؟"})

#     @app.route("/chat/health", methods=["POST"])
#     def chat_health():
#         """Occupational health chatbot endpoint"""
#         try:
#             user_message = request.json["message"]
            
#             # Process the health-related message
#             response = ChatUtils.process_chat(user_message, context="health")
            
#             # Fallback responses if API fails or for common keywords
#             if not response or len(response) < 10:
#                 health_responses = {
#                     "إرهاق": "يبدو أنك تعاني من الإرهاق المهني. أنصحك بأخذ فترات راحة منتظمة وممارسة تمارين الاسترخاء. هل ترغب في معرفة تقنيات للتعامل مع الضغط؟",
#                     "ضغط": "إدارة الضغط النفسي مهمة جداً للصحة المهنية. جرب تقنيات التنفس العميق والتأمل، وحدد أولوياتك بشكل واضح. هل ترغب في معرفة المزيد من تقنيات إدارة الضغط؟",
#                     "توازن": "التوازن بين العمل والحياة ضروري لصحتك. حاول وضع حدود واضحة للعمل، وخصص وقتاً للاسترخاء والعائلة والهوايات. هل تواجه صعوبة في تحقيق هذا التوازن؟",
#                     "جلوس": "الجلوس لفترات طويلة يضر بصحتك. حاول الوقوف والتحرك كل 30 دقيقة، وتأكد من ضبط مكتبك بشكل مريح. هل ترغب في نصائح أكثر حول بيئة العمل المريحة؟",
#                     "نوم": "النوم الجيد أساسي للصحة المهنية. حاول النوم 7-8 ساعات يومياً، وتجنب الشاشات قبل النوم بساعة على الأقل. هل تواجه مشكلات في النوم؟"
#                 }
                
#                 response = "شكراً على تواصلك مع مساعد الصحة المهنية. يمكنني مساعدتك في تحسين صحتك النفسية والجسدية في بيئة العمل. كيف يمكنني مساعدتك تحديداً؟"
                
#                 for keyword, reply in health_responses.items():
#                     if keyword in user_message:
#                         response = reply
#                         break
            
#             return jsonify({"reply": response})
#         except Exception as e:
#             app.logger.error(f"Error in health chat: {str(e)}")
#             return jsonify({"reply": "عذراً، واجهنا مشكلة في الاستجابة لاستفسارك. هل يمكنك المحاولة مرة أخرى؟"})