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
    scrollToBottom();

    try {
        // Call the all-in-one query endpoint
        const response = await api.query(question);

        // Add assistant message
        state.messages.push({
            type: 'assistant',
            data: response,
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
        scrollToBottom();
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
        scrollToBottom();
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
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
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

// Make functions globally accessible
window.askQuestion = askQuestion;
window.loadHistoryItem = loadHistoryItem;
window.copyToClipboard = copyToClipboard;
window.downloadCSV = downloadCSV;
window.toggleTheme = toggleTheme;
window.toggleLanguage = toggleLanguage;

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
