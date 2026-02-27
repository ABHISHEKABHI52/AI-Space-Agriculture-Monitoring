# Setup Script
# Automated setup for Plant Health Monitoring System

Write-Host "===============================================" -ForegroundColor Green
Write-Host "   Plant Health Monitoring System Setup" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check pip
Write-Host "Checking pip..." -ForegroundColor Cyan
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ Found pip" -ForegroundColor Green
} catch {
    Write-Host "✗ pip not found! Please install pip" -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Create directory structure
Write-Host ""
Write-Host "Creating directory structure..." -ForegroundColor Cyan

$directories = @(
    "data\raw\control",
    "data\raw\low_water",
    "data\raw\low_light",
    "data\processed",
    "data\features",
    "models\trained",
    "models\training_logs",
    "reports\figures",
    "reports\results",
    "demo\sample_images"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "✓ Directory structure created" -ForegroundColor Green

# Check if training data exists
Write-Host ""
Write-Host "Checking training data..." -ForegroundColor Cyan

if (Test-Path "data\plant_dataset.csv") {
    Write-Host "✓ Training data found" -ForegroundColor Green
    
    # Offer to train model
    Write-Host ""
    $response = Read-Host "Would you like to train the model now? (y/n)"
    
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host ""
        Write-Host "Training model..." -ForegroundColor Cyan
        python train_model.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Model trained successfully" -ForegroundColor Green
        } else {
            Write-Host "⚠ Model training encountered issues" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "ℹ Training data not found (optional)" -ForegroundColor Yellow
    Write-Host "  You can add data later to data\plant_dataset.csv" -ForegroundColor Gray
}

# Setup complete
Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "   Setup Complete!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run dashboard: python run_dashboard.py" -ForegroundColor White
Write-Host "  2. Or use Streamlit: streamlit run app\streamlit_app.py" -ForegroundColor White
Write-Host "  3. Try demo mode first for a quick tour" -ForegroundColor White
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  - Quick Start: QUICKSTART.md" -ForegroundColor White
Write-Host "  - Full Guide: README.md" -ForegroundColor White
Write-Host ""
Write-Host "Happy monitoring! 🌱🚀" -ForegroundColor Green
