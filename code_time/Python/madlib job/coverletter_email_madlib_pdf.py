#!/usr/bin/env python3

"""
coverletter_email_madlib_pdf.py

A Python program that prompts for personal and company info, then generates
two PDFs: 'cover_letter.pdf' and 'email.pdf'. It also prints the text
in the console so you can copy/paste it as needed.

Usage:
    1. pip install fpdf
    2. python coverletter_email_madlib_pdf.py
"""

try:
    from fpdf import FPDF
except ImportError:
    print("ERROR: fpdf library not found. Please install it with 'pip install fpdf' before running this script.")
    exit()

def save_to_pdf(filename, text):
    """
    Saves a given text to a PDF file using the fpdf library.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)
    print(f"{filename} has been created.")

def main():
    print("Welcome to the Cover Letter & Email Mad Lib Program (PDF-Enabled)!\n")
    print("You can copy/paste your information into each prompt if desired.\n")

    # Gather inputs
    your_name = input("Your Name: ")
    position_title = input("Position Title: ")
    company_name = input("Company Name: ")
    company_address = input("Company Address (Street, City, State): ")
    hiring_manager_name = input("Name of Hiring Manager (if known): ")
    your_skills = input("Key skills (comma-separated): ")
    your_background = input("Briefly describe your background or experience: ")
    your_value = input("What unique value do you bring to the company?: ")
    closing_statement = input("Closing statement (e.g., 'Sincerely,' 'Best regards,'): ")
    your_email = input("Your Email Address: ")
    your_phone = input("Your Phone Number: ")
    your_location = input("Your Location (City, State): ")

    # --- COVER LETTER TEMPLATE ---
    cover_letter = f"""
[Your Name]
[Your Address or City, State]
[Your Email] | [Your Phone]

{your_name}
{your_location}
{your_email} | {your_phone}

{company_name}
{company_address}

Dear {hiring_manager_name if hiring_manager_name else 'Hiring Manager'},

I am writing to apply for the position of {position_title} at {company_name}. With expertise in {your_skills}, I believe my background in {your_background} makes me an ideal candidate for this role. I have developed a thorough understanding of the industry through my experience, and I am excited at the prospect of bringing my unique skill set to your team.

What truly sets me apart is {your_value}, which I am eager to channel into meaningful contributions at {company_name}. I thrive in challenging environments, enjoy collaborating with diverse teams, and am passionate about continuous growth—both in myself and those around me.

Thank you for your time and consideration. I would love the opportunity to further discuss how my experiences and abilities align with the goals and culture of {company_name}.

{closing_statement},
{your_name}
    """

    # --- EMAIL TEMPLATE ---
    email_template = f"""
Subject: Application for {position_title} – {your_name}

Dear {hiring_manager_name if hiring_manager_name else 'Hiring Manager'},

I hope you are doing well! My name is {your_name}, and I recently came across the opening for a {position_title} at {company_name}. I am excited about this opportunity and would be grateful for your consideration.

Given my background in {your_background} and my strong skills in {your_skills}, I am confident that I would be a great fit for your team. I am especially drawn to {company_name} because {your_value}, and I believe this shared value aligns with your mission.

I have attached my resume and cover letter for your review. Should you have any questions or would like to schedule an interview, you can reach me at {your_phone} or by replying to this email.

Thank you very much for your time and consideration.

{closing_statement},
{your_name}
{your_email}
{your_phone}
    """

    # Print the generated texts (for copying/pasting directly)
    print("\n\n----- GENERATED COVER LETTER -----")
    print(cover_letter)

    print("\n\n----- GENERATED EMAIL -----")
    print(email_template)

    # Save the cover letter and email to PDFs
    save_to_pdf("cover_letter.pdf", cover_letter)
    save_to_pdf("email.pdf", email_template)

if __name__ == "__main__":
    main()
