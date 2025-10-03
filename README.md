# TikTok Affiliate Shop

A desktop application for managing TikTok affiliate shops, automating bot operations, and handling shop/product data. Built with Python and wxPython, supporting both Windows and cross-platform usage.

## Features

- User authentication and login panel
- Shop management (add, edit, delete shops)
- Product management
- Reporting and analytics panel
- Automated TikTok bot (country-specific logic for US/UK)
- Data storage via SQLite and JSON
- Modern GUI using wxPython
- Packaged for distribution with PyInstaller

## Project Structure

```
├── main.py                  # Entry point, wxPython GUI
├── login_panel.py           # Login screen
├── home_panel.py            # Home dashboard
├── shop_panel.py            # Shop management
├── reporting_panel.py       # Reporting/analytics
├── add_shop_dialog.py       # Dialog for adding shops
├── products_dialog.py       # Dialog for managing products
├── db_utils.py              # Database utilities (SQLite)
├── storage_utils.py         # File/data storage utilities
├── uploadfile.py            # File upload logic
├── shops.db                 # SQLite database
├── shops_data.json          # JSON data storage
├── assets/                  # Images and resources
├── icons/                   # Application icons
├── Tiktok_Bot_merge/        # Bot scripts and helpers
│   ├── TikTok.py            # Main bot runner
│   ├── botUS.py, botUK.py   # Country-specific bots
│   ├── ...                  # Helpers, batch messaging, captcha
├── build/                   # PyInstaller build output
├── myenv/, Python311/       # Python environments
├── requirements.txt         # Python dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Hassan-Arslan-Amir/TikTok-Affiliate-Shop.git
   cd TikTok-Affiliate-Shop
   ```
2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv myenv
   myenv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python main.py
   ```

## Packaging

To build a standalone executable (Windows):

```
pyinstaller --onefile --windowed main.py
```

Or use the provided `.spec` files for custom builds.

## Usage

- Launch the app and log in.
- Manage shops and products via the GUI.
- Start/stop the TikTok bot from the relevant panel.
- View reports and analytics.

## Contributing

Pull requests and suggestions are welcome!

## License

MIT License
