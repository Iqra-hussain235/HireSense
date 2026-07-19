"""
Certificate Analysis Module
Analyzes certificates and estimates their industry value and relevance.
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .document_extractor import DocumentExtractor, TextCleaner
from core.ai.base_llm import BaseLLMClient


@dataclass
class CertificateInfo:
    """Data class for certificate information."""
    name: str
    issuing_organization: str
    issue_date: Optional[str]
    expiration_date: Optional[str]
    credential_id: Optional[str]
    relevance_score: float
    industry_value: str
    skills_covered: List[str]
    recognition_level: str
    suggested_usage: str
    complementary_certifications: List[str]


class CertificateAnalyzer:
    """
    Analyze certificates and provide insights on their value and relevance.
    """
    
    def __init__(self, llm_client: BaseLLMClient):
        """
        Initialize certificate analyzer.
        
        Args:
            llm_client: LLM client instance for AI analysis.
        """
        self.llm_client = llm_client
        self.document_extractor = DocumentExtractor()
        self.text_cleaner = TextCleaner()
        
        # Known high-value certifications database
        self.high_value_certifications = {
            'cloud': {
                'aws': ['AWS Solutions Architect', 'AWS Developer', 'AWS SysOps'],
                'azure': ['Azure Administrator', 'Azure Developer', 'Azure Architect'],
                'gcp': ['Google Cloud Professional', 'GCP Architect'],
            },
            'data_science': {
                'general': ['Data Science', 'Machine Learning', 'AI'],
                'tools': ['TensorFlow', 'PyTorch', 'Tableau', 'Power BI'],
            },
            'devops': {
                'tools': ['Kubernetes', 'Docker', 'Jenkins', 'GitLab'],
                'methodologies': ['DevOps', 'Agile', 'Scrum'],
            },
            'cybersecurity': {
                'security': ['CISSP', 'CEH', 'CompTIA Security+', 'CISM'],
                'network': ['Network+', 'CCNA', 'CCNP'],
            },
            'programming': {
                'general': ['Oracle Certified', 'Microsoft Certified'],
                'specialized': ['React', 'Angular', 'Node.js'],
            },
            'project_management': {
                ' methodologies': ['PMP', 'PRINCE2', 'CAPM'],
                'agile': ['CSM', 'PSM', 'SAFe'],
            },
        }
    
    def analyze_certificate(
        self,
        certificate_file: Optional[str] = None,
        certificate_text: Optional[str] = None,
        resume_text: Optional[str] = None,
        target_role: Optional[str] = None
    ) -> CertificateInfo:
        """
        Analyze a certificate and provide comprehensive insights.
        
        Args:
            certificate_file: Path to certificate file (PDF, image).
            certificate_text: Pre-extracted certificate text.
            resume_text: Optional resume text for context.
            target_role: Optional target job role for relevance.
            
        Returns:
            CertificateInfo object with analysis results.
        """
        # Extract text if file is provided
        if certificate_file and not certificate_text:
            certificate_text = self.document_extractor.extract_text(certificate_file)
        
        if not certificate_text:
            raise ValueError("Either certificate_file or certificate_text must be provided")
        
        # Clean the text
        cleaned_text = self.text_cleaner.clean_text(certificate_text)
        
        # Use AI for detailed analysis
        ai_result = self.llm_client.analyze_certificate(
            cleaned_text,
            resume_text
        )
        
        if ai_result.success:
            ai_data = ai_result.data
            
            # Enhance with local knowledge base
            enhanced_data = self._enhance_with_knowledge_base(
                ai_data,
                target_role
            )
            
            return CertificateInfo(
                name=enhanced_data.get('certificate_name', 'Unknown'),
                issuing_organization=enhanced_data.get('issuing_organization', 'Unknown'),
                issue_date=enhanced_data.get('issue_date'),
                expiration_date=enhanced_data.get('expiration_date'),
                credential_id=enhanced_data.get('credential_id'),
                relevance_score=enhanced_data.get('relevance_score', 50),
                industry_value=enhanced_data.get('industry_value', 'medium'),
                skills_covered=enhanced_data.get('skills_covered', []),
                recognition_level=enhanced_data.get('recognition_level', 'organization'),
                suggested_usage=enhanced_data.get('suggested_usage', ''),
                complementary_certifications=enhanced_data.get('complementary_certifications', [])
            )
        else:
            # Fallback to basic analysis
            return self._basic_certificate_analysis(cleaned_text, target_role)
    
    def analyze_multiple_certificates(
        self,
        certificate_files: List[str],
        resume_text: Optional[str] = None,
        target_role: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze multiple certificates and provide combined insights.
        
        Args:
            certificate_files: List of certificate file paths.
            resume_text: Optional resume text for context.
            target_role: Optional target job role.
            
        Returns:
            Dictionary with combined analysis results.
        """
        certificates = []
        total_relevance_score = 0
        
        for cert_file in certificate_files:
            try:
                cert_info = self.analyze_certificate(
                    certificate_file=cert_file,
                    resume_text=resume_text,
                    target_role=target_role
                )
                certificates.append(cert_info)
                total_relevance_score += cert_info.relevance_score
            except Exception as e:
                continue
        
        if not certificates:
            return {
                'success': False,
                'error': 'No certificates could be analyzed',
                'certificates': []
            }
        
        # Calculate combined metrics
        all_skills = []
        for cert in certificates:
            all_skills.extend(cert.skills_covered)
        
        unique_skills = list(set(all_skills))
        
        return {
            'success': True,
            'certificates': certificates,
            'summary': {
                'total_certificates': len(certificates),
                'average_relevance_score': total_relevance_score / len(certificates),
                'all_skills_covered': unique_skills,
                'high_value_count': sum(1 for c in certificates if c.industry_value == 'high'),
                'recommendations': self._generate_certificate_recommendations(
                    certificates,
                    target_role
                )
            }
        }
    
    def _enhance_with_knowledge_base(
        self,
        ai_data: Dict[str, Any],
        target_role: Optional[str]
    ) -> Dict[str, Any]:
        """
        Enhance AI analysis with local knowledge base.
        
        Args:
            ai_data: Data from AI analysis.
            target_role: Target job role.
            
        Returns:
            Enhanced data dictionary.
        """
        cert_name = ai_data.get('certificate_name', '').lower()
        
        # Check against high-value certifications
        for category, certs in self.high_value_certifications.items():
            for subcategory, cert_list in certs.items():
                for high_value_cert in cert_list:
                    if high_value_cert.lower() in cert_name:
                        ai_data['industry_value'] = 'high'
                        ai_data['recognition_level'] = 'industry'
                        break
        
        # Adjust relevance based on target role
        if target_role:
            target_role_lower = target_role.lower()
            
            # Check if certificate aligns with target role
            role_keywords = {
                'developer': ['developer', 'programming', 'software', 'full stack'],
                'data scientist': ['data', 'machine learning', 'ai', 'analytics'],
                'devops': ['devops', 'cloud', 'kubernetes', 'docker'],
                'cybersecurity': ['security', 'cyber', 'network', 'cissp'],
                'project manager': ['project', 'management', 'pmp', 'agile'],
            }
            
            for role, keywords in role_keywords.items():
                if role in target_role_lower:
                    if any(keyword in cert_name for keyword in keywords):
                        ai_data['relevance_score'] = min(100, ai_data.get('relevance_score', 50) + 20)
        
        return ai_data
    
    def _basic_certificate_analysis(
        self,
        certificate_text: str,
        target_role: Optional[str]
    ) -> CertificateInfo:
        """
        Perform basic certificate analysis without AI.
        
        Args:
            certificate_text: Extracted certificate text.
            target_role: Target job role.
            
        Returns:
            CertificateInfo with basic analysis.
        """
        text_lower = certificate_text.lower()
        
        # Try to identify certificate name
        name = self._extract_certificate_name(certificate_text)
        
        # Try to identify organization
        org = self._extract_organization(certificate_text)
        
        # Determine industry value
        industry_value = 'medium'
        for category, certs in self.high_value_certifications.items():
            for subcategory, cert_list in certs.items():
                for high_value_cert in cert_list:
                    if high_value_cert.lower() in text_lower:
                        industry_value = 'high'
                        break
        
        return CertificateInfo(
            name=name,
            issuing_organization=org,
            issue_date=None,
            expiration_date=None,
            credential_id=None,
            relevance_score=50 if industry_value == 'medium' else 75,
            industry_value=industry_value,
            skills_covered=[],
            recognition_level='organization',
            suggested_usage='Include in certifications section of resume',
            complementary_certifications=[]
        )
    
    def _extract_certificate_name(self, text: str) -> str:
        """
        Extract certificate name from text.
        
        Args:
            text: Certificate text.
            
        Returns:
            Extracted certificate name.
        """
        lines = text.split('\n')
        
        # Look for common certificate patterns
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 100:
                # Skip common non-certificate lines
                skip_words = ['certificate', 'certification', 'of', 'completion', 'this']
                if not any(word in line.lower() for word in skip_words):
                    return line
        
        return 'Unknown Certificate'
    
    def _extract_organization(self, text: str) -> str:
        """
        Extract issuing organization from text.
        
        Args:
            text: Certificate text.
            
        Returns:
            Extracted organization name.
        """
        text_lower = text.lower()
        
        # Common organizations
        organizations = [
            'aws', 'amazon', 'microsoft', 'google', 'oracle',
            'cisco', 'ibm', 'compTIA', 'isc2', 'pmi',
            'coursera', 'udemy', 'edx', 'pluralsight'
        ]
        
        for org in organizations:
            if org in text_lower:
                return org.capitalize()
        
        return 'Unknown Organization'
    
    def _generate_certificate_recommendations(
        self,
        certificates: List[CertificateInfo],
        target_role: Optional[str]
    ) -> List[str]:
        """
        Generate recommendations based on certificate analysis.
        
        Args:
            certificates: List of analyzed certificates.
            target_role: Target job role.
            
        Returns:
            List of recommendations.
        """
        recommendations = []
        
        # Check for high-value certifications
        high_value_count = sum(1 for c in certificates if c.industry_value == 'high')
        
        if high_value_count == 0:
            recommendations.append(
                "Consider pursuing industry-recognized certifications to increase credibility"
            )
        
        # Check for skill gaps
        all_skills = []
        for cert in certificates:
            all_skills.extend(cert.skills_covered)
        
        if target_role:
            role_skill_mapping = {
                'developer': ['javascript', 'python', 'react', 'node.js', 'aws'],
                'data scientist': ['python', 'machine learning', 'sql', 'tensorflow', 'statistics'],
                'devops': ['docker', 'kubernetes', 'aws', 'ci/cd', 'linux'],
            }
            
            if target_role.lower() in role_skill_mapping:
                required_skills = role_skill_mapping[target_role.lower()]
                missing_skills = [
                    skill for skill in required_skills
                    if skill.lower() not in ' '.join(all_skills).lower()
                ]
                
                if missing_skills:
                    recommendations.append(
                        f"Consider certifications covering: {', '.join(missing_skills)}"
                    )
        
        # General recommendations
        if len(certificates) < 2:
            recommendations.append(
                "Having multiple relevant certifications can strengthen your profile"
            )
        
        return recommendations
    
    def calculate_certificate_score(
        self,
        certificates: List[CertificateInfo]
    ) -> Dict[str, Any]:
        """
        Calculate overall certificate score.
        
        Args:
            certificates: List of CertificateInfo objects.
            
        Returns:
            Dictionary with score breakdown.
        """
        if not certificates:
            return {
                'total_score': 0,
                'quantity_score': 0,
                'quality_score': 0,
                'relevance_score': 0,
                'diversity_score': 0
            }
        
        # Quantity score (0-25)
        quantity_score = min(25, len(certificates) * 5)
        
        # Quality score based on industry value (0-25)
        quality_score = 0
        for cert in certificates:
            if cert.industry_value == 'high':
                quality_score += 10
            elif cert.industry_value == 'medium':
                quality_score += 5
        quality_score = min(25, quality_score)
        
        # Relevance score (0-25)
        avg_relevance = sum(c.relevance_score for c in certificates) / len(certificates)
        relevance_score = (avg_relevance / 100) * 25
        
        # Diversity score based on skill coverage (0-25)
        all_skills = []
        for cert in certificates:
            all_skills.extend(cert.skills_covered)
        unique_skills = len(set(all_skills))
        diversity_score = min(25, unique_skills * 2)
        
        total_score = quantity_score + quality_score + relevance_score + diversity_score
        
        return {
            'total_score': round(total_score, 2),
            'quantity_score': round(quantity_score, 2),
            'quality_score': round(quality_score, 2),
            'relevance_score': round(relevance_score, 2),
            'diversity_score': round(diversity_score, 2)
        }
