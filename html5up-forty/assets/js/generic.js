function processFormData() {
    const nameElement = document.getElementById("username");
    const emailElement = document.getElementById("useremail");
    const feedbackElement = document.getElementById("feedback");
    const fileInput = document.getElementById("fileInput");

    const name = nameElement.value;
    const email = emailElement.value;
    const feedback = feedbackElement.value;

    if (!name || !email || !feedback) {
        // alert("請填寫所有欄位!");
        return;
    }

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const imageUrl = e.target.result; // 獲取圖片的 Base64 URL
            addComment(name, email, feedback, null, imageUrl);
            // alert(name + " 發布成功!");
        };
        reader.readAsDataURL(fileInput.files[0]); // 讀取圖片檔案
    } else {
        addComment(name, email, feedback);
        // alert(name + " 發布成功!");
    }

    nameElement.value = '';
    emailElement.value = '';
    feedbackElement.value = '';
    fileInput.value = ''; // 清空上傳檔案
}

function addComment(name, email, feedback, parentReplyList = null, imageUrl = null) {
    const commentsList = parentReplyList || document.getElementById("comments-list");

    const newComment = document.createElement("li");
    newComment.innerHTML = `
        <div class="comment-main-level">
            <div class="comment-avatar">
                <img src="https://via.placeholder.com/50" alt="Avatar">
            </div>
            <div class="comment-box">
                <div class="comment-head">
                    <h6 class="comment-name by-author"><a href="#">${name}</a></h6>
                    <span>${new Date().toLocaleString()}</span>
                    <i class="fa fa-reply"></i>
                    <i class="fa fa-heart"></i>
                </div>
                <div class="comment-content">
                    ${feedback}
                    ${imageUrl ? `<img src="${imageUrl}" alt="Uploaded Image" style="max-width: 200px; margin-top: 10px;">` : ''}
                </div>
                <div class="comment-actions">
                    <button class="reply-btn">回覆</button>
                    <button class="delete-btn">刪除</button>
                </div>
                <ul class="reply-list"></ul>
            </div>
        </div>
    `;

    // 監聽刪除按鈕
    const deleteBtn = newComment.querySelector(".delete-btn");
    deleteBtn.addEventListener("click", () => {
        commentsList.removeChild(newComment);
    });

    // 監聽回覆按鈕
    const replyBtn = newComment.querySelector(".reply-btn");
    replyBtn.addEventListener("click", () => showReplyForm(newComment));

    commentsList.appendChild(newComment);
}


function showReplyForm(parentComment) {
    // 檢查是否已經存在回覆表單
    if (parentComment.querySelector(".reply-form")) return;

    const replyForm = document.createElement("div");
    replyForm.classList.add("reply-form");
    replyForm.innerHTML = `
        <textarea class="reply-text" placeholder="輸入回覆內容..."></textarea>
        <div class="comment-actions">
            <input type="file" class="reply-file-input" accept="image/*">
            <button class="submit-reply-btn">提交回覆</button>
            <button class="cancel-reply-btn">取消</button>
        </div>
    `;

    // 監聽提交按鈕
    replyForm.querySelector(".submit-reply-btn").addEventListener("click", () => {
        const replyText = replyForm.querySelector(".reply-text").value.trim();
        const replyFileInput = replyForm.querySelector(".reply-file-input");
        if (!replyText) {
            // alert("請輸入回覆內容!");
            return;
        }

        if (replyFileInput.files && replyFileInput.files[0]) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const imageUrl = e.target.result; // 獲取圖片的 Base64 URL
                const replyList = parentComment.querySelector(".reply-list");
                addComment("用戶", "noreply@example.com", replyText, replyList, imageUrl);
                replyForm.remove();
            };
            reader.readAsDataURL(replyFileInput.files[0]); // 讀取圖片檔案
        } else {
            const replyList = parentComment.querySelector(".reply-list");
            addComment("用戶", "noreply@example.com", replyText, replyList);
            replyForm.remove();
        }
    });

    // 監聽取消按鈕
    replyForm.querySelector(".cancel-reply-btn").addEventListener("click", () => {
        replyForm.remove();
    });

    parentComment.querySelector(".comment-box").appendChild(replyForm);
}
