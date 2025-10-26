# TASK 08: Frontend Setup (Vanna-Flask UI)

**Status**: ⬜ Not Started
**Estimated Time**: 12-16 hours
**Dependencies**: TASK 07 (Extended API endpoints)
**Phase**: 4 - Frontend UI

---

## OVERVIEW

Build web UI for Detomo SQL Agent based on vanna-flask pattern with Detomo branding.

**Reference**: PRD Section 5

---

## OBJECTIVES

1. Create `static/index.html` with SPA structure
2. Add Detomo logo and branding
3. Implement chat interface
4. Add SQL results display with syntax highlighting
5. Add Plotly visualization rendering
6. Create query history sidebar
7. Add training data management UI
8. Implement dark mode
9. Add bilingual support (EN/JP)

---

## FOLDER STRUCTURE

```
static/
├── index.html              # Main SPA entry point
├── detomo_logo.svg        # Detomo branding
├── css/
│   └── styles.css         # Custom styles
└── js/
    ├── app.js             # Main application logic
    ├── api.js             # API client
    └── components.js      # UI components
```

---

## IMPLEMENTATION

Create `static/index.html`:

```html
<!DOCTYPE html>
<html lang="en" class="bg-white dark:bg-slate-900">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Detomo SQL Agent</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div id="app">
        <!-- Header -->
        <header class="bg-blue-600 text-white p-4">
            <h1 class="text-2xl font-bold">Detomo SQL Agent</h1>
        </header>

        <!-- Main content -->
        <main class="container mx-auto p-4">
            <div id="chat-container"></div>
            <div id="input-container">
                <input type="text" id="question-input" placeholder="Ask a question..." />
                <button id="send-button">Send</button>
            </div>
        </main>
    </div>

    <script src="/static/js/app.js"></script>
</body>
</html>
```

Implement JavaScript to call API endpoints and render results.

---

## SUCCESS CRITERIA

- [ ] UI accessible at http://localhost:5000
- [ ] Can input NL question → see SQL → see results → see chart
- [ ] All UI components functional
- [ ] Detomo branding applied
- [ ] Dark mode working
- [ ] Bilingual support (EN/JP)

---

**Last Updated**: 2025-10-26
