// ===== API CONFIGURATION =====
const API_BASE_URL = 'http://localhost:8000/api';

// ===== DOM ELEMENTS =====
const elements = {
    uploadArea: document.getElementById('uploadArea'),
    fileInput: document.getElementById('fileInput'),
    fileInfo: document.getElementById('fileInfo'),
    fileName: document.getElementById('fileName'),
    fileSize: document.getElementById('fileSize'),
    btnRemove: document.getElementById('btnRemove'),
    btnScan: document.getElementById('btnScan'),
    btnScanText: document.getElementById('btnScanText'),
    resultsSection: document.getElementById('resultsSection'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    signaturesCount: document.getElementById('signaturesCount'),
    statusIndicator: document.getElementById('statusIndicator'),
    statusText: document.getElementById('statusText'),
    riskBadge: document.getElementById('riskBadge'),
    riskLevel: document.getElementById('riskLevel'),
    scannedFileName: document.getElementById('scannedFileName'),
    totalLines: document.getElementById('totalLines'),
    matchesFound: document.getElementById('matchesFound'),
    matchesContainer: document.getElementById('matchesContainer'),
    signaturesGrid: document.getElementById('signaturesGrid')
};

// ===== STATE =====
let selectedFile = null;

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

async function initializeApp() {
    try {
        // Check API health
        await checkHealth();

        // Load signatures
        await loadSignatures();

        // Load stats
        await loadStats();
    } catch (error) {
        console.error('Initialization error:', error);
        showError('Failed to connect to API server');
    }
}

// ===== API CALLS =====
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health/`);
        const data = await response.json();

        if (data.status === 'healthy') {
            elements.statusText.textContent = 'Online';
            elements.statusIndicator.querySelector('.status-dot').style.background = '#10b981';
        }
    } catch (error) {
        elements.statusText.textContent = 'Offline';
        elements.statusIndicator.querySelector('.status-dot').style.background = '#ef4444';
        throw error;
    }
}

async function loadSignatures() {
    try {
        const response = await fetch(`${API_BASE_URL}/signatures/`);
        const data = await response.json();

        if (data.success) {
            elements.signaturesCount.textContent = data.count;
            displaySignatures(data.signatures);
        }
    } catch (error) {
        console.error('Failed to load signatures:', error);
    }
}

async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats/`);
        const data = await response.json();

        if (data.success) {
            console.log('Stats loaded:', data.stats);
        }
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

async function scanFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        showLoading(true);

        const response = await fetch(`${API_BASE_URL}/scan/file/`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'Scan failed');
        }
    } catch (error) {
        console.error('Scan error:', error);
        showError('Failed to scan file. Please try again.');
    } finally {
        showLoading(false);
    }
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    // Upload area click
    elements.uploadArea.addEventListener('click', (e) => {
        if (e.target !== elements.btnRemove) {
            elements.fileInput.click();
        }
    });

    // File input change
    elements.fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('dragleave', handleDragLeave);
    elements.uploadArea.addEventListener('drop', handleDrop);

    // Remove file button
    elements.btnRemove.addEventListener('click', (e) => {
        e.stopPropagation();
        removeFile();
    });

    // Scan button
    elements.btnScan.addEventListener('click', handleScan);
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        setSelectedFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    elements.uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    elements.uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    elements.uploadArea.classList.remove('drag-over');

    const file = e.dataTransfer.files[0];
    if (file) {
        setSelectedFile(file);
    }
}

function setSelectedFile(file) {
    selectedFile = file;

    // Show file info
    elements.fileName.textContent = file.name;
    elements.fileSize.textContent = formatFileSize(file.size);

    // Toggle UI
    elements.uploadArea.querySelector('.upload-content').style.display = 'none';
    elements.fileInfo.style.display = 'flex';
    elements.btnScan.disabled = false;
}

function removeFile() {
    selectedFile = null;
    elements.fileInput.value = '';

    // Toggle UI
    elements.uploadArea.querySelector('.upload-content').style.display = 'flex';
    elements.fileInfo.style.display = 'none';
    elements.btnScan.disabled = true;

    // Hide results
    elements.resultsSection.style.display = 'none';
}

async function handleScan() {
    if (!selectedFile) return;

    await scanFile(selectedFile);
}

// ===== DISPLAY FUNCTIONS =====
function displaySignatures(signatures) {
    elements.signaturesGrid.innerHTML = '';

    signatures.forEach(sig => {
        const card = document.createElement('div');
        card.className = 'signature-card';
        card.innerHTML = `
            <div class="signature-name">${sig.name}</div>
            <div class="signature-regex">${escapeHtml(sig.regex)}</div>
            <div class="signature-description">${sig.description}</div>
        `;
        elements.signaturesGrid.appendChild(card);
    });
}

function displayResults(data) {
    // Update summary
    elements.scannedFileName.textContent = data.filename;
    elements.totalLines.textContent = data.total_lines;
    elements.matchesFound.textContent = data.matches_found;

    // Update risk level
    const riskLevel = data.risk_level.toUpperCase();
    elements.riskLevel.textContent = riskLevel;
    elements.riskBadge.className = `risk-badge ${data.risk_level}`;

    // Display matches
    if (data.matches.length > 0) {
        displayMatches(data.matches);
    } else {
        elements.matchesContainer.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: var(--success);">
                <svg style="width: 64px; height: 64px; margin-bottom: 1rem;" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">No Threats Detected</h3>
                <p style="color: var(--text-muted);">This file appears to be clean and safe.</p>
            </div>
        `;
    }

    // Show results section
    elements.resultsSection.style.display = 'block';
    elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function displayMatches(matches) {
    elements.matchesContainer.innerHTML = '';

    matches.forEach((match, index) => {
        const matchItem = document.createElement('div');
        matchItem.className = 'match-item';
        matchItem.style.animationDelay = `${index * 0.1}s`;
        matchItem.innerHTML = `
            <div class="match-header">
                <span class="match-signature">${match.signature_name}</span>
                <span class="match-line">Line ${match.line_no}</span>
            </div>
            <div class="match-description">${match.description}</div>
            <div class="match-snippet">${escapeHtml(match.snippet)}</div>
        `;
        elements.matchesContainer.appendChild(matchItem);
    });
}

// ===== UTILITY FUNCTIONS =====
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showLoading(show) {
    elements.loadingOverlay.style.display = show ? 'flex' : 'none';
    elements.btnScan.disabled = show;

    if (show) {
        elements.btnScanText.textContent = 'Scanning...';
    } else {
        elements.btnScanText.textContent = 'Scan for Malware';
    }
}

function showError(message) {
    alert(`Error: ${message}`);
}

// ===== ANIMATIONS =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .match-item {
        animation: slideInUp 0.5s ease forwards;
        opacity: 0;
    }
`;
document.head.appendChild(style);
