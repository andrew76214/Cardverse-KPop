document.addEventListener('DOMContentLoaded', () => {
    const infoForm = document.getElementById('photoForm');

    infoForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const groupName = document.getElementById('groupName').value;
        const name = document.getElementById('name').value;
        const source = document.getElementById('source').value;
        const photoInput = document.getElementById('photoUpload');

        const file = photoInput.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function(e) {
                const photoURL = e.target.result;
                addPhotoCard(photoURL, groupName, name, source);
                infoForm.reset();
            };

            reader.readAsDataURL(file);
        }
    });

    function addPhotoCard(photoURL, groupName, name, source) {
        const cardGrid = document.querySelector('.ms-card-grid');

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
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;

        cardGrid.insertAdjacentHTML('beforeend', cardHTML);
        ensureFourPerRow();
    }

    function ensureFourPerRow() {
        const cardGrid = document.querySelector('.ms-card-grid');
        cardGrid.style.display = 'grid';
        cardGrid.style.gridTemplateColumns = 'repeat(4, 1fr)';
        cardGrid.style.gap = '5px';
    }

    // Initialize layout
    ensureFourPerRow();
});
