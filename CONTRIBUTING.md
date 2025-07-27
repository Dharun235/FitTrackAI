# Contributing to FitTrackAI

Thank you for your interest in contributing to FitTrackAI! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker
- Provide detailed descriptions of the problem
- Include steps to reproduce the issue
- Mention your operating system and Python version

### Suggesting Features
- Open a feature request issue
- Describe the feature and its benefits
- Provide use cases and examples
- Consider implementation complexity

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Git

### Local Development
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/FitTrackAI.git
   cd FitTrackAI
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   python app.py
   ```

## 📋 Code Style Guidelines

### Python
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

### JavaScript
- Use consistent indentation (2 spaces)
- Follow ES6+ conventions
- Add comments for complex logic
- Use meaningful variable names

### HTML/CSS
- Use semantic HTML elements
- Follow BEM naming convention for CSS
- Keep CSS organized and commented
- Ensure responsive design

## 🧪 Testing

### Running Tests
```bash
python -m pytest tests/
```

### Writing Tests
- Create test files in the `tests/` directory
- Use descriptive test names
- Test both success and error cases
- Mock external dependencies

## 📝 Documentation

### Code Documentation
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Document complex algorithms
- Update README.md for new features

### API Documentation
- Document all API endpoints
- Include request/response examples
- Specify data types and formats
- Add error handling information

## 🔧 Project Structure

```
FitTrackAI/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   └── index.html       # Main chat interface
├── data/                # Data directory
│   └── db/             # Database files
├── tests/               # Test files
├── docs/                # Documentation
├── README.md            # Project documentation
├── CONTRIBUTING.md      # This file
├── LICENSE              # MIT License
└── .gitignore           # Git ignore rules
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Add unit tests for core functionality
- [ ] Implement real LLM integration (Ollama, HuggingFace)
- [ ] Add data export functionality
- [ ] Improve error handling and user feedback

### Medium Priority
- [ ] Add more visualization types
- [ ] Implement user authentication
- [ ] Add goal setting and tracking
- [ ] Create mobile-responsive improvements

### Low Priority
- [ ] Add social sharing features
- [ ] Implement data backup/restore
- [ ] Add multi-language support
- [ ] Create admin dashboard

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Operating system and version
   - Python version
   - Browser (if applicable)
   - Package versions

2. **Bug Description**
   - Clear description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)

3. **Additional Context**
   - When did the issue start?
   - Does it happen consistently?
   - Any recent changes that might have caused it?

## 💡 Feature Requests

When suggesting features:

1. **Feature Description**
   - Clear explanation of the feature
   - Use cases and benefits
   - How it fits into the project

2. **Implementation Ideas**
   - Suggested approach
   - Technical considerations
   - Potential challenges

3. **Priority Level**
   - High/Medium/Low priority
   - Impact on users
   - Development effort required

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For general questions and ideas
- **Documentation**: Check README.md and inline docs

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📄 License

By contributing to FitTrackAI, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to FitTrackAI! 🎉 