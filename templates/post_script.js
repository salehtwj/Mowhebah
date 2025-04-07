document.addEventListener("DOMContentLoaded", function () {
    const postContainer = document.getElementById("post-container");
    const postText = document.getElementById("post-text");
    const postFile = document.getElementById("post-file");
    const postBtn = document.getElementById("post-btn");

    // قائمة أسماء عشوائية للمنشورات
    const fakeUsers = [
        "أحمد خالد", "محمد العتيبي", "فاطمة الزهراني", "سارة الدوسري", "عبد الله السبيعي",
        "نورة الشمري", "خالد المطيري", "ياسمين الحربي", "فيصل الشهراني", "ريم القحطاني"
    ];

    // بيانات منشورات وهمية
    const fakePosts = [
        { text: "🎉 مرحبًا بالجميع! أنا متحمس لمشاركة إنجازي الجديد اليوم.", media: "" },
        { text: "📢 فرصة رائعة لجميع الرياضيين! انضموا إلى تحدي المهارات الجديد.", media: "media/image1.jpg" },
        { text: "💪 استمروا في التدريب والعمل الجاد لتحقيق أهدافكم!", media: "" },
        { text: "🔥 فيديو تحفيزي لموهبة رائعة في كرة القدم!", media: "media/video1.mp4" }
    ];

    // تحميل المنشورات الوهمية
    fakePosts.forEach(post => addPost(post.text, post.media));

    // إضافة منشور جديد عند الضغط على زر "نشر"
    postBtn.addEventListener("click", function () {
        const text = postText.value;
        const file = postFile.files[0];

        if (!text && !file) {
            alert("يرجى إدخال نص أو رفع ملف!");
            return;
        }

        let mediaSrc = "";
        if (file) {
            mediaSrc = URL.createObjectURL(file);
        }

        const randomUser = fakeUsers[Math.floor(Math.random() * fakeUsers.length)];
        addPost(text, mediaSrc, randomUser);

        // إعادة تعيين المدخلات
        postText.value = "";
        postFile.value = "";
    });

    // دالة لإضافة منشور جديد بنفس تصميم التعليقات
    function addPost(text, media, username = "مستخدم مجهول") {
        const post = document.createElement("div");
        post.classList.add("card", "card-body", "mb-3");

        post.innerHTML = `
            <div class="row">
                <div class="col-md-2">
                    <a href="profile.html">
                        <img class="rounded-circle d-none d-md-block" src="https://www.gravatar.com/avatar/anything?s=200&d=mm" alt="" />
                    </a>
                    <br />
                    <p class="text-center">${username}</p>
                </div>
                <div class="col-md-10">
                    <p class="lead">${text}</p>
                    ${media ? (media.endsWith(".mp4") ? `<video controls src="${media}" class="w-100 mt-2"></video>` : `<img src="${media}" class="w-100 mt-2" />`) : ""}
                </div>
            </div>
        `;

        postContainer.prepend(post);
    }
});
