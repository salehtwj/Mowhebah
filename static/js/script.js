document.addEventListener("DOMContentLoaded", () => {
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const closeBtn = document.querySelector(".close-btn");
    const chatbox = document.querySelector(".chatbox");
    const chatInput = document.querySelector(".chat-input textarea");
    const sendChatBtn = document.querySelector("#send-btn");

    let userMessage = "";
    const API_URL = "http://127.0.0.1:5000/chat"; 

    const createChatLi = (message, className) => {
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat", className);
        let chatContent = className === "outgoing" 
            ? `<p></p>` 
            : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
        chatLi.innerHTML = chatContent;
        chatLi.querySelector("p").textContent = message;
        return chatLi;
    };

function displayBestCandidates(candidates) {
    const container = document.getElementById("profiles-container");

    // 🔥 حذف البيانات القديمة قبل عرض الجديدة
    container.innerHTML = "";

    candidates.forEach(candidate => {
        const candidateCard = document.createElement("div");
        candidateCard.classList.add("card", "card-body", "bg-light", "mb-3");
        candidateCard.innerHTML = `
            <div class="row">
                <div class="col-2">
                    <img class="rounded-circle" src="https://www.gravatar.com/avatar/anything?s=200&d=mm" alt="" />
                </div>
                <div class="col-lg-6 col-md-4 col-8">
                    <h3>${candidate.name}</h3>
                    <p>${candidate.position}</p>
                    <p>تقييم الذكاء الاصطناعي: %${candidate.ai_rating}</p>
                    <p>العمر: ${candidate.age}</p>
                    <a href="profile.html?id=${candidate.id}" class="btn btn-info">عرض الملف</a>
                </div>
                <div class="col-md-4 d-none d-lg-block">
                    <h4>المهارات</h4>
                    <ul class="list-group">
                        ${candidate.skills.split("،").map(skill => `<li class="list-group-item"><i class="fa fa-check pr-1"></i>${skill}</li>`).join("")}
                    </ul>
                </div>
            </div>
        `;

        container.appendChild(candidateCard);
    });

    console.log("✅ تم تحديث القائمة بنجاح!");
}


const generateResponse = () => {
    fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.reply;
        chatbox.appendChild(createChatLi(botResponse, "incoming"));
        chatbox.scrollTop = chatbox.scrollHeight;

        // ✅ التأكد من وجود best_candidates
        if (data.best_candidates && Array.isArray(data.best_candidates) && data.best_candidates.length > 0) {
            console.log("🔄 تحديث قائمة المرشحين...");
            displayBestCandidates(data.best_candidates);
        } else {
            console.log("❌ لا يوجد مرشحون متاحون.");
            document.getElementById("profiles-container").innerHTML = `<p class="text-center text-muted">❌ لا يوجد مرشحون متاحون.</p>`;
        }
    })
    .catch(error => {
        console.error("❌ خطأ في جلب البيانات:", error);
    });
};




    const handleChat = () => {
        userMessage = chatInput.value.trim();
        if (!userMessage) return;
        chatInput.value = "";
        chatbox.appendChild(createChatLi(userMessage, "outgoing"));
        chatbox.scrollTop = chatbox.scrollHeight;

        setTimeout(() => {
            const incomingChatLi = createChatLi("...", "incoming");
            chatbox.appendChild(incomingChatLi);
            chatbox.scrollTop = chatbox.scrollHeight;
            generateResponse();
        }, 600);
    };

    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleChat();
        }
    });

    sendChatBtn.addEventListener("click", handleChat);
    closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
    chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
});


document.addEventListener("DOMContentLoaded", function () {
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const chatbot = document.querySelector(".chatbot");
    const body = document.body;

    chatbotToggler.addEventListener("click", function () {
        body.classList.toggle("chatbot-open"); // إضافة أو إزالة كلاس عند فتح المحادثة
    });
    
    fetch("/profiles")
        .then(response => response.json())
        .then(data => {
            console.log("📢 البيانات المسترجعة:", data);  // ✅ طباعة البيانات في Console

            if (data.length > 0) {
                displayBestCandidates(data);
            } else {
                document.getElementById("profiles-container").innerHTML = `<p class="text-center text-muted">❌ لا يوجد مرشحون متاحون.</p>`;
            }
        })
        .catch(error => console.error("❌ خطأ في جلب البيانات:", error));
});



