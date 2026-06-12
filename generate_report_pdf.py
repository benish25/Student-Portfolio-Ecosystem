import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ─── Custom Numbered Canvas to dynamically compute total pages ───
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Suppress headers/footers on the first page
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#64748B')) # Slate
            self.drawString(54, 750, "MADRAS CHRISTIAN COLLEGE – STUDENT PORTFOLIO PLATFORM")
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.5)
            self.line(54, 742, 612-54, 742)

            # Footer
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.setFont("Helvetica", 9)
            self.drawRightString(612 - 54, 40, page_text)
            self.drawString(54, 40, "Department of Computer Science — Academic Implementation Report")
            self.line(54, 52, 612-54, 52)
        self.restoreState()

def create_diagrams():
    print("Generating diagrams for PDF...")
    # 1. System Architecture Diagram
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.axis('off')

    boxes = [
        ("Client Browser\n(Explore/Compare/Dashboard)", 0.03, 0.4, 0.22, 0.22, '#E0F2FE', '#0284C7'),
        ("Next.js Frontend\n(React Router + TS)", 0.32, 0.4, 0.22, 0.22, '#F0FDF4', '#16A34A'),
        ("ASP.NET Core Web API\n(C# Backend Engine)", 0.61, 0.4, 0.22, 0.22, '#FAF5FF', '#7E22CE'),
        ("PostgreSQL DB\n(mcc_portfolio)", 0.88, 0.4, 0.10, 0.22, '#FEF2F2', '#DC2626')
    ]

    for text, x, y, w, h, bg, border in boxes:
        rect = plt.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, lw=2, transform=ax.transAxes, zorder=3)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, color='#0F172A', fontsize=8, fontweight='bold',
                ha='center', va='center', wrap=True, transform=ax.transAxes, zorder=4)

    arrows = [
        (0.25, 0.51, 0.32, 0.51),
        (0.54, 0.51, 0.61, 0.51),
        (0.83, 0.51, 0.88, 0.51)
    ]
    for x1, y1, x2, y2 in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="<->", color='#475569', lw=2, zorder=2),
                    xycoords='axes fraction', textcoords='axes fraction')

    # Draw local AI Engine
    rect_ai = plt.Rectangle((0.63, 0.05), 0.18, 0.18, facecolor='#FEF3C7', edgecolor='#D97706', lw=1.5, ls='--', transform=ax.transAxes, zorder=3)
    ax.add_patch(rect_ai)
    ax.text(0.72, 0.14, "Rule Engine\n(AI Assistant)", color='#0F172A', fontsize=7, fontweight='bold',
            ha='center', va='center', wrap=True, transform=ax.transAxes, zorder=4)
    ax.annotate("", xy=(0.72, 0.4), xytext=(0.72, 0.23),
                arrowprops=dict(arrowstyle="<->", color='#64748B', lw=1.5, ls='--', zorder=2),
                xycoords='axes fraction', textcoords='axes fraction')

    plt.title("MCC Portfolio System - Multi-Tier Architecture", fontsize=10, fontweight='bold', pad=10, color='#1E293B')
    plt.tight_layout()
    plt.savefig('system_architecture.png', dpi=300)
    plt.close()

    # 2. Database Relationships Diagram
    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.axis('off')

    tables = [
        ("Users\n- Id [PK]\n- Username\n- Email\n- Role", 0.03, 0.72, 0.20, 0.22, '#F1F5F9', '#475569'),
        ("StudentProfiles\n- Id [PK]\n- UserId [FK]\n- FullName\n- Bio\n- Department\n- Theme\n- Approved", 0.36, 0.45, 0.25, 0.38, '#ECFDF5', '#059669'),
        ("Projects\n- Id [PK]\n- ProfileId [FK]\n- Title\n- TechStack\n- GithubUrl", 0.75, 0.81, 0.21, 0.17, '#EFF6FF', '#2563EB'),
        ("Certifications\n- Id [PK]\n- ProfileId [FK]\n- Name\n- Issuer\n- CredentialUrl", 0.75, 0.61, 0.21, 0.17, '#EFF6FF', '#2563EB'),
        ("ResearchPapers\n- Id [PK]\n- ProfileId [FK]\n- Title\n- JournalName\n- PublishDate", 0.75, 0.41, 0.21, 0.17, '#EFF6FF', '#2563EB'),
        ("Hackathons / Extra\n- Id [PK]\n- ProfileId [FK]\n- EventName\n- Prize", 0.75, 0.21, 0.21, 0.17, '#EFF6FF', '#2563EB'),
        ("ThemeConfigs\n- Id [PK]\n- Name\n- PrimaryColor\n- IsEnabled", 0.03, 0.35, 0.20, 0.20, '#FFFBEB', '#D97706'),
        ("Institutions\n- Id [PK]\n- Name\n- Address\n- WebsiteUrl", 0.03, 0.08, 0.20, 0.20, '#FFFBEB', '#D97706')
    ]

    for text, x, y, w, h, bg, border in tables:
        rect = plt.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, lw=1.5, transform=ax.transAxes, zorder=3)
        ax.add_patch(rect)
        ax.text(x + 0.02, y + h - 0.03, text, color='#0F172A', fontsize=7.5, fontname='monospace',
                ha='left', va='top', wrap=True, transform=ax.transAxes, zorder=4)

    # Drawing relationships (arrows)
    ax.annotate("", xy=(0.36, 0.75), xytext=(0.23, 0.82),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.1", color='#64748B', lw=1.5, zorder=2),
                xycoords='axes fraction', textcoords='axes fraction')
    ax.annotate("", xy=(0.75, 0.88), xytext=(0.61, 0.78),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.1", color='#64748B', lw=1.5, zorder=2),
                xycoords='axes fraction', textcoords='axes fraction')
    ax.annotate("", xy=(0.75, 0.70), xytext=(0.61, 0.65),
                arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.5, zorder=2),
                xycoords='axes fraction', textcoords='axes fraction')
    ax.annotate("", xy=(0.75, 0.50), xytext=(0.61, 0.58),
                arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.5, zorder=2),
                xycoords='axes fraction', textcoords='axes fraction')
    ax.annotate("", xy=(0.75, 0.30), xytext=(0.61, 0.50),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.1", color='#64748B', lw=1.5, zorder=2),
                xycoords='axes fraction', textcoords='axes fraction')

    plt.title("MCC Portfolio PostgreSQL Database Relationships Schema", fontsize=10, fontweight='bold', pad=10, color='#1E293B')
    plt.tight_layout()
    plt.savefig('database_relations.png', dpi=300)
    plt.close()

def build_pdf():
    print("Building PDF file...")
    # Setup document
    pdf_filename = "MCC_Student_Portfolio_Platform_Project_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    # Styles Setup
    styles = getSampleStyleSheet()
    
    # Custom palette
    mcc_maroon = colors.HexColor('#800020')
    slate_blue = colors.HexColor('#0284C7')
    text_color = colors.HexColor('#334155')

    # Modify existing styles to be clean
    styles['Normal'].textColor = text_color
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14

    # Define custom paragraphs styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        alignment=1, # Center
        textColor=mcc_maroon,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        alignment=1, # Center
        textColor=colors.HexColor('#475569'),
        spaceAfter=30
    )

    inst_style = ParagraphStyle(
        'CoverInstitution',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1, # Center
        textColor=colors.HexColor('#64748B'),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=mcc_maroon,
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=slate_blue,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        spaceAfter=10
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    story = []

    # ──── COVER PAGE ────
    story.append(Spacer(1, 120))
    story.append(Paragraph("MADRAS CHRISTIAN COLLEGE", inst_style))
    story.append(Paragraph("STUDENT PORTFOLIO PLATFORM", title_style))
    story.append(Paragraph("Project Implementation & Departmental Registry Report", subtitle_style))
    story.append(Spacer(1, 40))

    # Metadata table for cover page
    metadata_data = [
        [Paragraph("<b>Prepared For:</b>", styles['Normal']), Paragraph("Department of Computer Science / Academic Audit Committee", styles['Normal'])],
        [Paragraph("<b>Date of Report:</b>", styles['Normal']), Paragraph("June 9, 2026", styles['Normal'])],
        [Paragraph("<b>Software Stack:</b>", styles['Normal']), Paragraph("ASP.NET Core Web API, PostgreSQL, Next.js (TypeScript)", styles['Normal'])],
        [Paragraph("<b>Deployment Status:</b>", styles['Normal']), Paragraph("Ready for Production (0 errors, dev servers online)", styles['Normal'])]
    ]
    t = Table(metadata_data, colWidths=[2.0*inch, 4.5*inch])
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#F1F5F9'))
    ]))
    story.append(t)
    
    story.append(PageBreak())

    # ──── SECTION 1 ────
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "The Madras Christian College (MCC) Student Portfolio Platform is an advanced web-based registry and "
        "digital showcase application designed to track and publish student achievements. The platform addresses "
        "key institutional documentation challenges, enabling students to log their projects, certifications, research "
        "publications, hackathons, and community services. In doing so, it serves as a central registry that aligns "
        "directly with the rigorous document auditing parameters established by NAAC and NIRF accreditation teams.",
        body_style
    ))
    story.append(Paragraph(
        "By hosting a dynamic gallery with live profile sharing, side-by-side competency comparisons, and professional "
        "PDF resume exporting, the platform bridges the gap between academic progress and industry recruitment, "
        "advancing the digital footprint of the Computer Science Department.",
        body_style
    ))

    # ──── SECTION 2 ────
    story.append(Paragraph("2. System Architecture & Tech Stack", h1_style))
    story.append(Paragraph(
        "The platform utilizes a modern, decoupled multi-tier architecture to deliver high-performance user interfaces "
        "and securely managed relational database transactions. Standard JSON web tokens (JWT) handle student "
        "and administrator authorization states, while Entity Framework Core handles communication with a local PostgreSQL server.",
        body_style
    ))

    # Embed system architecture image
    if os.path.exists("system_architecture.png"):
        story.append(Spacer(1, 5))
        story.append(Image("system_architecture.png", width=6.0*inch, height=2.4*inch))
        caption_style = ParagraphStyle('Cap1', parent=styles['Normal'], fontSize=8.5, fontName='Helvetica-Oblique', alignment=1, textColor=colors.HexColor('#64748B'), spaceBefore=4)
        story.append(Paragraph("Figure 2.1: Multi-Tier System Architecture & Routing Flow", caption_style))
        story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Core Technology Specifications:</b>", body_style))
    bullets = [
        ("Frontend Application", "Next.js App Router (React, TypeScript) styling via CSS theme configurations and layout modules."),
        ("Backend Web API", "ASP.NET Core (C#) utilizing Controllers, custom DTO bindings, Cors middleware configuration, and Jwt security pipeline."),
        ("Database Layer", "PostgreSQL running locally at port 5432, storing tables for profiles, records, notifications, and institution themes."),
        ("AI Analytics Engine", "A C# logic rules engine assessing tech stacks, portfolio completeness scores, and crafting dynamic letters.")
    ]
    for title, desc in bullets:
        story.append(Paragraph(f"• <b><font color='#0284C7'>{title}</font></b>: {desc}", bullet_style))

    story.append(PageBreak())

    # ──── SECTION 3 ────
    story.append(Paragraph("3. Database Schema & Models", h1_style))
    story.append(Paragraph(
        "The relational database schema is structured to accommodate the diverse range of milestones "
        "encountered by undergraduate and postgraduate students. Cascading deletes are enforced on the User profile level "
        "to ensure student data integrity, matching standard privacy and compliance rules.",
        body_style
    ))

    # Embed database relations image
    if os.path.exists("database_relations.png"):
        story.append(Spacer(1, 5))
        story.append(Image("database_relations.png", width=6.2*inch, height=3.27*inch))
        caption2_style = ParagraphStyle('Cap2', parent=styles['Normal'], fontSize=8.5, fontName='Helvetica-Oblique', alignment=1, textColor=colors.HexColor('#64748B'), spaceBefore=4)
        story.append(Paragraph("Figure 3.1: PostgreSQL Relational Database Schema & Primary/Foreign Key Mappings", caption2_style))
        story.append(Spacer(1, 10))

    # ──── SECTION 4 ────
    story.append(Paragraph("4. Key Platform Features & Modules", h1_style))
    
    story.append(Paragraph("4.1 Interactive Accomplishment Milestones", h2_style))
    story.append(Paragraph(
        "To present a high-fidelity visual summary of students' accomplishments, the public portfolio route incorporates:\n"
        "1. Competency Skill Radar: An SVG radar polygon parsing coding project tech stacks, certifications, and creative "
        "contributions into five domain scores: Frontend, Backend, Databases, DevOps & Tools, and Creative/Research.\n"
        "2. Chronological Milestones Timeline: A vertical timeline sorting and presenting all student achievements. Supports "
        "filters (Projects, Credentials, Extracurriculars) and detail modal drawers.",
        body_style
    ))

    story.append(Paragraph("4.2 AI Career Guidance Console", h2_style))
    story.append(Paragraph(
        "Students are equipped with three helper functions driven by a local algorithmic rules engine:\n"
        "• Resume Completeness Critic: Automatically scores a profile from 0-100 based on modules completed and lists actionable suggestions.\n"
        "• Statement of Purpose (SOP) Generator: Automatically builds custom, formatted letters mapping projects to tone preferences.\n"
        "• Career Path Advisor: Identifies technical stack profiles and suggests roles, skills gaps, target universities, and scholarships.",
        body_style
    ))

    story.append(Paragraph("4.3 Public Directory & Side-by-Side Comparison Engine", h2_style))
    story.append(Paragraph(
        "For external visitors, admissions, or placement officers, the system provides:\n"
        "• Public Registry (/explore): Searchable directory allowing users to look up students by skills, name, or department.\n"
        "• Side-by-Side Comparison (/compare): Displays two students side-by-side. Highlights skill overlaps using a Dual-Overlay "
        "SVG Skill Radar Chart displaying both competency polygons in translucent Cyan and Purple layers.",
        body_style
    ))

    story.append(Paragraph("4.4 Print-to-PDF Stylesheets & Resume Exporting", h2_style))
    story.append(Paragraph(
        "A customized print layout configuration triggers on window.print() (Export Resume), instantly refactoring the "
        "profile structure into a clean, print-friendly 2-column professional resume layout. It automatically hides screen-only elements, "
        "inverts high-saturation background fills, and aligns contact parameters for high-fidelity printing.",
        body_style
    ))

    story.append(Paragraph("4.5 Administrator Management Panel", h2_style))
    story.append(Paragraph(
        "Department Heads and administrative users can check overall database counts, approve or revoke public profile listings, "
        "manage campus announcements, and download a single CSV backup containing all verified student details for record archiving.",
        body_style
    ))

    # ──── SECTION 5 ────
    story.append(Paragraph("5. Accreditation & Academic Implementation Value", h1_style))
    story.append(Paragraph(
        "The implementation of the MCC Student Portfolio Platform delivers measurable benefits for departments:\n"
        "1. NAAC/NIRF Criteria Data Audits: The administrative CSV exporter instantly maps student publications, projects, "
        "and community service logs, resolving manual information gathering.\n"
        "2. Streamlined Campus Recruitment: Provides recruiters with immediate, authenticated visibility into the students' coding portfolios, "
        "skills radar distribution charts, and project repositories.\n"
        "3. Departmental Showcasing: Organizes and preserves institutional memory, cataloging historical achievements, hackathons, and creative vector sketches.",
        body_style
    ))

    # Build the PDF using NumberedCanvas for "Page X of Y"
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {pdf_filename}")

if __name__ == "__main__":
    create_diagrams()
    build_pdf()
    # Clean up diagrams
    if os.path.exists("system_architecture.png"):
        os.remove("system_architecture.png")
    if os.path.exists("database_relations.png"):
        os.remove("database_relations.png")
    print("PDF build process finished.")
