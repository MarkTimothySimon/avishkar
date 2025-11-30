import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Commodity Volatility Index",
    page_icon="🧅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern aesthetics + Mobile fix
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    
    [data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 300px !important;
        max-width: 300px !important;
    }
    
    /* Make date input more mobile-friendly */
    .stDateInput {
        z-index: 9999 !important;
    }
    
    .stDateInput > div {
        z-index: 9999 !important;
    }
    
    /* Calendar popup should stay above sidebar */
    .react-datepicker-popper {
        z-index: 10000 !important;
    }
    
    .react-datepicker {
        z-index: 10000 !important;
    }
    
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: transparent;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.5);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .advisory-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border-left: 6px solid;
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 1rem 0;
    }
    
    .volatility-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 1rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .price-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 1rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .low-volatility {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .med-volatility, .medium-volatility {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #2d3748;
    }
    
    .high-volatility {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .price-up {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .price-down {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .price-stable {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
    }
    
    h1 {
        color: white !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 2rem !important;
        font-size: 3rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2, h3 {
        color: white !important;
        font-weight: 600 !important;
    }
    
    .metric-card h3 {
        color: #e0e7ff !important;
    }
    
    .metric-card p {
        color: #d1d5db !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .info-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-left: 5px solid #667eea;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .info-box h2 {
        color: white !important;
    }
    
    .risk-indicator {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        font-weight: 600;
        text-align: center;
        font-size: 1.1rem;
    }
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        
        .metric-card, .advisory-card {
            padding: 1rem;
        }
        
        .volatility-badge, .price-badge {
            font-size: 1rem;
            padding: 0.4rem 1rem;
        }
        
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_predictions(file_path='2025_predictions.csv'):
    """Load the predictions CSV file"""
    try:
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.error("Predictions file not found. Please ensure '2025_predictions.csv' is in the same directory.")
        return None
    except Exception as e:
        st.error(f"Error loading predictions: {str(e)}")
        return None

def determine_price_movement_from_column(price_movement_str):
    """Extract price movement from the price_movement column"""
    if pd.isna(price_movement_str):
        return "Stable"
    
    movement = str(price_movement_str).strip().lower()
    
    if 'up' in movement:
        return "Up"
    elif 'down' in movement:
        return "Down"
    else:
        return "Stable"

def get_advisory(volatility, price_movement):
    """Generate actionable advisory based on volatility and price movement"""
    advisories = {
        ("High", "Up"): {
            "title": "CAUTION: High Risk, Rising Prices",
            "message": "Commodity prices are rising but market is highly unstable. Avoid distress sales but be prepared for sharp reversals.",
            "action": "Action: Hold inventory. Monitor daily. Set price targets. Be ready to sell on peaks.",
            "color": "#f59e0b"
        },
        ("High", "Down"): {
            "title": "ALERT: High Risk, Falling Prices",
            "message": "Prices declining in volatile conditions. High probability of continued downward pressure.",
            "action": "Action: Avoid panic selling. Store if possible. Wait for market stabilization.",
            "color": "#ef4444"
        },
        ("High", "Stable"): {
            "title": "WARNING: High Volatility, Uncertain Direction",
            "message": "Market is unstable with no clear direction. Sharp price movements possible in either direction.",
            "action": "Action: Stay cautious. Monitor closely. Prepare for rapid changes. Have both sell and hold strategies ready.",
            "color": "#f59e0b"
        },
        ("Med", "Up"): {
            "title": "FAVORABLE: Moderate Risk, Rising Prices",
            "message": "Prices trending upward with manageable volatility. Good opportunity for strategic selling.",
            "action": "Action: Consider selling portion of inventory. Good conditions for market transactions.",
            "color": "#10b981"
        },
        ("Med", "Down"): {
            "title": "CAUTION: Moderate Risk, Declining Prices",
            "message": "Prices falling with moderate volatility. Exercise caution but not panic.",
            "action": "Action: Hold inventory if possible. Wait for price recovery. Monitor for reversal signals.",
            "color": "#f59e0b"
        },
        ("Med", "Stable"): {
            "title": "NEUTRAL: Moderate Volatility, Stable Prices",
            "message": "Market showing moderate activity with stable pricing. Reasonable conditions for trading.",
            "action": "Action: Normal trading conditions. Standard selling strategies apply. Good time for planned transactions.",
            "color": "#6366f1"
        },
        ("Low", "Up"): {
            "title": "OPTIMAL: Low Risk, Rising Prices",
            "message": "Best conditions! Prices rising in a stable environment. High confidence for continued growth.",
            "action": "Action: Excellent selling opportunity. Market is favorable. Consider selling at current rates.",
            "color": "#10b981"
        },
        ("Low", "Down"): {
            "title": "STABLE: Low Risk, Declining Prices",
            "message": "Prices declining gradually in stable conditions. Controlled downward movement.",
            "action": "Action: Hold inventory. Wait for price stabilization. Good conditions to prepare for next cycle.",
            "color": "#6366f1"
        },
        ("Low", "Stable"): {
            "title": "IDEAL: Low Risk, Stable Prices",
            "message": "Calm market with minimal volatility. Safe environment for all trading activities.",
            "action": "Action: Ideal conditions for farming operations. Low risk environment. Safe to proceed with planned sales.",
            "color": "#10b981"
        }
    }
    
    # Handle Medium label
    key = (volatility, price_movement)
    if volatility == "Medium":
        key = ("Med", price_movement)
    
    return advisories.get(key, advisories[("Med", "Stable")])

def create_volatility_timeline(df, current_date, days_back=30):
    """Create volatility timeline chart"""
    end_date = pd.to_datetime(current_date)
    start_date = end_date - timedelta(days=days_back)
    
    timeline_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    
    label_map = {'Low': 1, 'Med': 2, 'Medium': 2, 'High': 3}
    timeline_df['volatility_numeric'] = timeline_df['cvi_label'].map(label_map)
    
    fig = go.Figure()
    
    colors = {'Low': '#10b981', 'Med': '#f59e0b', 'Medium': '#f59e0b', 'High': '#ef4444'}
    
    for label in timeline_df['cvi_label'].unique():
        data = timeline_df[timeline_df['cvi_label'] == label]
        if not data.empty:
            fig.add_trace(go.Scatter(
                x=data['date'],
                y=data['volatility_numeric'],
                mode='markers+lines',
                name=f'{label} Volatility',
                marker=dict(size=10, color=colors.get(label, '#6366f1')),
                line=dict(color=colors.get(label, '#6366f1'), width=3),
                hovertemplate=f'<b>{label} Volatility</b><br>Date: %{{x|%b %d}}<br>CVI: %{{customdata:.4f}}<extra></extra>',
                customdata=data['cvi_score']
            ))
    
    fig.update_layout(
        title=f"{days_back}-Day Volatility Timeline",
        xaxis_title="Date",
        yaxis_title="Volatility Level",
        height=400,
        paper_bgcolor='rgba(0, 0, 0, 0.3)',
        plot_bgcolor='rgba(0, 0, 0, 0.2)',
        font={'family': 'Inter', 'size': 12, 'color': 'white'},
        hovermode='closest',
        yaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3],
            ticktext=['Low', 'Medium', 'High'],
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='white'
        ),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='white'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font={'color': 'white'}
        ),
        title_font={'color': 'white'}
    )
    
    return fig

def create_cvi_trend_chart(df, current_date, days_back=30):
    """Create CVI score trend chart"""
    end_date = pd.to_datetime(current_date)
    start_date = end_date - timedelta(days=days_back)
    
    trend_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_df['date'],
        y=trend_df['cvi_score'],
        mode='lines+markers',
        name='CVI Score',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2'),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)',
        hovertemplate='<b>CVI Score</b><br>Date: %{x|%b %d}<br>Score: %{y:.4f}<extra></extra>'
    ))
    
    fig.add_hline(y=33, line_dash="dash", line_color="#10b981", 
                  annotation_text="Low Threshold", annotation_position="right")
    fig.add_hline(y=66, line_dash="dash", line_color="#f59e0b", 
                  annotation_text="High Threshold", annotation_position="right")
    
    fig.update_layout(
        title=f"{days_back}-Day CVI Score Trend",
        xaxis_title="Date",
        yaxis_title="Commodity Volatility Index",
        height=400,
        paper_bgcolor='rgba(0, 0, 0, 0.3)',
        plot_bgcolor='rgba(0, 0, 0, 0.2)',
        font={'family': 'Inter', 'size': 12, 'color': 'white'},
        hovermode='x unified',
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='white'
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='white'
        ),
        title_font={'color': 'white'}
    )
    
    return fig

def create_momentum_chart(m7, m3, vol7, vol30):
    """Create price momentum comparison chart"""
    fig = go.Figure()
    
    categories = ['7-Day<br>Momentum', '3-Day<br>Momentum', '7-Day<br>Volatility', '30-Day<br>Volatility']
    values = [m7, m3, vol7, vol30]
    colors = ['#10b981' if v >= 0 else '#ef4444' for v in values]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=[f"{v:+.2f}%" for v in values],
        textposition='outside',
        textfont=dict(color='white'),
        hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Price Momentum & Volatility Indicators",
        xaxis_title="Indicator",
        yaxis_title="Percentage (%)",
        height=400,
        paper_bgcolor='rgba(0, 0, 0, 0.3)',
        plot_bgcolor='rgba(0, 0, 0, 0.2)',
        font={'family': 'Inter', 'size': 12, 'color': 'white'},
        showlegend=False,
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='white'
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='white'
        ),
        title_font={'color': 'white'}
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    return fig

# Main App
st.markdown("<h1>Farmer's Commodity Volatility Index</h1>", unsafe_allow_html=True)

df = load_predictions()

if df is not None:
    # Date selector moved to main area
    st.markdown("## 📅 Select Date")
    
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        selected_date = st.date_input(
            "Choose prediction date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            key="date_selector",
            help="Select a date to view market predictions"
        )
    
    with col2:
        timeline_days = st.slider("Timeline (days)", 7, 60, 30, key="timeline_slider")
    
    st.markdown("---")
    
    with st.sidebar:
        st.markdown("### ℹ️ About CVI")
        st.info("""
        **Commodity Volatility Index**
        
        Measures market instability:
        - Low: Stable market
        - Medium: Moderate swings
        - High: Unstable prices
        
        Combined with price direction for better decisions.
        """)
        
        st.markdown("---")
        st.markdown("### 📁 Dataset Info")
        st.metric("Total Predictions", len(df))
        st.metric("Date Range", f"{(max_date - min_date).days} days")
        
        st.markdown("---")
        st.markdown("### 📈 CVI Distribution")
        high_days = len(df[df['cvi_label'] == 'High'])
        med_days = len(df[(df['cvi_label'] == 'Med') | (df['cvi_label'] == 'Medium')])
        low_days = len(df[df['cvi_label'] == 'Low'])
        
        st.metric("High CVI Days", high_days)
        st.metric("Med CVI Days", med_days)
        st.metric("Low CVI Days", low_days)
    
    prediction = df[df['date'].dt.date == selected_date]
    
    if not prediction.empty:
        pred = prediction.iloc[0]
        
        volatility = pred['cvi_label']
        cvi_score = pred['cvi_score']
        prob_low = pred['prob_low']
        prob_med = pred['prob_med']
        prob_high = pred['prob_high']
        m7 = pred['price_momentum_7']
        m3 = pred['price_momentum_3']
        vol7 = pred['vol_7']
        vol30 = pred['vol_30']
        
        price_movement = determine_price_movement_from_column(pred['price_movement'])
        
        advisory = get_advisory(volatility, price_movement)
        
        st.markdown(f"<div class='info-box'><h2 style='margin:0;'>Market Analysis for {selected_date.strftime('%B %d, %Y')}</h2></div>", unsafe_allow_html=True)
        
        st.markdown("## Key Market Signals")
        col1, col2 = st.columns(2)
        
        with col1:
            volatility_class = f"{volatility.lower()}-volatility"
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin-top: 0; color: #667eea;">Market Volatility</h3>
                    <div class='volatility-badge {volatility_class}'>{volatility} Volatility</div>
                    <p style="color: #718096; margin-top: 1rem; font-size: 1.1rem;">
                        <strong>CVI Score:</strong> {cvi_score:.4f}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            price_class = f"price-{price_movement.lower()}"
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin-top: 0; color: #667eea;">Price Direction</h3>
                    <div class='price-badge {price_class}'>{price_movement}</div>
                    <p style="color: #718096; margin-top: 1rem; font-size: 1.1rem;">
                        <strong>7-Day Momentum:</strong> {m7:+.2f}%
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="advisory-card" style="border-left-color: {advisory['color']};">
                <h2 style="margin: 0; color: {advisory['color']};">{advisory['title']}</h2>
                <p style="font-size: 1.1rem; color: white; margin: 1rem 0; line-height: 1.6;">
                    {advisory['message']}
                </p>
                <div class="risk-indicator" style="background: {advisory['color']}; color: white;">
                    {advisory['action']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("## Price Momentum & Volatility Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_momentum = create_momentum_chart(m7, m3, vol7, vol30)
            st.plotly_chart(fig_momentum, use_container_width=True)
        
        with col2:
            st.markdown("### Key Indicators")
            
            st.metric("7-Day Price Momentum", f"{m7:+.2f}%", 
                     help="Price change over last 7 days")
            st.metric("3-Day Price Momentum", f"{m3:+.2f}%",
                     help="Price change over last 3 days")
            st.metric("7-Day Volatility", f"{vol7:.2f}%",
                     help="Price fluctuation intensity (7 days)")
            st.metric("30-Day Volatility", f"{vol30:.2f}%",
                     help="Price fluctuation intensity (30 days)")
        
        st.markdown("### Momentum Interpretation")
        
        if m7 > 3 and m3 > 2:
            st.markdown(f"""
            <div style='background: rgba(16, 185, 129, 0.1); backdrop-filter: blur(20px); border-left: 4px solid #10b981; 
            padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 1px solid rgba(16, 185, 129, 0.3);'>
                <p style='color: #d1fae5; margin: 0; font-size: 0.95rem;'>
                    <strong style='color: #10b981;'>✓ Strong Upward Momentum Detected</strong><br>
                    • 7-day momentum: {m7:+.2f}% (threshold: >3%)<br>
                    • 3-day momentum: {m3:+.2f}% (threshold: >2%)<br>
                    • <strong>Signal:</strong> Prices are rising consistently - Good time to sell if you need to
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif m7 < -3 and m3 < -2:
            st.markdown(f"""
            <div style='background: rgba(239, 68, 68, 0.1); backdrop-filter: blur(20px); border-left: 4px solid #ef4444; 
            padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 1px solid rgba(239, 68, 68, 0.3);'>
                <p style='color: #fecaca; margin: 0; font-size: 0.95rem;'>
                    <strong style='color: #ef4444;'>⚠ Strong Downward Momentum Detected</strong><br>
                    • 7-day momentum: {m7:+.2f}% (threshold: <-3%)<br>
                    • 3-day momentum: {m3:+.2f}% (threshold: <-2%)<br>
                    • <strong>Signal:</strong> Prices are falling - Hold if possible, avoid distress sales
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background: rgba(59, 130, 246, 0.1); backdrop-filter: blur(20px); border-left: 4px solid #3b82f6; 
            padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 1px solid rgba(59, 130, 246, 0.3);'>
                <p style='color: #dbeafe; margin: 0; font-size: 0.95rem;'>
                    <strong style='color: #3b82f6;'>ℹ Stable Price Movement</strong><br>
                    • 7-day momentum: {m7:+.2f}%<br>
                    • 3-day momentum: {m3:+.2f}%<br>
                    • <strong>Signal:</strong> No strong directional trend - Standard market conditions
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("## Volatility Probability Distribution")
        
        cols = st.columns(3)
        
        probabilities = {'Low': prob_low, 'Med': prob_med, 'High': prob_high}
        color_map = {'Low': '#10b981', 'Med': '#f59e0b', 'High': '#ef4444'}
        
        for idx, (label, prob) in enumerate(probabilities.items()):
            with cols[idx]:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': f"{label} Volatility", 'font': {'size': 18, 'color': 'white'}},
                    number={'suffix': "%", 'font': {'size': 36, 'color': 'white'}},
                    gauge={
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': 'white'},
                        'bar': {'color': color_map.get(label, '#667eea'), 'thickness': 0.8},
                        'bgcolor': "rgba(0, 0, 0, 0.2)",
                        'borderwidth': 2,
                        'bordercolor': "rgba(255, 255, 255, 0.2)",
                        'steps': [
                            {'range': [0, 33], 'color': 'rgba(16, 185, 129, 0.2)'},
                            {'range': [33, 66], 'color': 'rgba(245, 158, 11, 0.2)'},
                            {'range': [66, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
                        ]
                    }
                ))
                
                fig.update_layout(
                    height=280,
                    margin=dict(l=10, r=10, t=50, b=10),
                    paper_bgcolor='rgba(0, 0, 0, 0.3)',
                    font={'family': 'Inter', 'color': 'white'}
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("## Historical Market Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_timeline = create_volatility_timeline(df, selected_date, timeline_days)
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        with col2:
            fig_cvi = create_cvi_trend_chart(df, selected_date, timeline_days)
            st.plotly_chart(fig_cvi, use_container_width=True)
        
        st.markdown("## Risk Level Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_colors = {'Low': '#10b981', 'Med': '#f59e0b', 'Medium': '#f59e0b', 'High': '#ef4444'}
            
            st.markdown(f"""
                <div class="risk-indicator" style="background: {risk_colors.get(volatility, '#6366f1')}; color: white;">
                    Volatility Risk: {volatility}
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            movement_colors = {'Up': '#10b981', 'Down': '#ef4444', 'Stable': '#6366f1'}
            
            st.markdown(f"""
                <div class="risk-indicator" style="background: {movement_colors.get(price_movement, '#6366f1')}; color: white;">
                    Price Trend: {price_movement}
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            volatility_numeric = {'Low': 1, 'Med': 2, 'Medium': 2, 'High': 3}.get(volatility, 2)
            health_score = (3 - volatility_numeric) * 33.33
            health_label = "Excellent" if health_score > 66 else "Fair" if health_score > 33 else "Poor"
            health_color = "#10b981" if health_score > 66 else "#f59e0b" if health_score > 33 else "#ef4444"
            
            st.markdown(f"""
                <div class="risk-indicator" style="background: {health_color}; color: white;">
                    Market Health: {health_label}
                </div>
            """, unsafe_allow_html=True)
        
    else:
        st.warning("No prediction data available for the selected date.")
        
else:
    st.error("Failed to load predictions. Please check your data file.")
