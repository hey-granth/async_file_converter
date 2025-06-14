const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const selectedFile = document.getElementById('selectedFile');
const convertBtn = document.getElementById('convertBtn');
const formatSelect = document.getElementById('formatSelect');
const loading = document.getElementById('loading');
const downloadSection = document.getElementById('downloadSection');
const downloadBtn = document.getElementById('downloadBtn');
const errorMessage = document.getElementById('errorMessage');

let currentTaskId = null;

// File selection handling
fileInput.addEventListener('change', function(e) {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];

        // Check file size (100MB limit)
        if (file.size > 100 * 1024 * 1024) {
            showError('File size exceeds 100MB limit');
            return;
        }

        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileSize').textContent = formatFileSize(file.size);
        selectedFile.classList.add('show');
        hideError();
        updateConvertButton();
    }
});

formatSelect.addEventListener('change', updateConvertButton);

function updateConvertButton() {
    const hasFile = fileInput.files.length > 0;
    const hasFormat = formatSelect.value !== '';
    convertBtn.disabled = !(hasFile && hasFormat);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add('show');
}

function hideError() {
    errorMessage.classList.remove('show');
}

function resetUI() {
    loading.classList.remove('show');
    downloadSection.classList.remove('show');
    convertBtn.disabled = false;
    hideError();
}

// Drag and drop
uploadArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', function(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', function(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        fileInput.dispatchEvent(new Event('change'));
    }
});

// Convert button click handler
convertBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    const format = formatSelect.value;

    if (!file || !format) return;

    // Show loading
    loading.classList.add('show');
    convertBtn.disabled = true;
    hideError();

    const formData = new FormData();
    formData.append("file", file);
    formData.append("to_format", format);

    try {
        // Upload file to backend
        const convertRes = await fetch("http://localhost:8000/convert", {
            method: "POST",
            body: formData
        });

        if (!convertRes.ok) {
            throw new Error('Upload failed');
        }

        const { task_id } = await convertRes.json();
        currentTaskId = task_id;

        // Poll for status
        const checkStatus = async () => {
            try {
                const statusRes = await fetch(`http://localhost:8000/status/${task_id}`);
                const { status } = await statusRes.json();

                if (status === "SUCCESS") {
                    loading.classList.remove('show');
                    downloadSection.classList.add('show');
                    downloadBtn.onclick = () => {
                        window.location.href = `http://localhost:8000/download/${task_id}`;
                    };
                } else if (status === "FAILURE") {
                    loading.classList.remove('show');
                    showError("Conversion failed. Please try another file.");
                    convertBtn.disabled = false;
                } else {
                    // Still processing
                    setTimeout(checkStatus, 2000);
                }
            } catch (err) {
                loading.classList.remove('show');
                showError("Status check failed. Please try again.");
                convertBtn.disabled = false;
            }
        };

        checkStatus();

    } catch (err) {
        loading.classList.remove('show');
        showError("Upload failed. Please check your connection and try again.");
        convertBtn.disabled = false;
    }
});