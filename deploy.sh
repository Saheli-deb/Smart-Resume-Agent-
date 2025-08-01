#!/bin/bash

echo "🚀 AI Resume Analyzer Pro - Render Deployment Script"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin <your-github-repo-url>"
    exit 1
fi

# Check if all required files exist
echo "📋 Checking required files..."

required_files=("app.py" "requirements.txt" "render.yaml" "Procfile" "runtime.txt")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Missing required files:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    exit 1
fi

echo "✅ All required files found!"

# Check if .env file exists and warn about API key
if [ -f ".env" ]; then
    echo "⚠️  .env file found. Make sure to add OPENAI_API_KEY to Render environment variables."
else
    echo "⚠️  No .env file found. You'll need to add OPENAI_API_KEY to Render environment variables."
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Deploy to Render - $(date)"
git push origin main

echo ""
echo "🎉 Code pushed to GitHub!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://dashboard.render.com"
echo "2. Click 'New +' and select 'Web Service'"
echo "3. Connect your GitHub repository"
echo "4. Configure the service:"
echo "   - Name: ai-resume-analyzer-pro"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: streamlit run app.py --server.port \$PORT --server.address 0.0.0.0"
echo "5. Add environment variable: OPENAI_API_KEY = your_api_key"
echo "6. Click 'Create Web Service'"
echo ""
echo "🔗 Your app will be available at: https://your-app-name.onrender.com"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md" 