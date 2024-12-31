import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_plotly_mapbox_events import plotly_mapbox_events

st.set_page_config(layout="wide")

data_path = 'monthly_station_max_values.xlsx'
data = pd.read_excel(data_path, sheet_name='Sheet1')

data['timestamp'] = pd.to_datetime(data['timestamp']).dt.date 
data['year_month'] = pd.to_datetime(data['timestamp']).dt.to_period('M').astype(str)

st.title("2023-2024易淹水地區（雲林、嘉義、屏東、花蓮）情報")
st.subheader("選擇對應月份，查看當月最大淹水數值")

all_months = sorted(data['year_month'].unique())
selected_month = st.select_slider(
    'Select a Month',
    options=all_months,
    value=all_months[0]  # Default to the first month
)

filtered_data = data[data['year_month'] == selected_month]


# Group data by station and aggregate values for tooltip
tooltip_data = filtered_data.groupby(
    ['station_id', 'Latitude', 'Longitude', 'Organize_Name', 'PQ_name', 'PQ_fullname', 'timestamp']
)[['year_month', 'value']].agg(list).reset_index()

color_scale = px.colors.sequential.deep[::1]  # Reverse the color scale
color_scale = color_scale[-8:]  # Keep only the first 8 colors after reversal

# Initialize Mapbox plot with the adjusted color scale
fig = px.scatter_mapbox(
    tooltip_data,
    lat="Latitude",
    lon="Longitude",
    color=[max(values) for values in tooltip_data['value']],
    hover_data={
        'Latitude': False,
        'Longitude': False,
        'station_id': False,
        'Organize_Name': True, 
        'PQ_fullname': True,
        'timestamp': True,
        'value': True
    },
    zoom=7,
    height=620,
    color_continuous_scale=color_scale  
)

fig.update_traces(marker=dict(size=10))  
fig.update_layout(mapbox_style="open-street-map")

fig.update_traces(marker=dict(size=10), hovertemplate="<br>".join([
    "負責單位： %{customdata[3]}",  
    "淹水感測器站點： %{customdata[4]}",
    "時間： %{customdata[5]}",
    "當月最大淹水深度： %{customdata[6]} cm"
]))

mapbox_events = plotly_mapbox_events(fig, click_event=True, select_event=True, hover_event=True, override_height=600)

hover_placeholder = st.empty()

if mapbox_events[2]:  # Hover event
    hovered_point = mapbox_events[2][0]  # Get the first event in the list
    if 'customdata' in hovered_point:  # Ensure customdata exists
        station_id = hovered_point['customdata'][0]
        
        # Filter data for the hovered station
        station_data = tooltip_data[tooltip_data['station_id'] == station_id]
        
        if not station_data.empty:
            hover_display = pd.DataFrame({
                '負責單位': station_data['Organize_Name'].values[0],  # Updated column name
                '淹水感測器站點': station_data['PQ_name'].values[0],
                '時間': station_data['year_month'].values[0],
                '當月最大淹水深度': station_data['value'].values[0]
            })
            hover_placeholder.write(f"Hovered Point Data (Station {station_id}):")
            st.dataframe(hover_display)
        else:
            hover_placeholder.write("No data available for the hovered station.")
else:
    hover_placeholder.write("Hover over a point to see details.")
# Plot line chart for PQ_fullname value trend
st.write("### 2023-2024易淹水地區（雲林、嘉義、屏東、花蓮）各測站變化")
line_chart_data = data.copy()
line_chart_data['timestamp'] = pd.to_datetime(line_chart_data['timestamp'])  # 確保 timestamp 是 datetime 格式

# 按 PQ_fullname 和 timestamp 分組，計算平均值
line_chart_grouped = line_chart_data.groupby(['PQ_fullname', 'timestamp'])['value'].mean().reset_index()

# 使用 plotly express 繪製折線圖
line_fig = px.line(
    line_chart_grouped,
    x="timestamp",
    y="value",
    color="PQ_fullname",
    labels={
        "timestamp": "日期",
        "value": "當月最大淹水深度 (cm)",
        "PQ_fullname": "淹水感測器站點"
    },
    title="僅繪製颱風季（7-11月）各測站當月最大數值"
)

# 更新圖表布局
line_fig.update_layout(
    xaxis_title="日期",
    yaxis_title="當月最大淹水深度 (cm)",
    legend_title="淹水感測器站點",
    height=500
)

# 顯示折線圖
st.plotly_chart(line_fig, use_container_width=True)


# Download button for filtered data
if not filtered_data.empty:
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download Selected Data",
        data=csv,
        file_name=f"filtered_data_{selected_month}.csv",
        mime="text/csv"
    )
else:
    st.write("No data available for the selected month.")   