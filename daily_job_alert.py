import os
import sys
import json
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

SEEN_JOBS_FILE = "seen_jobs.json"
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
DRY_RUN = os.getenv("DRY_RUN", "1") == "1"  # set to 0 in .env to actually send email

FREE_DOMAINS = {
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
    "arbeitnow.com",
    "flexjobs.com",
    "remoteco.com",
    "workingnotworking.com",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

# =================== HELPERS =================== #


def save_seen_jobs(links: set):
    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(list(links), f)

def load_seen_jobs() -> set:
    try:
        with open(SEEN_JOBS_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

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
        res = requests.get(url, headers=HEADERS, timeout=30)
        res.raise_for_status()
        return res
    except RequestException as e:
        raise RuntimeError(f"Network error: {e}") from e


# =================== FETCH JOB SOURCES =================== #


def fetch_arbeitnow_jobs():
    """Fetch frontend jobs from Arbeitnow API - free job board"""
    url = "https://www.arbeitnow.com/api/job-board-api"
    try:
        res = safe_request(url)
        data = res.json().get("data", [])
        jobs = []
        
        for job in data:
            title = job.get("title", "") or ""
            tags = job.get("tags", [])
            
            # Check if frontend related
            frontend_keywords = ["frontend", "front-end", "react", "vue", "angular", "javascript", "web developer"]
            if any(keyword in title.lower() for keyword in frontend_keywords) or \
               any(keyword in " ".join(tags).lower() for keyword in frontend_keywords):
                company = job.get("company_name", "Unknown")
                link = job.get("url", "#")
                location = job.get("location", "Remote")
                
                if "remote" in location.lower() or job.get("remote", False):
                    jobs.append({
                        "company": company,
                        "title": title,
                        "link": link,
                        "keywords": ["remote", "frontend", "web"],
                        "skills": ["JavaScript", "React", "CSS"],
                        "apply_host": apply_host_from_url(link),
                        "free_to_apply": is_likely_free_apply(link)
                    })
        return jobs[:5]
    except Exception as e:
        print("Arbeitnow error:", e)
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







def fetch_remoteok_jobs():
    """Fetch jobs from Remote OK"""
    url = "https://remoteok.io/remote-frontend-jobs"
    try:
        res = safe_request(url)
        soup = BeautifulSoup(res.text, "html.parser")
        jobs = []
        for job in soup.select(".job")[:5]:
            title_elem = job.select_one("h2")
            company_elem = job.select_one("h3")
            link_elem = job.select_one("a.preventLink")

            if title_elem and company_elem and link_elem:
                title = title_elem.get_text(strip=True)
                company = company_elem.get_text(strip=True)
                link = link_elem['href']
                if not link.startswith("http"):
                    link = "https://remoteok.io" + link

                jobs.append({
                    "company": company,
                    "title": title,
                    "link": link,
                    "keywords": ["remote", "frontend", "developer"],
                    "skills": ["JavaScript", "React", "HTML", "CSS"],
                    "apply_host": apply_host_from_url(link),
                    "free_to_apply": is_likely_free_apply(link)
                })
        return jobs
    except Exception as e:
        print("Remote OK error:", e)
        return []

def fetch_jsjobbs_jobs():
    """Fetch jobs from JSJobbs.com"""
    url = "https://jsjobbs.com/jobs/remote"
    try:
        res = safe_request(url)
        soup = BeautifulSoup(res.text, "html.parser")
        jobs = []
        for job in soup.select(".job-card")[:5]:
            title = job.select_one(".job-title").get_text(strip=True)
            company = job.select_one(".company-name").get_text(strip=True)
            link = job.select_one("a")['href']
            if not link.startswith("http"):
                link = "https://jsjobbs.com" + link

            jobs.append({
                "company": company,
                "title": title,
                "link": link,
                "keywords": ["remote", "frontend", "javascript"],
                "skills": ["JavaScript", "React", "Vue", "Angular"],
                "apply_host": apply_host_from_url(link),
                "free_to_apply": is_likely_free_apply(link)
            })
        return jobs
    except Exception as e:
        print("JSJobbs error:", e)
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
                href = a.get("href", "")
                if not href.startswith("http"):
                    href = "https://weworkremotely.com" + href
                title_elem = a.select_one("span.title")
                company_elem = a.select_one("span.company")
                title = title_elem.get_text("", strip=True) if title_elem else ""
                company = company_elem.get_text("", strip=True) if company_elem else ""
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


def fetch_all_jobs(seen_jobs: set):
    jobs = []
    sources = [
        fetch_arbeitnow_jobs,
        fetch_remotive_jobs,
        fetch_wwr_jobs,
        fetch_jsjobbs_jobs,
        fetch_remoteok_jobs,
    ]
    
    for func in sources:
        try:
            fetched = func()
            jobs.extend(fetched)
            print(f"[OK] {func.__name__}: {len(fetched)} jobs")
        except Exception as e:
            print(f"[FAIL] {func.__name__}: {e}")
    
    if not jobs:
        raise RuntimeError("No jobs found from any source.")
    
    # Remove duplicates and seen jobs
    seen_links = set()
    unique_jobs = []
    for job in jobs:
        if job["link"] not in seen_links and job["link"] not in seen_jobs:
            seen_links.add(job["link"])
            unique_jobs.append(job)
    
    print(f"\nTotal unique jobs found: {len(unique_jobs)}")
    return unique_jobs


# =================== EMAIL BUILDING =================== #


def create_html_table(jobs):
    jobs = sorted(jobs, key=lambda j: (not j["free_to_apply"], j["company"]))
    rows = ""
    for i, j in enumerate(jobs, 1):
        free_badge = "Free" if j['free_to_apply'] else "Maybe Paid"
        free_color = "#28a745" if j['free_to_apply'] else "#ffc107"
        
        rows += f"""
        <tr>
            <td>{i}</td>
            <td><b>{j['company']}</b><br/><span style="color: #666;">{j['title']}</span></td>
            <td><a href="{j['link']}" style="color: #007bff;">Apply Now</a></td>
            <td>{', '.join(j['keywords'])}</td>
            <td>{', '.join(j['skills'])}</td>
            <td>{j['apply_host']}</td>
            <td style="background-color: {free_color}22; color: {free_color}; font-weight: bold;">{free_badge}</td>
        </tr>
        """
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h2 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th {{ background-color: #4CAF50; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
            tr:hover {{ background-color: #f5f5f5; }}
            a {{ text-decoration: none; }}
        </style>
    </head>
    <body>
        <h2>Daily Global Frontend Developer Jobs ({datetime.now().strftime('%Y-%m-%d')})</h2>
        <p>Found <strong>{len(jobs)}</strong> remote frontend opportunities today!</p>
        <table>
        <tr>
            <th>#</th><th>Company / Role</th><th>Link</th>
            <th>Keywords</th><th>Skills</th><th>Source</th><th>Apply Status</th>
        </tr>
        {rows}
        </table>
        <br/>
        <p style="color: #666; font-size: 12px;">
            Tip: Focus on jobs marked "Free" for immediate applications without subscriptions.
        </p>
    </body>
    </html>
    """


def send_email(html):
    msg = MIMEText(html, "html")
    msg["Subject"] = "Daily Remote Frontend Jobs Digest"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    if DRY_RUN:
        print("\n[DRY RUN] Email prepared but not sent.")
        print(msg.as_string()[:400] + "...\n")
        return

    if not EMAIL_USER or not EMAIL_PASS:
        raise RuntimeError("EMAIL_USER or EMAIL_PASS missing in .env")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
    print("Email sent successfully!")


def main():
    print("=" * 50)
    print("  REMOTE FRONTEND JOBS FETCHER")
    print("=" * 50)

    seen_jobs = load_seen_jobs()
    print(f"Loaded {len(seen_jobs)} previously seen jobs.")
    
    try:
        jobs = fetch_all_jobs(seen_jobs)
    except RuntimeError as e:
        print(f"Failed to fetch jobs: {e}")
        sys.exit(1)


    if not jobs:
        print("No new jobs found today.")
        return

    html = create_html_table(jobs)
    try:
        send_email(html)
    except Exception as e:
        print(f"Failed to send email: {e}")
        sys.exit(1)

    # Update seen jobs
    new_links = {job["link"] for job in jobs}
    seen_jobs.update(new_links)
    save_seen_jobs(seen_jobs)
    print(f"Saved {len(seen_jobs)} seen jobs.")

    if DRY_RUN:
        print("\nDry run complete - no email sent.")
        print("Set DRY_RUN=0 in .env to send actual emails.")
    else:
        print("\nSuccess! Daily job email sent.")


if __name__ == "__main__":
    main()