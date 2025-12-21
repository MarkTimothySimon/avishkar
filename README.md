# Farmer's Commodity Volatility Index Dashboard 🧅

A comprehensive Streamlit-based dashboard for predicting and analyzing commodity price volatility for farmers. This tool provides actionable insights combining calendar risk, market momentum, and short-term forecasts to help farmers make informed selling decisions.

## Features

### Multi-Language Support
- **English** and **मराठी (Marathi)** interface
- Real-time language switching
- Fully translated UI elements and advisories

### Market Analysis Components

1. **Calendar Risk (CVI)**
   - Seasonal volatility assessment
   - Low/Medium/High risk classification
   - Historical trend analysis

2. **Price Movement Indicators**
   - 7-day and 3-day momentum tracking
   - Price direction (Up/Down/Stable)
   - Volatility probability distribution

3. **Decision Matrix**
   - Combines Calendar Risk + Alert Risk
   - Provides clear farmer actions:
     - ✓ Sell normally (Both LOW)
     - ⚠ Be cautious (Seasonal LOW + Alert HIGH)
     - ℹ Seasonal risk exists, but market stable (Seasonal HIGH + Alert LOW)
     - ⚠ Strong warning - Stagger sales (Both HIGH)

4. **Multi-Step Forecast** (3-day & 7-day outlook)
   - Only shown from last data date onwards (Dec 13th+)
   - Short-term volatility predictions
   - Confidence scores for each forecast
   - Detailed probability distributions

5. **Visual Analytics**
   - Historical volatility timeline
   - CVI score trends
   - Momentum comparison charts
   - Interactive gauges for probability

## Requirements
```txt
streamlit
pandas
plotly
numpy
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/MarkTimothySimon/avishkar.git
cd commodity-volatility-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Prepare your data**
   - Place `2025_predictions.csv` in the root directory
   - Required columns:
     - `date`: Date in YYYY-MM-DD format
     - `cvi_label`: Volatility label (Low/Med/High)
     - `cvi_score`: Numerical CVI score
     - `prob_low`, `prob_med`, `prob_high`: Probability distributions
     - `price_momentum_7`, `price_momentum_3`: Momentum indicators
     - `vol_7`, `vol_30`: Volatility measures
     - `price_movement`: Price direction (Up/Down/Stable)
     - `multi_next`: Multi-step forecast data (optional)
     - `market_price`: Current market price (optional)
     - `modal_price`: Modal price (optional)

## Usage

1. **Run the dashboard**
```bash
streamlit run main.py
```

2. **Access the interface**
   - Open your browser to `http://localhost:8501`
   - Select language (English/मराठी) from sidebar
   - Choose a date to analyze
   - Adjust timeline slider for historical trends (7-60 days)

## Data Format

### CSV Structure
```csv
date,cvi_label,cvi_score,prob_low,prob_med,prob_high,price_momentum_7,price_momentum_3,vol_7,vol_30,price_movement,multi_next,market_price
2025-01-01,Low,15.23,0.85,0.12,0.03,2.5,1.8,3.2,5.1,Up,"{'2025-01-04': {'proba': [0.82, 0.15, 0.03], 'score': 18.5, 'label': 'Low'}}",4500.50
```

### Multi-Step Forecast Format
The `multi_next` column should contain a dictionary string:
```python
{
    '2025-01-04': {
        'proba': [0.82, 0.15, 0.03],  # [Low, Med, High] probabilities
        'score': 18.5,                 # CVI score
        'label': 'Low'                 # Predicted label
    },
    '2025-01-08': {
        'proba': [0.75, 0.20, 0.05],
        'score': 22.3,
        'label': 'Low'
    }
}
```

## Dashboard Sections

### 1. Market Analysis Header
- Selected date overview
- Market price display (if available)

### 2. Key Market Signals
- **Market Volatility**: Current CVI classification with score
- **Price Direction**: Current price movement with 7-day momentum

### 3. Advisory Card
- Context-aware recommendations based on volatility and price movement
- Color-coded alerts (Green/Yellow/Red)
- Specific farmer actions

### 4. Decision Guide
- **Situation**: Calendar Risk + Alert Risk combination
- **Recommended Action**: Clear, actionable guidance

### 5. Momentum Analysis
- Visual bar charts for momentum indicators
- Key metrics display
- Momentum interpretation with thresholds

### 6. Volatility Probability
- Interactive gauge charts
- Low/Med/High probability distributions

### 7. Historical Trends
- Volatility timeline over selected period
- CVI score trend analysis

### 8. Multi-Step Forecast
- 3-day and 7-day volatility predictions
- Confidence scores
- Expandable detailed probabilities
- Only visible from last data date onwards

### 9. Risk Summary
- Overall volatility risk
- Price trend indicator
- Market health assessment

## Configuration

### Language Settings
Located in `translations` dictionary at the top of `main.py`. Add new languages by extending this structure.

### Advisories
English advisories are in the `get_advisory()` function. Marathi advisories are in the `advisories_marathi` dictionary.

### Forecast Cutoff Date
Modify in `should_show_forecast()` function:
```python
last_data_date = pd.to_datetime('2024-12-13').date()
```

### Color Schemes
Adjust in the custom CSS section:
- Low Risk: `#10b981` (Green)
- Medium Risk: `#f59e0b` (Orange)
- High Risk: `#ef4444` (Red)
- Neutral: `#6366f1` (Blue)

## Mobile Responsive
- Optimized for mobile and tablet devices
- Touch-friendly date picker
- Collapsible sidebar
- Responsive charts and cards

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Charts powered by [Plotly](https://plotly.com/)
- Designed for Indian farmers


---

**Note**: This dashboard is for informational purposes. Always consult with local agricultural experts and consider multiple factors before making selling decisions.
