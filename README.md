# TikTok Affiliate Shop

A comprehensive desktop application for managing TikTok affiliate shops with automated bot operations, user management, and analytics. Built with Python and wxPython, featuring Selenium-based automation for TikTok affiliate marketing.

## 🚀 Features

### Desktop Application

- **User Authentication** - Secure login panel with user management
- **Shop Management** - Add, edit, delete, and monitor affiliate shops
- **Product Management** - Handle product catalogs and commission settings
- **CSV Upload** - Bulk import usernames and creator lists
- **Reporting Dashboard** - Analytics and performance tracking
- **Modern GUI** - Built with wxPython for cross-platform compatibility

### TikTok Bot Automation

- **Multi-Region Support** - Separate bots for US and UK markets
- **Creator Invitation** - Automated bulk invitations to TikTok creators
- **Smart Retry Logic** - Handles captchas, rate limits, and errors
- **Batch Processing** - Process creators in configurable batches
- **Cookie Management** - Persistent login sessions
- **Human-like Behavior** - Randomized delays and human typing simulation

### Data Management

- **SQLite Database** - Reliable local data storage
- **JSON Configuration** - Flexible settings and shop data
- **User Processing** - Track processed/unprocessed creators
- **Commission Tracking** - Monitor affiliate performance

## 📁 Project Structure

```
├── main.py                    # Main application entry point
├── login_panel.py             # User authentication interface
├── home_panel.py              # Main dashboard
├── shop_panel.py              # Shop management interface
├── reporting_panel.py         # Analytics and reporting
├── add_shop_dialog.py         # Shop creation dialog
├── products_dialog.py         # Product management dialog
├── uploadfile.py              # CSV upload functionality
├── db_utils.py                # Database operations
├── shops.db                   # SQLite database
├── assets/                    # Application assets
├── icons/                     # Application icons
└── Tiktok_Bot_merge/          # Bot automation modules
    ├── botUK.py              # UK TikTok bot
    ├── botUS.py              # US TikTok bot
    ├── helper.py             # Bot utility functions
    ├── utils.py              # General utilities
    ├── xpaths.py             # Web element selectors
    ├── slider_captcha.py     # Captcha solving
    ├── UK_batch_message.py   # UK batch messaging
    ├── US_batch_message.py   # US batch messaging
    └── login.py              # Bot authentication
```

## 🛠️ Installation

### Prerequisites

- Python 3.11 or higher
- Chrome browser (for bot automation)
- Windows/macOS/Linux

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Hassan-Arslan-Amir/TikTok-Affiliate-Shop.git
   cd TikTok-Affiliate-Shop
   ```

2. **Create virtual environment**

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r "Extra Files/requirements.txt"
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 📋 Dependencies

Key dependencies include:

- `wxPython` - GUI framework
- `selenium` - Web automation
- `sqlite3` - Database
- `requests` - HTTP requests
- `pandas` - Data processing
- `discord.py` - Discord integration (optional)

See `Extra Files/requirements.txt` for complete list.

## 🤖 Bot Usage

### Running TikTok Bots

**UK Bot:**

```bash
cd Tiktok_Bot_merge
python botUK.py <shop_name>
```

**US Bot:**

```bash
cd Tiktok_Bot_merge
python botUS.py <shop_name>
```

### Bot Features

- **Automated Login** - Uses saved cookies or manual login
- **Creator Search** - Find and invite TikTok creators
- **Product Assignment** - Automatically assign products to invitations
- **Free Sample Handling** - Configure free sample options
- **Bulk Processing** - Handle multiple creators efficiently
- **Error Recovery** - Robust error handling and retry logic

## 💾 Database Schema

The application uses SQLite with the following key tables:

- **Shops** - Store shop configurations and settings
- **Users** - Track creator usernames and processing status
- **Products** - Product catalog with commission rates
- **Invitations** - Invitation history and details

## 🔧 Configuration

### Shop Types

- **Target Write** - Direct invitation campaigns
- **Open Colab** - Open collaboration campaigns

### CSV Upload Format

The application accepts CSV files with creator usernames. Supported column names:

- `names` or `Names` - Creator usernames
- Additional columns ignored

### Environment Variables

- `DISCORD_BOT_TOKEN` - Discord bot integration (optional)

## 📊 Features Overview

### Desktop Application Features

- ✅ Multi-shop management
- ✅ User authentication
- ✅ CSV bulk upload
- ✅ Product management
- ✅ Reporting dashboard
- ✅ Database integration

### Bot Features

- ✅ Multi-region support (US/UK)
- ✅ Automated creator invitations
- ✅ Captcha handling
- ✅ Cookie management
- ✅ Human-like automation
- ✅ Batch processing
- ✅ Error recovery

## 🚨 Important Notes

1. **Chrome Browser Required** - Ensure Chrome is installed for bot functionality
2. **Rate Limiting** - Bots include delays to respect TikTok's rate limits
3. **Cookie Security** - Login cookies are stored locally for session management
4. **Legal Compliance** - Ensure bot usage complies with TikTok's Terms of Service

## 🏗️ Building Executable

To create a standalone executable:

```bash
pyinstaller "TikTok Affiliate Shop.spec"
```

The executable will be created in the `dist/` directory.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and legitimate affiliate marketing purposes only. Users are responsible for complying with TikTok's Terms of Service and applicable laws. The developers are not responsible for any misuse of this software.

## 📞 Support

For issues and questions:

- Create an issue on GitHub
- Check the documentation in `Extra Files/`
- Review the user guide: `How to use the TikTok Affiliate Shop.pdf`
  ├── assets/ # Images and resources
  ├── icons/ # Application icons
  ├── Tiktok_Bot_merge/ # Bot scripts and helpers
  │ ├── TikTok.py # Main bot runner
  │ ├── botUS.py, botUK.py # Country-specific bots
  │ ├── ... # Helpers, batch messaging, captcha
  ├── build/ # PyInstaller build output
  ├── myenv/, Python311/ # Python environments
  ├── requirements.txt # Python dependencies

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
```
