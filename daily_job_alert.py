import os
import sys
import smtplib
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.mime.text import MIMEText
from requests.exceptions import RequestException

# =================== CONFIG =================== #

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
DRY_RUN = os.getenv("DRY_RUN", "1") == "1"  # set to 0 in .env to actually send email

FREE_DOMAINS = {
    "remoteok.com",
    "remotive.com",
    "remotive.io",
    "weworkremotely.com",
    "wellfound.com",
    "angel.co",
    "jobspresso.co",
    "indeed.com",
    "glassdoor.com",
    "builtin.com",
    "linkedin.com",
    "stackoverflow.com",
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

# =================== HELPERS =================== #


def apply_host_from_url(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def is_likely_free_apply(url: str) -> bool:
    host = apply_host_from_url(url)
    if not host:
        return False
    if any(domain in host for domain in FREE_DOMAINS):
        return True
    if "premium" in host or "pay" in host or "subscription" in host:
        return False
    return True


def safe_request(url: str):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        return res
    except RequestException as e:
        raise RuntimeError(f"Network error: {e}") from e


# =================== FETCH JOB SOURCES =================== #


def fetch_remoteok_jobs():
    """Fetch frontend jobs from RemoteOK API"""
    url = "https://remoteok.com/api"
    try:
        res = safe_request(url)
        data = res.json()[1:]
        jobs = []
        for job in data:
            title = job.get("position", "") or ""
            if any(w in title.lower() for w in ["frontend", "front-end", "ui", "react", "web"]):
                company = job.get("company", "Unknown")
                link = job.get("url", "#")
                jobs.append({
                    "company": company,
                    "title": title,
                    "link": link,
                    "keywords": ["remote", "frontend", "web", "developer"],
                    "skills": ["React", "JavaScript", "CSS", "API integration"],
                    "apply_host": apply_host_from_url(link),
                    "free_to_apply": is_likely_free_apply(link)
                })
        return jobs[:5]
    except Exception as e:
        print("RemoteOK error:", e)
        return []


def fetch_remotive_jobs():
    """Fetch frontend jobs from Remotive API"""
    url = "https://remotive.com/api/remote-jobs?category=software-dev"
    try:
        res = safe_request(url)
        data = res.json().get("jobs", [])
        jobs = []
        for job in data:
            title = job.get("title", "") or ""
            if any(w in title.lower() for w in ["frontend", "front-end", "ui", "react", "vue", "web"]):
                company = job.get("company_name", "Unknown")
                link = job.get("url", "#")
                jobs.append({
                    "company": company,
                    "title": title,
                    "link": link,
                    "keywords": ["remote", "frontend", "web", "developer"],
                    "skills": ["React", "Vue", "CSS", "HTML"],
                    "apply_host": apply_host_from_url(link),
                    "free_to_apply": is_likely_free_apply(link)
                })
        return jobs[:5]
    except Exception as e:
        print("Remotive error:", e)
        return []


def fetch_wellfound_jobs():
    """Scrape Wellfound (AngelList) for remote frontend roles"""
    url = "https://wellfound.com/role/remote-frontend-developer-jobs"
    try:
        res = safe_request(url)
        soup = BeautifulSoup(res.text, "html.parser")
        jobs = []
        for link in soup.select("a.styles_component__a__job")[:5]:
            title = (link.text or "").strip()
            href = "https://wellfound.com" + link.get("href")
            company = "Startup (Wellfound)"
            jobs.append({
                "company": company,
                "title": title,
                "link": href,
                "keywords": ["remote", "frontend", "startup"],
                "skills": ["React", "Next.js", "TypeScript"],
                "apply_host": apply_host_from_url(href),
                "free_to_apply": is_likely_free_apply(href)
            })
        return jobs
    except Exception as e:
        print("Wellfound error:", e)
        return []


def fetch_wwr_jobs():
    """Fetch jobs from WeWorkRemotely"""
    url = "https://weworkremotely.com/categories/remote-front-end-programming-jobs"
    try:
        res = safe_request(url)
        soup = BeautifulSoup(res.text, "html.parser")
        jobs = []
        for section in soup.select("section.jobs")[:3]:
            for a in section.select("li a")[:5]:
                href = "https://weworkremotely.com" + a.get("href")
                title = (a.select_one("span.title") or {}).get_text("", strip=True)
                company = (a.select_one("span.company") or {}).get_text("", strip=True)
                if not title:
                    continue
                jobs.append({
                    "company": company or "Unknown",
                    "title": title,
                    "link": href,
                    "keywords": ["frontend", "remote", "javascript"],
                    "skills": ["React", "Vue", "CSS", "HTML"],
                    "apply_host": apply_host_from_url(href),
                    "free_to_apply": is_likely_free_apply(href)
                })
        return jobs
    except Exception as e:
        print("WWR error:", e)
        return []


# =================== JOB AGGREGATION =================== #


def fetch_all_jobs():
    jobs = []
    for func in [fetch_remoteok_jobs, fetch_remotive_jobs, fetch_wellfound_jobs, fetch_wwr_jobs]:
        jobs.extend(func())
    if not jobs:
        raise RuntimeError("No jobs found from any source.")
    return jobs


# =================== EMAIL BUILDING =================== #


def create_html_table(jobs):
    jobs = sorted(jobs, key=lambda j: (not j["free_to_apply"], j["company"]))
    rows = ""
    for i, j in enumerate(jobs, 1):
        rows += f"""
        <tr>
            <td>{i}</td>
            <td><b>{j['company']}</b> — {j['title']}</td>
            <td><a href="{j['link']}">View Job</a></td>
            <td>{', '.join(j['keywords'])}</td>
            <td>{', '.join(j['skills'])}</td>
            <td>{j['apply_host']}</td>
            <td>{'' if j['free_to_apply'] else ' Maybe'}</td>
        </tr>
        """
    return f"""
    <html>
    <body>
        <h2>Daily Global Frontend Developer Jobs ({datetime.now().strftime('%Y-%m-%d')})</h2>
        <table border="1" cellspacing="0" cellpadding="6">
        <tr>
            <th>#</th><th>Company / Role</th><th>Link</th>
            <th>Keywords</th><th>Skills</th><th>Source</th><th>Free to Apply</th>
        </tr>
        {rows}
        </table>
    </body>
    </html>
    """


def send_email(html):
    msg = MIMEText(html, "html")
    msg["Subject"] = " Daily Remote Frontend Jobs Digest"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    if DRY_RUN:
        print("[DRY RUN] Email prepared but not sent.")
        print(msg.as_string()[:400] + "...\n")
        return

    if not EMAIL_USER or not EMAIL_PASS:
        raise RuntimeError("EMAIL_USER or EMAIL_PASS missing in .env")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
    print(" Email sent successfully!")


def main():
    try:
        jobs = fetch_all_jobs()
    except RuntimeError as e:
        print(" Failed to fetch jobs:", e)
        sys.exit(1)

    html = create_html_table(jobs)
    try:
        send_email(html)
    except Exception as e:
        print(" Failed to send email:", e)
        sys.exit(1)

    if DRY_RUN:
        print(" Dry run complete — no email sent.")
    else:
        print(" Success! Daily job email sent.")


if __name__ == "__main__":
    main()
