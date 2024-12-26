function processFormData() {
    const nameElement = document.getElementById("username");
    const emailElement = document.getElementById("useremail");
    const feedbackElement = document.getElementById("feedback");

    const name = nameElement.value;
    const email = emailElement.value;
    const feedback = feedbackElement.value;

    if (!name || !email || !feedback) {
        alert("請填寫所有欄位!");
        return;
    }

    addComment(name, email, feedback);

    alert( name + "發布成功 ");

    nameElement.value = '';
    emailElement.value = '';
    feedbackElement.value = '';
}
function addComment(name, email, feedback, parentReplyList = null) {
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
            <button class="submit-reply-btn">提交回覆</button>
            <button class="cancel-reply-btn">取消</button>
            
            <form action="/upload" method="post" enctype="multipart/form-data">
              <!-- 上傳按鈕 -->
              <!--<label for="fileInput"></label>-->
              <input type="file" id="fileInput" name="image" accept="image/*">
              <!-- 提交按鈕 -->
              <button type="upload">上傳</button>
            </form>
        </div>
    `;

    // 監聽提交按鈕
    replyForm.querySelector(".submit-reply-btn").addEventListener("click", () => {
        const replyText = replyForm.querySelector(".reply-text").value.trim();
        if (replyText) {
            const replyList = parentComment.querySelector(".reply-list");
            addComment("用戶", "noreply@example.com", replyText, replyList);
            replyForm.remove();
        } else {
            alert("請輸入回覆內容!");
        }
    });

    // 監聽取消按鈕
    replyForm.querySelector(".cancel-reply-btn").addEventListener("click", () => {
        replyForm.remove();
    });

    parentComment.querySelector(".comment-box").appendChild(replyForm);
}