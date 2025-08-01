# 🚀 Deploy AI Resume Analyzer Pro on Render

This guide will help you deploy your AI Resume Analyzer Pro application on Render.

## 📋 Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **OpenAI API Key**: Get your API key from [OpenAI](https://platform.openai.com/api-keys)

## 🛠️ Deployment Steps

### Step 1: Prepare Your Repository

Make sure your repository has these files:
- `app.py` (main application)
- `requirements.txt` (dependencies)
- `render.yaml` (Render configuration)
- `Procfile` (process file)
- `runtime.txt` (Python version)
- All your modules (`extractor/`, `utils/`, `templates/`)

### Step 2: Deploy on Render

#### Option A: Using Render Dashboard (Recommended)

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign in with your account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure the Service**
   - **Name**: `ai-resume-analyzer-pro`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add variable: `OPENAI_API_KEY` = `your_openai_api_key_here`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (5-10 minutes)

#### Option B: Using render.yaml (Blue-Green Deployment)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment files"
   git push origin main
   ```

2. **Deploy via Render Dashboard**
   - Connect your repository
   - Render will automatically detect `render.yaml`
   - Configure environment variables
   - Deploy

### Step 3: Configure Environment Variables

In your Render dashboard, add these environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `OPENAI_API_KEY` | `sk-...` | Your OpenAI API key |
| `PYTHON_VERSION` | `3.9.0` | Python version (optional) |

### Step 4: Test Your Deployment

1. **Check Build Logs**
   - Monitor the build process in Render dashboard
   - Look for any errors in the logs

2. **Test the Application**
   - Visit your app URL (e.g., `https://ai-resume-analyzer-pro.onrender.com`)
   - Test all features: resume upload, LinkedIn analysis, etc.

## 🔧 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for correct versions
   - Ensure all dependencies are compatible
   - Check build logs for specific errors

2. **App Won't Start**
   - Verify start command in Procfile
   - Check if port is correctly set to `$PORT`
   - Ensure `app.py` is the correct entry point

3. **OpenAI API Errors**
   - Verify `OPENAI_API_KEY` is set correctly
   - Check if API key has sufficient credits
   - Ensure API key is valid

4. **File Upload Issues**
   - Check if temporary directories are writable
   - Verify file size limits
   - Test with different file formats

### Performance Optimization

1. **Enable Auto-Deploy**
   - Set up automatic deployments from GitHub
   - Configure branch protection rules

2. **Monitor Usage**
   - Check Render dashboard for resource usage
   - Monitor API calls to OpenAI

3. **Scale if Needed**
   - Upgrade to paid plan for better performance
   - Consider caching strategies

## 📊 Monitoring

### Render Dashboard Features
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, and network usage
- **Events**: Deployment and runtime events
- **Health Checks**: Automatic health monitoring

### Custom Monitoring
- Add logging to your app for better debugging
- Monitor OpenAI API usage and costs
- Track user interactions and errors

## 🔒 Security Considerations

1. **Environment Variables**
   - Never commit API keys to Git
   - Use Render's environment variable system
   - Rotate API keys regularly

2. **File Uploads**
   - Validate file types and sizes
   - Implement proper error handling
   - Clean up temporary files

3. **Rate Limiting**
   - Implement rate limiting for API calls
   - Monitor usage to prevent abuse
   - Set up alerts for unusual activity

## 🚀 Advanced Configuration

### Custom Domain
1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain and configure DNS

### SSL Certificate
- Render provides automatic SSL certificates
- No additional configuration needed

### Database Integration (Future)
- Add PostgreSQL service if needed
- Configure database connections
- Set up data persistence

## 📞 Support

If you encounter issues:

1. **Check Render Documentation**: [docs.render.com](https://docs.render.com)
2. **Review Build Logs**: Look for specific error messages
3. **Test Locally**: Ensure app works locally first
4. **Community Support**: Use Render's community forums

## 🎉 Success!

Once deployed, your AI Resume Analyzer Pro will be available at:
`https://your-app-name.onrender.com`

Share the URL with users and start analyzing resumes! 🚀 