"""
PDF Report Generation Module
Generates professional PDF reports for resume analysis.
"""

from typing import Dict, Any, Optional, List
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import KeepTogether, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime


class PDFReportGenerator:
    """
    Generate professional PDF reports for resume analysis.
    """
    
    def __init__(self, output_path: str):
        """
        Initialize PDF report generator.
        
        Args:
            output_path: Path to save the generated PDF.
        """
        self.output_path = output_path
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Custom styles
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6366f1'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#8b5cf6'),
            spaceAfter=20,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Normal text style
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            leading=16
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Score style
        self.styles.add(ParagraphStyle(
            name='ScoreText',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#6366f1'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
    
    def add_title(self, title: str):
        """Add title to report."""
        self.story.append(Paragraph(title, self.styles['CustomTitle']))
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_subtitle(self, subtitle: str):
        """Add subtitle to report."""
        self.story.append(Paragraph(subtitle, self.styles['CustomSubtitle']))
        self.story.append(Spacer(1, 0.1 * inch))
    
    def add_section_header(self, header: str):
        """Add section header."""
        self.story.append(Paragraph(header, self.styles['SectionHeader']))
    
    def add_paragraph(self, text: str):
        """Add paragraph text."""
        self.story.append(Paragraph(text, self.styles['CustomNormal']))
    
    def add_score_card(self, title: str, score: float, max_score: float = 100):
        """Add score card to report."""
        score_percentage = (score / max_score) * 100
        
        # Determine color based on score
        if score_percentage >= 80:
            color = colors.HexColor('#10b981')  # Green
        elif score_percentage >= 60:
            color = colors.HexColor('#f59e0b')  # Orange
        else:
            color = colors.HexColor('#ef4444')  # Red
        
        data = [
            [title, f"{score:.1f}/{max_score}"],
        ]
        
        table = Table(data, colWidths=[3 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [color]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_score_table(self, scores: Dict[str, float]):
        """Add multiple scores as a table."""
        data = [['Metric', 'Score']]
        
        for metric, score in scores.items():
            data.append([metric, f"{score:.1f}"])
        
        table = Table(data, colWidths=[3 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3 * inch))
    
    def add_list(self, items: List[str], bullet: str = '•'):
        """Add bulleted list."""
        for item in items:
            self.story.append(Paragraph(f"{bullet} {item}", self.styles['CustomNormal']))
        self.story.append(Spacer(1, 0.1 * inch))
    
    def add_strengths_weaknesses(self, strengths: List[str], weaknesses: List[str]):
        """Add strengths and weaknesses section."""
        # Strengths
        self.add_section_header("💪 Strengths")
        if strengths:
            self.add_list(strengths, '✓')
        else:
            self.add_paragraph("No specific strengths identified.")
        
        # Weaknesses
        self.add_section_header("🎯 Areas for Improvement")
        if weaknesses:
            self.add_list(weaknesses, '⚠️')
        else:
            self.add_paragraph("No specific weaknesses identified. Great job!")
        
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_improvements(self, improvements: List[str]):
        """Add improvement suggestions."""
        self.add_section_header("🚀 Improvement Suggestions")
        if improvements:
            self.add_list(improvements, '💡')
        else:
            self.add_paragraph("No specific improvement suggestions at this time.")
        
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_missing_skills(self, skills: List[str]):
        """Add missing skills section."""
        self.add_section_header("📚 Recommended Skills to Add")
        if skills:
            self.add_list(skills, '➕')
        else:
            self.add_paragraph("Your skill set looks comprehensive!")
        
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_recommended_projects(self, projects: List[str]):
        """Add recommended projects section."""
        self.add_section_header("🎨 Recommended Projects")
        if projects:
            self.add_list(projects, '📁')
        else:
            self.add_paragraph("Your project portfolio is strong!")
        
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_certificate_analysis(self, certificates: List[Dict[str, Any]]):
        """Add certificate analysis section."""
        self.add_section_header("🏆 Certificate Analysis")
        
        if certificates:
            for cert in certificates:
                self.story.append(Paragraph(
                    f"<b>{cert.get('name', 'Unknown Certificate')}</b>",
                    self.styles['CustomNormal']
                ))
                self.story.append(Paragraph(
                    f"Issuing Organization: {cert.get('issuing_organization', 'Unknown')}",
                    self.styles['CustomNormal']
                ))
                self.story.append(Paragraph(
                    f"Industry Value: {cert.get('industry_value', 'N/A').title()}",
                    self.styles['CustomNormal']
                ))
                self.story.append(Paragraph(
                    f"Relevance Score: {cert.get('relevance_score', 0):.1f}/100",
                    self.styles['CustomNormal']
                ))
                self.story.append(Spacer(1, 0.1 * inch))
        else:
            self.add_paragraph("No certificates analyzed.")
        
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_career_roadmap(self, roadmap: Dict[str, Any]):
        """Add career roadmap section."""
        self.add_section_header("🗺️ Career Roadmap")
        
        if roadmap:
            self.story.append(Paragraph(
                f"<b>Current Level:</b> {roadmap.get('current_level', 'N/A')}",
                self.styles['CustomNormal']
            ))
            self.story.append(Paragraph(
                f"<b>Target Level:</b> {roadmap.get('target_level', 'N/A')}",
                self.styles['CustomNormal']
            ))
            self.story.append(Paragraph(
                f"<b>Estimated Time:</b> {roadmap.get('estimated_time_to_target', 'N/A')}",
                self.styles['CustomNormal']
            ))
            
            self.story.append(Spacer(1, 0.1 * inch))
            
            # Skill gaps
            skill_gaps = roadmap.get('skill_gaps', [])
            if skill_gaps:
                self.story.append(Paragraph("<b>Skill Gaps:</b>", self.styles['CustomNormal']))
                self.add_list(skill_gaps, '•')
            
            # Recommended certifications
            certs = roadmap.get('recommended_certifications', [])
            if certs:
                self.story.append(Paragraph("<b>Recommended Certifications:</b>", self.styles['CustomNormal']))
                self.add_list(certs, '📜')
        else:
            self.add_paragraph("No career roadmap data available.")
        
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_salary_prediction(self, salary: Dict[str, Any]):
        """Add salary prediction section."""
        self.add_section_header("💰 Salary Prediction")
        
        if salary:
            self.story.append(Paragraph(
                f"<b>Salary Range:</b> ${salary.get('min_salary', 0):,.0f} - ${salary.get('max_salary', 0):,.0f}",
                self.styles['CustomNormal']
            ))
            self.story.append(Paragraph(
                f"<b>Average:</b> ${salary.get('average_salary', 0):,.0f}",
                self.styles['CustomNormal']
            ))
            self.story.append(Paragraph(
                f"<b>Market Comparison:</b> {salary.get('market_comparison', 'N/A').title()}",
                self.styles['CustomNormal']
            ))
            
            self.story.append(Spacer(1, 0.1 * inch))
            
            # Negotiation tips
            tips = salary.get('negotiation_tips', [])
            if tips:
                self.story.append(Paragraph("<b>Negotiation Tips:</b>", self.styles['CustomNormal']))
                self.add_list(tips, '💡')
        else:
            self.add_paragraph("No salary prediction data available.")
        
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_interview_questions(self, questions: Dict[str, Any]):
        """Add interview questions section."""
        self.add_section_header("❓ Interview Questions")
        
        if questions:
            # Technical questions
            tech_questions = questions.get('technical_questions', [])
            if tech_questions:
                self.story.append(Paragraph("<b>Technical Questions:</b>", self.styles['CustomNormal']))
                for q in tech_questions:
                    self.story.append(Paragraph(
                        f"• {q.get('question', '')} ({q.get('difficulty', 'N/A')})",
                        self.styles['CustomNormal']
                    ))
                self.story.append(Spacer(1, 0.1 * inch))
            
            # Behavioral questions
            behavioral_questions = questions.get('behavioral_questions', [])
            if behavioral_questions:
                self.story.append(Paragraph("<b>Behavioral Questions:</b>", self.styles['CustomNormal']))
                for q in behavioral_questions:
                    self.story.append(Paragraph(
                        f"• {q.get('question', '')}",
                        self.styles['CustomNormal']
                    ))
                self.story.append(Spacer(1, 0.1 * inch))
            
            # HR questions
            hr_questions = questions.get('hr_questions', [])
            if hr_questions:
                self.story.append(Paragraph("<b>HR Questions:</b>", self.styles['CustomNormal']))
                for q in hr_questions:
                    self.story.append(Paragraph(
                        f"• {q.get('question', '')}",
                        self.styles['CustomNormal']
                    ))
        else:
            self.add_paragraph("No interview questions available.")
        
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_footer(self):
        """Add footer to report."""
        self.story.append(Spacer(1, 0.5 * inch))
        self.story.append(Paragraph(
            f"Generated by HireSense AI on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['CustomNormal']
        ))
        self.story.append(Paragraph(
            "This report is AI-generated and should be used as a reference.",
            self.styles['CustomNormal']
        ))
    
    def generate_resume_analysis_report(
        self,
        analysis_data: Dict[str, Any],
        candidate_name: str = "Candidate"
    ) -> str:
        """
        Generate complete resume analysis report.
        
        Args:
            analysis_data: Complete analysis data from AI.
            candidate_name: Name of the candidate.
            
        Returns:
            Path to generated PDF file.
        """
        # Title
        self.add_title("HireSense AI - Resume Analysis Report")
        self.add_subtitle(f"Candidate: {candidate_name}")
        
        # Overall scores
        scores = {
            'Overall Score': analysis_data.get('overall_score', 0),
            'ATS Score': analysis_data.get('ats_score', 0),
            'Grammar Score': analysis_data.get('grammar_score', 0),
            'Communication Score': analysis_data.get('communication_score', 0),
            'Design Score': analysis_data.get('design_score', 0),
        }
        self.add_score_table(scores)
        
        # Sections analysis
        sections = analysis_data.get('sections', {})
        if sections:
            self.add_section_header("📊 Section Analysis")
            for section_name, section_data in sections.items():
                if isinstance(section_data, dict):
                    score = section_data.get('score', 0)
                    content = section_data.get('content', '')
                    suggestions = section_data.get('suggestions', [])
                    
                    self.story.append(Paragraph(
                        f"<b>{section_name.title()}:</b> {score:.1f}/100",
                        self.styles['CustomNormal']
                    ))
                    
                    if content:
                        self.story.append(Paragraph(
                            content[:200] + "..." if len(content) > 200 else content,
                            self.styles['CustomNormal']
                        ))
                    
                    if suggestions:
                        self.story.append(Paragraph("Suggestions:", self.styles['CustomNormal']))
                        self.add_list(suggestions[:3], '•')
                    
                    self.story.append(Spacer(1, 0.1 * inch))
        
        # Strengths and weaknesses
        self.add_strengths_weaknesses(
            analysis_data.get('strengths', []),
            analysis_data.get('weaknesses', [])
        )
        
        # Improvements
        self.add_improvements(analysis_data.get('improvement_suggestions', []))
        
        # Missing skills
        self.add_missing_skills(analysis_data.get('missing_skills', []))
        
        # Recommended projects
        self.add_recommended_projects(analysis_data.get('recommended_projects', []))
        
        # Footer
        self.add_footer()
        
        # Build PDF
        self.doc.build(self.story)
        
        return self.output_path
    
    def generate_hr_report(
        self,
        candidates: List[Dict[str, Any]],
        job_description: str
    ) -> str:
        """
        Generate HR recruitment report.
        
        Args:
            candidates: List of candidate analysis data.
            job_description: Job description used for analysis.
            
        Returns:
            Path to generated PDF file.
        """
        # Title
        self.add_title("HireSense AI - Recruitment Report")
        self.add_subtitle("Bulk Candidate Analysis")
        
        # Summary metrics
        total_candidates = len(candidates)
        strong_matches = sum(1 for c in candidates if c['analysis'].get('overall_score', 0) >= 70)
        avg_score = sum(c['analysis'].get('overall_score', 0) for c in candidates) / total_candidates if total_candidates > 0 else 0
        
        self.add_section_header("📊 Summary Metrics")
        metrics = [
            f"Total Candidates Analyzed: {total_candidates}",
            f"Strong Matches: {strong_matches}",
            f"Average Score: {avg_score:.1f}",
            f"Match Rate: {(strong_matches/total_candidates*100):.1f}%"
        ]
        self.add_list(metrics)
        
        # Job description snippet
        self.add_section_header("📋 Job Description")
        job_snippet = job_description[:300] + "..." if len(job_description) > 300 else job_description
        self.add_paragraph(job_snippet)
        
        # Candidate rankings
        self.add_section_header("🏆 Candidate Rankings")
        
        # Sort candidates by score
        sorted_candidates = sorted(
            candidates,
            key=lambda x: x['analysis'].get('overall_score', 0),
            reverse=True
        )
        
        for i, candidate in enumerate(sorted_candidates[:10]):  # Top 10
            analysis = candidate['analysis']
            score = analysis.get('overall_score', 0)
            
            self.story.append(Paragraph(
                f"<b>#{i + 1} {candidate['name']}</b>",
                self.styles['CustomNormal']
            ))
            self.story.append(Paragraph(
                f"Overall Score: {score:.1f} | ATS Score: {analysis.get('ats_score', 0):.1f}",
                self.styles['CustomNormal']
            ))
            
            # Status
            if score >= 80:
                status = "Strong Match ✓"
            elif score >= 60:
                status = "Potential Match ~"
            else:
                status = "Rejected ✗"
            
            self.story.append(Paragraph(f"Status: {status}", self.styles['CustomNormal']))
            self.story.append(Spacer(1, 0.1 * inch))
        
        # Footer
        self.add_footer()
        
        # Build PDF
        self.doc.build(self.story)
        
        return self.output_path
    
    def clear(self):
        """Clear current story for new report."""
        self.story = []


def generate_resume_report(
    analysis_data: Dict[str, Any],
    output_path: str,
    candidate_name: str = "Candidate"
) -> str:
    """
    Convenience function to generate resume analysis report.
    
    Args:
        analysis_data: Analysis data from AI.
        output_path: Path to save PDF.
        candidate_name: Name of candidate.
        
    Returns:
        Path to generated PDF.
    """
    generator = PDFReportGenerator(output_path)
    return generator.generate_resume_analysis_report(analysis_data, candidate_name)


def generate_hr_report(
    candidates: List[Dict[str, Any]],
    job_description: str,
    output_path: str
) -> str:
    """
    Convenience function to generate HR recruitment report.
    
    Args:
        candidates: List of candidate data.
        job_description: Job description.
        output_path: Path to save PDF.
        
    Returns:
        Path to generated PDF.
    """
    generator = PDFReportGenerator(output_path)
    return generator.generate_hr_report(candidates, job_description)
