# 📊 Global Data Jobs Market Analysis

An end-to-end data science project that analyzes global demand, salary trends, and skill requirements for data-related roles using real-world job listings.

---

## 🌍 Overview

This project collects and analyzes job postings for:

- Data Scientist  
- Machine Learning Engineer  
- AI Engineer  
- Data Analyst  
- Deep Learning Engineer  

Data is scraped from Glassdoor across multiple countries, including the US, UK, Canada, Australia, Singapore, and others.

The goal is to uncover **actionable insights** for job seekers and provide a **data-driven understanding of the global data job market**.

---

## 🎯 Business Understanding (CRISP-DM)

### 1. Problem Definition
The data job market is large and complex. Job seekers often struggle to understand:
- Which skills are most in demand  
- How salaries vary across roles and locations  
- What differentiates entry-level from senior roles  

---

### 2. Stakeholders
- Job seekers — understand market demand and salary expectations  
- Hiring managers — benchmark against competitors  
- Educators / bootcamps — align curriculum with industry needs  
- Project author — demonstrate end-to-end data science capability  

---

### 3. Key Questions
- What are the most in-demand skills across roles?  
- How do salaries vary by role, country, and seniority?  
- Which industries and companies hire the most data professionals?  
- What are the differences between global job markets?  

---

### 4. Success Criteria
- Clean, structured dataset ready for analysis  
- At least 3 actionable insights  
- Visualizations or dashboard showing trends  
- (Optional) Salary prediction model  

---

## 🛠️ Data Collection

Data is collected using a custom-built asynchronous scraper with Playwright.

### Key Features:
- Handles dynamic content and lazy loading  
- Automatically closes login popups  
- Expands full job descriptions ("Show more")  
- Robust pagination (load more + fallback navigation)  
- Error handling and fault tolerance  
- Supports multiple roles and countries  

---

## 📂 Dataset

Each record contains:
- Job Title  
- Company  
- Location  
- Salary Estimate  
- Job Description  
- Job Posting Age  

---

## 📚 References & Inspiration

### Data Source
- Glassdoor — job listings and salary data  

### Inspiration
- ds_salary_proj (PlayingNumbers) — project idea and initial dataset structure  

### Technical References
- Bright Data blog — scraping dynamic Glassdoor pages  
- Selenium — initial scraping concepts  

---

## ⚙️ Key Contributions

This project extends existing work by:

- Building an asynchronous scraping pipeline using Playwright  
- Handling real-world scraping challenges (popups, dynamic DOM, expandable content)  
- Extracting full job descriptions instead of partial snippets  
- Scaling data collection across multiple roles and countries  
- Implementing robust and reliable scraping logic  

---

## 🚀 Future Work

- Expand scraper to support any job category (user-defined roles)  
- Store data in a database (PostgreSQL)  
- Build interactive dashboards (Power BI / Streamlit)  
- Train a salary prediction model  
- Automate data collection pipeline  

---

## 📌 Project Status

In progress — data collection and analysis pipeline under active development.
