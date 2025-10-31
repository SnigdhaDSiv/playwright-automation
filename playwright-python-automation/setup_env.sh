#!/bin/bash
# Set up script
set -e  # Exit immediately if any command fails
echo "Setting up Python virtual environment..."
# Create venv if not exists
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  echo "Virtual environment created."
else
  echo "Virtual environment already exists."
fi

# Activate venv
source .venv/bin/activate
echo "Virtual environment activated."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip install -r requirements.txt
else
  echo "No requirements.txt found. Installing Playwright and pytest manually..."
  pip install playwright pytest pytest-xdist pytest-html python-dotenv
fi

# Install Playwright browsers
echo "Installing Playwright browsers..."
python -m playwright install

# Verify installations
echo "Verifying setup..."
python -m pytest --version || { echo "pytest not found!"; exit 1; }
python -m playwright --version || { echo "playwright not found!"; exit 1; }

echo "Setup complete!"
python -c "import playwright; print('Playwright ready!')"
