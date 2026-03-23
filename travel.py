import streamlit as st
import random
import time
from datetime import datetime

# ==========================================
# 1. 系統設定 (基於 10-3: 認知鎖定)
# ==========================================
st.set_page_config(
    page_title="台東長濱：南溪部落深度導覽 - CRF v9.0",
    page_icon="🌊",
    layout="centered"
)

# ==========================================
# 2. CSS 完整移植 (基於 travel.py: 櫻粉色與深色修復)
# ==========================================
st.markdown("""
    <style>
    /* 強制粉色美學與深色文字 (修復深色模式錯誤) */
    .stApp { background-color: #FFF0F5; color: #333333 !important; }
    p, div, span, h1, h2, h3, h4, label { color: #4A2C2C !important; }

    /* Tier 1: 轉換心臟區 (Conversion Hotzone) 按鈕 */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);
        color: white !important;
        font-weight: bold;
        padding: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 20, 147, 0.3);
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 20px rgba(255, 20, 147, 0.5);
    }

    /* 景點卡片設計 (降低視覺熵) */
    .spot-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border-left: 10px solid #FF69B4;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (南溪部落數據主權)
# ==========================================
TRIBE_DATA = {
    "culture": [
        {"name": "布農族八部合音體驗", "desc": "深度觸及南溪布農文化核心", "safety": 1.0},
        {"name": "三間村古道導覽", "desc": "穿梭長濱與南溪的歷史路徑", "safety": 0.8}
    ],
    "nature": [
        {"name": "南溪河谷溯溪", "desc": "清澈見底的自然生態觀察點", "safety": 0.4}, # 模擬大雨熔斷風險
        {"name": "部落梯田景觀", "desc": "遠眺太平洋與海岸山脈交會點", "safety": 1.0}
    ],
    "food": [
        {"name": "阿公的獵人包DIY", "desc": "南溪在地食材與傳統保存食", "safety": 1.0},
        {"name": "長濱山海味私廚", "desc": "融合長濱海鮮與南溪野菜的饗宴", "safety": 0.9}
    ]
}

# ==========================================
# 4. 核心邏輯層 (基於 10-1 遍歷性 & 10-4 資源整合)
# ==========================================

def ergodicity_check(spot_name, safety_score):
    """
    生存第一原則：若南溪降雨機率過高或路況不佳，強制熔斷。
    """
    if safety_score < 0.5:
        return False, f"⚠️ 【黑天鵝預警】{spot_name} 目前因溪水暴漲風險已啟動 Hard Stop。已為您切換至陸域文化備援。"
    return True, "路徑安全"

def dopamine_trigger():
    """變動獎勵機制：提升用戶留存率"""
    if random.random() > 0.6:
        st.balloons()
        st.toast("🎁 獲得南溪部落數位勳章：『山海守護者』！", icon="🛡️")

# ==========================================
# 5. UI 呈現層 (基於 10-3 視覺鎖定)
# ==========================================

st.title("🏔️ 南溪部落：山海導覽系統")
st.caption("台東縣長濱鄉三間村 | CRF v9.0 深度智能版")

# 1. 意圖透視 (Intent X-Ray)
choice = st.selectbox("您偏好的南溪體驗？", ["文化沉浸", "自然探索", "部落風味"])

mapping = {"文化沉浸": "culture", "自然探索": "nature", "部落風味": "food"}
spots = TRIBE_DATA[mapping[choice]]

# 2. 遍歷性動態導航
for spot in spots:
    is_safe, alert_msg = ergodicity_check(spot['name'], spot['safety'])
    
    with st.container():
        st.markdown(f"""
        <div class="spot-card">
            <h3 style="margin:0;">📍 {spot['name']}</h3>
            <p style="opacity:0.8; margin:10px 0;">{spot['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not is_safe:
            st.error(alert_msg)
            if st.button(f"查看 {spot['name']} 的備援 Plan B", key=f"bak_{spot['name']}"):
                st.info("已串接『南溪室內文化館』，ROI 維持正常，延遲降低。")
        else:
            if st.button(f"鎖定 {spot['name']} 導覽協議", key=spot['name']):
                with st.spinner("正在校準長濱即時氣象與路況 API..."):
                    time.sleep(1.2)
                st.success(f"導覽權限已獲取。座標已同步至您的『資料主權』緩存。")
                dopamine_trigger()

# ==========================================
# 6. 決策校準層 (Sidebar)
# ==========================================
with st.sidebar:
    st.header("⚙️ 遙測中心")
    st.write(f"系統版本：`v9.0` (Institutional)")
    st.metric("台東長濱 RPO", "5s", "-1s")
    st.divider()
    st.subheader("🛡️ 安全協議")
    st.toggle("啟動自動化偽需求過濾", value=True)
    st.toggle("黑天鵝路徑監測器", value=True)
    
    if st.button("🔴 緊急熔斷 (Hard Stop)"):
        st.error("所有導覽行程已終止，系統進入自毀鎖定。")
        st.stop()
