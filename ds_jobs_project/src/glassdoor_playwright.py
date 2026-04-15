# -*- coding: utf-8 -*-
import asyncio
import csv
from playwright.async_api import async_playwright, Playwright


async def scrape_jobs(playwright: Playwright, num_pages=5):
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()

# urls = [
#     # ===================== DATA SCIENTIST =====================
    
#     "https://www.glassdoor.com/Job/united-states-data-scientist-jobs-SRCH_IL.0,13_KO14,28_IP20.htm?typedKeyword=data%2520scientist&sc.keyword=data%2520scientist&locT=&locId=",
    
#     "https://www.glassdoor.com/Job/united-kingdom-data-scientist-jobs-SRCH_IL.0,14_IN2_KO15,29.htm",
    
#     "https://www.glassdoor.com/Job/canada-data-scientist-jobs-SRCH_IL.0,6_IN3_KO7,21.htm",
    
#     "https://www.glassdoor.com/Job/australia-data-scientist-jobs-SRCH_IL.0,9_IN16_KO10,24.htm",
    
#     "https://www.glassdoor.com/Job/singapore-singapore-data-scientist-jobs-SRCH_IL.0,19_IC3235921_KO20,34.htm",
    
#     "https://www.glassdoor.com/Job/indianapolis-data-scientist-jobs-SRCH_IL.0,12_IC1145013_KO13,27.htm",

#     # ===================== ML ENGINEER =====================
    
#     "https://www.glassdoor.com/Job/united-states-ml-engineer-jobs-SRCH_IL.0,13_IN1_KO14,25.htm",
    
#     "https://www.glassdoor.com/Job/united-kingdom-ml-engineer-jobs-SRCH_IL.0,14_IN2_KO15,26.htm",
    
#     "https://www.glassdoor.com/Job/australia-ml-engineer-jobs-SRCH_IL.0,9_IN16_KO10,21.htm",
    
#     "https://www.glassdoor.com/Job/singapore-ml-engineer-jobs-SRCH_IL.0,9_IC3235921_KO10,21.htm",
    
#     "https://www.glassdoor.com/Job/indianapolis-ml-engineer-jobs-SRCH_IL.0,12_IC1145013_KO13,24.htm",

#     # ===================== DATA ANALYST =====================
    
#     "https://www.glassdoor.com/Job/united-states-data-analyst-jobs-SRCH_IL.0,13_IN1_KO14,26.htm",
    
#     "https://www.glassdoor.com/Job/united-kingdom-data-analyst-jobs-SRCH_IL.0,14_IN2_KO15,27.htm",
    
#     "https://www.glassdoor.com/Job/canada-data-analyst-jobs-SRCH_IL.0,6_IN3_KO7,19.htm",
    
#     "https://www.glassdoor.com/Job/australia-data-analyst-jobs-SRCH_IL.0,9_IN16_KO10,22.htm",
    
#     "https://www.glassdoor.com/Job/singapore-data-analyst-jobs-SRCH_IL.0,9_IC3235921_KO10,22.htm",
    
#     "https://www.glassdoor.com/Job/indianapolis-data-analyst-jobs-SRCH_IL.0,12_IC1145013_KO13,25.htm",

#     # ===================== AI ENGINEER =====================
    
#     "https://www.glassdoor.com/Job/united-states-ai-engineer-jobs-SRCH_IL.0,13_IN1_KO14,25.htm",
    
#     "https://www.glassdoor.com/Job/united-kingdom-ai-engineer-jobs-SRCH_IL.0,14_IN2_KO15,26.htm",
    
#     "https://www.glassdoor.com/Job/indianapolis-ai-engineer-jobs-SRCH_IL.0,12_IC1145013_KO13,24.htm",

#     # ===================== DEEP LEARNING =====================
    
#     "https://www.glassdoor.com/Job/united-states-deep-learning-engineer-jobs-SRCH_IL.0,13_IN1_KO14,36.htm",
    
#     "https://www.glassdoor.com/Job/united-kingdom-deep-learning-engineer-jobs-SRCH_IL.0,14_IN2_KO15,37.htm"
# ]

    url = (
"https://www.glassdoor.com/Job/united-kingdom-deep-learning-engineer-jobs-SRCH_IL.0,14_IN2_KO15,37.htm"
                  )
    await page.goto(url)
    await asyncio.sleep(5)
    print("Page title:", await page.title())

    csv_filename = "deep_learning_engineer_jobs_united_kingdom.csv"

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Job Title",
            "Company",
            "Location",
            "Salary Estimate",
            "Job Description",
            "Job Age",
        ])

        record_count = 0
        current_page = 1

        while current_page <= num_pages:
            print(f"\nScraping page {current_page}...")

            # Wait for job cards
            try:
                await page.wait_for_selector("[data-test='jobListing']", timeout=10000)
            except Exception:
                print("Job cards not found — possible captcha or structure change.")
                await page.screenshot(path=f"error_page_{current_page}.png")
                break

            job_cards = await page.locator("[data-test='jobListing']").all()
            print(f"Found {len(job_cards)} job cards")

            for i, card in enumerate(job_cards):
                try:
                    # Extract from card directly (no click needed for basic fields)
                    async def card_text(selector, default="#N/A"):
                        try:
                            el = card.locator(selector)
                            if await el.count() > 0:
                                return (await el.first.text_content() or default).strip()
                            return default
                        except Exception:
                            return default

                    job_title   = await card_text("[data-test='job-title']")
                    location    = await card_text("[data-test='emp-location']")
                    salary      = await card_text("[data-test='detailSalary']")
                    description = await card_text("[data-test='descSnippet']")
                    job_age     = await card_text("[data-test='job-age']")

                    # Company name
                    company = "#N/A"
                    try:
                        company_el = card.locator("[class*='EmployerProfile_compactEmployerName']")
                        if await company_el.count() > 0:
                            company = (await company_el.first.text_content() or "#N/A").strip()
                    except Exception:
                        pass

                    # Click card to get full job description from detail panel
                    try:
                        await card.click()
                        await asyncio.sleep(2)

                        # Close modal if it appears
                        try:
                            modal = page.locator("[data-test='modal-close-btn'], [alt='Close']")
                            if await modal.count() > 0:
                                await modal.first.click()
                                await asyncio.sleep(1)
                        except Exception:
                            pass

                        # Click "Show more" to expand description
                        try:
                            show_more = page.locator("[data-test='show-more-cta']")
                            if await show_more.count() > 0:
                                await show_more.first.click()
                                await asyncio.sleep(1)
                        except Exception:
                            pass

                        # Get full description
                        try:
                            full_desc = page.locator(
                                "#JobDescriptionContainer, "
                                "[class*='JobDetails_jobDescriptionWrapper'], "
                                "[class*='jobDescriptionContent']"
                            )
                            if await full_desc.count() > 0:
                                description = (await full_desc.first.text_content() or description).strip()
                        except Exception:
                            pass

                    except Exception as e:
                        print(f"  Click error on card {i+1}: {e}")

                    writer.writerow([
                        job_title, company, location,
                        salary, description, job_age
                    ])
                    record_count += 1
                    print(f"  [{record_count}] {job_title} @ {company} | {location} | {salary}")

                except Exception as e:
                    print(f"  Error on card {i+1}: {e}")
                    continue

            print(f"Page {current_page} done — {record_count} total records so far.")
            # 🔥 CLOSE LOGIN POPUP (VERY IMPORTANT)
            try:
                modal_close = page.locator("[data-test='modal-close-btn'], button[aria-label='Close']")
                if await modal_close.count() > 0:
                    await modal_close.first.click()
                    await asyncio.sleep(1)
                    print("Closed login popup")
            except:
                pass

# Pagination — Glassdoor "Load more" button (robust version)
            try:
                load_more = page.locator(
                    "button[data-test='load-more'], "
                    "button:has-text('Show more jobs'), "
                    "button[aria-label*='Show more']"
                )

                if await load_more.count() > 0:
                    await load_more.first.scroll_into_view_if_needed()
                    await asyncio.sleep(1)

                    await load_more.first.click()
                    current_page += 1

                    # wait for new jobs to load
                    await page.wait_for_timeout(3000)
                    continue
                
                # fallback: next pagination (if exists)
                next_btn = page.locator("[data-test='pagination-next']")
                if await next_btn.count() > 0:
                    is_disabled = await next_btn.first.get_attribute("disabled")
                    if is_disabled:
                        print("Reached last page.")
                        break
                    
                    await next_btn.first.click()
                    current_page += 1
                    await page.wait_for_timeout(3000)
                else:
                    print("No pagination found — stopping.")
                    break
                
            except Exception as e:
                print(f"Pagination error: {e}")
                break






            # old Pagination — Glassdoor uses "Load more" button
            # try:
            #     load_more = page.locator("[data-test='load-more']")
            #     if await load_more.count() > 0:
            #         await load_more.click()
            #         current_page += 1
            #         await asyncio.sleep(3)
            #         continue

            #     next_btn = page.locator("[data-test='pagination-next']")
            #     if await next_btn.count() > 0:
            #         is_disabled = await next_btn.first.get_attribute("disabled")
            #         if is_disabled is not None:
            #             print("Reached last page.")
            #             break
            #         await next_btn.first.click()
            #         current_page += 1
            #         await asyncio.sleep(3)
            #     else:
            #         print("No pagination found — stopping.")
            #         break

            # except Exception as e:
            #     print(f"Pagination error: {e}")
            #     break

    print(f"\nDone! {record_count} jobs saved to '{csv_filename}'")
    await browser.close()


urls = [
    # ===================== DATA SCIENTIST =====================
    
    "https://www.glassdoor.com/Job/united-states-data-scientist-jobs-SRCH_IL.0,13_KO14,28_IP20.htm?typedKeyword=data%2520scientist&sc.keyword=data%2520scientist&locT=&locId=",
    
    "https://www.glassdoor.com/Job/united-kingdom-data-scientist-jobs-SRCH_IL.0,14_IN2_KO15,29.htm",
    
    "https://www.glassdoor.com/Job/canada-data-scientist-jobs-SRCH_IL.0,6_IN3_KO7,21.htm",
    
    "https://www.glassdoor.com/Job/australia-data-scientist-jobs-SRCH_IL.0,9_IN16_KO10,24.htm",
    
    "https://www.glassdoor.com/Job/singapore-singapore-data-scientist-jobs-SRCH_IL.0,19_IC3235921_KO20,34.htm",
    
    "https://www.glassdoor.com/Job/indianapolis-data-scientist-jobs-SRCH_IL.0,12_IC1145013_KO13,27.htm",

    # ===================== ML ENGINEER =====================
    
    "https://www.glassdoor.com/Job/united-states-ml-engineer-jobs-SRCH_IL.0,13_IN1_KO14,25.htm",
    
    "https://www.glassdoor.com/Job/united-kingdom-ml-engineer-jobs-SRCH_IL.0,14_IN2_KO15,26.htm",
    
    "https://www.glassdoor.com/Job/australia-ml-engineer-jobs-SRCH_IL.0,9_IN16_KO10,21.htm",
    
    "https://www.glassdoor.com/Job/singapore-ml-engineer-jobs-SRCH_IL.0,9_IC3235921_KO10,21.htm",
    
    "https://www.glassdoor.com/Job/indianapolis-ml-engineer-jobs-SRCH_IL.0,12_IC1145013_KO13,24.htm",

    # ===================== DATA ANALYST =====================
    
    "https://www.glassdoor.com/Job/united-states-data-analyst-jobs-SRCH_IL.0,13_IN1_KO14,26.htm",
    
    "https://www.glassdoor.com/Job/united-kingdom-data-analyst-jobs-SRCH_IL.0,14_IN2_KO15,27.htm",
    
    "https://www.glassdoor.com/Job/canada-data-analyst-jobs-SRCH_IL.0,6_IN3_KO7,19.htm",
    
    "https://www.glassdoor.com/Job/australia-data-analyst-jobs-SRCH_IL.0,9_IN16_KO10,22.htm",
    
    "https://www.glassdoor.com/Job/singapore-data-analyst-jobs-SRCH_IL.0,9_IC3235921_KO10,22.htm",
    
    "https://www.glassdoor.com/Job/indianapolis-data-analyst-jobs-SRCH_IL.0,12_IC1145013_KO13,25.htm",

    # ===================== AI ENGINEER =====================
    
    "https://www.glassdoor.com/Job/united-states-ai-engineer-jobs-SRCH_IL.0,13_IN1_KO14,25.htm",
    
    "https://www.glassdoor.com/Job/united-kingdom-ai-engineer-jobs-SRCH_IL.0,14_IN2_KO15,26.htm",
    
    "https://www.glassdoor.com/Job/indianapolis-ai-engineer-jobs-SRCH_IL.0,12_IC1145013_KO13,24.htm",

    # ===================== DEEP LEARNING =====================
    
    "https://www.glassdoor.com/Job/united-states-deep-learning-engineer-jobs-SRCH_IL.0,13_IN1_KO14,36.htm",
    
    "https://www.glassdoor.com/Job/united-kingdom-deep-learning-engineer-jobs-SRCH_IL.0,14_IN2_KO15,37.htm"
]

async def main():
    async with async_playwright() as playwright:
        await scrape_jobs(
            playwright,
            num_pages=20
        )




if __name__ == "__main__":
    asyncio.run(main())


# urls={
#     "https://www.glassdoor.com/Job/united-states-data-scientist-jobs-"
#         "SRCH_IL.0,13_KO14,28_IP20.htm?typedKeyword=data%2520scientist"
#         "&sc.keyword=data%2520scientist&locT=&locId=" # data scientist in US
    
#     "https://www.glassdoor.com/Job/united-kingdom-data-scientist-jobs-SRCH_IL.0,14_IN2_KO15,29.htm" # data scientist in UK
#     ,
#     "https://www.glassdoor.com/Job/canada-data-scientist-jobs-SRCH_IL.0,6_IN3_KO7,21.htm" # data scientist in Canada
# ,"https://www.glassdoor.com/Job/australia-data-scientist-jobs-SRCH_IL.0,9_IN16_KO10,24.htm" # data scientist in austrelia
# ,"https://www.glassdoor.com/Job/singapore-singapore-data-scientist-jobs-SRCH_IL.0,19_IC3235921_KO20,34.htm" # data scientist in singapore
# ,"https://www.glassdoor.com/Job/indianapolis-data-scientist-jobs-SRCH_IL.0,12_IC1145013_KO13,27.htm" # data scientist in indianapolis
# # ************************************************************
#     "https://www.glassdoor.com/Job/united-states-ml-engineer-jobs-SRCH_IL.0,13_IN1_KO14,25.htm" # machine learning engineer in us
#     ,
#     "https://www.glassdoor.com/Job/united-kingdom-ml-engineer-jobs-SRCH_IL.0,14_IN2_KO15,26.htm" # machine learning engineer in UK
#     ,"https://www.glassdoor.com/Job/australia-ml-engineer-jobs-SRCH_IL.0,9_IN16_KO10,21.htm" # machine learning engineer in australia
#     ,"https://www.glassdoor.com/Job/singapore-ml-engineer-jobs-SRCH_IL.0,9_IC3235921_KO10,21.htm" # machine learning engineer in singapore
# ,"https://www.glassdoor.com/Job/indianapolis-ml-engineer-jobs-SRCH_IL.0,12_IC1145013_KO13,24.htm" # machine learning engineer in indianapolis
# # ************************************************************
    
#     ,"https://www.glassdoor.com/Job/united-states-data-analyst-jobs-SRCH_IL.0,13_IN1_KO14,26.htm"# data analyst in us
#     ,"https://www.glassdoor.com/Job/united-kingdom-data-analyst-jobs-SRCH_IL.0,14_IN2_KO15,27.htm" # data analyst in UK
# ,"https://www.glassdoor.com/Job/canada-data-analyst-jobs-SRCH_IL.0,6_IN3_KO7,19.htm" # data analyst in Canada
# ,"https://www.glassdoor.com/Job/australia-data-analyst-jobs-SRCH_IL.0,9_IN16_KO10,22.htm" # data analyst in australia
# ,"https://www.glassdoor.com/Job/singapore-data-analyst-jobs-SRCH_IL.0,9_IC3235921_KO10,22.htm" # data analyst in singapore
# ,"https://www.glassdoor.com/Job/indianapolis-data-analyst-jobs-SRCH_IL.0,12_IC1145013_KO13,25.htm" # data analyst in indianapolis

# # ************************************************************

# "https://www.glassdoor.com/Job/united-states-ai-engineer-jobs-SRCH_IL.0,13_IN1_KO14,25.htm" # ai engineer in us

# ,"https://www.glassdoor.com/Job/united-kingdom-ai-engineer-jobs-SRCH_IL.0,14_IN2_KO15,26.htm" # ai engineer in UK
# ,"https://www.glassdoor.com/Job/indianapolis-ai-engineer-jobs-SRCH_IL.0,12_IC1145013_KO13,24.htm" # ai engineer in indianapolis
# # ************************************************************
# "https://www.glassdoor.com/Job/united-states-deep-learning-engineer-jobs-SRCH_IL.0,13_IN1_KO14,36.htm" # deep learning engineer in us
# ,
# "https://www.glassdoor.com/Job/united-kingdom-deep-learning-engineer-jobs-SRCH_IL.0,14_IN2_KO15,37.htm" # deep learning engineer in UK
#     # 390

# }

project2_urls={

    "https://www.glassdoor.com/Job/egypt-data-scientist-jobs-SRCH_IL.0,5_IN69_KO6,20.htm" # data scientist in egypt
    , "https://www.glassdoor.com/Job/italy-data-scientist-jobs-SRCH_IL.0,5_IN120_KO6,20.htm" # data scientist in Italy
    ,"https://www.glassdoor.com/Job/germany-data-scientist-jobs-SRCH_IL.0,7_IN96_KO8,22.htm" # data scientist in Germany

}