"""
Visualization Module
Create plots and graphs for plant health monitoring
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional
import os


class PlantVisualizer:
    """
    Create visualizations for plant data
    """
    
    def __init__(self, style: str = 'seaborn-v0_8'):
        """
        Initialize visualizer
        
        Args:
            style: Matplotlib style
        """
        try:
            plt.style.use(style)
        except:
            pass
        sns.set_palette("husl")
        
    def plot_growth_over_time(self, df: pd.DataFrame, plant_id: str = None,
                              save_path: str = None) -> plt.Figure:
        """
        Plot leaf area growth over time
        
        Args:
            df: DataFrame with historical data
            plant_id: Specific plant ID (optional)
            save_path: Path to save figure
            
        Returns:
            Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if plant_id:
            data = df[df['plant_id'] == plant_id]
            ax.plot(range(len(data)), data['leaf_area'], marker='o', linewidth=2)
            ax.set_title(f'Growth Curve - Plant {plant_id}')
        else:
            for pid in df['plant_id'].unique():
                plant_data = df[df['plant_id'] == pid]
                ax.plot(range(len(plant_data)), plant_data['leaf_area'], 
                       marker='o', label=f'Plant {pid}', linewidth=2)
            ax.legend()
            ax.set_title('Growth Curves - All Plants')
        
        ax.set_xlabel('Time Point')
        ax.set_ylabel('Leaf Area (pixels)')
        ax.grid(True, alpha=0.3)
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_group_comparison(self, df: pd.DataFrame, 
                             save_path: str = None) -> plt.Figure:
        """
        Compare leaf area across groups
        
        Args:
            df: DataFrame with group data
            save_path: Path to save figure
            
        Returns:
            Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        groups = df['group'].unique()
        colors = ['#2ecc71', '#e74c3c', '#f39c12']
        
        for i, group in enumerate(groups):
            group_data = df[df['group'] == group]
            ax.boxplot(group_data['leaf_area'].dropna(), positions=[i], 
                      widths=0.6, patch_artist=True,
                      boxprops=dict(facecolor=colors[i % len(colors)]))
        
        ax.set_xticklabels(groups)
        ax.set_xlabel('Group')
        ax.set_ylabel('Leaf Area (pixels)')
        ax.set_title('Leaf Area Comparison Across Groups')
        ax.grid(True, alpha=0.3, axis='y')
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_health_status_distribution(self, df: pd.DataFrame,
                                       save_path: str = None) -> plt.Figure:
        """
        Plot distribution of health statuses
        
        Args:
            df: DataFrame with health status
            save_path: Path to save figure
            
        Returns:
            Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        status_counts = df['health_status'].value_counts()
        colors = {'Healthy': '#2ecc71', 'Water_Stress': '#e74c3c', 
                 'Light_Stress': '#f39c12'}
        
        bars = ax.bar(status_counts.index, status_counts.values,
                     color=[colors.get(s, '#95a5a6') for s in status_counts.index])
        
        ax.set_xlabel('Health Status')
        ax.set_ylabel('Count')
        ax.set_title('Distribution of Plant Health Status')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_feature_correlation(self, df: pd.DataFrame,
                                 features: List[str] = None,
                                 save_path: str = None) -> plt.Figure:
        """
        Plot correlation heatmap of features
        
        Args:
            df: DataFrame with features
            features: List of feature columns
            save_path: Path to save figure
            
        Returns:
            Figure object
        """
        if features is None:
            features = ['leaf_area', 'green_intensity', 'green_index', 
                       'plant_height', 'plant_width']
        
        # Filter available features
        available_features = [f for f in features if f in df.columns]
        
        if not available_features:
            print("No valid features found")
            return None
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        corr = df[available_features].corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, ax=ax, square=True)
        
        ax.set_title('Feature Correlation Matrix')
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_dual_metric_over_time(self, df: pd.DataFrame, 
                                   metric1: str = 'leaf_area',
                                   metric2: str = 'green_index',
                                   plant_id: str = None,
                                   save_path: str = None) -> plt.Figure:
        """
        Plot two metrics over time with dual y-axes
        
        Args:
            df: DataFrame with data
            metric1: First metric column name
            metric2: Second metric column name
            plant_id: Specific plant ID
            save_path: Path to save figure
            
        Returns:
            Figure object
        """
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        if plant_id:
            data = df[df['plant_id'] == plant_id]
        else:
            data = df
        
        # First metric
        color1 = '#2ecc71'
        ax1.set_xlabel('Time Point')
        ax1.set_ylabel(metric1.replace('_', ' ').title(), color=color1)
        ax1.plot(range(len(data)), data[metric1], marker='o', 
                color=color1, linewidth=2, label=metric1)
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.grid(True, alpha=0.3)
        
        # Second metric
        ax2 = ax1.twinx()
        color2 = '#3498db'
        ax2.set_ylabel(metric2.replace('_', ' ').title(), color=color2)
        ax2.plot(range(len(data)), data[metric2], marker='s', 
                color=color2, linewidth=2, label=metric2)
        ax2.tick_params(axis='y', labelcolor=color2)
        
        title = f'Growth Metrics Over Time'
        if plant_id:
            title += f' - Plant {plant_id}'
        plt.title(title)
        
        fig.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig


def create_growth_plot(df: pd.DataFrame, plant_id: str = None, 
                      save_path: str = None) -> plt.Figure:
    """
    Convenience function to create growth plot
    
    Args:
        df: DataFrame with data
        plant_id: Plant ID
        save_path: Save path
        
    Returns:
        Figure object
    """
    viz = PlantVisualizer()
    return viz.plot_growth_over_time(df, plant_id, save_path)


if __name__ == "__main__":
    print("Visualization Module")
    print("=" * 60)
    print("Available plot types:")
    print("  - Growth over time")
    print("  - Group comparison")
    print("  - Health status distribution")
    print("  - Feature correlation")
    print("  - Dual metric comparison")
