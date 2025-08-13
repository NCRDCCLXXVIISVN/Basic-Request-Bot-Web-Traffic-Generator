# 🚀 Request Bot - Web Traffic Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

**A comprehensive web traffic generation tool collection with GUI interface for testing and educational purposes.**

## ⚠️ **IMPORTANT DISCLAIMER**

**This traffic bot is created for TESTING and EDUCATIONAL purposes only.** 

- ✅ **Current Status**: The bot actively sends direct requests to target URLs
- ⚠️ **Google Search**: You may encounter various errors when using Google search functionality
- 🔒 **Responsibility**: Usage is entirely at the user's own risk and responsibility
- 📚 **Purpose**: Designed for learning web automation, rate limiting, and HTTP request handling
- 🚫 **Not for**: Malicious activities, DDoS attacks, or violating website terms of service

**Please use responsibly and respect website policies and rate limits.**

---

## 🌟 Features

- **🎯 Direct Bot**: Sends direct HTTP requests to target URLs
- **🍪 Cookie Bot**: Handles requests with cookie management
- **🔍 Google Bot**: Searches Google and clicks on target websites from results
- **🖥️ GUI Interface**: User-friendly graphical interface built with Flet
- **⛔ Safe Stop**: All bots support CTRL+C for safe termination
- **🌐 Proxy Support**: Multi-proxy rotation for distributed requests
- **⚡ Multi-Threading**: High-performance parallel processing
- **🛡️ Rate Limiting**: Built-in token bucket algorithm to prevent rate limit violations
- **📊 Real-time Stats**: Live request statistics and success rates

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/smtozkn06/Basic-Request-Bot-Web-Traffic-Generator.git
cd Basic-Request-Bot-Web-Traffic-Generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### GUI Mode (Recommended)

```bash
python main_gui.py
```

**Interface Options:**
- **📋 Proxy List**: Enter one proxy per line (optional)
- **🔢 Thread Count**: Set concurrent request threads
- **🎯 Target URL**: Destination website for traffic
- **🔍 Search Query**: Search term for Google bot
- **⚙️ Settings**: Configure delays, timeouts, and rate limits

### Command Line Mode

```bash
# Direct traffic bot
python Module/direct.py

# Cookie-based bot
python Module/Cookie_Search.py

# Google search bot
python Module/google.py
```

## 🤖 Bot Types

### 1. Direct Bot (`direct.py`)
**🎯 Direct Bot** (`direct.py`)
- Sends direct HTTP requests to target URLs
- Fastest and simplest method
- Full proxy support included
- Ideal for basic traffic generation

**🍪 Cookie Bot** (`Cookie_Search.py`)
- Reads cookies from `all_cookies.txt` file
- Sends requests with cookie authentication
- Perfect for session-based websites
- Maintains user session state

**🔍 Google Bot** (`google.py`)
- Searches Google with specified terms
- Finds target site in search results
- Simulates organic traffic patterns
- Advanced URL matching algorithms

## ⚙️ Configuration

### 🌐 Proxy Format
```
http://username:password@proxy-server:port
https://proxy-server:port
socks5://username:password@proxy-server:port
```

### 🍪 Cookie Format (`all_cookies.txt`)
```
# Netscape HTTP Cookie File
.example.com	TRUE	/	FALSE	1234567890	session_id	abc123
.example.com	TRUE	/	FALSE	1234567890	auth_token	xyz789
```

### 🔧 Advanced Settings

- **Thread Count**: 1-100 (recommended: 5-20)
- **Request Delay**: 0.1-10 seconds
- **Timeout**: 5-30 seconds
- **Retry Attempts**: 1-5
- **Token Bucket**: Rate limiting configuration

## 📁 Project Structure

```
Request-Bot/
├── 📄 main_gui.py          # Main GUI application
├── 📁 Module/
│   ├── 🎯 direct.py        # Direct traffic bot
│   ├── 🍪 Cookie_Search.py # Cookie-based bot
│   └── 🔍 google.py        # Google search bot
├── 📁 Utils/
│   ├── 🛡️ token_bucket.py  # Rate limiting
│   └── 🔧 helpers.py       # Utility functions
├── 📄 requirements.txt     # Dependencies
├── 📄 all_cookies.txt      # Cookie storage
└── 📄 README.md           # This file
```

## 🛡️ Security & Legal

### ⚠️ Important Notes
- **Educational Purpose**: This tool is for learning and testing only
- **Respect Rate Limits**: Don't overwhelm target servers
- **Follow ToS**: Respect website terms of service
- **No Malicious Use**: Not intended for harmful activities
- **User Responsibility**: All usage is at your own risk

### 🔒 Best Practices
- Start with low thread counts (5-10)
- Use appropriate delays between requests
- Monitor target server response
- Stop if you encounter errors
- Use proxies to distribute load

## 🐛 Troubleshooting

### Common Issues

**"Token bucket empty" messages**
- Reduce thread count
- Increase request delays
- Check rate limiting settings

**Google search errors**
- Use different search queries
- Enable proxy rotation
- Reduce request frequency

**Connection timeouts**
- Check internet connection
- Verify proxy settings
- Increase timeout values

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions, issues, or suggestions:
- 🐛 [Report Issues](https://github.com/yourusername/Request-Bot/issues)
- 💬 [Discussions](https://github.com/yourusername/Request-Bot/discussions)
- 📧 Email: support@requestbot.com

## ⭐ Acknowledgments

- Built with Python and Flet framework
- Uses advanced rate limiting algorithms
- Inspired by web automation testing needs

---

**⚠️ Remember: Use responsibly and ethically. This tool is for educational and testing purposes only.**

## 🔧 Technical Details

- **User Agent**: Android Chrome browser simulation
- **Random Delays**: Randomized delays between requests
- **Error Handling**: Automatic retry on failures
- **Thread Safety**: Safe multi-threading implementation
- **Signal Handling**: Graceful shutdown with CTRL+C
- **Rate Limiting**: Token bucket algorithm implementation
- **SSL Context**: Secure HTTPS connections
- **Proxy Rotation**: Automatic proxy switching

## 📊 Performance Metrics

- **Request Rate**: Up to 100 requests/second (with proper configuration)
- **Success Rate**: 85-95% (depends on target and settings)
- **Memory Usage**: ~50-100MB (varies with thread count)
- **CPU Usage**: Low to moderate (optimized for efficiency)

## 🔄 Version History

- **v2.0**: Added GUI interface and token bucket rate limiting
- **v1.5**: Improved Google search bot with better URL matching
- **v1.0**: Initial release with basic traffic generation

---

**Made with ❤️ by Request Bot Team**
