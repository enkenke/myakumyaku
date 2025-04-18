import streamlit as st
from PIL import Image
import io
import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, PathPatch
from matplotlib.path import Path

# 色定義
COLOR_FACE = "#0066CC"
COLOR_OUTER = "#E50012"
COLOR_EYE_WHITE = "#FFFFFF"
COLOR_EYE_IRIS = "#0066CC"
COLOR_MOUTH = "#FFFFFF"

# 青い顔（楕円）
def draw_face(ax, center=(0, 0), width=0.9, height=0.9):
    ax.add_patch(Ellipse(center, width, height, color=COLOR_FACE, zorder=1))

# ランダムな口
def draw_random_mouth(ax, center=(0, 0.1)):
    width = random.uniform(0.22, 0.27)
    height = random.uniform(0.35, 0.5)
    curve_depth = random.uniform(0.03, 0.07)
    cx, cy = center
    rx = width / 2
    ry = height / 2
    verts = [(cx + rx, cy), (cx, cy - curve_depth), (cx - rx, cy),
             (cx - rx, cy - ry), (cx, cy - ry * 1.1), (cx + rx, cy - ry), (cx + rx, cy)]
    codes = [Path.MOVETO] + [Path.CURVE3] * 5 + [Path.LINETO]
    ax.add_patch(PathPatch(Path(verts, codes), facecolor=COLOR_MOUTH, edgecolor='none', zorder=2))

# 赤パーツ配置
def draw_outer_shapes(ax, center=(0, 0), face_width=0.9, face_height=0.9,
                      base_circle_radius=0.2, num=12, range_jitter=0.1,
                      size_jitter=0.3, aspect_jitter=0.3, rotate_ellipses=True,
                      snowman_prob=0.1):
    a = face_width / 2
    b = face_height / 2
    angles = [2 * math.pi * i / num for i in range(num)]
    positions = []
    for theta in angles:
        radius_scale = random.uniform(1 - range_jitter, 1 + range_jitter)
        x = center[0] + a * math.cos(theta) * radius_scale
        y = center[1] + b * math.sin(theta) * radius_scale
        this_r = base_circle_radius * random.uniform(1 - size_jitter, 1 + size_jitter)
        if random.random() < snowman_prob:
            r1, r2 = this_r * 0.9, this_r * 0.7
            gap = this_r * 1.1
            ax.add_patch(Circle((x, y + gap / 2), r1, color=COLOR_OUTER, zorder=3))
            ax.add_patch(Circle((x, y - gap / 2), r2, color=COLOR_OUTER, zorder=3))
            positions += [(x, y + gap / 2, r1), (x, y - gap / 2, r2)]
        else:
            if random.random() < 0.7:
                ax.add_patch(Circle((x, y), this_r, color=COLOR_OUTER, zorder=3))
            else:
                w = 2 * this_r * random.uniform(1 - aspect_jitter, 1 + aspect_jitter)
                h = 2 * this_r * random.uniform(1 - aspect_jitter, 1 + aspect_jitter)
                ang = random.uniform(0, 360) if rotate_ellipses else 0
                ax.add_patch(Ellipse((x, y), w, h, angle=ang, color=COLOR_OUTER, zorder=3))
            positions.append((x, y, this_r))
    return positions

# 目を描く
def draw_eyes(ax, positions, num_eyes=5):
    indices = random.sample(range(len(positions)), num_eyes)
    for idx in indices:
        x, y, r = positions[idx]
        dx = (0 - x) * 0.1 + random.uniform(-0.02, 0.02)
        dy = (0 - y) * 0.1 + random.uniform(-0.02, 0.02)
        eye_x, eye_y = x + dx, y + dy
        eye_radius = r * 0.5
        ax.add_patch(Circle((eye_x, eye_y), eye_radius, color=COLOR_EYE_WHITE, zorder=4))
        iris_radius = eye_radius * 0.5
        offset = eye_radius * 0.4
        ang = random.uniform(0, 2 * math.pi)
        dx, dy = offset * math.cos(ang), offset * math.sin(ang)
        ax.add_patch(Circle((eye_x + dx, eye_y + dy), iris_radius, color=COLOR_EYE_IRIS, zorder=5))

# 全体描画
def draw_myakumyaku_to_buffer(num_outer=12, num_eyes=5, user_seed=None):
    # シード処理
    if user_seed is not None:
        seed = user_seed
    else:
        seed = random.randint(0, 999999999)

    random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)

    face_width = round(random.uniform(0.7, 1.2), 2)
    face_height = round(random.uniform(0.7, 1.2), 2)

    draw_face(ax, width=face_width, height=face_height)
    draw_random_mouth(ax, center=(0, 0.1))
    base_radius = 0.18 * math.sqrt(12 / num_outer)
    positions = draw_outer_shapes(
        ax,
        face_width=face_width,
        face_height=face_height,
        base_circle_radius=base_radius,
        num=num_outer,
        range_jitter=0.2,
        size_jitter=0.23,
        aspect_jitter=0.25,
        rotate_ellipses=True,
        snowman_prob=0.15
    )
    draw_eyes(ax, positions, num_eyes=num_eyes)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return buf, seed
st.set_page_config(
    page_title="ミャクミャク生成装置",
    page_icon="🧬",
    layout="centered"
)

# ✅ 背景色とボタンデザインのカスタムCSS

st.markdown("""
<!-- Google Fonts 読み込み -->
<link href="https://fonts.googleapis.com/css2?family=Kosugi+Maru&display=swap" rel="stylesheet">

<style>
    html, body, [class*="css"] {
        font-family: 'Kosugi Maru', sans-serif;
        background-color: #fffcee;
    }

    h1, h2, h3 {
        font-weight: bold;
    }

    .stButton>button {
        font-family: 'Kosugi Maru', sans-serif;
        font-weight: bold;
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }

    .stDownloadButton>button {
        font-family: 'Kosugi Maru', sans-serif;
        background-color: #cc0000;
        color: white;
        border-radius: 6px;
        font-weight: bold;
        padding: 6px 12px;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
    body {
        background-color: #fffcee;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: none;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #004b99;
        color: #e6f0ff;
    }
    .stDownloadButton>button {
        background-color: #cc0000;
        color: white;
        border-radius: 6px;
        font-weight: bold;
        padding: 6px 12px;
    }
    .stDownloadButton>button:hover {
        background-color: #a30000;
        color: #fff0f0;
    }
</style>
""", unsafe_allow_html=True)

# 🧬 アプリ説明
st.markdown("""
# 🧬 ミャクミャク生成装置
大阪・関西万博のシンボル「ミャクミャク」を生成します。

💡 **細胞の数**が多いほど複雑な形に、  
👁️ **目の数**が多いほど感情豊かになります。
""")

# 🔘 ユーザー設定
num_outer = st.slider("🧫 細胞の数", min_value=7, max_value=30, value=12)
num_eyes = st.slider("👁️ 目の数", min_value=1, max_value=num_outer, value=min(5, num_outer))

# 🛠️ 詳細設定（折りたたみ）
with st.expander("🛠️ 高度な設定（シード値の指定）", expanded=False):
    user_seed_input = st.text_input("🔢 シード値（任意）", placeholder="空欄ならランダム")

# 🚀 実行
if st.button("🚀 ミャクミャクを生成！"):
    try:
        user_seed = int(user_seed_input) if user_seed_input else None
    except ValueError:
        st.error("⚠️ シード値には整数を入力してください。")
        user_seed = None

    buf, used_seed = draw_myakumyaku_to_buffer(
        num_outer=num_outer,
        num_eyes=num_eyes,
        user_seed=user_seed
    )

    st.markdown("---")
    st.image(Image.open(buf), caption=f"目: {num_eyes}｜細胞: {num_outer}｜Seed: {used_seed}")

    st.download_button(
        label="⬇️ このミャクミャクを保存する",
        data=buf,
        file_name=f"myakumyaku_{used_seed}.png",
        mime="image/png"
    )

    st.success("🎉 新しいミャクミャクが生成されました！")
    st.caption(f"この個体のシード値： `{used_seed}`（再生成用）")
st.markdown("""
<br><br>
<div style="text-align: right;">
    <a href="https://x.com/make_myakumyaku" target="_blank" style="
        font-family: 'Kosugi Maru', sans-serif;
        background-color: #eeeeee;
        color: #333;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 12px;
        text-decoration: none;
        border: 1px solid #ccc;
    ">
    📩 お問い合わせ (@make_myakumyaku)
    </a>
</div>
""", unsafe_allow_html=True)

