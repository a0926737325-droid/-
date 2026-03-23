import streamlit as st
import random
import time
from datetime import datetime

# ==========================================
# 1. 系統設定 (基於 10-3: 認知鎖定)
# ==========================================
st.set_page_config(
    page_title="部落深度導覽系統 - CRF v9.0 Pro",
    page_icon="🏔️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS 完整封裝 (基於 travel.py 與 10-3 轉換心臟區)
# ==========================================
st.markdown("""
    <style>
    /* 全域背景與字體顏色 - 避免深色模式衝突 */
    .stApp { background-color: #FFF0F5; color: #333333 !important; }
    p, div, span, h1, h2, h3, label { color: #4A2C2C !important; }

    /* Tier 1: Conversion Hotzone (轉換心臟區) 按鈕設計 */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);
        color: white !important;
        font-size: 18px;
        font-weight: bold;
        border: none;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(255, 20, 147, 0.3);
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 20, 147, 0.5);
    }

    /* 景點卡片設計 - 降低視覺熵 */
    .tribe-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-left: 8px solid #FF69B4;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .status-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (基於 10-4: 資料主權與整合)
# ==========================================
# 確保資料不依賴外部脆弱 API，建立本地備援資料結構
TRIBE_DB = {
    "前山區": [
        {"name": "詩朗部落", "desc": "枝垂櫻與祕境步道", "hot": "⭐⭐⭐⭐", "safety": 1.0},
        {"name": "霞雲部落", "desc": "山水環抱的泰雅原鄉", "hot": "⭐⭐⭐", "safety": 1.0}
    ],
    "後山區": [
        {"name": "中巴陵", "desc": "櫻木花道 (昭和櫻隧道)", "hot": "⭐⭐⭐⭐⭐", "safety": 0.3}, # 模擬擁堵風險
        {"name": "高義部落", "desc": "溪口台地與古道探幽", "hot": "⭐⭐⭐⭐", "safety": 1.0},
        {"name": "拉拉山部落", "desc": "神木群與雲海餐桌", "hot": "⭐⭐⭐⭐⭐", "safety": 0.9}
    ]
}

# ==========================================
# 4. 邏輯驅動層 (基於 10-1 遍歷性 & 10-2 MVP 策略)
# ==========================================

def ergodicity_filter(tribe_name, safety_score):
    """
    遍歷性檢查 (Survival First): 
    若安全性分值過低，強制觸發熔斷機制，禁止進入該路徑。
    """
    if safety_score < 0.5:
        return False, f"⚠️ 【系統預警】{tribe_name} 聯外道路目前處於紅皇后臨界值 (擁塞/維修)。"
    return True, "路徑安全"

def apply_variable_reward():
    """多巴胺成癮機制: 隨機觸發獎勵互動"""
    if random.random() > 0.7:
        st.balloons()
        st.toast("🎉 解鎖部落隱藏版圖章：『櫻之勇者』！", icon="🌸")

# ==========================================
# 5. UI 交互呈現 (基於 10-3 視覺鎖定)
# ==========================================

st.title("🏔️ 部落深度導覽系統")
st.markdown("**Version:** `9.0 Institutional` | **Core:** `Black Swan Defense Enabled`")

# 1. 客製化意圖透視 (Intent X-Ray)
tab_front, tab_back = st.tabs(["🚶 前山區 (低認知模式)", "🎒 後山區 (深度遍歷模式)"])

def render_tribe_list(region_key):
    for tribe in TRIBE_DB[region_key]:
        with st.container():
            # 渲染卡片
            safe, msg = ergodicity_filter(tribe['name'], tribe['safety'])
            status_color = "#28a745" if safe else "#dc3545"
            status_text = "● 推薦前往" if safe else "● 建議避開"
            
            st.markdown(f"""
            <div class="tribe-card">
                <span class="status-tag" style="background: {status_color}22; color: {status_color};">
                    {status_text}
                </span>
                <h2 style="margin:0; padding-bottom:10px;">{tribe['name']}</h2>
                <p style="font-size: 16px; opacity: 0.8;">{tribe['desc']}</p>
                <p>熱門程度：{tribe['hot']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 轉換心臟區按鈕
            if safe:
                if st.button(f"啟動 {tribe['name']} 導覽協議", key=tribe['name']):
                    with st.status(f"正在計算 {tribe['name']} 最優路徑...", expanded=True) as status:
                        time.sleep(1)
                        st.write("🔗 正在整合天氣、交通 API (Tier 3 動態路由)...")
                        time.sleep(0.8)
                        status.update(label="導覽協議已鎖定！", state="complete", expanded=False)
                    apply_variable_reward()
                    st.success(f"已將 {tribe['name']} 的座標存入『資料主權』本地緩存。")
            else:
                st.error(msg)
                if st.button(f"獲取 {tribe['name']} 的備援 Plan B", key=f"bak_{tribe['name']}"):
                    st.info("系統已自動重定向至：高義部落。預計提升 45% ROI 並降低延遲。")

with tab_front:
    render_tribe_list("前山區")

with tab_back:
    render_tribe_list("後山區")

# ==========================================
# 6. 決策校準層 (Sidebar)
# ==========================================
with st.sidebar:
    st.header("⚙️ 系統監控 (Telemetry)")
    st.write("---")
    st.metric("核心存活率", "99.99%", "+0.01%")
    st.metric("認知負荷 (Entropy)", "1.2 bit", "-0.4 bit")
    
    st.divider()
    st.subheader("🛡️ 資源備援矩陣")
    st.checkbox("開啟 Dark API 備援導航", value=True)
    st.checkbox("啟動自動化偽需求過濾", value=True)
    
    if st.button("🔴 緊急熔斷 (Hard Stop)"):
        st.error("系統進入自毀鎖定模式，所有對外通訊已切斷。")
        st.stop()
        
    st.markdown("""
    ---
    **憲法警告：**
    本介面嚴禁引入『認知超載』元素。
    任何 Tier 4 虛榮功能一律一票否決。
    """)
