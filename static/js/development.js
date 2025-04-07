document.addEventListener("DOMContentLoaded", () => {
    // Career Chatbot Elements
    const careerChatbotToggler = document.querySelector(".career-chatbot-toggler");
    const careerCloseBtn = document.querySelector(".career-close-btn");
    const careerChatbox = document.querySelector(".career-chatbox");
    const careerInput = document.querySelector(".career-input");
    const careerSendBtn = document.getElementById("career-send-btn");
    const openCareerBtn = document.getElementById("open-career-chat");

    // Health Chatbot Elements
    const healthChatbotToggler = document.querySelector(".health-chatbot-toggler");
    const healthCloseBtn = document.querySelector(".health-close-btn");
    const healthChatbox = document.querySelector(".health-chatbox");
    const healthInput = document.querySelector(".health-input");
    const healthSendBtn = document.getElementById("health-send-btn");
    const openHealthBtn = document.getElementById("open-health-chat");

    // API URLs
    const CAREER_API_URL = "/chat/career";
    const HEALTH_API_URL = "/chat/health";

    // Create a chat message element
    const createChatLi = (message, className) => {
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat", className);
        let chatContent = className === "outgoing" 
            ? `<p></p>` 
            : className === "incoming-career" 
              ? `<span class="material-symbols-outlined">work</span><p></p>` 
              : `<span class="material-symbols-outlined">health_and_safety</span><p></p>`;
        chatLi.innerHTML = chatContent;
        chatLi.querySelector("p").textContent = message;
        return chatLi;
    };

    // Generate response from Career Chatbot
    const generateCareerResponse = (userMessage) => {
        fetch(CAREER_API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.reply;
            careerChatbox.querySelector("li:last-child").remove(); // Remove loading dots
            careerChatbox.appendChild(createChatLi(botResponse, "incoming-career"));
            careerChatbox.scrollTop = careerChatbox.scrollHeight;
        })
        .catch(error => {
            careerChatbox.querySelector("li:last-child").remove(); // Remove loading dots
            careerChatbox.appendChild(createChatLi("حدث خطأ. يرجى المحاولة مرة أخرى.", "incoming-career"));
            console.error("❌ خطأ في جلب البيانات:", error);
        });
    };

    // Generate response from Health Chatbot
    const generateHealthResponse = (userMessage) => {
        fetch(HEALTH_API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.reply;
            healthChatbox.querySelector("li:last-child").remove(); // Remove loading dots
            healthChatbox.appendChild(createChatLi(botResponse, "incoming-health"));
            healthChatbox.scrollTop = healthChatbox.scrollHeight;
        })
        .catch(error => {
            healthChatbox.querySelector("li:last-child").remove(); // Remove loading dots
            healthChatbox.appendChild(createChatLi("حدث خطأ. يرجى المحاولة مرة أخرى.", "incoming-health"));
            console.error("❌ خطأ في جلب البيانات:", error);
        });
    };

    // Handle Career Chatbot messages
    const handleCareerChat = () => {
        const userMessage = careerInput.value.trim();
        if (!userMessage) return;
        careerInput.value = "";
        careerChatbox.appendChild(createChatLi(userMessage, "outgoing"));
        careerChatbox.scrollTop = careerChatbox.scrollHeight;

        setTimeout(() => {
            const incomingChatLi = createChatLi("...", "incoming-career");
            careerChatbox.appendChild(incomingChatLi);
            careerChatbox.scrollTop = careerChatbox.scrollHeight;
            generateCareerResponse(userMessage);
        }, 600);
    };

    // Handle Health Chatbot messages
    const handleHealthChat = () => {
        const userMessage = healthInput.value.trim();
        if (!userMessage) return;
        healthInput.value = "";
        healthChatbox.appendChild(createChatLi(userMessage, "outgoing"));
        healthChatbox.scrollTop = healthChatbox.scrollHeight;

        setTimeout(() => {
            const incomingChatLi = createChatLi("...", "incoming-health");
            healthChatbox.appendChild(incomingChatLi);
            healthChatbox.scrollTop = healthChatbox.scrollHeight;
            generateHealthResponse(userMessage);
        }, 600);
    };

    // Career Chatbot Event Listeners
    careerInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleCareerChat();
        }
    });

    careerSendBtn.addEventListener("click", handleCareerChat);
    careerCloseBtn.addEventListener("click", () => document.body.classList.remove("show-career-chatbot"));
    careerChatbotToggler.addEventListener("click", () => {
        document.body.classList.remove("show-health-chatbot"); // Close health chatbot if open
        document.body.classList.toggle("show-career-chatbot");
    });

    openCareerBtn.addEventListener("click", () => {
        document.body.classList.remove("show-health-chatbot"); // Close health chatbot if open
        document.body.classList.add("show-career-chatbot");
    });

    // Health Chatbot Event Listeners
    healthInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleHealthChat();
        }
    });

    healthSendBtn.addEventListener("click", handleHealthChat);
    healthCloseBtn.addEventListener("click", () => document.body.classList.remove("show-health-chatbot"));
    healthChatbotToggler.addEventListener("click", () => {
        document.body.classList.remove("show-career-chatbot"); // Close career chatbot if open
        document.body.classList.toggle("show-health-chatbot");
    });

    openHealthBtn.addEventListener("click", () => {
        document.body.classList.remove("show-career-chatbot"); // Close career chatbot if open
        document.body.classList.add("show-health-chatbot");
    });
});