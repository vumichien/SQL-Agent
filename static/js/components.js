/**
 * Detomo SQL AI - UI Components
 * Rendering functions for all UI components
 */

// Translations for bilingual support
const translations = {
    en: {
        askQuestion: 'Ask a question about the database...',
        send: 'Send',
        you: 'You',
        assistant: 'Detomo AI',
        sql: 'SQL Query',
        results: 'Results',
        visualization: 'Visualization',
        copy: 'Copy',
        copied: 'Copied!',
        downloadCSV: 'Download CSV',
        error: 'Error',
        loading: 'Loading...',
        history: 'Query History',
        trainingData: 'Training Data',
        noHistory: 'No query history yet',
        suggestedQuestions: 'Suggested Questions',
        emptyStateTitle: 'Welcome to Detomo SQL AI',
        emptyStateSubtitle: 'Ask a question in natural language to query your database',
        followupQuestions: 'Follow-up Questions',
        retry: 'Retry',
        sqlCorrect: 'Is this SQL correct?',
        thumbsUp: 'Yes, this SQL is correct',
        thumbsDown: 'No, this SQL is incorrect',
        feedbackThanks: 'Thank you for your feedback!',
    },
    ja: {
        askQuestion: 'データベースについて質問してください...',
        send: '送信',
        you: 'あなた',
        assistant: 'Detomo AI',
        sql: 'SQLクエリ',
        results: '結果',
        visualization: '可視化',
        copy: 'コピー',
        copied: 'コピーしました！',
        downloadCSV: 'CSVダウンロード',
        error: 'エラー',
        loading: '読み込み中...',
        history: 'クエリ履歴',
        trainingData: 'トレーニングデータ',
        noHistory: 'クエリ履歴がありません',
        suggestedQuestions: '候補の質問',
        emptyStateTitle: 'Detomo SQL AIへようこそ',
        emptyStateSubtitle: '自然言語で質問してデータベースを検索してください',
        followupQuestions: 'フォローアップの質問',
        retry: '再試行',
        sqlCorrect: 'このSQLは正しいですか？',
        thumbsUp: 'はい、正しいです',
        thumbsDown: 'いいえ、間違っています',
        feedbackThanks: 'フィードバックをありがとうございます！',
    },
};

let currentLanguage = 'en';

function setLanguage(lang) {
    currentLanguage = lang;
}

function t(key) {
    return translations[currentLanguage][key] || key;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Format timestamp
 */
function formatTime(date) {
    return new Date(date).toLocaleString(currentLanguage === 'ja' ? 'ja-JP' : 'en-US', {
        hour: '2-digit',
        minute: '2-digit',
    });
}

/**
 * Render empty state
 */
function renderEmptyState() {
    return `
        <div class="empty-state">
            <div class="empty-state-icon">💬</div>
            <h2>${t('emptyStateTitle')}</h2>
            <p>${t('emptyStateSubtitle')}</p>
        </div>
    `;
}

/**
 * Render user message
 */
function renderUserMessage(question) {
    return `
        <div class="message">
            <div class="message-header message-user">
                <span>👤</span>
                <span>${t('you')}</span>
            </div>
            <div class="message-content">
                <div class="message-question">${escapeHtml(question)}</div>
            </div>
        </div>
    `;
}

/**
 * Render SQL block with copy button and validation feedback
 */
function renderSQL(sql, id, question) {
    return `
        <div class="sql-container">
            <div class="sql-header">
                <div class="sql-label">${t('sql')}</div>
                <div class="sql-actions">
                    <button class="copy-button" onclick="copyToClipboard('${id}', \`${escapeHtml(sql).replace(/`/g, '\\`')}\`)">
                        ${t('copy')}
                    </button>
                </div>
            </div>
            <pre class="sql-code">${escapeHtml(sql)}</pre>
            <div class="sql-feedback">
                <span class="feedback-label">${t('sqlCorrect')}</span>
                <button class="feedback-button feedback-positive" onclick="provideSQLFeedback('${id}', '${escapeHtml(question).replace(/'/g, "\\'")}', \`${escapeHtml(sql).replace(/`/g, '\\`')}\`, true)" title="${t('thumbsUp')}">
                    👍
                </button>
                <button class="feedback-button feedback-negative" onclick="provideSQLFeedback('${id}', '${escapeHtml(question).replace(/'/g, "\\'")}', \`${escapeHtml(sql).replace(/`/g, '\\`')}\`, false)" title="${t('thumbsDown')}">
                    👎
                </button>
            </div>
        </div>
    `;
}

/**
 * Render results table
 */
function renderResultsTable(df) {
    if (!df || df.length === 0) {
        return '<p>No results found.</p>';
    }

    const columns = Object.keys(df[0]);
    const rows = df;

    let html = `
        <div class="results-container">
            <div class="sql-label">${t('results')} (${rows.length} rows)</div>
            <table class="results-table">
                <thead>
                    <tr>
                        ${columns.map(col => `<th>${escapeHtml(col)}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
                    ${rows.slice(0, 100).map(row => `
                        <tr>
                            ${columns.map(col => `<td>${escapeHtml(String(row[col] ?? ''))}</td>`).join('')}
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;

    if (rows.length > 100) {
        html += `<p style="margin-top: 8px; color: var(--text-secondary); font-size: 14px;">Showing first 100 of ${rows.length} rows</p>`;
    }

    return html;
}

/**
 * Render Plotly chart
 */
function renderChart(plotlyFigure, containerId) {
    if (!plotlyFigure) {
        return '';
    }

    const chartId = `chart-${containerId}`;

    // Schedule Plotly rendering after DOM update
    setTimeout(() => {
        try {
            const element = document.getElementById(chartId);
            if (element && typeof Plotly !== 'undefined') {
                Plotly.newPlot(chartId, plotlyFigure.data, plotlyFigure.layout, {
                    responsive: true,
                    displayModeBar: true,
                });
            }
        } catch (error) {
            console.error('Failed to render chart:', error);
        }
    }, 100);

    return `
        <div class="chart-container">
            <div class="sql-label">${t('visualization')}</div>
            <div id="${chartId}"></div>
        </div>
    `;
}

/**
 * Render CSV download button
 */
function renderDownloadButton(id) {
    return `
        <button class="download-csv-button" onclick="downloadCSV('${id}')">
            📥 ${t('downloadCSV')}
        </button>
    `;
}

/**
 * Render follow-up questions
 */
function renderFollowupQuestions(questions) {
    if (!questions || questions.length === 0) {
        return '';
    }

    return `
        <div class="suggested-questions">
            <div class="suggested-questions-title">${t('followupQuestions')}</div>
            ${questions.map(q => `
                <div class="suggested-question" onclick="askQuestion('${escapeHtml(q).replace(/'/g, "\\'")}')">
                    ${escapeHtml(q)}
                </div>
            `).join('')}
        </div>
    `;
}

/**
 * Render complete assistant response
 */
function renderAssistantMessage(data) {
    // Handle both response formats: vanna-flask pattern and simple query endpoint
    const {
        id,
        question,
        sql,
        df,                      // vanna-flask pattern
        results,                 // simple query endpoint
        plotly_figure,          // vanna-flask pattern
        visualization,          // simple query endpoint
        error,
        followup_questions
    } = data;

    if (error) {
        return `
            <div class="message">
                <div class="message-header message-assistant">
                    <span>🤖</span>
                    <span>${t('assistant')}</span>
                </div>
                <div class="message-content">
                    <div class="error-message">
                        <div class="error-header">
                            <span class="error-icon">⚠️</span>
                            <strong>${t('error')}</strong>
                        </div>
                        <div class="error-details">
                            ${escapeHtml(error)}
                        </div>
                        ${question ? `
                            <button class="retry-button" onclick="askQuestion('${escapeHtml(question).replace(/'/g, "\\'")}')">
                                🔄 ${t('retry')}
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    // Use df if available, otherwise use results
    const resultsData = df || results;
    // Use plotly_figure if available, otherwise use visualization
    const chartData = plotly_figure || visualization;

    return `
        <div class="message">
            <div class="message-header message-assistant">
                <span>🤖</span>
                <span>${t('assistant')}</span>
            </div>
            <div class="message-content">
                ${sql ? renderSQL(sql, id || 'sql', question) : ''}
                ${resultsData ? renderResultsTable(resultsData) : ''}
                ${resultsData && id ? renderDownloadButton(id) : ''}
                ${chartData ? renderChart(chartData, id || Date.now()) : ''}
                ${followup_questions ? renderFollowupQuestions(followup_questions) : ''}
            </div>
        </div>
    `;
}

/**
 * Render loading message
 */
function renderLoadingMessage() {
    return `
        <div class="message">
            <div class="message-header message-assistant">
                <span>🤖</span>
                <span>${t('assistant')}</span>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <span>${t('loading')}</span>
                </div>
            </div>
        </div>
    `;
}

/**
 * Render history item
 */
function renderHistoryItem(item, isActive = false) {
    return `
        <li class="history-item ${isActive ? 'active' : ''}" onclick="loadHistoryItem('${item.id}')">
            ${escapeHtml(item.question.substring(0, 50))}${item.question.length > 50 ? '...' : ''}
        </li>
    `;
}

/**
 * Render history list
 */
function renderHistoryList(history, activeId = null) {
    if (!history || history.length === 0) {
        return `<p style="color: var(--text-secondary); font-size: 14px;">${t('noHistory')}</p>`;
    }

    return `
        <ul class="history-list">
            ${history.map(item => renderHistoryItem(item, item.id === activeId)).join('')}
        </ul>
    `;
}

/**
 * Render suggested questions
 */
function renderSuggestedQuestions(questions) {
    if (!questions || questions.length === 0) {
        return '';
    }

    return `
        <div class="suggested-questions">
            <div class="suggested-questions-title">${t('suggestedQuestions')}</div>
            ${questions.map(q => `
                <div class="suggested-question" onclick="askQuestion('${escapeHtml(q).replace(/'/g, "\\'")}')">
                    ${escapeHtml(q)}
                </div>
            `).join('')}
        </div>
    `;
}
