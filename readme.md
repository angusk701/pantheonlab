## Project Structure

```
project/
├── backend/
│   ├── appCombine.py
│   └── api_keys.py (you need to create this)
├── frontend/
│     └── frontend.html
├── readme.md
└── requirements.txt

```

## Backend Setup

### Prerequisites
- Python 3.7+
- Required Python packages (install via pip):
  ```bash
  pip install -r  requirements.txt
  ```
- API keys for Unsplash, Pixabay, and Storyblocks

### Configuration

1. Create an `api_keys.py` file in the `backend` directory with the following content:
   ```python
   # Replace with your actual API keys
   unsplash_key = "your_unsplash_access_key"
   pixabay_key = "your_pixabay_api_key"
   storyblocks_pubkey = "your_storyblocks_public_key"
   storyblocks_privkey = "your_storyblocks_private_key"
   ```

### Running the Backend

Navigate to the backend directory and run the Python script:
```bash
cd backend
python appCombine.py
```

The script will prompt you to enter a search term, then fetch images from all three services.

## Frontend Setup

### Prerequisites
- Visual Studio Code
- Live Server extension for VS Code

### Installation

1. Install the Live Server extension in VS Code:
   - Open VS Code
   - Go to Extensions (or press `Ctrl+Shift+X`)
   - Search for "Live Server"
   - Click Install

### Running the Frontend

1. Open the project folder in VS Code.
2. Navigate to the `frontend` directory.
3. Right-click on the `frontend.html` file.
4. Select **"Open with Live Server"**.
5. The application will open in your default web browser.

## License

[MIT License](LICENSE)
