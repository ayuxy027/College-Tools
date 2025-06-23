from fpdf import FPDF, XPos, YPos
from datetime import datetime
import os

# Custom PDF class for professional letter
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(20, 20, 20)  # left, top, right margins
        self.set_auto_page_break(auto=False)  # Disable auto page break for single page control

# Create the PDF
pdf = PDF()
pdf.add_page()

# Start with Date (right aligned) - removed header section
pdf.set_font("Helvetica", size=11)
pdf.cell(0, 8, f"Date: {datetime.now().strftime('%B %d, %Y')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
pdf.ln(12)

# To section
pdf.set_font("Helvetica", size=11)
pdf.cell(0, 6, "To,", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 6, "Dr. Rachna Sable", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 6, "Head of Department", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 6, "Computer Science and Engineering (AI & ML)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 6, "GHRCEM Pune", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(10)

# Subject line
pdf.set_font("Helvetica", "B", 11)
pdf.cell(0, 6, "Subject: Request for Attendance Consideration Due to Internship", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(10)

# Salutation
pdf.set_font("Helvetica", size=11)
pdf.cell(0, 6, "Respected Ma'am,", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(8)

# Body paragraphs with tighter spacing
body_paragraphs = [
    "I hope this letter finds you well. I am writing to inform you that I have started a 6-month internship as an SDE Intern at Heizen on May 28, 2025, with a stipend of Rs. 35,000 per month. The internship involves comprehensive full-stack development responsibilities, including frontend, backend, API integrations, and database systems, which are greatly enhancing my practical skills and complementing my academic learning.",
    
    "I sincerely value my education and am fully committed to balancing this opportunity with my academic responsibilities. I am making every effort to keep up with lectures and assignments. However, due to the internship commitments, I kindly request your support in managing my attendance during the internship period if it falls short of the 75% requirement, and kindly communicate my situation to other subject teachers if necessary.",
    
    "My enrollment number is 23ACSE1101078, and my class teacher is Ms. Deepika Dabhade. I have attached the offer letter for your reference.",
    
    "Thank you for your understanding and support in this matter."
]

for paragraph in body_paragraphs:
    pdf.multi_cell(0, 5, paragraph, align='J')  # Reduced line height from 6 to 5
    pdf.ln(4)  # Reduced spacing from 5 to 4

# Closing with controlled spacing
pdf.ln(2)
pdf.cell(0, 6, "Yours sincerely,", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(10)  # Reduced space for signature from 15 to 10

# Student details
pdf.cell(0, 6, "Ayush Yadav", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 6, "TY B.Tech - CSE (AIML)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 6, "Enrollment No: 23ACSE1101078", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 6, "GHRCEM, Pune", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# Calculate remaining space for signatures
current_y = pdf.get_y()
remaining_space = 297 - current_y - 20  # A4 height - current position - bottom margin

# Add appropriate spacing before signatures
if remaining_space > 40:
    pdf.ln(20)
else:
    pdf.ln(10)

# Signature section with proper spacing
pdf.set_font("Helvetica", size=10)

# Two column signature layout with better spacing
col_width = 85
pdf.cell(col_width, 6, "_________________________", align='C')
pdf.cell(col_width, 6, "_________________________", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
pdf.cell(col_width, 6, "Dr. Rachna Sable", align='C')
pdf.cell(col_width, 6, "Ms. Deepika Dabhade", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
pdf.cell(col_width, 6, "Head of Department", align='C')
pdf.cell(col_width, 6, "Class Teacher", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
pdf.cell(col_width, 6, "CSE AI & ML", align='C')
pdf.cell(col_width, 6, "CSE AI & ML", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

# Save the PDF
output_path = "Professional_Attendance_Request_Letter.pdf"

try:
    pdf.output(output_path)
    print(f"✅ Professional PDF successfully created: {os.path.abspath(output_path)}")
    print(f"📄 File saved as: {output_path}")
    print(f"🎯 Clean layout with proper signature spacing!")
except Exception as e:
    print(f"❌ Error creating PDF: {e}")
