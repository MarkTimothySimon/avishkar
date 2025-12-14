import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np


translations = {
    "English": {
        "title": "Farmer's Commodity Volatility Index",
        "select_date": "📅 Select Date",
        "choose_date": "Choose prediction date",
        "timeline": "Timeline (days)",
        "market_analysis": "Market Analysis for",
        "key_signals": "Key Market Signals",
        "market_volatility": "Market Volatility",
        "cvi_score": "CVI Score",
        "price_direction": "Price Direction",
        "momentum_7day": "7-Day Momentum",
        "market_price": "Market Price",
        "modal_price": "Modal Price (Most Common)",
        "momentum_analysis": "Price Momentum & Volatility Analysis",
        "key_indicators": "Key Indicators",
        "price_momentum_7": "7-Day Price Momentum",
        "price_momentum_3": "3-Day Price Momentum",
        "volatility_7": "7-Day Volatility",
        "volatility_30": "30-Day Volatility",
        "momentum_interpretation": "Momentum Interpretation",
        "volatility_probability": "Volatility Probability Distribution",
        "low_volatility": "Low Volatility",
        "med_volatility": "Med Volatility",
        "high_volatility": "High Volatility",
        "historical_trends": "Historical Market Trends",
        "price_trend_analysis": "Price Trend Analysis",
        "risk_summary": "Risk Level Summary",
        "volatility_risk": "Volatility Risk",
        "price_trend": "Price Trend",
        "market_health": "Market Health",
        "excellent": "Excellent",
        "fair": "Fair",
        "poor": "Poor",
        "up": "Up",
        "down": "Down",
        "stable": "Stable",
        "low": "Low",
        "med": "Med",
        "medium": "Medium",
        "high": "High",
        "dataset_info": "📊 Dataset Info",
        "total_predictions": "Total Predictions",
        "date_range": "Date Range",
        "days": "days",
        "cvi_distribution": "📈 CVI Distribution",
        "high_cvi_days": "High CVI Days",
        "med_cvi_days": "Med CVI Days",
        "low_cvi_days": "Low CVI Days",
        "about_cvi": "About CVI",
        "about_text": """**Commodity Volatility Index**
            
Measures market instability:
- Low: Stable market
- Medium: Moderate swings
- High: Unstable prices

Combined with price direction for better decisions.""",
        "strong_upward": "Strong Upward Momentum Detected",
        "strong_downward": "Strong Downward Momentum Detected",
        "stable_movement": "Stable Price Movement",
        "signal": "Signal",
        "prices_rising": "Prices are rising consistently - Good time to sell if you need to",
        "prices_falling": "Prices are falling - Hold if possible, avoid distress sales",
        "no_strong_trend": "No strong directional trend - Standard market conditions",
        "volatility": "Volatility",
    },
    "मराठी (Marathi)": {
        "title": "शेतकऱ्यांचा कमोडिटी व्होलॅटिलिटी इंडेक्स",
        "select_date": "📅 तारीख निवडा",
        "choose_date": "अंदाज तारीख निवडा",
        "timeline": "टाइमलाइन (दिवस)",
        "market_analysis": "बाजार विश्लेषण",
        "key_signals": "मुख्य बाजार संकेत",
        "market_volatility": "बाजार अस्थिरता",
        "cvi_score": "सीव्हीआय स्कोअर",
        "price_direction": "किंमत दिशा",
        "momentum_7day": "७-दिवस गती",
        "market_price": "बाजार किंमत",
        "modal_price": "मोडल किंमत (सर्वसाधारण)",
        "momentum_analysis": "किंमत गती आणि अस्थिरता विश्लेषण",
        "key_indicators": "मुख्य सूचक",
        "price_momentum_7": "७-दिवस किंमत गती",
        "price_momentum_3": "३-दिवस किंमत गती",
        "volatility_7": "७-दिवस अस्थिरता",
        "volatility_30": "३०-दिवस अस्थिरता",
        "momentum_interpretation": "गती स्पष्टीकरण",
        "volatility_probability": "अस्थिरता संभाव्यता वितरण",
        "low_volatility": "कमी अस्थिरता",
        "med_volatility": "मध्यम अस्थिरता",
        "high_volatility": "उच्च अस्थिरता",
        "historical_trends": "ऐतिहासिक बाजार ट्रेंड",
        "price_trend_analysis": "किंमत ट्रेंड विश्लेषण",
        "risk_summary": "जोखीम पातळी सारांश",
        "volatility_risk": "अस्थिरता जोखीम",
        "price_trend": "किंमत ट्रेंड",
        "market_health": "बाजार आरोग्य",
        "excellent": "उत्तम",
        "fair": "चांगले",
        "poor": "खराब",
        "up": "वर",
        "down": "खाली",
        "stable": "स्थिर",
        "low": "कमी",
        "med": "मध्यम",
        "medium": "मध्यम",
        "high": "उच्च",
        "dataset_info": "📊 डेटासेट माहिती",
        "total_predictions": "एकूण अंदाज",
        "date_range": "तारीख श्रेणी",
        "days": "दिवस",
        "cvi_distribution": "📈 सीव्हीआय वितरण",
        "high_cvi_days": "उच्च सीव्हीआय दिवस",
        "med_cvi_days": "मध्यम सीव्हीआय दिवस",
        "low_cvi_days": "कमी सीव्हीआय दिवस",
        "about_cvi": "सीव्हीआय बद्दल",
        "about_text": """**कमोडिटी व्होलॅटिलिटी इंडेक्स**
            
बाजार अस्थिरता मोजते:
- कमी: स्थिर बाजार
- मध्यम: मध्यम बदल
- उच्च: अस्थिर किंमती

चांगल्या निर्णयांसाठी किंमत दिशेसह एकत्रित.""",
        "strong_upward": "मजबूत वरच्या दिशेने गती आढळली",
        "strong_downward": "मजबूत खालच्या दिशेने गती आढळली",
        "stable_movement": "स्थिर किंमत हालचाल",
        "signal": "संकेत",
        "prices_rising": "किंमती सातत्याने वाढत आहेत - आवश्यक असल्यास विकण्यासाठी चांगली वेळ",
        "prices_falling": "किंमती घसरत आहेत - शक्य असल्यास धरून ठेवा, घाईची विक्री टाळा",
        "no_strong_trend": "कोणताही मजबूत दिशात्मक कल नाही - मानक बाजार परिस्थिती",
        "volatility": "अस्थिरता",
    }
}

# Marathi advisories
advisories_marathi = {
    ("High", "Up"): {
        "title": "सावधगिरी: उच्च जोखीम, वाढणाऱ्या किंमती",
        "message": "किंमती वाढत आहेत पण बाजार अत्यंत अस्थिर आहे. तातडीची विक्री टाळा पण तीव्र उलटसुलट होण्यासाठी तयार रहा.",
        "action": "कृती: साठा ठेवा. दररोज निरीक्षण करा. किंमत लक्ष्य ठेवा. शिखरावर विकण्यास तयार रहा.",
        "color": "#f59e0b"
    },
    ("High", "Down"): {
        "title": "सावधानता: उच्च जोखीम, घटणाऱ्या किंमती",
        "message": "अस्थिर परिस्थितीत किंमती घटत आहेत. सतत खालच्या दिशेने दबाव येण्याची उच्च शक्यता.",
        "action": "कृती: घाबरून विक्री टाळा. शक्य असल्यास साठवा. बाजार स्थिर होण्याची प्रतीक्षा करा.",
        "color": "#ef4444"
    },
    ("High", "Stable"): {
        "title": "चेतावणी: उच्च अस्थिरता, अनिश्चित दिशा",
        "message": "बाजार अस्थिर आहे आणि स्पष्ट दिशा नाही. दोन्ही दिशेने तीव्र किंमत बदल शक्य.",
        "action": "कृती: सावध रहा. बारकाईने निरीक्षण करा. जलद बदलांसाठी तयार रहा. विक्री आणि होल्ड दोन्ही धोरणे ठेवा.",
        "color": "#f59e0b"
    },
    ("Med", "Up"): {
        "title": "अनुकूल: मध्यम जोखीम, वाढणाऱ्या किंमती",
        "message": "व्यवस्थापन करण्यायोग्य अस्थिरतेसह किंमती वाढत आहेत. धोरणात्मक विक्रीसाठी चांगली संधी.",
        "action": "कृती: साठ्याचा काही भाग विकण्याचा विचार करा. बाजार व्यवहारांसाठी चांगल्या परिस्थिती.",
        "color": "#10b981"
    },
    ("Med", "Down"): {
        "title": "सावधगिरी: मध्यम जोखीम, घटणाऱ्या किंमती",
        "message": "मध्यम अस्थिरतेसह किंमती घटत आहेत. सावधगिरी बाळगा पण घाबरू नका.",
        "action": "कृती: शक्य असल्यास साठा ठेवा. किंमत पुनर्प्राप्तीची प्रतीक्षा करा. उलटसुलट संकेतांसाठी निरीक्षण करा.",
        "color": "#f59e0b"
    },
    ("Med", "Stable"): {
        "title": "तटस्थ: मध्यम अस्थिरता, स्थिर किंमती",
        "message": "स्थिर किंमतीसह बाजार मध्यम क्रियाकलाप दर्शवित आहे. व्यापारासाठी वाजवी परिस्थिती.",
        "action": "कृती: सामान्य व्यापार परिस्थिती. मानक विक्री धोरणे लागू. नियोजित व्यवहारांसाठी चांगली वेळ.",
        "color": "#6366f1"
    },
    ("Low", "Up"): {
        "title": "इष्टतम: कमी जोखीम, वाढणाऱ्या किंमती",
        "message": "सर्वोत्तम परिस्थिती! स्थिर वातावरणात किंमती वाढत आहेत. सतत वाढीसाठी उच्च आत्मविश्वास.",
        "action": "कृती: उत्कृष्ट विक्री संधी. बाजार अनुकूल आहे. सध्याच्या दरावर विकण्याचा विचार करा.",
        "color": "#10b981"
    },
    ("Low", "Down"): {
        "title": "स्थिर: कमी जोखीम, घटणाऱ्या किंमती",
        "message": "स्थिर परिस्थितीत किंमती हळूहळू घटत आहेत. नियंत्रित खालच्या दिशेने हालचाल.",
        "action": "कृती: साठा ठेवा. किंमत स्थिरीकरणाची प्रतीक्षा करा. पुढील चक्रासाठी तयार होण्यासाठी चांगल्या परिस्थिती.",
        "color": "#6366f1"
    },
    ("Low", "Stable"): {
        "title": "आदर्श: कमी जोखीम, स्थिर किंमती",
        "message": "किमान अस्थिरतेसह शांत बाजार. सर्व व्यापार क्रियाकलापांसाठी सुरक्षित वातावरण.",
        "action": "कृती: शेती कार्यांसाठी आदर्श परिस्थिती. कमी जोखीम वातावरण. नियोजित विक्रीसह पुढे जाणे सुरक्षित.",
        "color": "#10b981"
    }
}

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
        
        /* Keep sidebar open on mobile */
        [data-testid="stSidebar"] {
            transform: none !important;
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

def get_advisory(volatility, price_movement, language="English"):
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
    
    # Use Marathi advisories if language is Marathi
    if language == "मराठी (Marathi)":
        return advisories_marathi.get(key, advisories_marathi[("Med", "Stable")])
    
    return advisories.get(key, advisories[("Med", "Stable")])

def create_volatility_timeline(df, current_date, days_back=30, t=None):
    """Create volatility timeline chart"""
    if t is None:
        t = translations["English"]
    
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
            label_key = label.lower() if label.lower() in ['low', 'high'] else 'med'
            volatility_label = t[f'{label_key}_volatility']
            fig.add_trace(go.Scatter(
                x=data['date'],
                y=data['volatility_numeric'],
                mode='markers+lines',
                name=volatility_label,
                marker=dict(size=10, color=colors.get(label, '#6366f1')),
                line=dict(color=colors.get(label, '#6366f1'), width=3),
                hovertemplate=f'<b>{volatility_label}</b><br>Date: %{{x|%b %d}}<br>CVI: %{{customdata:.4f}}<extra></extra>',
                customdata=data['cvi_score']
            ))
    
    fig.update_layout(
        title=f"{days_back}-{t['days']} {t['historical_trends']}",
        xaxis_title=t['date_range'],
        yaxis_title=t['market_volatility'],
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

def create_cvi_trend_chart(df, current_date, days_back=30, t=None):
    """Create CVI score trend chart"""
    if t is None:
        t = translations["English"]
    end_date = pd.to_datetime(current_date)
    start_date = end_date - timedelta(days=days_back)

    trend_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend_df['date'],
        y=trend_df['cvi_score'],
        mode='lines+markers',
        name=t['cvi_score'],
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2'),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)',
        hovertemplate=f"<b>{t['cvi_score']}</b><br>Date: %{{x|%b %d}}<br>Score: %{{y:.4f}}<extra></extra>"
    ))

    fig.add_hline(y=33, line_dash="dash", line_color="#10b981",
                  annotation_text=f"{t['low']} Threshold", annotation_position="right")
    fig.add_hline(y=66, line_dash="dash", line_color="#f59e0b",
                  annotation_text=f"{t['high']} Threshold", annotation_position="right")

    fig.update_layout(
        title=f"{days_back}-{t['days']} {t['cvi_score']} {t['price_trend']}",
        xaxis_title=t['date_range'],
        yaxis_title=t['cvi_score'],
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
        )
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
if 'language' not in st.session_state:
    st.session_state.language = "English"

st.markdown(f"<h1>{translations[st.session_state.language]['title']}</h1>", unsafe_allow_html=True)
df = load_predictions()
if df is not None:
    # Sidebar with language selection
    with st.sidebar:
        st.markdown("### 🌐 Language / भाषा")
        language = st.radio(
            "Select Language",
            options=["English", "मराठी (Marathi)"],
            index=0 if st.session_state.language == "English" else 1,
            key="lang_radio"
        )
     # Update session state when language changes
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()
        
        st.markdown("---")
        
        # Get translations for selected language - MOVED HERE
        t = translations[language]
        
        st.markdown(f"### ℹ️ {t['about_cvi']}")
        st.info(t['about_text'])

# Get translations for current language
t = translations[st.session_state.language]

# Date selector moved to main area
st.markdown(f"## {t['select_date']}")

min_date = df['date'].min().date()
max_date = df['date'].max().date()

col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    selected_date = st.date_input(
        t['choose_date'],
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        key="date_selector",
        help="Select a date to view market predictions"
    )

with col2:
    timeline_days = st.slider(t['timeline'], 7, 60, 30, key="timeline_slider")

st.markdown("---")

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
    
    advisory = get_advisory(volatility, price_movement, st.session_state.language)
    
    st.markdown(f"<div class='info-box'><h2 style='margin:0;'>{t['market_analysis']} {selected_date.strftime('%B %d, %Y')}</h2></div>", unsafe_allow_html=True)
    
    # Display market price if available in CSV
    if 'market_price' in pred.index and pd.notna(pred['market_price']):
        st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <h3 style="margin-top: 0; color: #667eea;">{t['market_price']}</h3>
                <p style="font-size: 2rem; font-weight: 700; color: #10b981; margin: 0.5rem 0;">
                    ₹{pred['market_price']:.2f}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"## {t['key_signals']}")
    col1, col2 = st.columns(2)
    
    with col1:
        volatility_class = f"{volatility.lower()}-volatility"
        volatility_text = t[volatility.lower()] + " " + t['volatility']
        st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin-top: 0; color: #667eea;">{t['market_volatility']}</h3>
                <div class='volatility-badge {volatility_class}'>{volatility_text}</div>
                <p style="color: #718096; margin-top: 1rem; font-size: 1.1rem;">
                    <strong>{t['cvi_score']}:</strong> {cvi_score:.4f}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        price_class = f"price-{price_movement.lower()}"
        price_text = t[price_movement.lower()]
        st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin-top: 0; color: #667eea;">{t['price_direction']}</h3>
                <div class='price-badge {price_class}'>{price_text}</div>
                <p style="color: #718096; margin-top: 1rem; font-size: 1.1rem;">
                    <strong>{t['momentum_7day']}:</strong> {m7:+.2f}%
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
    
    st.markdown(f"## {t['momentum_analysis']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_momentum = create_momentum_chart(m7, m3, vol7, vol30)
        st.plotly_chart(fig_momentum, use_container_width=True)
    
    with col2:
        st.markdown(f"### {t['key_indicators']}")
        
        st.metric(t['price_momentum_7'], f"{m7:+.2f}%", 
                 help="Price change over last 7 days")
        st.metric(t['price_momentum_3'], f"{m3:+.2f}%",
                 help="Price change over last 3 days")
        st.metric(t['volatility_7'], f"{vol7:.2f}%",
                 help="Price fluctuation intensity (7 days)")
        st.metric(t['volatility_30'], f"{vol30:.2f}%",
                 help="Price fluctuation intensity (30 days)")
    
    st.markdown(f"### {t['momentum_interpretation']}")
    
    if m7 > 3 and m3 > 2:
        st.markdown(f"""
        <div style='background: rgba(16, 185, 129, 0.1); backdrop-filter: blur(20px); border-left: 4px solid #10b981; 
        padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 1px solid rgba(16, 185, 129, 0.3);'>
            <p style='color: #d1fae5; margin: 0; font-size: 0.95rem;'>
                <strong style='color: #10b981;'>✓ {t['strong_upward']}</strong><br>
                • 7-{t['days']} {t['momentum_7day'].lower()}: {m7:+.2f}% (threshold: >3%)<br>
                • 3-{t['days']} {t['momentum_7day'].lower()}: {m3:+.2f}% (threshold: >2%)<br>
                • <strong>{t['signal']}:</strong> {t['prices_rising']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    elif m7 < -3 and m3 < -2:
        st.markdown(f"""
        <div style='background: rgba(239, 68, 68, 0.1); backdrop-filter: blur(20px); border-left: 4px solid #ef4444; 
        padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 1px solid rgba(239, 68, 68, 0.3);'>
            <p style='color: #fecaca; margin: 0; font-size: 0.95rem;'>
                <strong style='color: #ef4444;'>⚠ {t['strong_downward']}</strong><br>
                • 7-{t['days']} {t['momentum_7day'].lower()}: {m7:+.2f}% (threshold: <-3%)<br>
                • 3-{t['days']} {t['momentum_7day'].lower()}: {m3:+.2f}% (threshold: <-2%)<br>
                • <strong>{t['signal']}:</strong> {t['prices_falling']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background: rgba(59, 130, 246, 0.1); backdrop-filter: blur(20px); border-left: 4px solid #3b82f6; 
        padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 1px solid rgba(59, 130, 246, 0.3);'>
            <p style='color: #dbeafe; margin: 0; font-size: 0.95rem;'>
                <strong style='color: #3b82f6;'>ℹ {t['stable_movement']}</strong><br>
                • 7-{t['days']} {t['momentum_7day'].lower()}: {m7:+.2f}%<br>
                • 3-{t['days']} {t['momentum_7day'].lower()}: {m3:+.2f}%<br>
                • <strong>{t['signal']}:</strong> {t['no_strong_trend']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"## {t['volatility_probability']}")
    
    cols = st.columns(3)
    
    probabilities = {t['low']: prob_low, t['med']: prob_med, t['high']: prob_high}
    color_map = {t['low']: '#10b981', t['med']: '#f59e0b', t['high']: '#ef4444'}
    
    for idx, (label, prob) in enumerate(probabilities.items()):
        with cols[idx]:
            label_key = 'low' if t['low'] == label else ('high' if t['high'] == label else 'med')
            volatility_label = t[f'{label_key}_volatility']
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': volatility_label, 'font': {'size': 18, 'color': 'white'}},
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
    
    st.markdown(f"## {t['historical_trends']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_timeline = create_volatility_timeline(df, selected_date, timeline_days, t)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        fig_cvi = create_cvi_trend_chart(df, selected_date, timeline_days, t)
        st.plotly_chart(fig_cvi, use_container_width=True)
    
    st.markdown(f"## {t['risk_summary']}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_colors = {'Low': '#10b981', 'Med': '#f59e0b', 'Medium': '#f59e0b', 'High': '#ef4444'}
        
        st.markdown(f"""
            <div class="risk-indicator" style="background: {risk_colors.get(volatility, '#6366f1')}; color: white;">
                {t['volatility_risk']}: {t[volatility.lower()]}
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        movement_colors = {'Up': '#10b981', 'Down': '#ef4444', 'Stable': '#6366f1'}
        
        st.markdown(f"""
            <div class="risk-indicator" style="background: {movement_colors.get(price_movement, '#6366f1')}; color: white;">
                {t['price_trend']}: {t[price_movement.lower()]}
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        volatility_numeric = {'Low': 1, 'Med': 2, 'Medium': 2, 'High': 3}.get(volatility, 2)
        health_score = (3 - volatility_numeric) * 33.33
        health_label = "Excellent" if health_score > 66 else "Fair" if health_score > 33 else "Poor"
        health_color = "#10b981" if health_score > 66 else "#f59e0b" if health_score > 33 else "#ef4444"
        
        st.markdown(f"""
            <div class="risk-indicator" style="background: {health_color}; color: white;">
                {t['market_health']}: {t[health_label.lower()]}
            </div>
        """, unsafe_allow_html=True)
    
else:
    st.warning("No prediction data available for the selected date.")
