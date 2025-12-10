# Daily Remote Frontend Job Alert

This script automates the process of finding and reporting remote frontend developer jobs. It fetches job listings from various sources, filters them for relevance, and sends a daily summary email.

## Features

- **Multi-Source Aggregation:** Fetches jobs from multiple platforms:
    - Arbeitnow
    - Remotive
    - Remote.co
    - Wellfound (formerly AngelList)
    - WeWorkRemotely
- **Frontend Focused:** Filters jobs for frontend-related keywords (e.g., "frontend", "react", "vue", "javascript").
- **Free-to-Apply Detection:**  Identifies and flags jobs that are likely free to apply to, helping to avoid paid application platforms.
- **HTML Email Reports:** Generates a clean, easy-to-read HTML email with the aggregated job listings.
- **Duplicate Removal:** Ensures the final list of jobs is unique.
- **Dry Run Mode:** Allows you to test the script without sending actual emails.

## How to Use

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Easysoul1/Daily-Job-Report.git
    cd Daily-Job-Report
    ```

3.  **Create a `.env` file:**
    Create a `.env` file in the root of the project and add the following variables:
    ```
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASS=your_gmail_app_password
    DRY_RUN=1
    ```
    - `EMAIL_USER`: Your Gmail address.
    - `EMAIL_PASS`: Your Gmail App Password (not your regular password).
    - `DRY_RUN`: Set to `1` to run the script without sending an email (logs to console). Set to `0` to send the email.

4.  **Run the script:**
    ```bash
    python daily_job_alert.py
    ```

## Dependencies

The script relies on the following Python libraries:

- `requests`
- `beautifulsoup4`
- `python-dotenv`

You can install them using pip:
```bash
pip install requests beautifulsoup4 python-dotenv
```
