
# 🚀 Aloy - AN Engineer's Intent Compiler

![Aloy Demo](assets/aloy-demo.gif)

> **"Stop writing the same Docker and CI/CD files over and over again."**

Turn your Python project into a production-ready, containerized application **in 30 seconds** using AI. No more copy-pasting outdated Dockerfiles or wrestling with YAML syntax.

---

## 🤔 What Problem Does This Solve?

**The Problem:** Manually writing Dockerfiles, .dockerignore, and CI/CD configs for every new Python project is a slow, error-prone, 30-minute tax on developer productivity.

**The Solution:** Aloy automates this entire process in 30 seconds, generating production-grade, secure, and optimized files from a single command.

---

## 🎯 What You Get

When you run Aloy on your Python project, you'll instantly get:

### 📦 Dockerfile
- **AI-Generated:** Analyzes your project to create a bespoke, multi-stage build.
- **Secure:** Enforces non-root user and security best practices by default.
- **Optimized:** Smart layer caching and framework detection (Flask, FastAPI, or general scripts) for faster builds.

### 🚫 .dockerignore
- **Comprehensive:** Excludes git files, IDE configs, cache files, and sensitive files.
- **Security-Focused:** Keeps secrets and credentials out of your image.
- **Build Optimization:** Reduces image size and build time.

### 🔄 gitlab-ci.yml
- **Production-Ready:** Two-stage pipeline (build → push) with Docker-in-Docker configuration.
- **Industry Standard:** Follows best practices for CI/CD.
- **Easy to Use:** Ready-to-use template with clear instructions.

---

## 🏃‍♂️ Quick Start (5 Minutes)

### Step 1: Get Your Environment Ready

**Clone and set up:**
```bash
git clone https://github.com/your-username/intent-compiler.git
cd intent-compiler

# Create virtual environment (recommended)
python -m venv venv

# Activate it
# On Windows:
.\venv\Scripts\Activate.ps1
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get Your API Key

This tool uses **Google Gemini AI** (it's free for most usage). 

1. 🌐 Go to [Google AI Studio](https://aistudio.google.com/)
2. 🔑 Create a free API key
3. 📋 Copy your key

**Set the environment variable:**
```bash
# On Windows (PowerShell):
$env:GOOGLE_API_KEY="your-actual-api-key-here"

# On Mac/Linux:
export GOOGLE_API_KEY="your-actual-api-key-here"
```


### Step 3: Run It On Your Project

```bash
python -m compiler.main .
```

**Optional:**
Use a different AI model with the `--model` flag:
```bash
python -m compiler.main /your/project --model gemini-1.5-pro
```

**That's it!** 🎉 Check your project folder - you now have production-ready Docker and CI/CD files.

---

## 💡 How It Works

1. **Reads your `requirements.txt`** to understand what kind of app you're building
2. **Scans your project files** to get additional context
3. **Uses AI (Gemini)** to generate expert-level configuration files
4. **Writes the files** directly to your project directory

The tool is smart! As long as you have a `requirements.txt`, it will work—no matter your project structure.

---

## 📋 Requirements

- **Python 3.8+**
- **A `requirements.txt` file** in your project
- **Google Gemini API key** (free)
- **Internet connection** (for AI calls)

---

## 🚨 Important Notes

### 🔑 Security
- **Never commit your API key** to version control
- The generated files use **security best practices** (non-root users, etc.)
- Review generated files before using in production

### 🎯 Accuracy
- The AI is **very good** but not perfect
- **Always review** the generated files
- **Test your Docker build** before deploying
- **Update registry URLs** in the GitLab CI file

### 💰 Cost
- Google Gemini has a **generous free tier**
- Each run costs **~$0.001** (one-tenth of a cent)
- You can generate hundreds of projects for free

---

## 🤝 Contributing

Found a bug? Have an idea? Want to add support for other frameworks?

1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. 💻 Make your changes
4. 🧪 Test thoroughly
5. 📤 Submit a pull request

---

## 📄 License

MIT License - feel free to use this in your projects!

---

## 🆘 Need Help?

**Common Issues:**

**"GOOGLE_API_KEY environment variable not set"**
- Make sure you set the environment variable in the same terminal session
- On Windows, use `$env:GOOGLE_API_KEY="your-key"`

**"requirements.txt not found"**
- The tool must be run on a directory that contains `requirements.txt`
- Make sure you're pointing to the right directory

**"Error calling Gemini API"**
- Check your internet connection
- Verify your API key is valid
- Make sure you haven't exceeded the API rate limits

**Still stuck?** Open an issue on GitHub with:
- Your Python version
- Your operating system  
- The exact error message
- What you were trying to do

---

## 🌟 Star This Project

If this tool saved you time, **please star it** ⭐ - it helps other developers find it!

---

*Made with ❤️ for developers who hate writing the same boilerplate code over and over again.*
