# Contributing to HTCondor Tutorial

Thank you for your interest in improving this tutorial! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the issue tracker
2. Create a new issue with:
   - Clear description of the problem or suggestion
   - Steps to reproduce (if applicable)
   - Expected vs. actual behavior
   - Environment details (PIC cluster, Python version, etc.)

### Making Changes

1. **Fork the repository** (if applicable)
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation as needed
4. **Test your changes**:
   - Verify code runs correctly
   - Test on PIC HTCondor cluster if possible
   - Check for linting errors
5. **Commit your changes**:
   - Write clear, descriptive commit messages
   - Reference related issues if applicable
6. **Submit a pull request** (if applicable)

### Code Style

- **Python**: Follow PEP 8 style guide
- **Bash scripts**: Use consistent indentation (2 or 4 spaces)
- **HTCondor files**: Include comments explaining each section
- **Documentation**: Use clear, concise language

### Documentation

When adding new features:

- Update `README.md` if it affects the main workflow
- Update `TUTORIAL.md` for detailed explanations
- Add inline comments to code
- Include examples where helpful

### Testing

Before submitting:

- Test locally if possible
- Verify HTCondor submission works
- Check that outputs are generated correctly
- Ensure no sensitive information is included

## Questions?

For questions about:
- **HTCondor usage**: Check [PIC HTCondor Wiki](https://pwiki.pic.es/index.php?title=HTCondor)
- **This tutorial**: Open an issue for discussion
- **PIC infrastructure**: Contact PIC support at contact@pic.es

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and improve
- Follow PIC's acceptable use policies

Thank you for contributing! 🎉

