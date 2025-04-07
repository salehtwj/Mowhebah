import os
import pandas as pd
import markdown
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import LLMChain

# # إعداد البيانات
# data = {
#     "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#     "الاسم": ["أحمد سعود", "خالد فيصل", "علي ناصر", "نواف محمد", "سلطان عبد الله", 
#               "فهد إبراهيم", "ماجد يوسف", "ياسر خالد", "راكان عبد الرحمن", "عبد الله فهد"],
#     "العمر": [23, 22, 21, 20, 19, 18, 17, 16, 15, 14],
#     "الجنسية": ["السعودية"] * 10,
#     "المجال الرياضي": ["كرة القدم", "كرة السلة", "ألعاب القوى", "كرة القدم", "السباحة", 
#                       "كرة اليد", "التايكوندو", "رفع الأثقال", "الجودو", "كرة القدم"],
#     "المركز/التخصص": ["مهاجم", "صانع ألعاب", "عدو 100م", "حارس مرمى", "سباحة حرة", 
#                       "جناح أيمن", "قتال فردي", "وزن 85 كجم", "وزن تحت 73 كجم", "مدافع"],
#     "المهارات": [
#         "التسديد، السرعة، التحكم بالكرة",
#         "المراوغة، التمرير الدقيق، الرؤية الميدانية",
#         "السرعة، الانطلاقة، القدرة على التحمل",
#         "رد الفعل السريع، التمركز الجيد، التحكم بالكرة",
#         "القوة البدنية، التنفس الطويل، التحكم بالحركة",
#         "الدقة في التمرير، الرؤية التكتيكية، الدفاع الجيد",
#         "التركيز، المرونة، الدقة في الضربات",
#         "القوة، التحمل، الثبات",
#         "التكنيك العالي، السرعة، المرونة",
#         "التمركز الدفاعي، قطع الكرات، اللعب الجماعي"
#     ],
#     "تقييم الذكاء الاصطناعي (%)": [85, 90, 88, 75, 92, 83, 78, 94, 86, 89],
#     "الطول (سم)": [170, 169, 168, 167, 166, 165, 164, 163, 162, 161],
#     "رقم الجوال": ["0501111111", "0502222222", "0503333333", "0504444444", "0505555555",
#                    "0506666666", "0507777777", "0508888888", "0509999999", "0501010101"],
#     "البريد الإلكتروني": ["ahmed@example.com", "khaled@example.com", "ali@example.com", "nawaf@example.com", "sultan@example.com",
#                         "fahad@example.com", "majed@example.com", "yasser@example.com", "rakan@example.com", "abdullah@example.com"]
# }

# df = pd.DataFrame(data)

# # إنشاء `LangChain` RAG
directory = 'markdown'
os.makedirs(directory, exist_ok=True)

# IDs = df['ID']
# information = df.drop(columns=['ID'])

# # # حفظ البيانات في ملفات Markdown
# for i in range(len(df)):
#     id = IDs.iloc[i]
#     info = information.iloc[i]
#     markdown_text = f'# {id} \n'
#     for col, value in zip(information.columns, info):
#         markdown_text += f'{col}: {value} \n\n'

#     with open(f'{directory}/data_{i}.md', 'w', encoding='utf-8') as file:
#         file.write(markdown_text)

# # تحويل ملفات Markdown إلى HTML
marked_text = []
for filename in os.listdir(directory):
    if filename.endswith('.md'):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            temp = file.read()
            html_text = markdown.markdown(temp)
            marked_text.append((html_text, filename))

# تقسيم النصوص إلى أجزاء
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30)
docs = []
for text, filename in marked_text:
    doc_parts = text_splitter.create_documents([text])
    for doc in doc_parts:
        doc.metadata = {"source": filename}  # حفظ اسم الملف كمعرف
        docs.append(doc)

# تكوين الـ Embedding
embeddings = HuggingFaceEmbeddings(model_name="Omartificial-Intelligence-Space/GATE-AraBert-v0")

# استخدام FAISS
arabic_VDB = FAISS.from_documents(docs, embeddings)

prompt = """
# Role
You are a professional expert in discovering and evaluating athletic talents.

# Instructions
- Respond **in Arabic only**.
- **Do not deviate** from the given context or query.
- Provide a **comprehensive analysis** of the talented individuals.
- **Compare** the talents based on their skills, potential, and suitability for different sports or roles.
- Offer **practical recommendations** and insights to guide the user in decision-making.

# Context
{context}

# Query
{query}
"""

arabic_prompt = PromptTemplate(template=prompt, input_variables=["context", "query"])

key_API = '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'
LLM = ChatGroq(temperature=0, groq_api_key=key_API, model_name="llama3-70b-8192")
model = LLMChain(llm=LLM, prompt=arabic_prompt, verbose=True)

# دالة الاستعلام
import re

def query_rag(query: str, thr: float):
    results = arabic_VDB.similarity_search_with_score(query, k=6)

    best_candidates = []
    context_texts = []

    for doc, score in results:
        if score > thr:
            context_texts.append(doc.page_content)
            source_file = doc.metadata.get("source", "")
            match = re.search(r'data_(\d+)\.md', source_file)
            print(match)
            if match:
                best_candidates.append(int(match.group(1)) + 1)

    context_text = "\n\n".join(context_texts)
    rag_response = model.invoke({"context": context_text, "query": query})

    print(type(best_candidates))

    return rag_response["text"], best_candidates
