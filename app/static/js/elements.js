const groupButtons = document.querySelectorAll('.group-options button');
const nameOptions = document.querySelector('.name-options');
const resetButton = document.querySelector('.reset');

// 預設的角色資料
const groupToNames = {
    'aespa': ['Karina', 'Giselle', 'Winter', 'NingNing'],
    'NCT DREAM': ['Mark', 'Renjun', 'Jeno', 'Haechan', 'Jaemin', 'Chenle', 'Jisung'],
    'NCT 127': ['角色7', '角色8','Mark', 'Haechan'],
    'Y': ['角色10', '角色11'],
    'Z': ['角色12', '角色13']
};

// 點擊 Group Name 時更新 Name 按鈕
groupButtons.forEach(button => {
    button.addEventListener('click', () => {
        // 切換 Group Name 的選中狀態
        groupButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        // 根據選中 Group 動態更新 Name 按鈕
        const groupName = button.dataset.group;
        const names = groupToNames[groupName] || [];
        updateNameOptions(names);
    });
});

// 動態生成 Name 按鈕
function updateNameOptions(names) {
    nameOptions.innerHTML = ''; // 清空 Name 區域
    names.forEach(name => {
        const nameButton = document.createElement('button');
        nameButton.textContent = name;
        nameButton.addEventListener('click', () => {
            nameButton.classList.toggle('active');
        });
        nameOptions.appendChild(nameButton);
    });
}

// 重設按鈕
resetButton.addEventListener('click', () => {
    groupButtons.forEach(button => button.classList.remove('active'));
    nameOptions.innerHTML = ''; // 清空 Name 區域
});
