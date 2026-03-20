import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Food Delivery Analytics",
    page_icon="🍕",
    layout="wide"
)

# ── Storm Color Theme CSS ──────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0a0f1e; }
    .block-container { padding: 2rem; }
    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00b4ff, #ff69b4, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #7eb8d4;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #0d1b2a, #1a2744);
        border: 1px solid #00b4ff;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #7eb8d4;
        margin-top: 4px;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #00b4ff;
        border-left: 4px solid #ff69b4;
        padding-left: 10px;
        margin: 1.5rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────
st.markdown('<div class="title">🍕 Food Delivery Analytics</div>',
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered insights from food delivery operations</div>',
            unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    return df

df = load_data()

# ── KPI Cards ──────────────────────────────────────────
st.markdown('<div class="section-title">📊 Key Metrics</div>',
            unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#00b4ff;">{len(df)}</div>
        <div class="metric-label">Total Orders</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#ffffff;">
            {df['delivery_time_min'].mean():.1f} min
        </div>
        <div class="metric-label">Avg Delivery Time</div>
    </div>""", unsafe_allow_html=True)

with c3:
    delayed = len(df[df['is_delayed'] == 'Delayed'])
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#ff69b4;">{delayed}</div>
        <div class="metric-label">Delayed Orders</div>
    </div>""", unsafe_allow_html=True)

with c4:
    ontime = len(df[df['is_delayed'] == 'On Time'])
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#00d4ff;">{ontime}</div>
        <div class="metric-label">On Time Orders</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Chart Styling ──────────────────────────────────────
CHART_BG = '#0d1b2a'
PAPER_BG = '#0a0f1e'
GRID_COLOR = '#1a2744'
TEXT_COLOR = '#7eb8d4'
TITLE_COLOR = '#00b4ff'

# Storm color scale
STORM_SCALE = [
    [0.0,  '#0a0f1e'],
    [0.25, '#003366'],
    [0.5,  '#0057b8'],
    [0.75, '#00b4ff'],
    [1.0,  '#ff69b4']
]

# Storm discrete colors
STORM_COLORS = ['#00b4ff', '#ff69b4', '#ffffff', 
                '#003d7a', '#00d4ff', '#ff1493']

def style_chart(fig):
    fig.update_layout(
        plot_bgcolor=CHART_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=TEXT_COLOR),
        title_font=dict(color=TITLE_COLOR, size=14),
        xaxis=dict(gridcolor=GRID_COLOR, color=TEXT_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, color=TEXT_COLOR),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            bgcolor=CHART_BG,
            bordercolor=GRID_COLOR,
            font=dict(color=TEXT_COLOR)
        )
    )
    return fig

# ── Charts Row 1 ───────────────────────────────────────
st.markdown('<div class="section-title">🌩 Delivery Analysis</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    weather_df = df.groupby('weather')['delivery_time_min'].mean().reset_index()
    fig1 = px.bar(weather_df,
                  x='delivery_time_min',
                  y='weather',
                  orientation='h',
                  title='Avg Delivery Time by Weather',
                  color='delivery_time_min',
                  color_continuous_scale=STORM_SCALE)
    fig1 = style_chart(fig1)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    traffic_df = df.groupby('traffic_level')['delivery_time_min'].mean().reset_index()
    fig2 = px.bar(traffic_df,
                  x='delivery_time_min',
                  y='traffic_level',
                  orientation='h',
                  title='Avg Delivery Time by Traffic Level',
                  color='delivery_time_min',
                  color_continuous_scale=STORM_SCALE)
    fig2 = style_chart(fig2)
    st.plotly_chart(fig2, use_container_width=True)

# ── Charts Row 2 ───────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    pie_df = df['is_delayed'].value_counts().reset_index()
    fig3 = px.pie(pie_df,
                  names='is_delayed',
                  values='count',
                  title='Delayed vs On Time Orders',
                  color_discrete_sequence=['#00b4ff', '#ff69b4'],
                  hole=0.4)
    fig3 = style_chart(fig3)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    time_df = df.groupby('time_of_day')['delivery_time_min'].mean().reset_index()
    fig4 = px.bar(time_df,
                  x='time_of_day',
                  y='delivery_time_min',
                  title='Avg Delivery Time by Time of Day',
                  color='delivery_time_min',
                  color_continuous_scale=STORM_SCALE)
    fig4 = style_chart(fig4)
    st.plotly_chart(fig4, use_container_width=True)

# ── Charts Row 3 ───────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    vehicle_df = df.groupby('vehicle_type')['delivery_time_min'].mean().reset_index()
    fig5 = px.bar(vehicle_df,
                  x='vehicle_type',
                  y='delivery_time_min',
                  title='Avg Delivery Time by Vehicle Type',
                  color='vehicle_type',
                  color_discrete_sequence=STORM_COLORS)
    fig5 = style_chart(fig5)
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    fig6 = px.scatter(df,
                      x='distance_km',
                      y='delivery_time_min',
                      color='vehicle_type',
                      title='Distance vs Delivery Time',
                      opacity=0.7,
                      color_discrete_sequence=STORM_COLORS)
    fig6 = style_chart(fig6)
    st.plotly_chart(fig6, use_container_width=True)

# ── Line Chart ─────────────────────────────────────────
st.markdown('<div class="section-title">📉 Courier Experience Impact</div>',
            unsafe_allow_html=True)

exp_df = df.groupby('courier_experience')['delivery_time_min'].mean().reset_index()
fig7 = px.line(exp_df,
               x='courier_experience',
               y='delivery_time_min',
               title='Avg Delivery Time by Courier Experience',
               markers=True,
               color_discrete_sequence=['#00b4ff'])
fig7 = style_chart(fig7)
fig7.update_traces(line=dict(width=3),
                   marker=dict(size=8, color='#ff69b4',
                               line=dict(width=2, color='#ffffff')))
st.plotly_chart(fig7, use_container_width=True)

st.divider()

# ── Filters + Data Table ───────────────────────────────
st.markdown('<div class="section-title">🔍 Explore Data</div>',
            unsafe_allow_html=True)

col7, col8 = st.columns(2)

with col7:
    weather_filter = st.selectbox(
        "Filter by Weather",
        ["All"] + df['weather'].unique().tolist()
    )

with col8:
    traffic_filter = st.selectbox(
        "Filter by Traffic",
        ["All"] + df['traffic_level'].unique().tolist()
    )

filtered_df = df.copy()
if weather_filter != "All":
    filtered_df = filtered_df[filtered_df['weather'] == weather_filter]
if traffic_filter != "All":
    filtered_df = filtered_df[filtered_df['traffic_level'] == traffic_filter]

st.dataframe(filtered_df, use_container_width=True)
st.caption(f"Showing {len(filtered_df)} of {len(df)} orders")