// JavaScript для интерактивности
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.querySelector('.form__input-image');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const previewRemove = document.getElementById('preview-remove');
    
    // Обработка перетаскивания файлов
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });
    
    // Обработка выбора файла
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelection(e.target.files[0]);
        }
    });
    
    // Удаление превью
    previewRemove.addEventListener('click', () => {
        previewContainer.style.display = 'none';
        fileInput.value = '';
    });
    
    // Функция обработки выбранного файла
    function handleFileSelection(file) {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewContainer.style.display = 'block';
            }
            
            reader.readAsDataURL(file);
        }
    }
});