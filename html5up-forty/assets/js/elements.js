const groupButtons = document.querySelectorAll('.group-options button');
const nameOptions = document.querySelector('.name-options');
const resetButton = document.querySelector('.reset');
const applyButton = document.querySelector('.apply');
const imagesContainer = document.querySelector('.images');

// 預設的角色資料
const groupToNames = {
    'aespa': ['Karina', 'Giselle', 'Winter', 'NingNing'],
    'NCT DREAM': ['Mark', 'Renjun', 'Jeno', 'Haechan', 'Jaemin', 'Chenle', 'Jisung'],
};

// 預設的圖片資料
const nameToImages = {
    //'Karina': '../html5up-forty/images/',
    //'Giselle': '../html5up-forty/images/',
    'Winter': '../html5up-forty/images/aespa_myworld_msk_pob_winter.webp',
    'NingNing': '../html5up-forty/images/aespa_myworld_msk_pob_ningning.webp',
    //'Mark': '../html5up-forty/images/',
    //'Renjun': '../html5up-forty/images/',
    //'Jeno': '../html5up-forty/images/',
    'Haechan': '../html5up-forty/images/nctdreamistjinterasiahaechan.webp',
    'Jaemin': '../html5up-forty/images/nctdreamistjinterasiajaemin.webp',
    //'Chenle': '../html5up-forty/images/',
    'Jisung': '../html5up-forty/images/nctdreamistjinterasiajisung.webp',
};

// 添加 All 按鈕邏輯
const allButton = document.createElement('button');
allButton.textContent = 'All';
allButton.classList.add('all-button');
document.querySelector('.group-options').appendChild(allButton);

allButton.addEventListener('click', () => {
    groupButtons.forEach(button => button.classList.remove('active'));
    allButton.classList.add('active');

    const allNames = Object.values(groupToNames).flat(); // 獲取所有成員
    displayGroupImages(allNames, 'All Groups');
});

groupButtons.forEach(button => {
    button.addEventListener('click', () => {
        // 切換 Group Name 的選中狀態
        groupButtons.forEach(btn => btn.classList.remove('active'));
        allButton.classList.remove('active');
        button.classList.add('active');

        // 根據選中 Group 動態生成成員按鈕
        const groupName = button.dataset.group;
        const names = groupToNames[groupName] || [];
        generateMemberButtons(names);
    });
});

// 生成成員按鈕
function generateMemberButtons(names) {
    nameOptions.innerHTML = ''; // 清空成員區域
    names.forEach(name => {
        const nameButton = document.createElement('button');
        nameButton.textContent = name;
        nameButton.classList.add('name-button');
        nameButton.addEventListener('click', () => {
            nameButton.classList.toggle('active');
        });
        nameOptions.appendChild(nameButton);
    });
}

// 點擊 "使用" 按鈕顯示選中成員圖片
applyButton.addEventListener('click', () => {
    const selectedNames = Array.from(nameOptions.querySelectorAll('.active')).map(button => button.textContent);
    imagesContainer.innerHTML = ''; // 清空圖片容器

    selectedNames.forEach(name => {
        const imageUrl = nameToImages[name];
        if (imageUrl) {
            addPhotoCard(imageUrl, 'Selected Group', name, 'Source');
        }
    });
});

// 顯示全組圖片
function displayGroupImages(names, groupName) {
    imagesContainer.innerHTML = ''; // 清空圖片容器
    names.forEach(name => {
        const imageUrl = nameToImages[name];
        if (imageUrl) {
            addPhotoCard(imageUrl, groupName, name, 'Source');
        }
    });
}

// 添加圖片卡片
function addPhotoCard(photoURL, groupName, name, source) {
    const cardHTML = `
        <div class="ms-card-wrapper">
            <div class="ms-card-inside">
                <div class="ms-card-front">
                    <div class="ms-card-front-bg" style="background-image:url('${photoURL}');"></div>
                    <div class="ms-tarot-gradient">
                        <div class="ms-tarot-border">
                            <div class="ms-tarot-title"></div>
                        </div>
                    </div>
                </div>
                <div class="ms-card-back">
                    <div class="ms-tarot-border">
                        <div class="ms-tarot-info">
                            ${groupName} <br>
                            ${name} <br>
                            ${source} <br>
                            <button class="add-button" data-name="${name}" style="color: white; background-color: red; border: none; border-radius: 4px; padding: 5px; cursor: pointer;">+</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;

    imagesContainer.insertAdjacentHTML('beforeend', cardHTML);
    ensureFourPerRow();

    // 添加按鈕點擊事件
    const addButton = imagesContainer.querySelector(`.add-button[data-name="${name}"]`);
    addButton.addEventListener('click', () => {
        alert(`Added ${name} to your list!`);
    });
}

// 設置四列布局
function ensureFourPerRow() {
    imagesContainer.style.display = 'grid';
    imagesContainer.style.gridTemplateColumns = 'repeat(4, 1fr)';
    imagesContainer.style.gap = '5px';
}

// 重設按鈕
resetButton.addEventListener('click', () => {
    groupButtons.forEach(button => button.classList.remove('active'));
    allButton.classList.remove('active');
    nameOptions.innerHTML = ''; // 清空成員區域
    imagesContainer.innerHTML = ''; // 清空圖片
});
