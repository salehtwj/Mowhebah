document.addEventListener("DOMContentLoaded", function () {
    const postContainer = document.getElementById("post-container");
    const postForm = document.getElementById("post-form");
    const postText = document.getElementById("post-text");
    const postFile = document.getElementById("post-file");
    const postTypeSelect = document.getElementById("post-type");

    const fakeUsers = [
        "أحمد خالد", "محمد العتيبي", "فاطمة الزهراني", "سارة الدوسري", "عبد الله السبيعي",
        "نورة الشمري", "خالد المطيري", "ياسمين الحربي", "فيصل الشهراني", "ريم القحطاني"
    ];

    // const fakePosts = [
    //     { type: "regular", name: "أحمد خالد", text: "🎉 مرحبًا بالجميع! أنا متحمس لمشاركة إنجازي الجديد اليوم.", image: "", time: "2025-04-08 10:30" },
    //     { type: "regular", name: "محمد العتيبي", text: "💪 استمروا في التدريب والعمل الجاد لتحقيق أهدافكم!", image: "https://source.unsplash.com/600x400/?training", time: "2025-04-07 15:45" },
    //     { type: "challenge", name: "سارة الدوسري", text: "تحدي اليوم: هل يُمكنك ركل الكرة لتسجيل هدف جميل؟ شاركوا فيديوهاتكم! ⚽🥅", image: "https://source.unsplash.com/600x400/?soccer", time: "2025-04-06 09:15" },
    //     { type: "regular", name: "فاطمة الزهراني", text: "🔥 شاهدوا هذا الفيديو التحفيزي لموهبة رائعة في كرة القدم!", video: "https://www.w3schools.com/html/mov_bbb.mp4", time: "2025-04-05 14:20" },
    //     { type: "challenge", name: "سارة الدوسري", text: "تحدي جديد: من يستطيع المراوغة بأفضل طريقة؟ أرونا مهاراتكم! 🎯", image: "https://source.unsplash.com/600x400/?football", time: "2025-04-04 11:10" }
    // ];

    const fakePosts = [
        {
            type: "regular",
            name: "زياد",
            text: "🔥 هذا الفيديو يوضح كيف يمكن للتحفيز والمثابرة أن تصنع منك بطلاً في التنس. شاهدوا كيف قلب اللاعب النتيجة لصالحه!",
            video: "https://youtube/hkHnqrDZPpI?si=eXxcrAQU4LKTffj7",
            time: "2025-04-09 10:00"
        },
        {
            type: "challenge",
            name: "جود ",
            text: "تحدي اليوم: هل يُمكنك ركل الكرة لتسجيل هدف جميل؟ شاركوا فيديوهاتكم! ⚽🥅",
            video: "",
            time: "2025-04-08 17:25"
        },
        {
            type: "regular",
            name: "عبدالرحمن ",
            text: "⚽ شاهدوا هذا الهدف الأسطوري من منتصف الملعب! الإبداع ممكن لما تثق في مهاراتك وتغامر!",
            video: "https://www.youtube.com/watch?v=MF2Qp0HG0ow",
            time: "2025-04-08 13:15"
        },
        {
            type: "challenge",
            name: "نورة ",
            text: "💪 تحدي القوة والتحمل! شاهدوا هذا التمرين المكثف وجربوا مثله. مين يقدر يكمله للنهاية؟",
            video: "https://www.youtube.com/watch?v=S7X8NDyR7i0",
            time: "2025-04-07 19:00"
        },
        {
            type: "regular",
            name: "فيصل ",
            text: "لقطات مذهلة للاعبين وهم يسجلون من زوايا مستحيلة! هذا هو الإبداع الرياضي الحقيقي!",
            video: "https://www.youtube.com/watch?v=29vmcEnAWTI",
            time: "2025-04-07 11:40"
        }
    ];
    
    fakePosts.forEach(post => {
        addPost(post.type, post.text, post.image || post.video, post.name, post.time);
    });

    postForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const text = postText.value.trim();
        const file = postFile.files[0];
        const postType = postTypeSelect.value;

        if (!text && !file) {
            alert("يرجى إدخال نص أو رفع ملف!");
            return;
        }

        let mediaSrc = "";
        if (file) {
            mediaSrc = URL.createObjectURL(file);
        }

        const now = new Date();
        const time = now.toLocaleString("ar-SA", { hour12: false });

        const username = postType === "challenge" ? "صالح التويجري" : fakeUsers[Math.floor(Math.random() * fakeUsers.length)];
        
        addPost(postType, text, mediaSrc, username, time);

        postForm.reset();
        $("#postModal").modal("hide");
    });

    // Function to analyze the video with challenge context
    function analyzeVideo(videoFile, challengeText) {
        const formData = new FormData();
        formData.append('video', videoFile);
        formData.append('challenge', challengeText);
        
        return fetch('/analyze_video', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
    }

    // Enhanced function to show the analysis result in a popup with chart
    function showAnalysisPopup(result) {
        // Parse the result if it's a string
        let data;
        
        try {
            // Handle if result is already a parsed object or still a string
            if (typeof result === 'string') {
                data = JSON.parse(result);
            } else {
                data = result;
            }
        } catch (error) {
            // If parsing fails, treat as raw text
            data = { rating: 0, description: result };
        }
        
        // Create the modal backdrop
        const modalBackdrop = document.createElement('div');
        modalBackdrop.classList.add('modal-backdrop', 'fade', 'show');
        modalBackdrop.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        document.body.appendChild(modalBackdrop);
        
        // Create the modal HTML with chart container
        const modalHTML = `
            <div class="modal fade show" style="display: block;" tabindex="-1" role="dialog" dir="rtl">
                <div class="modal-dialog" role="document">
                    <div class="modal-content" style="background-color: #f8f9fa; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                        <div class="modal-header" style="border-bottom: none; padding: 15px 20px;">
                            <h5 class="modal-title" style="color: #8900ce; font-weight: bold;">نتيجة تحليل التحدي</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close" style="font-size: 24px; color: #8900ce;">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body text-center" style="padding: 20px;">
                            <div class="chart-container my-3" style="position: relative; height:220px; width:100%">
                                <canvas id="analysisChart"></canvas>
                            </div>
                            <div class="result-value text-center my-2" style="font-size: 24px; font-weight: bold;">
                                ${data.rating}%
                            </div>
                            <div class="result-description mt-3 p-3" style="color: #333; font-size: 16px; text-align: center;">
                                ${data.description || 'لا يوجد وصف متاح'}
                            </div>
                        </div>
                        <div class="modal-footer" style="border-top: none; justify-content: center; padding-bottom: 20px;">
                            <button type="button" class="btn" data-dismiss="modal" style="background-color: #6c757d; color: white; min-width: 80px; border-radius: 5px;">إغلاق</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add the modal to the DOM
        const modalContainer = document.createElement('div');
        modalContainer.innerHTML = modalHTML;
        document.body.appendChild(modalContainer);
        
        // Add event listeners to close buttons
        const closeButtons = modalContainer.querySelectorAll('[data-dismiss="modal"]');
        closeButtons.forEach(button => {
            button.addEventListener('click', () => {
                document.body.removeChild(modalContainer);
                document.body.removeChild(modalBackdrop);
            });
        });
        
        // Also close on backdrop click
        modalBackdrop.addEventListener('click', () => {
            document.body.removeChild(modalContainer);
            document.body.removeChild(modalBackdrop);
        });

        // Create the chart after the modal is added to the DOM
        setTimeout(() => {
            const ctx = document.getElementById('analysisChart').getContext('2d');
            
            // Create a gauge chart
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [data.rating, 100 - data.rating],
                        backgroundColor: [
                            // Use a more vibrant purple color similar to your screenshot
                            '#8900ce', 
                            '#e0e0e0'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    cutout: '75%',
                    rotation: -90,
                    circumference: 180,
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            enabled: false
                        }
                    },
                    animation: {
                        animateRotate: true,
                        animateScale: true,
                        duration: 1200
                    }
                },
                plugins: [{
                    id: 'centerText',
                    afterDraw: function(chart) {
                        // No text drawn in the center by the plugin
                        // We'll use a separate div for this as seen in your screenshot
                    }
                }]
            });
        }, 100); // Short delay to ensure DOM elements are ready
    }

    function addPost(type, text, media, username, time) {
        const post = document.createElement("div");
        post.classList.add("card", "card-body", "mb-3");
        
        if (type === "challenge") {
            post.classList.add("challenge-post");
        }

        let mediaHTML = "";
    if (media) {
        if (media.includes("youtube.com/watch?v=")) {
            // Extract YouTube video ID
            const videoId = media.split("v=")[1].split("&")[0];
            mediaHTML = `<iframe width="100%" height="315" src="https://www.youtube.com/embed/${videoId}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
        } else if (typeof media === "string" && media.endsWith(".mp4")) {
            mediaHTML = `<video controls src="${media}" class="w-100 mt-2"></video>`;
        } else {
            mediaHTML = `<img src="${media}" class="w-100 mt-2" alt="" />`;
        }
    }

        let responseButtonHTML = "";
        if (type === "challenge") {
            responseButtonHTML = `
                <div class="mt-3">
                    <button class="btn btn-primary response-btn" style="background-color: #8900ce; border-color: #8900ce;">
                        <i class="fas fa-upload"></i> رفع فيديو للتحدي
                    </button>
                    <input type="file" class="d-none challenge-response" accept="video/*">
                </div>
                <div class="challenge-responses mt-3"></div>
            `;
        }

        post.innerHTML = `
            <div class="row">
                <div class="col-md-2">
                    <img class="rounded-circle d-none d-md-block" src="https://www.gravatar.com/avatar/anything?s=200&d=mm" alt="صورة المستخدم"/>
                    <p class="text-center">${username}</p>
                    <p class="text-muted text-center" style="font-size: 12px;">${time}</p>
                </div>
                <div class="col-md-10">
                    ${type === "challenge" ? '<span class="badge badge-warning mb-2" style="background-color: #8900ce;">تحدي</span>' : ''}
                    <p class="lead">${text}</p>
                    ${mediaHTML}
                    ${responseButtonHTML}
                </div>
            </div>
        `;

        const responseBtn = post.querySelector(".response-btn");
        if (responseBtn) {
            responseBtn.addEventListener("click", function() {
                const fileInput = this.nextElementSibling;
                fileInput.click();
            });
            
            const fileInput = post.querySelector(".challenge-response");
            fileInput.addEventListener("change", function() {
                if (this.files.length > 0) {
                    const file = this.files[0];
                    const videoURL = URL.createObjectURL(file);
                    
                    // Get the challenge text from the post
                    const challengeText = post.querySelector(".lead").textContent;
                    
                    // First add the response to the UI
                    const responseContainer = post.querySelector(".challenge-responses");
                    const response = document.createElement("div");
                    response.classList.add("challenge-response-item", "mt-3", "p-3", "border", "rounded");
                    
                    const randomUser = fakeUsers[Math.floor(Math.random() * fakeUsers.length)];
                    const now = new Date();
                    const responseTime = now.toLocaleString("ar-SA", { hour12: false });
                    
                    response.innerHTML = `
                        <div class="d-flex align-items-center mb-2">
                            <img class="rounded-circle mr-2" src="https://www.gravatar.com/avatar/anything?s=50&d=mm" style="width: 30px; height: 30px;" alt="صورة المستخدم" />
                            <span class="font-weight-bold">${randomUser}</span>
                            <small class="text-muted mr-2">${responseTime}</small>
                        </div>
                        <video controls src="${videoURL}" class="w-100"></video>
                        <div class="analysis-status mt-2 text-center">
                            <div class="spinner-border" style="color: #8900ce;" role="status">
                                <span class="sr-only">جاري التحليل...</span>
                            </div>
                            <p>جاري تحليل الفيديو...</p>
                        </div>
                    `;
                    
                    responseContainer.appendChild(response);
                    
                    // Then analyze the video with challenge context
                    analyzeVideo(file, challengeText)
                        .then(data => {
                            // Update the status indicator
                            const analysisStatus = response.querySelector('.analysis-status');
                            if (analysisStatus) {
                                analysisStatus.innerHTML = `
                                    <p class="text-success">تم التحليل بنجاح ✓</p>
                                    <button class="btn btn-sm mt-2" style="background-color: #8900ce; color: white; border-radius: 5px;">
                                        <i class="fas fa-chart-bar"></i> عرض النتيجة
                                    </button>
                                `;

                                // Add event listener to the "View Result" button
                                const viewResultBtn = analysisStatus.querySelector('button');
                                viewResultBtn.addEventListener('click', () => {
                                    showAnalysisPopup(data.result);
                                });
                            }
                            
                            // Show the analysis result immediately
                            if (data.result) {
                                showAnalysisPopup(data.result);
                            } else if (data.error) {
                                showAnalysisPopup({ rating: 0, description: "خطأ في تحليل الفيديو: " + data.error });
                            }
                        })
                        .catch(error => {
                            console.error("Error analyzing video:", error);
                            
                            // Update the status indicator
                            const analysisStatus = response.querySelector('.analysis-status');
                            if (analysisStatus) {
                                analysisStatus.innerHTML = '<p class="text-danger">حدث خطأ أثناء تحليل الفيديو</p>';
                            }
                            
                            showAnalysisPopup({ rating: 0, description: "حدث خطأ أثناء تحليل الفيديو" });
                        });
                }
            });
        }

        postContainer.prepend(post);
    }
});