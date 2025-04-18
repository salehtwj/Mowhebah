document.addEventListener("DOMContentLoaded", () => {
    // Chatbot elements
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const closeBtn = document.querySelector(".close-btn");
    const chatbox = document.querySelector(".chatbox");
    const chatInput = document.querySelector(".chat-input textarea");
    const sendChatBtn = document.querySelector("#send-btn");
    const body = document.body;

    let userMessage = "";
    const API_URL = "/chat"; // Changed to relative path for better flexibility

    // Initialize the page
    initializeChatbot();
    loadProfilesData();

    function initializeChatbot() {
        // Add event listeners for the chatbot
        chatInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleChat();
            }
        });

        sendChatBtn.addEventListener("click", handleChat);
        closeBtn.addEventListener("click", () => body.classList.remove("show-chatbot"));
        chatbotToggler.addEventListener("click", () => {
            body.classList.toggle("show-chatbot");
            body.classList.toggle("chatbot-open");
        });

        console.log("✅ تم تهيئة المحادثة الآلية بنجاح");
    }

    function createChatLi(message, className) {
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat", className);
        let chatContent = className === "outgoing" 
            ? `<p></p>` 
            : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
        chatLi.innerHTML = chatContent;
        chatLi.querySelector("p").textContent = message;
        return chatLi;
    }

    function handleChat() {
        userMessage = chatInput.value.trim();
        if (!userMessage) return;
        
        // Clear input field
        chatInput.value = "";
        
        // Add outgoing message to chatbox
        chatbox.appendChild(createChatLi(userMessage, "outgoing"));
        chatbox.scrollTop = chatbox.scrollHeight;

        // Show "typing" indication
        setTimeout(() => {
            const incomingChatLi = createChatLi("...", "incoming");
            chatbox.appendChild(incomingChatLi);
            chatbox.scrollTop = chatbox.scrollHeight;
            generateResponse(incomingChatLi);
        }, 600);
    }

    function generateResponse(typingElement) {
        fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Remove the typing indicator
            if (typingElement) {
                typingElement.remove();
            }
            
            // Add the bot's response
            const botResponse = data.reply;
            chatbox.appendChild(createChatLi(botResponse, "incoming"));
            chatbox.scrollTop = chatbox.scrollHeight;

            // Check for candidate data and update if available
            if (data.best_candidates && Array.isArray(data.best_candidates) && data.best_candidates.length > 0) {
                console.log("🔄 تحديث قائمة المرشحين من المحادثة...");
                processAndDisplayCandidates(data.best_candidates);
            } else {
                console.log("❌ لا يوجد مرشحون متاحون من المحادثة.");
            }
        })
        .catch(error => {
            // Remove the typing indicator
            if (typingElement) {
                typingElement.remove();
            }
            
            // Show error message
            console.error("❌ خطأ في المحادثة:", error);
            chatbox.appendChild(createChatLi("عذراً، حدث خطأ في المعالجة. يرجى المحاولة مرة أخرى.", "incoming"));
            chatbox.scrollTop = chatbox.scrollHeight;
        });
    }

    function loadProfilesData() {
        console.log("📢 جاري تحميل بيانات المرشحين...");
        
        fetch("/api/profiles")
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("📢 البيانات المسترجعة:", data);
                
                if (data && Array.isArray(data) && data.length > 0) {
                    processAndDisplayCandidates(data);
                } else {
                    document.getElementById("profiles-container").innerHTML = `
                        <div class="text-center text-muted p-5">
                            <h4>❌ لا يوجد مرشحون متاحون حاليًا</h4>
                            <p>يرجى استخدام المحادثة الآلية لتحديد احتياجاتك والعثور على المرشحين المناسبين</p>
                        </div>`;
                }
            })
            .catch(error => {
                console.error("❌ خطأ في جلب البيانات:", error);
                document.getElementById("profiles-container").innerHTML = `
                    <div class="text-center text-danger p-5">
                        <h4>❌ حدث خطأ في تحميل البيانات</h4>
                        <p>يرجى المحاولة مرة أخرى لاحقًا</p>
                    </div>`;
            });
    }

    // JavaScript
function processAndDisplayCandidates(candidates) {
    const processedCandidates = candidates.map(candidate => {
        if (Array.isArray(candidate)) {
            return {
                id: candidate[0],
                name: candidate[1],
                age: candidate[2],
                country: candidate[3],
                field: candidate[4],
                position: candidate[5],
                skills: candidate[6],
                ai_rating: candidate[7],
                height: candidate[8],
                phone: candidate[9],
                email: candidate[10]
            };
        }
        return candidate;
    });

    console.log("🔄 المرشحون بعد المعالجة:", processedCandidates);
    displayBestCandidates(processedCandidates);
}

function displayBestCandidates(candidates) {
    const container = document.getElementById("profiles-container");
    container.innerHTML = "";

    if (!candidates || candidates.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted p-5">
                <h4>❌ لا يوجد مرشحون متاحون حاليًا</h4>
                <p>يرجى استخدام المحادثة الآلية لتحديد احتياجاتك والعثور على المرشحين المناسبين</p>
            </div>`;
        return;
    }

    candidates.forEach(candidate => {
        console.log("🧪 معالجة المرشح:", candidate);

        let skillsList = '<li class="list-group-item">لا توجد مهارات مسجلة</li>';
        if (candidate.skills) {
            const skills = candidate.skills.split(/[,،]/).filter(skill => skill.trim() !== '');
            if (skills.length > 0) {
                skillsList = skills.map(skill => 
                    `<li class="list-group-item"><i class="fa fa-check pr-1"></i>${skill.trim()}</li>`
                ).join("");
            }
        }

        const candidateCard = document.createElement("div");
        candidateCard.classList.add("card", "card-body", "bg-light", "mb-3");
        candidateCard.innerHTML = `
            <div class="row">
                <div class="col-2">
                    <img class="rounded-circle" src="https://www.gravatar.com/avatar/anything?s=200&d=mm" alt="" />
                </div>
                <div class="col-lg-6 col-md-4 col-8">
                    <h3>${candidate.name || 'بدون اسم'}</h3>
                    <p>${candidate.position || 'غير محدد'}</p>
                    <p>تقييم الذكاء الاصطناعي: %${candidate.ai_rating || '0'}</p>
                    <p>العمر: ${candidate.age || 'غير محدد'}</p>
                    <a href="/profile?id=${candidate.id}" class="btn btn-info">عرض الملف</a>
                </div>
                <div class="col-md-4 d-none d-lg-block">
                    <h4>المهارات</h4>
                    <ul class="list-group">
                        ${skillsList}
                    </ul>
                </div>
            </div>
        `;

        container.appendChild(candidateCard);
    });

    console.log("✅ تم تحديث قائمة المرشحين بنجاح!");
}

});