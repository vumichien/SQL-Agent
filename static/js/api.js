/**
 * Detomo SQL AI - API Client
 * Handles all API communication with the FastAPI backend
 */

const API_BASE_URL = window.location.origin;

class DetomoAPI {
    constructor() {
        this.baseUrl = API_BASE_URL;
    }

    /**
     * Generic request handler with error handling
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;

        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers,
                },
                ...options,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API request failed: ${endpoint}`, error);
            throw error;
        }
    }

    /**
     * Health check
     */
    async getHealth() {
        return await this.request('/api/v0/health');
    }

    /**
     * All-in-one query: NL → SQL → Results → Visualization
     */
    async query(question) {
        return await this.request('/api/v0/query', {
            method: 'POST',
            body: JSON.stringify({ question }),
        });
    }

    /**
     * Generate suggested questions
     */
    async generateQuestions() {
        return await this.request('/api/v0/generate_questions');
    }

    /**
     * Generate SQL from question (multi-step workflow)
     */
    async generateSQL(question) {
        return await this.request('/api/v0/generate_sql', {
            method: 'POST',
            body: JSON.stringify({ question }),
        });
    }

    /**
     * Run SQL from cache (multi-step workflow)
     */
    async runSQL(id) {
        return await this.request('/api/v0/run_sql', {
            method: 'POST',
            body: JSON.stringify({ id }),
        });
    }

    /**
     * Generate Plotly figure from cache (multi-step workflow)
     */
    async generatePlotlyFigure(id) {
        return await this.request('/api/v0/generate_plotly_figure', {
            method: 'POST',
            body: JSON.stringify({ id }),
        });
    }

    /**
     * Generate follow-up questions
     */
    async generateFollowupQuestions(question, df) {
        return await this.request('/api/v0/generate_followup_questions', {
            method: 'POST',
            body: JSON.stringify({ question, df }),
        });
    }

    /**
     * Load question from cache
     */
    async loadQuestion(id) {
        return await this.request('/api/v0/load_question', {
            method: 'POST',
            body: JSON.stringify({ id }),
        });
    }

    /**
     * Get question history
     */
    async getQuestionHistory() {
        return await this.request('/api/v0/get_question_history');
    }

    /**
     * Get training data
     */
    async getTrainingData() {
        return await this.request('/api/v0/get_training_data');
    }

    /**
     * Add training data
     */
    async train(trainType, data) {
        const payload = {
            train_type: trainType,
        };

        if (trainType === 'ddl') {
            payload.ddl = data;
        } else if (trainType === 'documentation') {
            payload.documentation = data;
        } else if (trainType === 'sql') {
            payload.question = data.question;
            payload.sql = data.sql;
        }

        return await this.request('/api/v0/train', {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    }

    /**
     * Remove training data
     */
    async removeTrainingData(id) {
        return await this.request('/api/v0/remove_training_data', {
            method: 'POST',
            body: JSON.stringify({ id }),
        });
    }

    /**
     * Download CSV
     */
    getDownloadCSVUrl(id) {
        return `${this.baseUrl}/api/v0/download_csv?id=${id}`;
    }
}

// Export singleton instance
const api = new DetomoAPI();
