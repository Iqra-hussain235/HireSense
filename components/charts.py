"""
Data Visualization Components
Creates professional charts using Plotly for resume analysis and HR dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np


class ChartGenerator:
    """
    Generate professional charts for resume analysis and HR dashboard.
    """
    
    def __init__(self, theme: str = 'dark'):
        """
        Initialize chart generator.
        
        Args:
            theme: Chart theme ('dark' or 'light').
        """
        self.theme = theme
        self.colors = {
            'primary': '#6366f1',
            'secondary': '#8b5cf6',
            'tertiary': '#a855f7',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'info': '#3b82f6',
        }
        
        # Plotly template
        self.template = 'plotly_dark' if theme == 'dark' else 'plotly'
    
    def create_score_gauge(self, score: float, title: str = "Score") -> go.Figure:
        """
        Create a gauge chart for score visualization.
        
        Args:
            score: Score value (0-100).
            title: Chart title.
            
        Returns:
            Plotly figure object.
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': self.colors['primary']},
                'steps': [
                    {'range': [0, 50], 'color': self.colors['error']},
                    {'range': [50, 75], 'color': self.colors['warning']},
                    {'range': [75, 100], 'color': self.colors['success']},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            template=self.template,
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        
        return fig
    
    def create_score_radar(self, scores: Dict[str, float], title: str = "Skill Analysis") -> go.Figure:
        """
        Create a radar chart for multi-dimensional score visualization.
        
        Args:
            scores: Dictionary of metric names and scores.
            title: Chart title.
            
        Returns:
            Plotly figure object.
        """
        categories = list(scores.keys())
        values = list(scores.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Scores',
            line_color=self.colors['primary'],
            fillcolor=f'rgba(99, 102, 241, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            template=self.template,
            title=title,
            height=400,
        )
        
        return fig
    
    def create_score_comparison_bar(self, scores: Dict[str, float], title: str = "Score Comparison") -> go.Figure:
        """
        Create a bar chart for score comparison.
        
        Args:
            scores: Dictionary of metric names and scores.
            title: Chart title.
            
        Returns:
            Plotly figure object.
        """
        categories = list(scores.keys())
        values = list(scores.values())
        
        colors = [self.colors['primary'] if v >= 70 else self.colors['warning'] if v >= 50 else self.colors['error'] for v in values]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=colors,
                text=values,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            template=self.template,
            title=title,
            yaxis_title='Score',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        
        return fig
    
    def create_candidate_ranking_chart(self, candidates: List[Dict[str, Any]], title: str = "Candidate Ranking") -> go.Figure:
        """
        Create a horizontal bar chart for candidate ranking.
        
        Args:
            candidates: List of candidate dictionaries with 'name' and 'score'.
            title: Chart title.
            
        Returns:
            Plotly figure object.
        """
        names = [c['name'][:20] for c in candidates]  # Truncate long names
        scores = [c['analysis'].get('overall_score', 0) for c in candidates]
        
        colors = [self.colors['success'] if s >= 70 else self.colors['warning'] if s >= 50 else self.colors['error'] for s in scores]
        
        fig = go.Figure(data=[
            go.Bar(
                x=scores,
                y=names,
                orientation='h',
                marker_color=colors,
                text=scores,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            template=self.template,
            title=title,
            xaxis_title='Overall Score',
            height=max(400, len(candidates) * 30),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        
        return fig
    
    def create_skill_distribution_pie(self, skills: Dict[str, int], title: str = "Skill Distribution") -> go.Figure:
        """
        Create a pie chart for skill distribution.
        
        Args:
            skills: Dictionary of skill names and counts.
            title: Chart title.
            
        Returns:
            Plotly figure object.
        """
        labels = list(skills.keys())
        values = list(skills.values())
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            marker=dict(colors=px.colors.qualitative.Plotly)
        )])
        
        fig.update_layout(
            template=self.template,
            title=title,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        
        return fig
    
    def create_experience_scatter(self, candidates: List[Dict[str, Any]], title: str = "Experience vs Score") -> go.Figure:
        """
        Create a scatter plot for experience vs score analysis.
        
        Args:
            candidates: List of candidate dictionaries.
            title: Chart title.
            
        Returns:
            Plotly figure object.
        """
        experiences = []
        scores = []
        names = []
        
        for candidate in candidates:
            analysis = candidate.get('analysis', {})
            sections = analysis.get('sections', {})
            experience_section = sections.get('experience', {})
            
            experiences.append(experience_section.get('years', 0))
            scores.append(analysis.get('overall_score', 0))
            names.append(candidate['name'][:15])
        
        fig = go.Figure(data=go.Scatter(
            x=experiences,
            y=scores,
            mode='markers',
            text=names,
            marker=dict(
                size=10,
                color=scores,
                colorscale='Viridis',
                showscale=True
            )
        ))
        
        fig.update_layout(
            template=self.template,
            title=title,
            xaxis_title='Years of Experience',
            yaxis_title='Overall Score',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        
        return fig
    
    def create_ats_distribution(self, candidates: List[Dict[str, Any]], title: str = "ATS Score Distribution") -> go.Figure:
        """
        Create a histogram for ATS score distribution.
        
        Args:
            candidates: List of candidate dictionaries.
            title: Chart title.
            
        Returns:
            Plotly figure object.
        """
        ats_scores = [c['analysis'].get('ats_score', 0) for c in candidates]
        
        fig = go.Figure(data=[go.Histogram(
            x=ats_scores,
            nbinsx=10,
            marker_color=self.colors['primary'],
        )])
        
        fig.update_layout(
            template=self.template,
            title=title,
            xaxis_title='ATS Score',
            yaxis_title='Count',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        
        return fig
    
    def create_skill_matrix_heatmap(self, candidates: List[Dict[str, Any]], skills: List[str], title: str = "Skill Matrix") -> go.Figure:
        """
        Create a heatmap for skill matrix comparison.
        
        Args:
            candidates: List of candidate dictionaries.
            skills: List of skills to compare.
            title: Chart title.
            
        Returns:
            Plotly figure object.
        """
        # Create skill matrix
        matrix = []
        candidate_names = []
        
        for candidate in candidates:
            candidate_names.append(candidate['name'][:15])
            row = []
            analysis = candidate.get('analysis', {})
            sections = analysis.get('sections', {})
            skills_section = sections.get('skills', {})
            candidate_skills = skills_section.get('technical', []) + skills_section.get('soft', [])
            
            for skill in skills:
                # Check if candidate has the skill (simplified)
                has_skill = any(skill.lower() in s.lower() for s in candidate_skills)
                row.append(1 if has_skill else 0)
            
            matrix.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=skills,
            y=candidate_names,
            colorscale='Viridis',
            showscale=True
        ))
        
        fig.update_layout(
            template=self.template,
            title=title,
            height=max(400, len(candidates) * 30),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        
        return fig
    
    def create_timeline_chart(self, milestones: List[Dict[str, Any]], title: str = "Career Roadmap") -> go.Figure:
        """
        Create a timeline chart for career roadmap.
        
        Args:
            milestones: List of milestone dictionaries with 'phase', 'timeline'.
            title: Chart title.
            
        Returns:
            Plotly figure object.
        """
        phases = [m['phase'] for m in milestones]
        timelines = [m['timeline'] for m in milestones]
        
        fig = go.Figure()
        
        for i, (phase, timeline) in enumerate(zip(phases, timelines)):
            fig.add_trace(go.Scatter(
                x=[i, i],
                y=[0, 1],
                mode='lines',
                line=dict(color=self.colors['primary'], width=2),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=[i],
                y=[0.5],
                mode='markers+text',
                marker=dict(size=15, color=self.colors['secondary']),
                text=phase,
                textposition='top center',
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=[i],
                y=[0],
                mode='text',
                text=timeline,
                textposition='bottom center',
                showlegend=False
            ))
        
        fig.update_layout(
            template=self.template,
            title=title,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False, range=[-0.2, 1.2]),
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        
        return fig
    
    def create_metrics_dashboard(self, metrics: Dict[str, Any]) -> go.Figure:
        """
        Create a comprehensive metrics dashboard.
        
        Args:
            metrics: Dictionary containing various metrics.
            
        Returns:
            Plotly figure object with subplots.
        """
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Score Distribution', 'Candidate Status', 'Experience Analysis', 'Skill Coverage'),
            specs=[[{'type': 'histogram'}, {'type': 'pie'}],
                    [{'type': 'scatter'}, {'type': 'bar'}]]
        )
        
        # Score distribution
        if 'scores' in metrics:
            fig.add_trace(
                go.Histogram(x=metrics['scores'], name='Scores'),
                row=1, col=1
            )
        
        # Candidate status
        if 'status_distribution' in metrics:
            fig.add_trace(
                go.Pie(labels=list(metrics['status_distribution'].keys()),
                      values=list(metrics['status_distribution'].values())),
                row=1, col=2
            )
        
        # Experience analysis
        if 'experience_data' in metrics:
            exp_data = metrics['experience_data']
            fig.add_trace(
                go.Scatter(x=exp_data['experience'], y=exp_data['scores'],
                          mode='markers', name='Experience vs Score'),
                row=2, col=1
            )
        
        # Skill coverage
        if 'skill_coverage' in metrics:
            fig.add_trace(
                go.Bar(x=list(metrics['skill_coverage'].keys()),
                      y=list(metrics['skill_coverage'].values()),
                      name='Skills'),
                row=2, col=2
            )
        
        fig.update_layout(
            template=self.template,
            height=800,
            showlegend=False,
            title_text="Recruitment Metrics Dashboard"
        )
        
        return fig


class HRDashboardCharts:
    """
    Specialized charts for HR dashboard.
    """
    
    def __init__(self, theme: str = 'dark'):
        """Initialize HR dashboard charts."""
        self.chart_generator = ChartGenerator(theme)
    
    def create_hiring_funnel(self, candidates: List[Dict[str, Any]]) -> go.Figure:
        """
        Create a hiring funnel chart.
        
        Args:
            candidates: List of candidate data.
            
        Returns:
            Plotly figure object.
        """
        total = len(candidates)
        screened = sum(1 for c in candidates if c['analysis'].get('overall_score', 0) >= 50)
        interviewed = sum(1 for c in candidates if c['analysis'].get('overall_score', 0) >= 70)
        hired = sum(1 for c in candidates if c['analysis'].get('overall_score', 0) >= 85)
        
        fig = go.Figure(go.Funnel(
            y=["Total Applicants", "Screened", "Interviewed", "Hired"],
            x=[total, screened, interviewed, hired],
            textinfo="value+percent initial",
            marker=dict(color=[self.chart_generator.colors['primary'],
                             self.chart_generator.colors['secondary'],
                             self.chart_generator.colors['tertiary'],
                             self.chart_generator.colors['success']])
        ))
        
        fig.update_layout(
            template=self.chart_generator.template,
            title="Hiring Funnel",
            height=500,
        )
        
        return fig
    
    def create_candidate_comparison_radar(self, candidate1: Dict[str, Any], candidate2: Dict[str, Any]) -> go.Figure:
        """
        Create a radar chart comparing two candidates.
        
        Args:
            candidate1: First candidate data.
            candidate2: Second candidate data.
            
        Returns:
            Plotly figure object.
        """
        metrics = ['Overall Score', 'ATS Score', 'Grammar Score', 
                  'Communication Score', 'Design Score']
        
        scores1 = [candidate1['analysis'].get(m.lower().replace(' ', '_'), 0) for m in metrics]
        scores2 = [candidate2['analysis'].get(m.lower().replace(' ', '_'), 0) for m in metrics]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=scores1,
            theta=metrics,
            fill='toself',
            name=candidate1['name'][:15],
            line_color=self.chart_generator.colors['primary']
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=scores2,
            theta=metrics,
            fill='toself',
            name=candidate2['name'][:15],
            line_color=self.chart_generator.colors['secondary']
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            template=self.chart_generator.template,
            title="Candidate Comparison",
            height=500,
        )
        
        return fig


def create_score_card(score: float, label: str, color: str = '#6366f1') -> str:
    """
    Create HTML for a score card.
    
    Args:
        score: Score value.
        label: Score label.
        color: Card color.
        
    Returns:
        HTML string for score card.
    """
    return f"""
    <div style="background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 24px;
                text-align: center;
                min-width: 150px;">
        <div style="font-size: 48px;
                    font-weight: 700;
                    color: {color};
                    background: linear-gradient(135deg, {color}, #8b5cf6);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;">
            {score:.1f}
        </div>
        <div style="color: #a1a1aa;
                    font-size: 14px;
                    margin-top: 8px;">
            {label}
        </div>
    </div>
    """
