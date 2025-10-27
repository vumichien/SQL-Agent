/**
 * Detomo SQL AI - Main Application
 * Application logic, state management, and event handlers
 */

// Application state
const state = {
    messages: [],
    history: [],
    suggestedQuestions: [],
    currentQueryId: null,
    isLoading: false,
    darkMode: false,
    language: 'en',
    sidebarCollapsed: false,
};

/**
 * Initialize the application
 */
async function initApp() {
    console.log('Initializing Detomo SQL AI...');

    // Load theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        state.darkMode = true;
        document.documentElement.classList.add('dark');
    }

    // Load language preference
    const savedLanguage = localStorage.getItem('language') || 'en';
    state.language = savedLanguage;
    setLanguage(savedLanguage);

    // Load sidebar state
    const savedSidebarState = localStorage.getItem('sidebarCollapsed');
    state.sidebarCollapsed = savedSidebarState === 'true';
    if (state.sidebarCollapsed) {
        document.querySelector('.main-layout').classList.add('sidebar-collapsed');
        document.getElementById('sidebar-toggle').classList.add('active');
    }

    // Update UI
    updateLanguageButton();

    // Setup event listeners
    setupEventListeners();

    // Load initial data
    await loadInitialData();

    // Render initial state
    render();

    console.log('Detomo SQL AI initialized');
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Send button
    const sendButton = document.getElementById('send-button');
    sendButton.addEventListener('click', handleSendMessage);

    // Question input - enter key
    const questionInput = document.getElementById('question-input');
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    // Theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('click', toggleTheme);

    // Language toggle button
    const languageToggle = document.getElementById('language-toggle');
    languageToggle.addEventListener('click', toggleLanguage);

    // Sidebar toggle button
    const sidebarToggle = document.getElementById('sidebar-toggle');
    sidebarToggle.addEventListener('click', toggleSidebar);

    // Training data button
    const manageTrainingBtn = document.getElementById('manage-training-btn');
    manageTrainingBtn.addEventListener('click', openTrainingModal);

    // Training type radio buttons
    document.querySelectorAll('input[name="train-type"]').forEach(radio => {
        radio.addEventListener('change', handleTrainingTypeChange);
    });

    // Tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Close modal on outside click
    const modal = document.getElementById('training-modal');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeTrainingModal();
        }
    });
}

/**
 * Load initial data
 */
async function loadInitialData() {
    try {
        // Check API health
        const health = await api.getHealth();
        console.log('API Health:', health);

        // Load suggested questions
        const questions = await api.generateQuestions();
        state.suggestedQuestions = questions.questions || [];

        // Load query history
        await loadHistory();

        // Load training data count
        await loadTrainingData();
        renderTrainingDataInfo();
    } catch (error) {
        console.error('Failed to load initial data:', error);
        showError('Failed to connect to the API. Please make sure the server is running.');
    }
}

/**
 * Load query history
 */
async function loadHistory() {
    try {
        const history = await api.getQuestionHistory();
        state.history = history.history || [];
        renderSidebar();
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

/**
 * Handle send message
 */
async function handleSendMessage() {
    const input = document.getElementById('question-input');
    const question = input.value.trim();

    if (!question || state.isLoading) {
        return;
    }

    // Clear input
    input.value = '';

    // Ask the question
    await askQuestion(question);
}

/**
 * Ask a question
 */
async function askQuestion(question) {
    if (state.isLoading) {
        return;
    }

    // Add user message
    state.messages.push({
        type: 'user',
        question,
    });

    // Set loading state
    state.isLoading = true;

    // Render
    render();
    scrollToBottomImmediate();

    try {
        // Call the all-in-one query endpoint
        const response = await api.query(question);

        // Generate follow-up questions if we have results
        let followupQuestions = [];
        if (response.results && response.results.length > 0) {
            try {
                const followupResponse = await api.generateFollowupQuestions(
                    question,
                    response.results
                );
                followupQuestions = followupResponse.questions || [];
            } catch (error) {
                console.warn('Failed to generate follow-up questions:', error);
            }
        }

        // Add assistant message with follow-up questions
        state.messages.push({
            type: 'assistant',
            data: {
                ...response,
                followup_questions: followupQuestions,
            },
        });

        // Store current query ID
        state.currentQueryId = response.id;

        // Reload history
        await loadHistory();

    } catch (error) {
        console.error('Query failed:', error);
        state.messages.push({
            type: 'assistant',
            data: {
                error: error.message || 'Failed to process query',
            },
        });
    } finally {
        state.isLoading = false;
        render();
        // Delay scroll to ensure DOM is fully rendered
        setTimeout(() => scrollToBottom(), 150);
    }
}

/**
 * Load a history item
 */
async function loadHistoryItem(id) {
    if (state.isLoading) {
        return;
    }

    try {
        state.isLoading = true;
        render();

        const response = await api.loadQuestion(id);

        // Clear current messages
        state.messages = [];

        // Add user message
        state.messages.push({
            type: 'user',
            question: response.question,
        });

        // Add assistant message
        state.messages.push({
            type: 'assistant',
            data: response,
        });

        state.currentQueryId = id;

    } catch (error) {
        console.error('Failed to load history item:', error);
        showError('Failed to load history item');
    } finally {
        state.isLoading = false;
        render();
        // Delay scroll to ensure DOM is fully rendered
        setTimeout(() => scrollToBottom(), 150);
    }
}

/**
 * Copy SQL to clipboard
 */
async function copyToClipboard(buttonId, text) {
    try {
        await navigator.clipboard.writeText(text);

        // Update button text temporarily
        const button = document.querySelector(`[onclick*="${buttonId}"]`);
        if (button) {
            const originalText = button.textContent;
            button.textContent = t('copied');
            setTimeout(() => {
                button.textContent = originalText;
            }, 2000);
        }
    } catch (error) {
        console.error('Failed to copy to clipboard:', error);
    }
}

/**
 * Download CSV
 */
function downloadCSV(id) {
    const url = api.getDownloadCSVUrl(id);
    window.open(url, '_blank');
}

/**
 * Provide SQL feedback (thumbs up/down)
 */
async function provideSQLFeedback(id, question, sql, isCorrect) {
    try {
        // If feedback is positive, add to training data
        if (isCorrect) {
            await api.train('sql', { question, sql });

            // Update button visual feedback
            const buttons = event.target.parentElement.querySelectorAll('.feedback-button');
            buttons.forEach(btn => {
                btn.classList.add('selected');
                btn.disabled = true;
            });

            // Show thank you message
            alert(t('feedbackThanks'));
        } else {
            // For negative feedback, we could potentially log it or ask for correction
            // For now, just acknowledge
            const buttons = event.target.parentElement.querySelectorAll('.feedback-button');
            buttons.forEach(btn => {
                btn.classList.add('selected');
                btn.disabled = true;
            });

            alert(t('feedbackThanks') + ' We will work on improving this.');
        }
    } catch (error) {
        console.error('Failed to provide feedback:', error);
        alert('Failed to submit feedback. Please try again.');
    }
}

/**
 * Toggle dark mode
 */
function toggleTheme() {
    state.darkMode = !state.darkMode;

    if (state.darkMode) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    }

    updateThemeButton();
}

/**
 * Toggle language
 */
function toggleLanguage() {
    state.language = state.language === 'en' ? 'ja' : 'en';
    setLanguage(state.language);
    localStorage.setItem('language', state.language);
    updateLanguageButton();
    render();
}

/**
 * Toggle sidebar
 */
function toggleSidebar() {
    state.sidebarCollapsed = !state.sidebarCollapsed;
    localStorage.setItem('sidebarCollapsed', state.sidebarCollapsed);

    const mainLayout = document.querySelector('.main-layout');
    const toggleButton = document.getElementById('sidebar-toggle');

    if (state.sidebarCollapsed) {
        mainLayout.classList.add('sidebar-collapsed');
        toggleButton.classList.add('active');
    } else {
        mainLayout.classList.remove('sidebar-collapsed');
        toggleButton.classList.remove('active');
    }
}

/**
 * Update theme button text
 */
function updateThemeButton() {
    const button = document.getElementById('theme-toggle');
    button.textContent = state.darkMode ? '☀️ Light' : '🌙 Dark';
}

/**
 * Update language button text
 */
function updateLanguageButton() {
    const button = document.getElementById('language-toggle');
    button.textContent = state.language === 'en' ? '🇯🇵 日本語' : '🇺🇸 English';
}

/**
 * Show error message
 */
function showError(message) {
    state.messages.push({
        type: 'assistant',
        data: {
            error: message,
        },
    });
    render();
}

/**
 * Scroll to bottom of messages
 */
function scrollToBottom() {
    const messagesContainer = document.getElementById('messages-container');
    if (messagesContainer) {
        // Use requestAnimationFrame for smoother scrolling
        requestAnimationFrame(() => {
            messagesContainer.scrollTo({
                top: messagesContainer.scrollHeight,
                behavior: 'smooth'
            });
        });
    }
}

/**
 * Scroll to bottom immediately (no animation)
 */
function scrollToBottomImmediate() {
    const messagesContainer = document.getElementById('messages-container');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

/**
 * Render the entire UI
 */
function render() {
    renderMessages();
    renderSidebar();
    updateInputState();
    updateThemeButton();
}

/**
 * Render messages
 */
function renderMessages() {
    const container = document.getElementById('messages-container');

    if (state.messages.length === 0) {
        // Show empty state with suggested questions
        container.innerHTML = `
            ${renderEmptyState()}
            ${renderSuggestedQuestions(state.suggestedQuestions)}
        `;
        return;
    }

    // Render all messages
    let html = '';
    for (const message of state.messages) {
        if (message.type === 'user') {
            html += renderUserMessage(message.question);
        } else if (message.type === 'assistant') {
            html += renderAssistantMessage(message.data);
        }
    }

    // Add loading indicator if loading
    if (state.isLoading) {
        html += renderLoadingMessage();
    }

    container.innerHTML = html;
}

/**
 * Render sidebar
 */
function renderSidebar() {
    const historyContainer = document.getElementById('history-container');
    historyContainer.innerHTML = renderHistoryList(state.history, state.currentQueryId);
}

/**
 * Update input state
 */
function updateInputState() {
    const sendButton = document.getElementById('send-button');
    const questionInput = document.getElementById('question-input');

    if (state.isLoading) {
        sendButton.disabled = true;
        sendButton.innerHTML = '<span class="loading"></span>';
        questionInput.disabled = true;
    } else {
        sendButton.disabled = false;
        sendButton.textContent = t('send');
        questionInput.disabled = false;
        questionInput.placeholder = t('askQuestion');
    }
}

/**
 * Training Data Management Functions
 */

// Training data state
let trainingData = [];

/**
 * Load training data
 */
async function loadTrainingData() {
    try {
        const response = await api.getTrainingData();
        trainingData = response.training_data || [];
        return trainingData;
    } catch (error) {
        console.error('Failed to load training data:', error);
        return [];
    }
}

/**
 * Render training data count in sidebar
 */
function renderTrainingDataInfo() {
    const container = document.getElementById('training-data-info');
    if (container) {
        container.innerHTML = `
            <p style="font-size: 14px; color: var(--text-secondary);">
                <span class="training-count">${trainingData.length}</span> items
            </p>
        `;
    }
}

/**
 * Open training modal
 */
function openTrainingModal() {
    const modal = document.getElementById('training-modal');
    modal.classList.add('active');
    loadAndRenderTrainingData();
}

/**
 * Close training modal
 */
function closeTrainingModal() {
    const modal = document.getElementById('training-modal');
    modal.classList.remove('active');
}

/**
 * Load and render training data in modal
 */
async function loadAndRenderTrainingData() {
    const container = document.getElementById('training-data-list');

    // Show loading
    container.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--text-secondary);">Loading training data...</div>';

    try {
        await loadTrainingData();
        renderTrainingDataList();
        renderTrainingDataInfo();
    } catch (error) {
        console.error('Failed to load training data:', error);
        container.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--error-color);">Failed to load training data. Please try again.</div>';
    }
}

/**
 * Render training data list in modal
 */
function renderTrainingDataList() {
    const container = document.getElementById('training-data-list');

    if (!trainingData || trainingData.length === 0) {
        container.innerHTML = '<p style="color: var(--text-secondary);">No training data found.</p>';
        return;
    }

    container.innerHTML = trainingData.map(item => {
        // Vanna returns: id, question, content, training_data_type
        const type = item.training_data_type || 'unknown';

        // For SQL type, show question + content
        let displayContent = '';
        if (type === 'sql' && item.question) {
            displayContent = `<strong>Q:</strong> ${escapeHtml(item.question)}<br><strong>SQL:</strong> ${escapeHtml(item.content || '')}`;
        } else {
            displayContent = escapeHtml(item.content || '');
        }

        return `
            <div class="training-data-item">
                <div class="training-data-header">
                    <span class="training-data-type">${escapeHtml(type)}</span>
                    <button class="training-data-delete" onclick="deleteTrainingData('${escapeHtml(item.id)}')">
                        🗑️ Delete
                    </button>
                </div>
                <div class="training-data-content">${displayContent}</div>
            </div>
        `;
    }).join('');
}

/**
 * Escape HTML helper function (also available in components.js)
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Add training data
 */
async function addTrainingData(type) {
    try {
        let data = {};

        if (type === 'ddl') {
            const ddl = document.getElementById('ddl-input').value.trim();
            if (!ddl) {
                alert('Please enter DDL');
                return;
            }
            data = { ddl };
        } else if (type === 'documentation') {
            const documentation = document.getElementById('doc-input').value.trim();
            if (!documentation) {
                alert('Please enter documentation');
                return;
            }
            data = { documentation };
        } else if (type === 'sql') {
            const question = document.getElementById('sql-question-input').value.trim();
            const sql = document.getElementById('sql-input').value.trim();
            if (!question || !sql) {
                alert('Please enter both question and SQL');
                return;
            }
            data = { question, sql };
        }

        await api.train(type, data);

        // Clear inputs
        if (type === 'ddl') {
            document.getElementById('ddl-input').value = '';
        } else if (type === 'documentation') {
            document.getElementById('doc-input').value = '';
        } else if (type === 'sql') {
            document.getElementById('sql-question-input').value = '';
            document.getElementById('sql-input').value = '';
        }

        // Reload training data
        await loadAndRenderTrainingData();

        // Switch to view tab
        switchTab('view');

        alert('Training data added successfully!');
    } catch (error) {
        console.error('Failed to add training data:', error);
        alert('Failed to add training data: ' + error.message);
    }
}

/**
 * Delete training data
 */
async function deleteTrainingData(id) {
    if (!confirm('Are you sure you want to delete this training data?')) {
        return;
    }

    try {
        await api.removeTrainingData(id);
        await loadAndRenderTrainingData();
        alert('Training data deleted successfully!');
    } catch (error) {
        console.error('Failed to delete training data:', error);
        alert('Failed to delete training data: ' + error.message);
    }
}

/**
 * Switch tabs in modal
 */
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`tab-${tabName}`).classList.add('active');
}

/**
 * Handle training type radio change
 */
function handleTrainingTypeChange() {
    const selectedType = document.querySelector('input[name="train-type"]:checked').value;

    document.getElementById('form-ddl').style.display = selectedType === 'ddl' ? 'flex' : 'none';
    document.getElementById('form-documentation').style.display = selectedType === 'documentation' ? 'flex' : 'none';
    document.getElementById('form-sql').style.display = selectedType === 'sql' ? 'flex' : 'none';
}

// Make functions globally accessible
window.askQuestion = askQuestion;
window.loadHistoryItem = loadHistoryItem;
window.copyToClipboard = copyToClipboard;
window.downloadCSV = downloadCSV;
window.provideSQLFeedback = provideSQLFeedback;
window.toggleTheme = toggleTheme;
window.toggleLanguage = toggleLanguage;
window.toggleSidebar = toggleSidebar;
window.openTrainingModal = openTrainingModal;
window.closeTrainingModal = closeTrainingModal;
window.addTrainingData = addTrainingData;
window.deleteTrainingData = deleteTrainingData;

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
