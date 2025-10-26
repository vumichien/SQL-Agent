# Documentation - Detomo SQL AI

Complete documentation for Detomo SQL AI project.

---

## Documentation Structure

```
docs/
├── api/                          # API Documentation
│   ├── API_DOCUMENTATION.md      # Complete API reference
│   └── BACKEND_SWITCHING.md      # Backend switching guide
│
├── guides/                       # User Guides
│   └── QUICKSTART_API.md         # Quick start guide
│
├── development/                  # Development Documentation
│   ├── CLAUDE.md                 # Claude Code Assistant instructions
│   └── TASK_05_SUMMARY.md        # Task 05 completion summary
│
└── README.md                     # This file
```

---

## Quick Links

### 🚀 Getting Started
- [Quick Start Guide](guides/QUICKSTART_API.md) - Get API running in 5 minutes
- [Main README](../README.md) - Project overview

### 📚 API Documentation
- [API Documentation](api/API_DOCUMENTATION.md) - Complete API reference
- [Backend Switching](api/BACKEND_SWITCHING.md) - How to switch between backends

### 👨‍💻 Development
- [Claude Instructions](development/CLAUDE.md) - Instructions for Claude Code Assistant
- [Task 05 Summary](development/TASK_05_SUMMARY.md) - Task completion details

### 📊 Project Management
- [TASK_MASTER.md](../TASK_MASTER.md) - Overall project progress
- [PRD.md](../PRD.md) - Product Requirements Document

---

## Document Categories

### API Documentation (`docs/api/`)
Complete API reference and backend configuration guides.

**API_DOCUMENTATION.md**
- All 8 API endpoints
- Request/response formats
- Error codes
- Examples with curl

**BACKEND_SWITCHING.md**
- Backend architecture
- Configuration
- Switching between Claude Agent SDK and Anthropic API
- Performance comparison

### Guides (`docs/guides/`)
Step-by-step guides for users.

**QUICKSTART_API.md**
- 5-minute setup
- Basic usage examples
- Common issues and solutions

### Development (`docs/development/`)
Documentation for developers and AI assistants.

**CLAUDE.md**
- Task execution workflow
- Auto-execution mode
- Manual commands
- Task-by-task instructions

**TASK_05_SUMMARY.md**
- Task completion details
- Architecture decisions
- Files created
- Test results

---

## Documentation Standards

### Format
- All documentation in Markdown
- Clear headers and sections
- Code examples with syntax highlighting
- Links to related documents

### Structure
```markdown
# Document Title

Brief description

---

## Section 1
Content...

## Section 2
Content...

---

**Last Updated**: YYYY-MM-DD
```

### Code Examples
```bash
# Bash commands with comments
python app.py
```

```python
# Python code with comments
from app import create_app
```

---

## Updating Documentation

### When to Update
- New features added
- API changes
- Configuration changes
- Bug fixes affecting behavior

### How to Update
1. Edit the relevant markdown file
2. Update "Last Updated" date
3. Add entry to changelog if major change
4. Verify all links still work

---

## Documentation Maintenance

### Regular Tasks
- [ ] Review documentation monthly
- [ ] Update screenshots if UI changes
- [ ] Fix broken links
- [ ] Update version numbers
- [ ] Add new examples

### Quality Checks
- [ ] All code examples work
- [ ] All links functional
- [ ] No outdated information
- [ ] Clear and concise
- [ ] Proper formatting

---

## Contributing

When adding new documentation:
1. Follow existing structure
2. Use clear, concise language
3. Include code examples
4. Add to this README
5. Update relevant sections

---

## Document Index

### API & Usage
| Document | Description | Location |
|----------|-------------|----------|
| API Documentation | Complete API reference | [api/API_DOCUMENTATION.md](api/API_DOCUMENTATION.md) |
| Backend Switching | Backend configuration guide | [api/BACKEND_SWITCHING.md](api/BACKEND_SWITCHING.md) |
| Quick Start | 5-minute setup guide | [guides/QUICKSTART_API.md](guides/QUICKSTART_API.md) |

### Development
| Document | Description | Location |
|----------|-------------|----------|
| Claude Instructions | AI assistant workflow | [development/CLAUDE.md](development/CLAUDE.md) |
| Task 05 Summary | Task completion details | [development/TASK_05_SUMMARY.md](development/TASK_05_SUMMARY.md) |

### Project
| Document | Description | Location |
|----------|-------------|----------|
| README | Project overview | [../README.md](../README.md) |
| PRD | Product requirements | [../PRD.md](../PRD.md) |
| TASK_MASTER | Project progress | [../TASK_MASTER.md](../TASK_MASTER.md) |

---

## Search & Find

### Find by Topic
- **Setup**: Quick Start Guide
- **API**: API Documentation
- **Backends**: Backend Switching
- **Development**: Claude Instructions
- **Testing**: tests/README.md
- **Progress**: TASK_MASTER.md

### Find by Audience
- **End Users**: Quick Start, API Documentation
- **Developers**: All development docs, API docs
- **AI Assistants**: Claude Instructions
- **Project Managers**: TASK_MASTER, PRD

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-26 | Initial documentation structure |

---

**Last Updated**: 2025-10-26
**Maintained By**: Detomo Development Team
