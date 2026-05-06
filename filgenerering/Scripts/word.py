from docx import Document
from docx.shared import Inches

# Create a new document
document = Document()
if not document:
    print("Failed to create a new document.")
    exit(1)
# Add a title (Heading Level 0)
document.add_heading('Project Report', 0)

document.save('example_report.docx')
