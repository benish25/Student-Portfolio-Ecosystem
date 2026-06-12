import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ─── Custom Numbered Canvas to dynamically compute total pages ───
class AcademicNumberedCanvas(canvas.Canvas):
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
        # Suppress headers/footers on the first page (Cover page)
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#64748B')) # Slate
            self.drawString(54, 750, "MADRAS CHRISTIAN COLLEGE – COMPUTER SCIENCE DEPARTMENT")
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.5)
            self.line(54, 742, 612-54, 742)

            # Footer
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.setFont("Helvetica", 9)
            self.drawRightString(612 - 54, 40, page_text)
            self.drawString(54, 40, "Academic Project Implementation Report")
            self.line(54, 52, 612-54, 52)
        self.restoreState()

def create_report_diagrams():
    print("Generating diagrams for academic report...")
    # 1. System Architecture Diagram
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.axis('off')

    boxes = [
        ("Client Browser\n(Explore / Compare)", 0.03, 0.4, 0.22, 0.22, '#E0F2FE', '#0284C7'),
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
    plt.savefig('academic_system_architecture.png', dpi=300)
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
    plt.savefig('academic_database_relations.png', dpi=300)
    plt.close()

def build_academic_pdf():
    print("Building Academic PDF file...")
    pdf_filename = "MCC_Student_Portfolio_Platform_Academic_Report.pdf"
    
    # Document dimensions
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
    
    # Palette definition (MCC Maroon Theme)
    mcc_maroon = colors.HexColor('#800020')
    slate_blue = colors.HexColor('#0284C7')
    text_color = colors.HexColor('#334155')

    styles['Normal'].textColor = text_color
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14

    # Header style configurations
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=28,
        alignment=1, 
        textColor=mcc_maroon,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=15,
        alignment=1, 
        textColor=colors.HexColor('#475569'),
        spaceAfter=30
    )

    inst_style = ParagraphStyle(
        'CoverInstitution',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1, 
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=mcc_maroon,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    sub_section_style = ParagraphStyle(
        'SubSectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=slate_blue,
        spaceBefore=10,
        spaceAfter=4,
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

    # ──── TITLE / COVER PAGE ────
    story.append(Spacer(1, 100))
    story.append(Paragraph("MADRAS CHRISTIAN COLLEGE", inst_style))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE", inst_style))
    story.append(Paragraph("DEVELOPMENT OF AN INTERACTIVE STUDENT PORTFOLIO AND CAREER ENGINE", title_style))
    story.append(Paragraph("A Unified Digital Accomplishments Registry & Evaluation Platform", subtitle_style))
    story.append(Spacer(1, 40))

    # Cover Page Metadata Table
    metadata_data = [
        [Paragraph("<b>Submitted By:</b>", styles['Normal']), Paragraph("Student Project Implementation Team", styles['Normal'])],
        [Paragraph("<b>Submitted To:</b>", styles['Normal']), Paragraph("Department of Computer Science / Academic Audit Committee", styles['Normal'])],
        [Paragraph("<b>Institutional Context:</b>", styles['Normal']), Paragraph("NAAC / NIRF Student Activity Documentation & Analytics", styles['Normal'])],
        [Paragraph("<b>Status:</b>", styles['Normal']), Paragraph("Verified, Compiled, and Ready for Deployment", styles['Normal'])]
    ]
    t = Table(metadata_data, colWidths=[2.0*inch, 4.5*inch])
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0'))
    ]))
    story.append(t)
    story.append(PageBreak())

    # ──── INTRODUCTION ────
    story.append(Paragraph("1. Introduction", section_header_style))
    story.append(Paragraph(
        "Modern academic audit requirements demand structured, verified documentation of student achievements, "
        "including coding projects, certifications, research publications, hackathons, and NSS community services. "
        "Traditionally, this information is compiled manually via decentralized spreadsheets, which often leads to "
        "inconsistencies, duplicate reporting, and loss of institutional data. Furthermore, students require a unified, "
        "visually striking digital showcase to present their competencies to prospective recruiters during placements.",
        body_style
    ))
    story.append(Paragraph(
        "This project reports the design, development, and implementation of the <b>MCC Student Portfolio Platform</b>. "
        "The system acts as a secure multi-tenant student registry, combining advanced web technologies with custom SVG "
        "visual analytics, rules-based AI assistants, and centralized administrative controls.",
        body_style
    ))

    # ──── OBJECTIVES ────
    story.append(Paragraph("2. Objectives", section_header_style))
    story.append(Paragraph(
        "The primary developmental and institutional objectives of this project are as follows:",
        body_style
    ))
    objectives_list = [
        ("Unified Academic Registry", "To establish a secure relational database schema for capturing diverse student accomplishments, including projects, papers, hackathons, and certifications."),
        ("Interactive Visual Summaries", "To engineer dynamic frontend widgets (SVG radar competence charts and chronological milestone timelines) that model student capabilities in real-time."),
        ("AI-Powered Support Engine", "To integrate algorithmic rule models providing resume critic scores, career advisory paths, and automated Statement of Purpose (SOP) letters."),
        ("Public Directory & Comparison", "To design an anonymous directory search (/explore) and side-by-side comparison screen (/compare) with overlaid skill radar visualizations for recruiters."),
        ("Accreditation Auditing", "To equip administrators with analytics, profile verification workflows, and 1-click CSV exports to support NAAC/NIRF reporting documentation.")
    ]
    for title, desc in objectives_list:
        story.append(Paragraph(f"• <b><font color='#0284C7'>{title}</font></b>: {desc}", bullet_style))

    # ──── WORK DONE ────
    story.append(Paragraph("3. Work Done", section_header_style))
    story.append(Paragraph(
        "The project development was executed systematically across the following system layers:",
        body_style
    ))

    story.append(Paragraph("3.1 Core Database & API Backend Setup", sub_section_style))
    story.append(Paragraph(
        "Built a relational PostgreSQL database schema and developed a decoupled ASP.NET Core REST API backend. "
        "Implemented Entity Framework Core context models, custom DTO data structures, JWT authentication handlers, "
        "and controllers for student accomplishments and administrative metrics.",
        body_style
    ))

    # Embed DB schema
    if os.path.exists("academic_database_relations.png"):
        story.append(Spacer(1, 3))
        story.append(Image("academic_database_relations.png", width=6.2*inch, height=3.27*inch))
        caption_style = ParagraphStyle('CapDB', parent=styles['Normal'], fontSize=8, fontName='Helvetica-Oblique', alignment=1, textColor=colors.HexColor('#64748B'), spaceBefore=3)
        story.append(Paragraph("Figure 3.1: PostgreSQL Relational Database Schema & Entities Relationships Map", caption_style))
        story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 Next.js Responsive Frontend & Styling Engine", sub_section_style))
    story.append(Paragraph(
        "Designed and compiled a Next.js App Router (TypeScript, React) application. Developed responsive screens, "
        "established dynamic branding themes (Academic, Corporate, Startup, Creative, AI Futuristic) using CSS variables, "
        "and implemented print stylesheets to render high-fidelity, dual-column print profiles.",
        body_style
    ))

    # Embed system arch
    if os.path.exists("academic_system_architecture.png"):
        story.append(Spacer(1, 3))
        story.append(Image("academic_system_architecture.png", width=6.0*inch, height=2.4*inch))
        caption2_style = ParagraphStyle('CapArch', parent=styles['Normal'], fontSize=8, fontName='Helvetica-Oblique', alignment=1, textColor=colors.HexColor('#64748B'), spaceBefore=3)
        story.append(Paragraph("Figure 3.2: Multi-Tier Web Application Architecture & Data Routing", caption2_style))
        story.append(Spacer(1, 6))

    story.append(Paragraph("3.3 Visual Components & Comparison Module", sub_section_style))
    story.append(Paragraph(
        "Engineered the SVG Skill Radar pentagon visualizer and the chronological milestones timelines. Developed the "
        "public-facing search directory and the comparison dashboard, including the Dual-Overlay SVG Competency "
        "Radar Chart which displays two student polygons overlaid in translucent Cyan and Purple colors.",
        body_style
    ))

    story.append(PageBreak())

    # ──── LEARNING & CHALLENGES ────
    story.append(Paragraph("4. Learning & Challenges", section_header_style))
    
    story.append(Paragraph("4.1 Key Learning Outcomes", sub_section_style))
    story.append(Paragraph(
        "• <b>Full-Stack Development</b>: Mastered the integration of decoupled Next.js routers with C# RESTful controller pipelines.\n"
        "• <b>SVG Mathematics & Visuals</b>: Applied polar coordinate math to translate dynamically calculated database counts into "
        "interactive, multi-axis SVG canvas overlays.\n"
        "• <b>Static Rendering Constraints</b>: Learned page compilation optimization techniques within Next.js App Router static generators.",
        body_style
    ))

    story.append(Paragraph("4.2 System Challenges & Resolutions", sub_section_style))
    story.append(Paragraph(
        "• <b>Static Prerendering Failures</b>: When rendering the comparison screen (/compare), extracting URL search "
        "parameters triggered Next.js compilation bailouts. This was resolved by wrapping parameter-dependent components "
        "inside optimized React Suspense boundaries.\n"
        "• <b>Database Type Normalization</b>: PostgreSQL Npgsql drivers enforce DateTimeKind.Utc specifications. Data dates "
        "received from React state date selectors arrived unspecified. This was resolved by writing a custom static UTC converter "
        "normalizing dates before saving database records.\n"
        "• <b>Print Layout Formatting</b>: Maintaining complex grids under print layout exports caused clipping on pages. This was "
        "resolved by injecting strict CSS print rules overriding grid classes to print as compact, high-contrast layouts.",
        body_style
    ))

    # ──── OUTCOMES ────
    story.append(Paragraph("5. Outcomes", section_header_style))
    story.append(Paragraph(
        "The project succeeded in producing the following tangible deliverables:",
        body_style
    ))
    outcomes_list = [
        ("Operational Platform", "A compiled and verified client-server web app operating in local test domains with zero build warnings."),
        ("Verification Reports", "Central administrative controls producing clean CSV exports containing verified records for college archives."),
        ("Student Resume Generator", "A one-click, theme-aware print stylesheet generating standardized resume PDFs ready for recruiter review."),
        ("Comparison Console", "An interactive side-by-side compare layout featuring a dual-overlay Skill Radar Chart.")
    ]
    for title, desc in outcomes_list:
        story.append(Paragraph(f"• <b>{title}</b>: {desc}", bullet_style))

    # ──── FUTURE WORK ────
    story.append(Paragraph("6. Future Work", section_header_style))
    story.append(Paragraph(
        "• <b>API OAuth Scraper Integrations</b>: Establish automated integrations with GitHub and LinkedIn to pull student repository commits "
        "and certification credentials dynamically.\n"
        "• <b>Live LLM Integration</b>: Replace the rules-based local engine with conversational LLM APIs (e.g., Gemini) for AI career chat guidance.\n"
        "• <b>Verifiable Digital Credentials</b>: Integrate cryptographic signatures or decentralized ledger tokens (blockchain) to secure "
        "achievement verification against forgery.",
        body_style
    ))

    # ──── CONCLUSION ────
    story.append(Paragraph("7. Conclusion", section_header_style))
    story.append(Paragraph(
        "The MCC Student Portfolio Platform provides an innovative approach to student tracking and digital "
        "self-showcasing. By addressing both student branding requirements and administrative compliance protocols, "
        "the application reduces manual gathers for NAAC audits while preparing graduates for recruitment drives. The decoupled "
        "C# and TypeScript architecture proves the viability of modern frameworks in optimizing academic processes.",
        body_style
    ))

    # Build the PDF using AcademicNumberedCanvas for page numbers
    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print(f"Academic PDF successfully built: {pdf_filename}")

if __name__ == "__main__":
    create_report_diagrams()
    build_academic_pdf()
    # Clean up diagrams
    if os.path.exists("academic_system_architecture.png"):
        os.remove("academic_system_architecture.png")
    if os.path.exists("academic_database_relations.png"):
        os.remove("academic_database_relations.png")
    print("Academic PDF build process finished.")
