const imagesContainer = document.querySelector('.images');
document.addEventListener("DOMContentLoaded", async () => {
    const groupOptions = document.querySelector('.group-options');
    const nameOptions = document.querySelector('.name-options');
    const resetButton = document.querySelector('.reset');
    const submitButton = document.querySelector('.apply');
    const allButton = document.querySelector('.all-btn');
    const selectedCharacters = new Set();
    var selectedIPID = 0;

    // 向後端撈取 IP 資料
    try {
        const response = await fetch('/get_all_ip', {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            const result = await response.json();
            if (result.status === "success") {
                const ipData = result.ip_data || [];
                // console.log("IP data:", ipData);
                generateGroupButtons(ipData); // 動態生成 Group 按鈕
            } else {
                console.error("Failed to fetch IP data:", result.message);
            }
        } else {
            console.error("HTTP error:", response.status);
        }
    } catch (err) {
        console.error("Fetch error:", err);
    }

    // 動態生成 Group 按鈕
    function generateGroupButtons(ipData) {
        groupOptions.innerHTML = ''; // 清空現有的按鈕
        ipData.forEach(ip => {
            const button = document.createElement('button');
            button.textContent = ip.ip_name;    // 按鈕文字為 ip_name
            button.dataset.group = ip.ip_name; // 將 ip_name 設定為按鈕的 dataset
            button.dataset.ipId = ip.ip_id;    // 將 ip_id 設定為按鈕的 dataset

            // 點擊事件，撈取角色資料
            button.addEventListener('click', async () => {
                // 切換選中狀態
                document.querySelectorAll('.group-options button').forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                // 撈取角色資料
                selectedIPID = button.dataset.ipId;
                selectedCharacters.clear();
                // console.log("IP ID:", selectedIPID);
                await fetchCharactersByIpId(selectedIPID);
            });

            groupOptions.appendChild(button);
        });
    }
    // 使用 fetch 撈取角色資料
    async function fetchCharactersByIpId(ipId) {
        try {
            const response = await fetch(`/get_character_by_ipid?ip_id=${ipId}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (response.ok) {
                const result = await response.json();
                if (result.status === "success") {
                    const characters = result.characters || [];
                    // console.log("Characters data:", characters);
                    updateNameOptions(characters); // 動態生成 Name 按鈕
                } else {
                    console.error("Failed to fetch characters:", result.message);
                }
            } else {
                console.error("HTTP error:", response.status);
            }
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    // 動態生成 Name 按鈕
    function updateNameOptions(characters) {
        nameOptions.innerHTML = ''; // 清空 Name 區域
        characters.forEach(character => {
            const nameButton = document.createElement('button');
            nameButton.textContent = character.char_name; // 按鈕文字為角色名稱
            nameButton.dataset.charId = character.char_id; // 將角色 ID 存入 dataset

            nameButton.addEventListener('click', () => {
                const charId = nameButton.dataset.charId;

                // 切換選中狀態
                if (nameButton.classList.contains('active')) {
                    nameButton.classList.remove('active'); // 取消選中
                    selectedCharacters.delete(charId); // 從選中列表中移除
                } else {
                    nameButton.classList.add('active'); // 設為選中
                    selectedCharacters.add(charId); // 加入選中列表
                }

                // console.log("Selected characters:", Array.from(selectedCharacters));
            });

            nameOptions.appendChild(nameButton);
        });
    }

    submitButton.addEventListener('click', async () => {
        try {
            // 檢查是否有選中的 IP ID
            if (!selectedIPID) {
                // console.log("No IP ID selected.");
                alert("請先選擇一個 IP ID！");
                return;
            }
    
            // 將選中的數據轉換為可發送格式
            const dataToSend = {
                ip_id: selectedIPID,
                character_ids: Array.from(selectedCharacters), // 將 Set 轉換為 Array
            };
    
            // console.log("Submitting data:", dataToSend);
    
            // 使用 fetch 將數據發送到後端
            const response = await fetch('/get_merch_by_id', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend), // 將數據轉換為 JSON 字符串
            });
    
            // 處理後端返回的結果
            if (response.ok) {
                const result = await response.json();
                // console.log("Server response:", result);
    
                if (result.status === "success") {
                    // console.log("Received merchandise data:", result.merchandise);
                    imagesContainer.innerHTML = ''; // 清空圖片卡片
                    result.merchandise.forEach(item => {
                        addPhotoCard(item);
                    });
                } else {
                    alert(`提交失敗: ${result.message}`);
                }
            } else {
                console.error("HTTP error:", response.status);
                alert("提交失敗，請稍後重試！");
            }
        } catch (error) {
            // 捕獲異常
            console.error("Error occurred during submission:", error);
            alert("提交過程中發生錯誤！");
        }
    });

    // 重置按鈕：清空選擇
    resetButton.addEventListener('click', () => {
        document.querySelectorAll('.group-options button').forEach(btn => btn.classList.remove('active'));
        nameOptions.innerHTML = ''; // 清空 Name 按鈕
        imagesContainer.innerHTML = ''; // 清空圖片卡片
        selectedIPID = 0; // 清空選擇的 IP ID
        selectedCharacters.clear();
    });

    // "All" 按鈕點擊事件
    allButton.addEventListener('click', async () => {
        try {
            // console.log("Fetching all merchandise...");
            
            // 發送 GET 請求到後端
            const response = await fetch('/get_all_merch', { method: 'GET' });
            
            if (response.ok) {
                const result = await response.json();
                
                if (result.status === "success") {
                    // console.log("Received merchandise data:", result.merchandise);

                    // 顯示所有商品圖片
                    displayAllMerchImages(result.merchandise);
                } else {
                    console.error("Failed to fetch merchandise:", result.message);
                    alert(`無法獲取商品資料：${result.message}`);
                }
            } else {
                console.error("HTTP error:", response.status);
                alert("無法獲取商品資料，請稍後重試！");
            }
        } catch (error) {
            console.error("Error occurred while fetching merchandise:", error);
            alert("獲取商品資料時發生錯誤！");
        }
    });

    // 顯示所有商品圖片的函數
    function displayAllMerchImages(merchandise) {
        imagesContainer.innerHTML = ''; // 清空圖片容器
        // console.log("Displaying all merchandise...");
        // console.log("Merchandise:", merchandise);

        merchandise.forEach(item => {
            addPhotoCard(item);
        });
    }
    
    // 添加圖片卡片
    async function addPhotoCard(item) {
        const { char_id, ip_id, image_path, name, price, release_at, merch_id ,path} = item;
        const photoURL = `/get_image?image_path=${encodeURIComponent(image_path)}`;
        // console.log("Generated photoURL:", photoURL);
        var ipData = {};
        var is_fav = false;
        const addBtnText = `<button class="add-button" data-name="${name}" data-merch-id="${merch_id}" style="color: white; background-color: green; border: none; border-radius: 4px; padding: 5px; cursor: pointer;">+</button>`;
        const deleteBtnText = `<button class="delete-button" data-name="${name}" data-merch-id="${merch_id}" style="color: white; background-color: red; border: none; border-radius: 4px; padding: 5px; cursor: pointer;">-</button>`;
        try {
            const response = await fetch(`/get_ip_by_id?ip_id=${ip_id}`, {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (response.ok) {
                const result = await response.json();
                if (result.status === "success") {
                    ipData = result.ip_data || [];
                    console.log("IP data:", ipData);
                } else {
                    console.error("Failed to fetch IP data:", result.message);
                }
            } else {
                console.error("HTTP error:", response.status);
            }
        } catch (err) {}
        try {
            const favResponse = await fetch(`/get_user_favorite_by_id?merch_id=${merch_id}`, {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                },
            });
        
            if (favResponse.ok) {
                const favResult = await favResponse.json();
                if (favResult.status === "success") {
                    if (favResult.is_favorite) {
                        // console.log(ipData);
                        is_fav = true;
                    }
                } else {
                    console.error("Failed to fetch favorite data:", favResult.message);
                }
            } else {
                console.error("HTTP error when fetching favorite data:", favResponse.status);
            }
        } catch (err) {
            console.error("Error occurred while fetching favorite data:", err);
        }
        const BtnTxt = is_fav ? `<button class="delete-button" data-name="${name}" data-merch-id="${merch_id}" style="color: white; background-color: red; border: none; border-radius: 4px; padding: 5px; cursor: pointer;">-</button>` : `<button class="add-button" data-name="${name}" data-merch-id="${merch_id}" style="color: white; background-color: green; border: none; border-radius: 4px; padding: 5px; cursor: pointer;">+</button>`;
        const groupName = ipData.ip_name;
        const cardHTML = `
            <div class="ms-card-wrapper">
                <div class="ms-card-inside">
                    <div class="ms-card-front">
                        <div class="ms-card-front">
                            <img class ="ms-card-front-img" src="${photoURL}" alt="Card Image">
                        </div>
                    </div>
                    <div class="ms-card-back">
                        <div class="ms-tarot-border">
                            <div class="ms-tarot-info">
                                ${groupName} <br>
                                ${name} <br>
                                ${path} <br>
                                ${BtnTxt}
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;

        imagesContainer.insertAdjacentHTML('beforeend', cardHTML);
        ensureFourPerRow();

        // const addButton = imagesContainer.querySelector(`.add-button`);
        // console.log("add"+addButton); // 如果是 null，按鈕可能未加載成功或選取器有問題
        // addButton.addEventListener('click', async () => {
        //     const merchId = addButton.getAttribute('data-merch-id');
        //     console.log(`Sending merch_id ${merchId} to the backend...`);
    
        //     try {
        //         const response = await fetch('/create_user_favorite', {
        //             method: 'POST',
        //             headers: {
        //                 'Content-Type': 'application/json',
        //             },
        //             body: JSON.stringify({ merch_id: merchId }),
        //         });
    
        //         if (response.ok) {
        //             const result = await response.json();
        //             if (result.status === 'success') {
        //                 alert(`Added ${name} to your list!`);
        //             } else {
        //                 alert(`Failed to add ${name}: ${result.message}`);
        //             }
        //         } else {
        //             alert(`HTTP error: ${response.status}`);
        //         }
        //     } catch (err) {
        //         console.error('Error while adding item:', err);
        //         alert('Failed to add item to the list.');
        //     }
        // });

        // const deleteButton = imagesContainer.querySelector(`.delete-button`);
        // console.log("delete"+deleteButton); // 如果是 null，按鈕可能未加載成功或選取器有問題
        // deleteButton.addEventListener('click', async () => {
        //     const merchId = deleteButton.getAttribute('data-merch-id');
        //     console.log(`Sending merch_id ${merchId} to the backend...`);
    
        //     try {
        //         const response = await fetch('/delete_user_favorite', {
        //             method: 'POST',
        //             headers: {
        //                 'Content-Type': 'application/json',
        //             },
        //             body: JSON.stringify({ merch_id: merchId }),
        //         });
    
        //         if (response.ok) {
        //             const result = await response.json();
        //             if (result.status === 'success') {
        //                 alert(`Deleted ${name} from your list!`);
        //             } else {
        //                 alert(`Failed to delete ${name}: ${result.message}`);
        //             }
        //         } else {
        //             alert(`HTTP error: ${response.status}`);
        //         }
        //     } catch (err) {
        //         console.error('Error while deleting item:', err);
        //         alert('Failed to delete item from the list.');
        //     }
        // });
    }

    // 設置四列布局->6感覺比較好看
    function ensureFourPerRow() {
        imagesContainer.style.display = 'grid';
        imagesContainer.style.gridTemplateColumns = 'repeat(6, 1fr)';
        imagesContainer.style.gap = '5px';
    }
});

let isProcessing = false;

imagesContainer.addEventListener('click', async (event) => {
    if (isProcessing) return;

    const target = event.target;
    if (target.classList.contains('add-button')) {
        isProcessing = true;
        await handleAdd(target);
        isProcessing = false;
    } else if (target.classList.contains('delete-button')) {
        isProcessing = true;
        await handleDelete(target);
        isProcessing = false;
    }
});

async function handleAdd(button) {
    const merchId = button.getAttribute('data-merch-id');
    console.log(`Adding merch_id ${merchId}...`);
    button.disabled = true;

    try {
        const response = await fetch('/create_user_favorite', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ merch_id: merchId }),
        });

        if (response.ok) {
            const result = await response.json();
            if (result.status === 'success') {
                button.textContent = '-';
                button.classList.remove('add-button');
                button.classList.add('delete-button');
                button.style.backgroundColor = 'red';
            } else {
                alert(`Add failed: ${result.message}`);
            }
        } else {
            alert(`HTTP Error: ${response.status}`);
        }
    } catch (err) {
        console.error('Error while adding item:', err);
        alert('Failed to add item.');
    } finally {
        button.disabled = false; // 確保按鈕可再次操作
    }
}

async function handleDelete(button) {
    const merchId = button.getAttribute('data-merch-id');
    console.log(`Deleting merch_id ${merchId}...`);
    button.disabled = true;

    try {
        const response = await fetch('/delete_user_favorite', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ merch_id: merchId }),
        });

        if (response.ok) {
            const result = await response.json();
            if (result.status === 'success') {
                button.textContent = '+';
                button.classList.remove('delete-button');
                button.classList.add('add-button');
                button.style.backgroundColor = 'green';
            } else {
                alert(`Delete failed: ${result.message}`);
            }
        } else {
            alert(`HTTP Error: ${response.status}`);
        }
    } catch (err) {
        console.error('Error while deleting item:', err);
        alert('Failed to delete item.');
    } finally {
        button.disabled = false; // 確保按鈕可再次操作
    }
}
