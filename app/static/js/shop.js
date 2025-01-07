
//Upload Image
document.addEventListener('DOMContentLoaded', async () => {
    await loadTopics();
    var filename = null;
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const fileInput = document.getElementById('fileInput');
            const responseMessage = document.getElementById('responseMessage');
            
            if (!fileInput.files.length) {
                responseMessage.textContent = "請選擇檔案上傳！";
                responseMessage.style.color = "red";
                return;
            }

            const formData = new FormData();
            formData.append('image', fileInput.files[0]);

            try {
                const response = await fetch('/upload_shop_image', {
                    method: 'POST',
                    body: formData,
                });

                const result = await response.json();

                if (result.status === "success") {
                    filename = result.filename;
                    responseMessage.textContent = result.message;
                    responseMessage.style.color = "green";
                } else {
                    responseMessage.textContent = result.message;
                    responseMessage.style.color = "red";
                }
            } catch (error) {
                responseMessage.textContent = "上傳失敗，請稍後再試！";
                responseMessage.style.color = "red";
                console.error("上傳過程中出現錯誤:", error);
            }
        });
    } else {
        console.error("表單未找到，請檢查 HTML 中的 ID 是否正確。");
    }

    // 檢查 submitBtn 是否存在
    if (submitBtn) {
        submitBtn.addEventListener('click', processFormData);
    } else {
        console.error("提交按鈕未找到，請檢查 HTML 中的 ID 是否正確。");
    }

    async function processFormData() {
        const topicTitleElement = document.getElementById("topic_title");
        const contentElement = document.getElementById("content");
    
        const topicTitle = topicTitleElement.value;
        const content = contentElement.value;
        var user_data = null;
        try {
            const response = await fetch(`/get_user_by_id`, {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                },
            });
        
            if (response.ok) {
                const user_data_result = await response.json();
                if (user_data_result.status === "success") {
                    if (user_data_result.user_data) {
                        user_data = user_data_result.user_data;
                    }
                } else {
                    console.error("Error when fetching user data:", user_data_result.message);
                }
            } else {
                console.error("HTTP error when fetching user data:", response.status);
            }
        } catch (err) {
            console.error("Error when fetching user data:", err);
        }
        const user_id = user_data ? user_data.id : null;
        const user_name = user_data ? user_data.cn : "Visitor";
    
        if (!topicTitle || !content) {
            alert("請填寫所有欄位!");
            return;
        }
    
        if (filename) {
            createTopicInDB(topicTitle, user_id, content, filename);
            // addTopic(topicTitle,user_name, content, filename);
        } else {
            createTopicInDB(topicTitle, user_id, content);
            // addTopic(topicTitle, user_name, content);
        }
    
        topicTitleElement.value = '';
        contentElement.value = '';
        fileInput.value = ''; // 清空上傳檔案
        filename = null;
    }
    
    async function createTopicInDB(topicTitle, user_id, content, filename = null) {
        var topic_data = null;
        try {
            const response = await fetch("/create_topic", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    topicTitle: topicTitle,
                    user_id: user_id,
                    content: content,
                    filename: filename,
                }),
            });
    
            const data = await response.json();
    
            if (data.status === "success") {
                topic_data = data.topic_data;
    
                console.log("Topic created in DB:\n", topic_data);
            } else {
                console.error("Error when creating topic in DB:", data.message);
            }
        } catch (error) {
            console.error("Error when creating topic in DB:", error);
        }
        const topic_id = topic_data ? topic_data.id : null;
        const user_name = topic_data ? topic_data.user_name : "Visitor";
        addTopic(topic_id, topicTitle,user_name, content, filename);
        createCommentInDB(content, topic_id, filename, 1);
    }

    async function createCommentInDB(content, topic_id, filename = null, comment_order = null, father_comment_id = null) {
        try {
            const response = await fetch("/create_comment", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    content: content,
                    topic_id: topic_id,
                    father_comment_id: father_comment_id,
                    comment_order: comment_order,
                    filename: filename,
                }),
            });
    
            const data = await response.json();
    
            if (data.status === "success") {
                console.log("Comment created in DB:", data.comment_data);
                filename = "";
            } else {
                console.error("Error when creating comment in DB:", data.message);
            }
        } catch (error) {
            console.error("Error when creating comment in DB:", error);
        }
    }
    
    
    
    async function addTopic(topic_id, topicTitle, user_name, content, filename = null) {
        const commentsList = document.getElementById("comments-list");
        const newComment = document.createElement("li");
        var topic_data = null;

        try {
            const response = await fetch(`/get_topic_by_id?topic_id=${encodeURIComponent(topic_id)}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });
        
            const data = await response.json();
        
            if (data.status === "success") {
                topic_data = data.topic_data;
            } else {
                console.error("Error: ", data.message);
            }
        } catch (error) {
            console.error("Error:", error);
        }
        



        newComment.setAttribute("data-topic-id", topic_id); // 添加 topic_id
        var photoURL = `/get_shop_image?filename=${encodeURIComponent(filename)}`;      
        if(!filename) {
            photoURL = null;
        }
        // const topic_id = topic_data ? topic_data.id : null;
        const created_at = topic_data ? topic_data.created_at : null;
        console.log("topicdata", topic_data);
        console.log("topic_id", topic_id);
        console.log("created_at", created_at);

        newComment.innerHTML = `
            <div class="comment-main-level">
                <div class="comment-avatar">
                    <img src="https://via.placeholder.com/50" alt="Avatar">
                </div>
                <div class="comment-box" id="comment-box-${topic_id}-1">
                    <div class="comment-head">
                        <h6 class="comment-name">
                            <a href="#">${user_name}</a> <span class="comment-title">${topicTitle}</span>
                        </h6>
                        <span>${created_at}</span>
                        <i class="fa fa-reply"></i>
                        <i class="fa fa-heart"></i>
                    </div>
                    <div class="comment-content">
                        ${content}
                        ${photoURL ? `<img src="${photoURL}" alt="Uploaded Image" style="max-width: 200px; margin-top: 10px;">` : ''}
                    </div>
                    <div class="comment-actions">
                        <button class="reply-btn" id="reply-btn-${topic_id}-1">回覆</button>
                        <button class="delete-btn">刪除</button>
                    </div>
                    <ul class="reply-list" id="reply-list-${topic_id}"></ul>
                </div>
            </div>
        `;
    
        // 監聽刪除按鈕
        const deleteBtn = newComment.querySelector(".delete-btn");
        deleteBtn.addEventListener("click", () => {
            commentsList.removeChild(newComment);
        });
    
        // 監聽回覆按鈕
        const replyBtn = newComment.querySelector("#reply-btn-"+topic_id+"-1");
        replyBtn.addEventListener("click", () => showReplyForm(newComment, topic_id, 1));
    
        commentsList.appendChild(newComment);
    }
    async function addComment(topic_id, comment_id, user_name, content, parentReplyList = null, filename = null) {
        // const commentsList = parentReplyList || document.getElementById("comments-list");
        // 獲取主評論列表
        const commentsList = document.getElementById("comments-list");
        var replyList = parentReplyList || null;

        // 確保 commentsList 存在
        if (commentsList) {
            // 根據 topic_id 構建選擇器，找到 reply-list
            const replyListSelector = "#reply-list-"+topic_id; // 假設 topic_id 是 16
            console.log("replyListSelector:", replyListSelector);
            const replyList = commentsList.querySelector(replyListSelector);
            console.log("replyList:", replyList);

            if (replyList) {
                console.log("Found reply list:", replyList);
            } else {
                console.error("Reply list not found! Selector:", replyListSelector);
            }
        } else {
            console.error("comments-list not found in the DOM!");
        }

        var photoURL = null;
        if(!filename) {
            photoURL = null;
        }
        var comment_data = null;
        try {
            // 将 comment_id 添加到查询字符串中
            const url = `/get_comment_by_id?comment_id=${encodeURIComponent(comment_id)}`;
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                },
            });
        
            // 检查 HTTP 响应是否成功
            if (!response.ok) {
                console.error(`HTTP error! Status: ${response.status}`);
                return;
            }
        
            // 解析 JSON 响应
            const result = await response.json();
        
            if (result.status === "success") {
                comment_data = result.comment_data;
                console.log("Comment fetched from DB:", result.comment_data);
            } else {
                console.error("Error fetching comment data:", result.message);
                if (responseMessage) {
                    responseMessage.textContent = result.message;
                    responseMessage.style.color = "red";
                }
            }
        } catch (error) {
            console.error("Error when fetching comment data:", error);
        }
        const created_at = comment_data ? comment_data.created_at : null;
        

        const newComment = document.createElement("li");
        newComment.innerHTML = `
            <div class="comment-main-level">
                <div class="comment-avatar">
                    <img src="https://via.placeholder.com/50" alt="Avatar">
                </div>
                <div class="comment-box" id="comment-box-${topic_id}-${comment_id}">
                    <div class="comment-head">
                        <h6 class="comment-name">
                            <a href="#">${user_name}</a></span>
                        </h6>
                        <span>${created_at}</span>
                        <i class="fa fa-reply"></i>
                        <i class="fa fa-heart"></i>
                    </div>
                    <div class="comment-content">
                        ${content}
                        ${photoURL ? `<img src="${photoURL}" alt="Uploaded Image" style="max-width: 200px; margin-top: 10px;">` : ''}
                    </div>
                    <div class="comment-actions">
                        <button class="reply-btn" id="reply-btn-${topic_id}-${comment_id}">回覆</button>
                        <button class="delete-btn">刪除</button>
                    </div>
                    <ul class="reply-list" id="reply-list-${topic_id}-${comment_id}"></ul>
                </div>
            </div>
        `;
        console.log("newComment", newComment);
    
        // 監聽刪除按鈕
        const deleteBtn = newComment.querySelector(".delete-btn");
        deleteBtn.addEventListener("click", () => {
            replyList.removeChild(newComment);
        });

        // 正確生成選擇器
        const selector = `#reply-btn-${topic_id}-${comment_id}`;
        console.log(selector);

        // 查找按鈕
        const replyBtn = newComment.querySelector(selector);
        replyBtn.addEventListener("click", () => showReplyForm(newComment, topic_id, comment_id));

        console.log("replyList", replyList);
    
        replyList.appendChild(newComment);
    }
    
    async function showReplyForm(parentComment, topic_id, comment_id) {
        // 檢查是否已經存在回覆表單
        if (parentComment.querySelector(".reply-form")) return;
    
        const replyForm = document.createElement("div");
        replyForm.classList.add("reply-form");
        var father_comment_id = 1;
        var comment_order = 1;
        replyForm.innerHTML = `
            <textarea class="reply-text" placeholder="輸入回覆內容..."></textarea>
            <div class="comment-actions">
                <button class="submit-reply-btn">提交回覆</button>
                <button class="cancel-reply-btn">取消</button>
            </div>
        `;
    
        // 監聽提交按鈕
        replyForm.querySelector(".submit-reply-btn").addEventListener("click", async () => {
            const replyText = replyForm.querySelector(".reply-text").value.trim();
            var comment_data = null;

            // console.log(parentComment, topic_id, comment_id);
            console.log("parentComment", parentComment);
            console.log("topic_id", topic_id);
            console.log("comment_id", comment_id);

            
            if (!replyText) {
                alert("請輸入回覆內容!");
                return;
            }

            try {
                // 将 comment_id 添加到查询字符串中
                const response = await fetch(`/get_comment_by_id?comment_id=${encodeURIComponent(comment_id)}`, {
                    method: 'GET',
                    headers: {
                        "Content-Type": "application/json",
                    },
                });
            
                // 检查响应是否成功
                if (!response.ok) {
                    console.error(`HTTP error! Status: ${response.status}`);
                    return;
                }
            
                const result = await response.json();
            
                if (result.status === "success") {
                    comment_data = result.comment_data;
                    console.log("Comment fetched from DB:", result.comment_data);
                } else {
                    console.error("Error when fetching comment data:", result.message);
                }
            } catch (error) {
                console.error("Error when fetching comment data:", error);
            }
            
            console.log("**********");
            console.log("comment_data", comment_data);
            console.log("**********");

            comment_order = comment_data ? comment_data.comment_order + 1 : null;
            console.log("comment_order", comment_order);
            father_comment_id = comment_data ? comment_data.id : 1;

            createCommentInDB(replyText, topic_id, null, comment_order, father_comment_id);
    
            const replyList = parentComment.querySelector(".reply-list");

            var new_comment_data = null;


            try {
                // 将 topic_id 和 comment_order 添加到查询字符串中
                const url = `/get_comment_by_topicid_and_comment_order?topic_id=${encodeURIComponent(topic_id)}&comment_order=${encodeURIComponent(comment_order)}`;
            
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        "Content-Type": "application/json",
                    },
                });
            
                // 检查响应是否成功
                if (!response.ok) {
                    console.error(`HTTP error! Status: ${response.message}`);
                    return;
                }
            
                const result = await response.json();
            
                if (result.status === "success") {
                    new_comment_data = result.comment_data;
                    console.log("Comment fetched from DB:", result.comment_data);
                } else {
                    console.error("Error when fetching comment data:", result.message);
                    if (responseMessage) {
                        responseMessage.textContent = result.message;
                        responseMessage.style.color = "red";
                    }
                }
            } catch (error) {
                console.error("Error when fetching comment data:", error);
            }
            console.log("HIHIHI");
            console.log("new_comment_data", new_comment_data);
            console.log("HIHIHI");
            

            const new_comment_id = new_comment_data ? new_comment_data.id : null;
            const new_user_name = new_comment_data ? new_comment_data.user_name : "Visitor";
            const new_content = new_comment_data ? new_comment_data.content : null;
            console.log("new_comment_id", new_comment_id);
            console.log("new_user_name", new_user_name);
            console.log("new_content", new_content);

            addComment(topic_id, new_comment_id, new_user_name, new_content, replyList, null);
            replyForm.remove();
        });
    
        // 監聽取消按鈕
        replyForm.querySelector(".cancel-reply-btn").addEventListener("click", () => {
            replyForm.remove();
        });
        console.log("parentComment", parentComment);
        console.log(".comment-box-"+topic_id+"-"+father_comment_id);
        console.log(parentComment.querySelector("#comment-box-"+topic_id+"-"+father_comment_id));
        parentComment.querySelector("#comment-box-"+topic_id+"-"+father_comment_id).appendChild(replyForm);
    }

    async function loadTopics() {
        try {
            const response = await fetch('/get_all_topic', {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                },
            });
    
            if (response.ok) {
                const data = await response.json();
                if (data.status === "success") {
                    const topicList = data.topic_data;

                    // 對每個 topic 加載內容和第一條評論
                    for (const topic of topicList) {
                        await addTopicWithFirstComment(topic);
                    }
                } else {
                    console.error("Error fetching topics:", data.message);
                }
            } else {
                console.error("HTTP error fetching topics:", response.status);
            }
        } catch (err) {
            console.error("Error fetching topics:", err);
        }
    }

    async function addTopicWithFirstComment(topic) {
        try {
            // 添加主題到頁面
            // 加載第一條評論
            const commentResponse = await fetch(`/get_comments?topic_id=${topic.id}&limit=1`, {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                },
            });
    
            if (commentResponse.ok) {
                const commentData = await commentResponse.json();
                if (commentData.status === "success" && commentData.comment_data.length > 0) {
                    const firstComment = commentData.comment_data[0];
                    addTopic(topic.id, topic.title, firstComment.user_name, firstComment.content, firstComment.image_path);
                }
            } else {
                console.error("HTTP error fetching comments for topic:", topic.id, commentResponse.status);
            }
        } catch (err) {
            console.error("Error fetching first comment for topic:", topic.id, err);
        }
    }
    
});




