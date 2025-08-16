from fpdf import FPDF, XPos, YPos
import os
from datetime import datetime

class ProfessionalPRD(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(20, 20, 20)
        
        # Black and white only - no colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.light_gray = (240, 240, 240)
        
        # Track current section for better page breaks
        self.current_section = ""
        
    def header(self):
        if self.page_no() == 1:
            # Title page header - simple black text on white
            self.set_y(15)
            self.set_font('Helvetica', 'B', 24)
            self.set_text_color(0, 0, 0)
            self.cell(0, 12, 'Product Requirements Document', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            
            self.set_font('Helvetica', '', 16)
            self.cell(0, 8, 'AI Presentation Generator', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            
            # Simple line under title
            self.ln(5)
            self.set_draw_color(0, 0, 0)
            self.set_line_width(0.5)
            self.line(20, self.get_y(), 190, self.get_y())
            self.ln(15)
        else:
            # Regular page header - simple line
            self.set_y(8)
            self.set_font('Helvetica', 'B', 12)
            self.set_text_color(0, 0, 0)
            self.cell(100, 6, 'AI Presentation Generator PRD')
            
            # Page number on right
            self.set_x(150)
            self.cell(40, 6, f'Page {self.page_no()}', align='R')
            
            # Simple line under header
            self.ln(8)
            self.set_draw_color(0, 0, 0)
            self.set_line_width(0.3)
            self.line(20, self.get_y(), 190, self.get_y())
            self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        
        # Simple line above footer
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)
        self.line(20, self.get_y() - 5, 190, self.get_y() - 5)
        
        # Left side - date
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%B %d, %Y")}', align='L')
        
        # Right side - confidential
        self.set_x(150)
        self.cell(40, 10, 'Confidential', align='R')
    
    def add_title_page_content(self):
        """Add content to the title page"""
        self.set_y(70)
        
        # Document info box - simple border
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        self.rect(30, 70, 150, 60, 'D')
        
        self.set_y(80)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, 'Document Information', align='C')
        self.ln(12)
        
        # Document details
        details = [
            ('Version:', '1.0'),
            ('Date:', datetime.now().strftime('%B %d, %Y')),
            ('Status:', 'Draft'),
            ('Author:', 'Product Team')
        ]
        
        self.set_font('Helvetica', '', 10)
        for label, value in details:
            self.set_x(40)
            self.cell(30, 6, label, border=0)
            self.cell(0, 6, value, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Executive summary box
        self.set_y(160)
        self.rect(20, 160, 170, 80, 'D')
        
        self.set_y(170)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, 'Executive Summary', align='C')
        self.ln(12)
        
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        summary_text = ("An AI-powered presentation generator that creates professional, "
                       "customizable presentations with real photography integration. "
                       "Built to outperform existing solutions through superior design "
                       "control, structured templates, and seamless user experience.")
        
        self.set_x(30)
        self.multi_cell(150, 6, summary_text, align='J')
    
    def check_space_and_break(self, needed_space=30):
        """Check if we need a page break and add one if necessary"""
        if self.get_y() + needed_space > self.h - 25:
            self.add_page()
            return True
        return False
    
    def add_section_title(self, title, level=1):
        """Add a section title with proper spacing and formatting"""
        self.current_section = title
        
        # Check if we need a page break
        self.check_space_and_break(25)
        
        self.ln(10)
        
        if level == 1:
            # Main section - bold text with underline
            self.set_font('Helvetica', 'B', 14)
            self.set_text_color(0, 0, 0)
            self.cell(0, 12, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
            
            # Underline
            self.set_draw_color(0, 0, 0)
            self.set_line_width(0.5)
            self.line(self.l_margin, self.get_y() - 2, self.w - self.r_margin, self.get_y() - 2)
            
        elif level == 2:
            # Subsection
            self.set_font('Helvetica', 'B', 12)
            self.set_text_color(0, 0, 0)
            self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
            # Light underline
            self.set_draw_color(0, 0, 0)
            self.set_line_width(0.3)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        
        self.ln(8)
    
    def add_paragraph(self, text, indent=0):
        """Add a paragraph with proper formatting"""
        self.check_space_and_break(20)
        
        self.set_font('Helvetica', '', 11)
        self.set_text_color(0, 0, 0)
        
        if indent > 0:
            self.set_x(self.l_margin + indent)
            width = self.w - self.l_margin - self.r_margin - indent
        else:
            width = 0
        
        self.multi_cell(width, 6, text, align='J')
        self.ln(5)
    
    def add_bullet_list(self, items, indent=10, bullet_char='*'):
        """Add a bullet list with proper formatting - using * instead of •"""
        self.check_space_and_break(len(items) * 6 + 10)
        
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        
        for item in items:
            if isinstance(item, dict) and 'main' in item:
                # Main bullet point
                self.set_x(self.l_margin + indent)
                self.multi_cell(0, 6, f'{bullet_char} {item["main"]}', align='L')
                
                # Sub-items
                if 'sub' in item and item['sub']:
                    self.set_font('Helvetica', '', 9)
                    for sub_item in item['sub']:
                        self.set_x(self.l_margin + indent + 15)
                        self.multi_cell(0, 5, f'- {sub_item}', align='L')
                    self.set_font('Helvetica', '', 10)
            else:
                # Simple bullet point
                self.set_x(self.l_margin + indent)
                self.multi_cell(0, 6, f'{bullet_char} {item}', align='L')
        
        self.ln(5)
    
    def add_info_box(self, title, content):
        """Add an information box with title and content - black border only"""
        self.check_space_and_break(40)
        
        start_y = self.get_y()
        
        # Title - bold text
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        
        # Content area
        content_start_y = self.get_y()
        
        # Calculate content height first
        temp_y = self.get_y()
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        
        for item in content:
            self.set_x(self.l_margin + 10)
            self.multi_cell(self.w - self.l_margin - self.r_margin - 20, 6, f'* {item}', align='L')
        
        content_end_y = self.get_y()
        content_height = content_end_y - content_start_y
        
        # Draw simple black border around the box
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        self.rect(self.l_margin, start_y, self.w - self.l_margin - self.r_margin, 10 + content_height, 'D')
        
        self.ln(8)
    
    def add_two_column_layout(self, left_title, left_items, right_title, right_items):
        """Add a two-column layout for comparisons or related content"""
        self.check_space_and_break(50)
        
        start_y = self.get_y()
        col_width = (self.w - self.l_margin - self.r_margin - 10) / 2
        
        # Column headers with borders
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        
        # Left column header
        self.rect(self.l_margin, start_y, col_width, 8, 'D')
        self.set_xy(self.l_margin, start_y)
        self.cell(col_width, 8, left_title, align='C')
        
        # Right column header
        self.rect(self.l_margin + col_width + 10, start_y, col_width, 8, 'D')
        self.set_xy(self.l_margin + col_width + 10, start_y)
        self.cell(col_width, 8, right_title, align='C')
        
        self.ln(8)
        
        # Content
        left_y = self.get_y()
        right_y = left_y
        
        # Left column content
        self.set_xy(self.l_margin, left_y)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        
        for item in left_items:
            self.set_x(self.l_margin + 5)
            self.multi_cell(col_width - 10, 6, f'* {item}', align='L')
        
        left_end_y = self.get_y()
        
        # Right column content
        self.set_xy(self.l_margin + col_width + 10, right_y)
        
        for item in right_items:
            self.set_x(self.l_margin + col_width + 15)
            self.multi_cell(col_width - 10, 6, f'* {item}', align='L')
        
        right_end_y = self.get_y()
        
        # Draw borders around content
        max_height = max(left_end_y, right_end_y) - left_y
        
        # Left column border
        self.rect(self.l_margin, left_y, col_width, max_height, 'D')
        
        # Right column border
        self.rect(self.l_margin + col_width + 10, left_y, col_width, max_height, 'D')
        
        self.set_y(max(left_end_y, right_end_y) + 10)

# Create the PDF document
def create_prd_pdf():
    pdf = ProfessionalPRD()
    
    # Title page
    pdf.add_page()
    pdf.add_title_page_content()
    
    # Content pages
    pdf.add_page()
    
    # 1. Product Vision
    pdf.add_section_title('1. Product Vision')
    pdf.add_paragraph(
        'A modern, AI-powered presentation generator that outperforms existing solutions '
        'like Gamma through superior design control, real image integration, and structured '
        'content formatting. Users input prompts to generate fully-designed, editable '
        'presentations with professional layouts and Unsplash photography.'
    )
    
    # 2. Problem Statement
    pdf.add_section_title('2. Problem Statement')
    pdf.add_paragraph(
        'Existing presentation tools like Gamma lack precise design control, use AI-generated '
        'images instead of real photography, and provide limited customization options. Users '
        'need a solution that combines AI intelligence with professional design standards and '
        'real image integration.'
    )
    
    # 3. Objectives
    pdf.add_section_title('3. Objectives')
    objectives = [
        'Create AI-powered presentation generation with superior design control',
        'Integrate real Unsplash photography instead of AI-generated images',
        'Provide professional template system with consistent layouts',
        'Enable precise typography control and spacing optimization',
        'Implement version control with side-by-side comparison',
        'Build a scalable, modular architecture for future enhancements'
    ]
    pdf.add_bullet_list(objectives)
    
    # 4. Target Users
    pdf.add_section_title('4. Target Users')
    target_users = [
        'Professionals needing quick, high-quality presentations',
        'Design-conscious users who value real photography',
        'Teams requiring consistent branding and templates',
        'Open source contributors interested in AI/design integration'
    ]
    pdf.add_bullet_list(target_users)
    
    # 5. Core Features
    pdf.add_section_title('5. Core Features')
    
    pdf.add_section_title('AI Slide Generation', level=2)
    ai_features = [
        'Prompt-based multi-slide creation with intelligent content organization',
        'Structured content hierarchy (Title, Subtitle, Body, Lists)',
        'Groq API integration for fast natural language processing'
    ]
    pdf.add_info_box('Key Capabilities', ai_features)
    
    pdf.add_section_title('Template & Design System', level=2)
    design_features = [
        '4-5 professional, responsive templates built with CSS Grid approach',
        'Consistent layouts, spacing, and customizable theme parameters',
        '5-10 professional font families with automatic sizing and pairing'
    ]
    pdf.add_info_box('Design Features', design_features)
    
    pdf.add_section_title('Image & Version Control', level=2)
    control_features = [
        'Automated Unsplash image selection and smart placement',
        'Robust version control with side-by-side visual diffing',
        'Secure, Clerk-based authentication with tiered access'
    ]
    pdf.add_info_box('Advanced Features', control_features)
    
    # 6. User Journey Flow
    pdf.add_section_title('6. User Journey Flow')
    user_flow = [
        'Landing: Public page visit and feature overview',
        'Authentication: Clerk signup/login process',
        'Dashboard: Project overview and management',
        'Creation: Prompt input and editing interface',
        'Generation: AI processing and content creation',
        'Refinement: Follow-up edits and adjustments',
        'Export: High-quality PDF download with preserved formatting'
    ]
    pdf.add_bullet_list(user_flow, bullet_char='>')
    
    # 7. Technology Stack
    pdf.add_section_title('7. Technology Stack')
    
    frontend_items = [
        'Next.js 14 (App Router)',
        'TypeScript',
        'Tailwind CSS',
        'Shadcn/ui Components',
        'Framer Motion',
        'Puppeteer for PDF Export'
    ]
    
    backend_items = [
        'Next.js API Routes',
        'Prisma ORM + PostgreSQL',
        'OpenAI & Groq APIs',
        'Unsplash API',
        'Clerk Authentication',
        'Vercel Deployment'
    ]
    
    pdf.add_two_column_layout('Frontend Technologies', frontend_items, 
                             'Backend Technologies', backend_items)
    
    # 8. Competitive Analysis
    pdf.add_section_title('8. Competitive Analysis vs. Gamma')
    differentiators = [
        'Image Quality: Real Unsplash photos vs. AI-generated art',
        'Layout Control: Structured templates vs. limited customization',
        'Typography: Professional font pairing vs. basic selection',
        'Version Control: Side-by-side comparison vs. basic revisions'
    ]
    pdf.add_info_box('Key Differentiators', differentiators)
    
    # 9. Success Metrics
    pdf.add_section_title('9. Success Metrics')
    success_items = [
        'User Retention (30d): Achieve 40% target retention rate',
        'Free to Paid Conversion Rate: Hit 8% conversion target',
        'Generation Completion Rate: Ensure 85% successful completions',
        'User Satisfaction Score (CSAT): Maintain 4.2/5 or higher'
    ]
    pdf.add_info_box('Primary KPIs', success_items)
    
    # 10. Contribution Opportunities
    pdf.add_section_title('10. Contribution Opportunities')
    
    contribution_areas = [
        {
            'main': 'Frontend Development:',
            'sub': [
                'React component architecture',
                'Template design system',
                'Responsive layouts'
            ]
        },
        {
            'main': 'Backend Development:',
            'sub': [
                'API integration layers',
                'Database schema design',
                'Content generation logic'
            ]
        },
        {
            'main': 'Design & UX:',
            'sub': [
                'Template creation',
                'Typography systems',
                'User experience flows'
            ]
        }
    ]
    pdf.add_bullet_list(contribution_areas)
    
    return pdf

# Generate and save the PDF
if __name__ == "__main__":
    try:
        pdf = create_prd_pdf()
        output_path = "AI_Presentation_Generator_PRD.pdf"
        pdf.output(output_path)
        
        print("✅ PDF created successfully!")
        print(f"📄 File saved to: {os.path.abspath(output_path)}")
        print("🖤 Clean black and white formatting with proper pagination applied.")
        
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        print("Please ensure you have fpdf2 installed: pip install fpdf2")