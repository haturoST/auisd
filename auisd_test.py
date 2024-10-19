import streamlit as st
import requests
from PIL import Image
import numpy as np
import base64
import mimetypes
import io
from io import BytesIO
import os
import sys
import shutil
import time

# Add the project's root directory to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 処理フラグを初期化
st.session_state['step'] = 0

##############################################################
#   画像の保存先ディレクトリのパスを定義
##############################################################

#####---> Streamlit Clour(Linux Server)
# ホームディレクトリを取得してから定義
# home_dir = os.path.expanduser('~') 
# save_dir = save_dir = os.path.join(home_dir, 'tmp')

# save_dir = '/tmp'
# save_dir_materials = save_dir + '/materials'
# save_dir_temp = save_dir + '/temp'
# save_dir_outputs = save_dir + '/outputs'

#####---> Windwos Local
save_dir = 'c:/tmp'
save_dir_materials = save_dir + '/materials'
save_dir_temp = save_dir + '/temp'
save_dir_outputs = save_dir + '/outputs'

#####---> Mac Local or Linux Local
# ホームディレクトリを取得してから定義
# home_dir = os.path.expanduser('~') 
# save_dir = os.path.join(home_dir, 'tmp')
# save_dir_materials = os.path.join(home_dir, ',materials')
# save_dir_temp = os.path.join(home_dir, 'temp')
# save_dir_outputs = os.path.join(home_dir, 'outputs')

# パス定義をセッションステートに保存
st.session_state['save_dir'] = save_dir
st.session_state['save_dir_materials'] = save_dir_materials
st.session_state['save_dir_temp'] = save_dir_temp
st.session_state['save_dir_outputs'] = save_dir_outputs

# ディレクトリが存在しない場合は作成
os.makedirs(save_dir, exist_ok=True)
os.makedirs(save_dir_materials, exist_ok=True)
os.makedirs(save_dir_temp, exist_ok=True)
os.makedirs(save_dir_outputs, exist_ok=True)


###################################################################
#   空のダミー画像を作成
###################################################################

# 画像ファイルのパスを定義
# output1_path = os.path.join(save_dir_temp, "output1.png")
# output2_path = os.path.join(save_dir_temp, "output2.png")
# hires_output1_path = os.path.join(save_dir_temp, "output_hires1.png")
# hires_output2_path = os.path.join(save_dir_temp, "output_hires2.png")

# 空の画像を作成
# def create_empty_image(file_path):

    # 1x1ピクセルの空の白い画像を作成
#     empty_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
#     empty_image.save(file_path)

# アプリ起動時に一度だけ空の画像を作成
# if not os.path.exists(output1_path):
#     create_empty_image(output1_path)

# if not os.path.exists(output2_path):
#     create_empty_image(output2_path)

# if not os.path.exists(hires_output1_path):
#     create_empty_image(hires_output1_path)

# if not os.path.exists(hires_output2_path):
#     create_empty_image(hires_output2_path)


###################################################################
#   Session Stateを初期化
###################################################################

# ボタンの有効・無効状態（現在未使用）
if 'button_disabled' not in st.session_state:
    st.session_state['button_disabled'] = False

# Gradio URLを初期化
if 'api_url' not in st.session_state:
    st.session_state['api_url'] = None

# 処理フラグを初期化
if 'step' not in st.session_state:
    st.session_state['step'] = 0

# 衣装画像とマスク画像の有無を初期化
if 'image1' not in st.session_state:
    st.session_state['image1'] = None
    
if 'image2' not in st.session_state:
    st.session_state['image2'] = None

# 衣装画像とマスク画像の幅と高さを初期化
if 'width1' not in st.session_state:
    st.session_state['width1'] = None
    st.session_state['height1'] = None

if 'width2' not in st.session_state:
    st.session_state['width2'] = None
    st.session_state['height2'] = None


###################################################################
#   StreamlitでUIを作成
###################################################################

# カスタムCSSを追加
st.markdown(
    """
    <style>
        body {
        margin: 0;
    }
        .custom-file-upload {
        border: 2px dashed #ccc;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        font-size: 16px;
        color: #333;
    }
        .file-uploader-label {
        font-size: 8px;
        font-weight: bold;
        color: #FF5733;
    }
    .stslider > div > div > div > input[type=range] {
        accent-color: #FFFF00;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# フッターを追加
footer = """
    <style>
        .footer {
            /*position: fixed;*/
            left: 0;
            bottom: 0;
            width: 100%;
            /*background-color: #f1f1f1;*/
            color: #ffffff;
            text-align: center;
            /*font-size: 5px;*/
            padding: 10px 0;
            /*font-size:small;text-align:center;*/
        }
    </style>
    <div class="footer">
        <p style="font-size: 12px;">©2024 Habanero Groove AI art Studio All rights reserved</p>
    </div>
"""

##### タイトル・処理説明 ##################################################

st.title('Aui for SD AUTOMATIC1111')
st.markdown("<br>", unsafe_allow_html=True)
st.write('Google Colabで起動したAUTOMATIC1111でAIモデル化画像を2枚生成します。\n\r(1)img2img - Inpaint Upload(Pose Settings))　>　(2)img2img - Inpaint Upload　>　(3)img2img - Upscale　>　(4)img2img - Adetailer(Skip img2img)')


st.markdown("<br>", unsafe_allow_html=True)


##### 手順1：URL入力エリア ################################################

# 手順1：Stable Diffusion WebUIのURLを入力
st.markdown('<p style="font-size:18px;color:#00ffff;">手順1：Stable Diffusion WebUIのURLを入力してください。</P>', unsafe_allow_html=True)
api_url_tmp = st.text_input("https://~~~.gradio.live　※http: //0.0.0.0：7860ではありません。")

# 入力フィールドが空の場合、警告を表示して処理を中断
#if not api_url_tmp:
    # st.warning("Gradio.live API URL is required to proceed.")
#    st.session_state['step'] = 0
#    st.stop()

# urlの末尾に'/'がある場合は削除
api_url = api_url_tmp.rstrip("/")
st.session_state['api_url'] = api_url

st.session_state['step'] = 0

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


##### 手順2：画像選択エリア ###############################################

# 手順2：衣装画像、マスク画像、マネキン画像、ポーズ画像を選択
st.markdown('<p style="font-size:18px;color:#00ffff;">手順2：衣装画像、マスク画像、マネキン画像を選択してください。</P>', unsafe_allow_html=True)
st.markdown('<div style="color:#ff0000;font-size:14px;line-height:0;">※衣装画像とマスク画像は、幅と高さが同じ画像を使用して下さい。</div><br><br>', unsafe_allow_html=True)

# アップロード可能な画像サイズを定義
MAX_SIZE_MB = 2  # 最大ファイルサイズ (MB)
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 2048  # バイト単位での制限

# 3つのカラムを作成
col1, col2, col3= st.columns([1, 1, 1])

# 各カラムに画像アップロードとプレビューのウィジェットを追加
with col1:

    #st.header("画像 1")
    uploaded_file1 = st.file_uploader("衣装画像", type=["jpg", "jpeg", "png"], key="1")

    # 衣装画像のファイル名のリスト
    cloth_to_delete = ['cloth.png', 'cloth.jpg']

    if uploaded_file1 is not None:

        # 既存のファイルを削除
        for cloth_img in cloth_to_delete:
            file_path = os.path.join(save_dir_materials, cloth_img)
            if os.path.exists(file_path):
                os.remove(file_path)
                # st.write(f"{filename} を削除しました")

        # 画像情報（サイズ、タイプ、拡張子）を取得
        file_size1 = uploaded_file1.size
        img1 = Image.open(uploaded_file1)
        img1_data = uploaded_file1.getvalue()
        img1_ext = mimetypes.guess_extension(uploaded_file1.type)

        # 幅と高さを取得
        width1, height1 = img1.size    

        # ファイルサイズのチェック
        if file_size1 > MAX_SIZE_BYTES:

            st.error(f"ファイルサイズが{MAX_SIZE_MB}MBを超えています。別のファイルを選択してください。")
            st.session_state['step'] = 0
        
        else:
        
            # ファイルサイズが制限内の場合、画像を表示
            st.image(uploaded_file1, caption= str(width1)+' x '+str(height1), use_column_width=True) 
            st.session_state['step'] = 0

            # 保存するファイルのフルパスを定義
            img1_path = f"{save_dir_materials}/cloth{img1_ext}"

            # 画像を保存
            with open(img1_path, "wb") as f:
                f.write(img1_data)

            # セッションステートに保存
            st.session_state['width1'] = width1
            st.session_state['height1'] = height1
            st.session_state['step'] = 0

with col2:

    # マスク画像のファイル名のリスト
    mask_to_delete = ['mask.png', 'mask.jpg']

    #st.header("画像 2")
    uploaded_file2 = st.file_uploader("マスク画像", type=["jpg", "jpeg", "png"], key="2")
    
    if uploaded_file2 is not None:

        # 既存のファイルを削除
        for mask_img in mask_to_delete:
            file_path = os.path.join(save_dir_materials, mask_img)
            if os.path.exists(file_path):
                os.remove(file_path)
                # st.write(f"{filename} を削除しました")
        
        # 画像情報（サイズ、タイプ、拡張子）を取得
        file_size2 = uploaded_file2.size
        img2 = Image.open(uploaded_file2)
        img2_data = uploaded_file2.getvalue()
        img2_ext = mimetypes.guess_extension(uploaded_file2.type)

        # 幅と高さを取得
        width2, height2 = img2.size    

        # ファイルサイズのチェック
        if file_size2 > MAX_SIZE_BYTES:
            st.error(f"ファイルサイズが{MAX_SIZE_MB}MBを超えています。別のファイルを選択してください。")
            st.session_state['step'] = 0

        else:
            # ファイルサイズが制限内の場合、画像を表示
            st.image(uploaded_file2, caption= str(width2)+' x '+str(height2), use_column_width=True)
            st.session_state['step'] = 0

            # 保存するファイルのフルパスを定義
            img2_path = f"{save_dir_materials}/mask{img2_ext}"

            # 画像を保存
            with open(img2_path, "wb") as f:
                f.write(img2_data)

            # セッションステートに保存
            st.session_state['width2'] = width2
            st.session_state['height2'] = height2
            st.session_state['step'] = 0

            #画像サイズの比較とメッセージ表示
            if uploaded_file1 is not None and uploaded_file2 is not None:
                if (width1 != width2) or (height1 != height2): 
                    st.error("衣装とマスクの画像サイズが違います。幅と高さが同じサイズの画像を選択してください。")
                    st.session_state['step'] = 0
                    #st.stop()

with col3:

    # マスク画像のファイル名のリスト
    body_to_delete = ['body.png', 'body.jpg']

    #st.header("画像 3")
    uploaded_file3 = st.file_uploader("マネキン画像", type=["jpg", "jpeg", "png"], key="3")

    if uploaded_file3 is not None:

        # 既存のファイルを削除
        for body_img in body_to_delete:
            file_path = os.path.join(save_dir_materials, body_img)
            if os.path.exists(file_path):
                os.remove(file_path)
                # st.write(f"{filename} を削除しました")
        
        # 画像情報（サイズ、タイプ、拡張子）を取得
        file_size3 = uploaded_file3.size
        img3 = Image.open(uploaded_file3)
        img3_data = uploaded_file3.getvalue()
        img3_ext = mimetypes.guess_extension(uploaded_file3.type)

        # 幅と高さを取得
        width3, height3 = img3.size    

        # ファイルサイズのチェック
        if file_size3 > MAX_SIZE_BYTES:
            st.error(f"ファイルサイズが{MAX_SIZE_MB}MBを超えています。別のファイルを選択してください。")
            st.session_state['step'] = 0

        else:
            # ファイルサイズが制限内の場合、画像を表示
            st.image(uploaded_file3, caption='', use_column_width=True)
            st.session_state['step'] = 0

            # 保存するファイルのフルパスを定義
            img3_path = f"{save_dir_materials}/body{img3_ext}"

            # 画像を保存
            with open(img3_path, "wb") as f:
                f.write(img3_data)

            st.session_state['step'] = 0


st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


##### 手順3_4_5：ラジオボタンの定義と作成 ##########################################

# 髪型ラジオボタンを定義
hair_prompt_L = " long hair"
hair_prompt_S = " shoulder length hair"
hair_prompt_B = " (layered short hair, extra short hair:1.3), undercut, straight hair"  # A-line bob/angled bob/inverted bob/handsome short hair
hair_prompt_P = " ducktail"  # ducktail/ponytail
hair_prompt_A = " braid"
hair_prompt_R = " { long hair | bob cut | ponytail }"

hair_options = {
    "ロング":hair_prompt_L,
    "ショート":hair_prompt_S,
    "ショートボブ":hair_prompt_B,
    "編み込み":hair_prompt_A,
    "ポニーテール":hair_prompt_P,
    "ランダム":hair_prompt_R,
}

# 靴ラジオボタンを定義
shoes_prompt_H = "high heels"
shoes_prompt_S = "Sneakers"
shoes_prompt_L = "long dress boots"
shoes_prompt_B = "dress boots"
shoes_prompt_R = "{ high heels | shoes | long boots | boots }"

shoes_options = {
    "ハイヒール系":shoes_prompt_H,
    "スニーカー系":shoes_prompt_S,
    "ロングブーツ系":shoes_prompt_L,
    "ブーツ系":shoes_prompt_B,
    "ランダム":shoes_prompt_R,
}

# トップス・ボトムスラジオボタンを定義（プロンプトにポーズを入れるか入れないか）
tops_prompt_P0 = ", { hand up | arm behind back }" # 腕を上げる / 腕を背後
tops_prompt_P1 = ""
tops_prompt_P2 = ", { standing | walking }"

tops_options = {
    "袖あり（半袖を含む）": tops_prompt_P1,
    "袖なし（肩が出るようなもの）": tops_prompt_P0,
}

# ボトムスラジオボタンを定義
bottoms_options = {
    "パンツ": tops_prompt_P1,
    "ロングスカート": tops_prompt_P1,
    "丈が短いスカートやパンツ": tops_prompt_P2,
}

# 背景ラジオボタンを定義
room = "indoors, white floor, large room, white background"
cafe = "indoors, cafe"
street = "street"
park = "park"

back_options = {
    "背景 1：室内（白を基調とした部屋）": room,
    "背景 2：屋内（カフェ）": cafe,
    "背景 3：屋外（街中）": street,
    "背景 4：屋外（公園）": park,
}

# へそ出しラジオボタンを定義
navel = ", navel"
no_navel = ""

navel_options = {
    "なし": no_navel,
    "あり": navel,
}

# 手順3：髪型・靴を選択
st.markdown('<p style="font-size:18px;color:#00ffff;">手順3：髪型と靴を選択してください。</P>', unsafe_allow_html=True)

# 髪型・靴用のカラムを作成
col_radio1, col_radio2= st.columns([1, 1])
with col_radio1:

    # 手順3-1：髪型を選択
    # st.markdown('<p style="font-size:18px;color:#00ffff;">手順3：髪型</P>', unsafe_allow_html=True)

    # 髪型ラジオボタンを作成
    hair_radio = st.radio('髪型', list(hair_options.keys()))
    st.session_state['step'] = 0


    st.markdown("<br>", unsafe_allow_html=True)

with col_radio2:
    # 手順3-2：靴を選択
    # st.markdown('<p style="font-size:18px;color:#00ffff;">手順4：靴</P>', unsafe_allow_html=True)

    # 靴ラジオボタンを作成
    shoes_radio = st.radio('靴', list(shoes_options.keys()))
    st.session_state['step'] = 0


st.markdown("<br>", unsafe_allow_html=True)

# 手順4：トップスとボトムスを選択
st.markdown('<p style="font-size:18px;color:#00ffff;">手順4：トップスとボトムスの概要を選択してください。</P>', unsafe_allow_html=True)

# トップス・ボトムス用のカラムを作成
col_radio3, col_radio4= st.columns([1, 1])
with col_radio3:
    # 手順4-1：トップスの種類を選択
    # st.markdown('<p style="font-size:18px;color:#00ffff;">手順5：トップスの種類</P>', unsafe_allow_html=True)

    # トップスラジオボタンを作成
    tops_radio = st.radio('トップス', list(tops_options.keys()))
    st.session_state['step'] = 0

with col_radio4:
    # 手4-2：ボトムスの種類を選択
    # st.markdown('<p style="font-size:18px;color:#00ffff;">手順6：ボトムスの種類</P>', unsafe_allow_html=True)

    # ボトムスラジオボタンを作成
    bottoms_radio = st.radio('ボトムス', list(bottoms_options.keys()))
    st.session_state['step'] = 0

    # 袖なしトップスと短いボトムスの場合、プロンプトに dynamic pose を追加
    # if tops_options[tops_radio] == tops_prompt_P0 and bottoms_options[bottoms_radio] == tops_prompt_P0:

    #     pose_prompt = tops_prompt_P0

    # else:

    #     pose_prompt = tops_prompt_P1


st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# 背景・へそ用のカラムを作成
col_radio5, col_radio6= st.columns([1, 1])

with col_radio5:
    # 手順5：へそ出しを選択
    st.markdown('<p style="font-size:18px;color:#00ffff;">手順5：へそ出しの衣装ですか？</P>', unsafe_allow_html=True)

    # へそ出し選択ラジオボタンを作成
    navel_radio = st.radio("へそあり・なし", list(navel_options.keys()))
    st.session_state['step'] = 0


with col_radio6:
    # 手順6：画像の背景を選択
    st.markdown('<p style="font-size:18px;color:#00ffff;">手順6：画像の背景を選択してください。</P>', unsafe_allow_html=True)

    # プロンプト選択ラジオボタンを作成
    back_radio = st.radio("背景の種類", list(back_options.keys()))
    st.session_state['step'] = 0


##### プロンプトとネガティブプロンプトを定義 #########################

# SD1.5用ベースプロンプト
myprompt = "best quality, highres, masterpiece, photorealistic, realistic, 1girl, beautiful hands, beautiful fingers, brown hair, " + f"{hair_options[hair_radio]}{navel_options[navel_radio]}, { shoes_options[shoes_radio]}" + f"{ tops_options[tops_radio]}{bottoms_options[bottoms_radio]}" + ", light smile, looking at viewer, collarbone, " + f"{back_options[back_radio]}" + ", brightness, daylight, bloom, bokeh,"  # + f"{pose_prompt}"


### 室内のプロンプト
# SDXL用
# myprompt_room = "Portrait MagMix Girl, { brown long hair | bob cut | ponytail }, { high heels | shoes }, indoors, white wall, white ceiling, white floor, white background,"
# Hand, detailed, perfect, perfection,<lora:hand 4:0.31>"

### 屋外（街中）のプロンプト
# SDXL用
# myprompt_street = "Portrait MagMix Girl, { brown long hair | bob cut | ponytail }, { high heels | shoes }, street,"
# Hand, detailed, perfect, perfection,<lora:hand 4:0.31>"

### 屋外（カフェ）のプロンプト
# SDXL用
# myprompt_cafe = "Portrait MagMix Girl, { brown long hair | bob cut | ponytail }, { high heels | shoes }, cafe,"
# Hand, detailed, perfect, perfection,<lora:hand 4:0.31>"

### 屋外（公園）のプロンプト
# SDXL用
# myprompt_park = "Portrait MagMix Girl, { brown long hair | bob cut | ponytail }, { high heels | shoes }, park,"
# Hand, detailed, perfect, perfection,<lora:hand 4:0.31>"


# SD1.5用ネガティブプロンプト
mynegativeprompt = "clothes, sandals, worst_quality, low quality, lowres, negative_hand, photograph by bad-artist, cgi, render, illustration, painting, drawing, arm cover, long sleeves, bag, from behind, extra legs, bad feet, extra arms, extra limb, pubic hair, text, disfigured, mutated, deformed, floating hair, bad-hands-5, negative_hand-neg,"

# bad_prompt_version2,

# mynegativeprompt = "clothes, sandals, (worst_quality:2.0), low quality, lowres, cgi, render, illustration, painting, drawing, bad-hands-5, photograph by bad-artist, arm cover, long sleeves, bag, from behind, bad hands, too many fingers, fused fingers, mutated hands and fingers, malformed hands, extra legs, missing fingers, poorly drawn hands, mutated hands, malformed limbs, missing limb, floating limbs, disconnected limbs, bad feet, long body, bad body, extra arms, extra limb, pubic hair, text, disfigured, mutated, deformed, long neck, floating hair,"

# SDXL用ネガティブプロンプト
# mynegativeprompt = "(worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch), from behind, bad hands, too many fingers, fused fingers, mutated hands and fingers, malformed hands,extra legs, missing fingers, oorly drawn hands, mutated hands, malformed limbs, missing limb, floating limbs, disconnected limbs, bad feet, long body, bad body ,extra arms, extra limb, pubic hair, text,disfigured, mutated, deformed, long neck, clothes, gloves, arm cover, long sleeves, sandals,"


st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


##### Control weight 調整スライダーを作成 ###############################################

# 修正手順：Control weight調整
st.markdown('<p style="font-size:18px;color:#ffff00;">以下のパラメータ値は、完成画像を参考にしながら必要に応じて調整してください。</P>', unsafe_allow_html=True)
st.markdown('<div style="color:#ff0000;font-size:14px;line-height:0;">※全ての画像が微調整可能ではありません。微調整が不可能な画像もあります。</div><br><br>', unsafe_allow_html=True)

# Control weight 調整スライダー用カラムを作成
col_weight1, col_weight2 = st.columns([1, 1])

# Cannyコントロールウエイト調整スライダーを作成
with col_weight1:

    canny_value = st.slider(
        '衣装デザインの微調整（標準値：1.0）',
        min_value=0.0,  # 最小値
        max_value=1.5,  # 最大値
        value=1.0,      # デフォルト値
        step=0.05       # ステップ（刻み）
    )

    st.markdown('<p style="font-size:12px;color:#666666;">衣装の模様や文字などの細かなデザインを修正します。数値が大きいほどデザインが反映されますが、破綻率も上がります。</P>', unsafe_allow_html=True)


# Opneposeコントロールウエイト調整スライダーを作成
with col_weight2:
   
    openpose_value = st.slider(
        'ポージングの微調整（標準値：0.7）',
        min_value=0.0,  # 最小値
        max_value=1.0,  # 最大値
        value=0.7,      # デフォルト値
        step=0.05       # ステップ（刻み）
    )

    st.markdown('<p style="font-size:12px;color:#666666;">ポーズと手の描画を微調整します。主に足の向きや角度に影響します。腕への影響は、ほぼありません。衣装と人体がズレている場合は、数値を上げます。※大幅なポーズの変更はできません。</P>', unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


##### Adetailer Control weight 調整スライダーを作成 ###############################################

# Control weight 調整スライダー用カラムを作成
col_weight3, col_weight4 = st.columns([1, 1])

# Adetailerコントロールウエイト調整スライダーを作成
with col_weight3:

    adetailer_weight_value = st.slider(
        '手の描画の微調整①（標準値：0.35）',
        min_value=0.0,  # 最小値
        max_value=1.0,  # 最大値
        value=0.35,      # デフォルト値
        step=0.01       # ステップ（刻み）
    )

    st.markdown('<p style="font-size:12px;color:#666666;">手の描画に違和感がある場合に調整します。0.3～0.35を目安にしてください。<br>・手の描画面積が広い場合：↓（数値を下げる）<br>・手の描画面積が狭い場合：↑（数値を上げる）</P>', unsafe_allow_html=True)


# Adetailer start調整スライダーを作成
with col_weight4:
   
    adetailer_start_value = st.slider(
        '手の描画の微調整②（標準値：0.05）',
        min_value=0.0,  # 最小値
        max_value=1.0,  # 最大値
        value=0.05,      # デフォルト値
        step=0.01       # ステップ（刻み）
    )

    st.markdown('<p style="font-size:12px;color:#666666;">手の描画の微調整①で修正しきれない場合のみ調整します。0～0.1を目安にしてください。</P>', unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# 選択したプロンプト・ネガティブプロンプトを表示
st.write("適用するプロンプト:\n\r", myprompt)
st.markdown("<br>", unsafe_allow_html=True)
st.write("適用するネガティブプロンプト:\n\r", mynegativeprompt)


# フッターを挿入
st.markdown(footer, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


##### 画像生成ボタンを作成 ##########################################

with st.container():

    # 画像生成ボタン       
    if st.button("画像を生成", use_container_width = True):

        st.markdown("<br>", unsafe_allow_html=True)

        # 標準画像の生成を開始
        st.session_state['step'] = 1  

        api_url = st.session_state['api_url']
        
        # 生成情報の確認
        if not api_url:
            st.error('"URL"が入力されていません。')
            st.stop()

        elif not uploaded_file1 or not uploaded_file2 or not uploaded_file3:

            st.error("全ての画像を選択してください。")
            st.stop()

        else:
            st.error("画像生成が終了するまで画面スクロール以外の操作をしないでください！")
            st.success(f"{api_url} にリクエストを送信します。")

        # ボタンを無効化
        st.session_state['button_disabled'] = True
        #enable_button()


#---------------------------------------------------------------------------// UI作成終了 //-----


################################################################################################
#   処理(1):img2img Inpaint Upload + Canny でtemp.png（openposeを作成するための画像） を生成
################################################################################################

if st.session_state['step'] == 1:

    with open(img1_path, "rb") as f:
        # 衣装画像（Inpaint Upload用画像1）
        img1_base64 = base64.b64encode(f.read()).decode('utf-8')

    with open(img2_path, "rb") as f:
        # マスク画像（Inpaint Upload用画像2）
        img2_base64 = base64.b64encode(f.read()).decode('utf-8')

    with open(img3_path, "rb") as f:
        # Canny用画像（マネキン画像または衣装画像）
        img3_base64 = base64.b64encode(f.read()).decode('utf-8')

        temp_payload = {
            "batch_size" :1,
            "cfg_scale": 2,
            "denoising_strength": 0.75,
            "height": height1,  #読み込んだ高さを使用
            "init_images": [img1_base64], # 衣装画像を指定
            "inpaint_full_res": 1,  # Inpaint area - 0:Whole picture, 1:Only masked
            "inpaint_full_res_padding": 32,
            "inpainting_fill": 3,  # Masked content - 0:fill, 1:original, 2:latent noise, 3:latent nothing
            "inpainting_mask_invert": 1,  # Mask mode - 0:inpaint not masked, 1:inpaint not masked
            "mask": img2_base64,  # マスク画像を指定
            "n_iter": 1,  # batch count
            "negative_prompt": mynegativeprompt,
            "prompt": myprompt,
            "resize_mode": 0,  # Resize mode
            "sampler_name": "LCM",
            "scheduler": "Automatic", # "Karras",
            "steps": 12,
            "width": width1,  # 読み込んだ幅を使用
            "alwayson_scripts": {
                "ControlNet": {
                    "args": [
                        {  ##### cannyを適用 #############################
                            "control_mode": "Balanced",
                            "enabled": True,
                            "guidance_end": 1.0,
                            "guidance_start": 0.0,
                            "image": img3_base64, # 衣装を着たマネキン画像を指定
                            # "image": {
                            #     "image": img3_base64,  # 衣装を着たマネキン画像を指定
                            #     "mask": img3_base64    # 衣装を着たマネキン画像を指定
                            # },
                            "input_mode": "simple",
                            "is_ui": True,
                            "loopback": False,
                            "low_vram": False,
                            "mask": None,
                            "model": "control_v11p_sd15_canny", # "sdxl_cannyv2",
                            "module": "canny",
                            "output_dir": "",
                            "pixel_perfect": True,
                            "processor_res": 512,
                            "pulid_mode": "Fidelity",
                            "resize_mode": "Crop and Resize",
                            "save_detected_map": True,
                            "threshold_a": 100,
                            "threshold_b": 200,
                            "weight": 1.0  # 0.5
                        }
                    ]
                },
                "Dynamic Prompts v2.17.1": {
                    "args": [
                        True,
                        False,
                        1,
                        False,
                        False,
                        False,
                        1.1,
                        1.5,
                        100,
                        0.7,
                        False,
                        False,
                        True,
                        False,
                        False,
                        0,
                        "Gustavosta/MagicPrompt-Stable-Diffusion",
                        ""
                    ]
                },
                "Soft Inpainting": {
                    "args": [
                        True,
                        1,
                        0.5,
                        4,
                        0,
                        0.5,
                        2
                    ]
                }
            }
        }
            
        # APIリクエスト送信
        if st.session_state['step'] != 1:

            st.error("セッションステートの値が1ではありません。")
            st.write(st.session_state['step'])

        else:
            
            # APIリクエスト送受信
            temp_response = requests.post(api_url+'/sdapi/v1/img2img', json=temp_payload, timeout=600)

            # レスポンス確認
            if temp_response.status_code != 200:
                st.error(f"ColabでStable Diffusionを起動してください。{temp_response.status_code}: {api_url+'/sdapi/v1/img2img'}")

            # 画像保存処理
            if temp_response.status_code == 200:

                # 生成された画像を取得
                temp_result = temp_response.json()

                # 生成した高解像度化画像変数を定義
                temp_generated_image = temp_result['images']

                # 保存先のパス
                save_dir = st.session_state['save_dir_temp']

                # 最後の画像データ（Contorolnet画像）を削除する
                if len(temp_result['images']) > 1:
                    temp_result['images'].pop(1)  # 最後の画像を除外

                # st.write("3秒待機")
                # time.sleep(3)

                # 画像の保存処理
                for idx, image_data in enumerate(temp_generated_image):
                    temp_image_name = f'temp_{idx}.png'  # 画像が複数ある場合に名前を一意にする
                    temp_full_path = os.path.join(save_dir, temp_image_name)
                    # st.write(f"保存名は{temp_image_name}。パスは{temp_full_path}")
                    # st.write(f"画像情報：{image_data}")

                    try:
                        with open(temp_full_path, 'wb') as f:
                            f.write(base64.b64decode(image_data))
                            # st.write(f"画像 {temp_image_name} の保存が完了しました。")

                    except Exception as e:
                        st.error(f"画像 {temp_image_name} の保存に失敗しました。: {e}")
                        st.stop()

                st.write("1/6：ポージング処理が終了しました。")

                # 高解像度化処理開始のフラグ
                st.session_state['step'] = 2

                # st.write("5秒待機")
                # time.sleep(5)


################################################################################################
#    処理(2):img2img Inpaint Upload + Canny + Openpose で　output1.png を生成
#    ※袖なし衣装対応のため Openpose を追加
################################################################################################

if st.session_state['step'] == 2:

    # 衣装画像（Inpaint Upload用画像1）
    with open(img1_path, "rb") as f:
        img1_base64 = base64.b64encode(f.read()).decode('utf-8')

    # マスク画像（Inpaint Upload用画像2）
    with open(img2_path, "rb") as f:
        img2_base64 = base64.b64encode(f.read()).decode('utf-8')

    # Canny用画像（マネキン画像または衣装画像）
    with open(img3_path, "rb") as f:
        img3_base64 = base64.b64encode(f.read()).decode('utf-8')

    # Openpose画像の読み込み
    img_path = '/tmp/temp/temp_0.png'

    with open(img_path, 'rb') as img_file:
        img_data = img_file.read()

        # 画像をBase64にエンコード
        openpose_img = base64.b64encode(img_data).decode('utf-8')

        # Base64エンコードされた画像データをデコードして表示
        # openpose_img_show = Image.open(BytesIO(base64.b64decode(openpose_img)))
        # st.image(openpose_img_show, caption="Openpose Image")

    payload = {
        "batch_size" :2,
        "cfg_scale": 2,
        "denoising_strength": 0.75,
        "height": height1,  #読み込んだ高さを使用
        "init_images": [img1_base64],  # マネキン画像を指定
        "inpaint_full_res": 1,  # Inpaint area - 0:Whole picture, 1:Only masked
        "inpaint_full_res_padding": 32,
        "inpainting_fill": 3,  # Masked content - 0:fill, 1:original, 2:latent noise, 3:latent nothing
        "inpainting_mask_invert": 1,  # Mask mode - 0:inpaint not masked, 1:inpaint not masked
        "mask": img2_base64,  # マスク画像を指定
        "n_iter": 1,  # batch count
        "negative_prompt": mynegativeprompt,
        "prompt": myprompt,
        "resize_mode": 0,  # Resize mode
        "sampler_name": "LCM",
        "scheduler": "Automatic", # "Karras",
        "steps": 12,
        "width": width1,  # 読み込んだ幅を使用
        "alwayson_scripts": {
            "ControlNet": {  # cannyを適用
                "args": [
                    {  ##### cannyを適用 #############################
                        "control_mode": "Balanced",
                        "enabled": True,
                        "guidance_end": 1.0,
                        "guidance_start": 0.0,
                        "image": img1_base64, # { #####---> 衣装画像を指定
                        #     "image": img3_base64,  # 衣装を着たマネキン画像を指定
                        #     "mask": img3_base64    # 衣装を着たマネキン画像を指定
                        # },
                        "input_mode": "simple",
                        "is_ui": True,
                        "loopback": False,
                        "low_vram": True,
                        "mask": None,
                        "model": "control_v11p_sd15_canny",
                        "module": "canny",
                        "output_dir": "",
                        "pixel_perfect": True,
                        "processor_res": 512,
                        "pulid_mode": "Fidelity",
                        "resize_mode": "Crop and Resize",
                        "save_detected_map": True,
                        "threshold_a": 100,
                        "threshold_b": 200,
                        "weight": canny_value,
                    },
                    {  ##### openposeを適用 #############################
                        "advanced_weighting": None,
                        "animatediff_batch": False,
                        "batch_image_files": [],
                        "batch_images": "",
                        "batch_keyframe_idx": None,
                        "batch_mask_dir": None,
                        "batch_modifiers": [],
                        "control_mode": "Balanced",
                        "effective_region_mask": None,
                        "enabled": True,
                        "guidance_end": 1.0,
                        "guidance_start": 0.0,
                        "hr_option": "Both",
                        "image": openpose_img, # openpose用画像 temp_0.pngを指定
                        "inpaint_crop_input_image": True,
                        "input_mode": "simple",
                        "ipadapter_input": None,
                        "is_ui": True,
                        "loopback": False,
                        "low_vram": True,
                        "mask": None,
                        "model": "control_v11p_sd15_openpose",
                        "module": "dw_openpose_full",
                        "output_dir": "",
                        "pixel_perfect": True,
                        "processor_res": 512,
                        "pulid_mode": "Fidelity",
                        "resize_mode": "Crop and Resize",
                        "save_detected_map": True,
                        "threshold_a": 0.5,
                        "threshold_b": 0.5,
                        "union_control_type": "OpenPose",
                        "weight": openpose_value, #####---> スライダーで調整
                    },
                ]
            },
            "Dynamic Prompts v2.17.1": {
                "args": [
                    True,
                    False,
                    1,
                    False,
                    False,
                    False,
                    1.1,
                    1.5,
                    100,
                    0.7,
                    False,
                    False,
                    True,
                    False,
                    False,
                    0,
                    "Gustavosta/MagicPrompt-Stable-Diffusion",
                    ""
                ]
            },
            "Soft Inpainting": {
                "args": [
                    True,
                    1,
                    0.5,
                    4,
                    0,
                    0.5,
                    2
                ]
            }
        }
    }
        
    # APIリクエスト送信
    if st.session_state['step'] != 2:

        st.error("セッションステートの値が2ではありません。")
        st.write(st.session_state['step'])
        st.stop()

    else:
        
        # APIリクエスト送信
        response = requests.post(api_url+'/sdapi/v1/img2img', json=payload, timeout=1200)

        # レスポンス確認
        if response.status_code == 404:
            st.error(f"404 Not Found: {api_url+'/sdapi/v1/img2img'}")

        # 画像保存処理
        if response.status_code == 200:

            # st.write("30秒待機")
            # time.sleep(30)

            response_data = response.json()

            # 画像保存処理
            def save_images(images_data, base_filename="output"):

                images_data = response_data.get('images', [])
                
                # エラー対応（response.json()の中身を表示）
                # st.write(response_data)

                # エラー対応（response.json()のimages(画像情報の部分)を表示）
                # st.write(images_data)

                # ControlNetが生成する画像を除外
                num_to_exclude = 2 * payload.get('n_iter', 1)  # ControlNetの画像を除外するための数を計算

                if len(images_data) > num_to_exclude:
                    images_data = images_data[:-num_to_exclude]  # 最後の ControlNet の画像を除外

                # 生成された画像を保存
                image_paths = []
                for idx, img_data in enumerate(images_data, start=1):
                    # base64から画像データをデコード
                    image = Image.open(BytesIO(base64.b64decode(img_data)))

                    # ファイルパスの作成
                    file_path = f"{save_dir_temp}/{base_filename}{idx}.png"

                    # 画像を保存
                    image.save(file_path, format="PNG")
                    image_paths.append(file_path)

                return image_paths
            
            # 保存処理の実行
            image_paths = save_images(response_data.get('images', []))

        else:
            st.error(f"Request failed with status code {response.status_code}")
            #st.error(response.text)
            st.error(f"画像生成に失敗しました。: {response.text}")
            st.stop()

    st.write("2/6：標準画像の生成が終了しました。")
    
    # 高解像度化処理開始のフラグ
    st.session_state['step'] = 3

    # st.write("5秒待機")
    # time.sleep(5)


################################################################################################
#    処理(3):img2img + Tile + R-ESRGAN 4x+ で高解像度化
################################################################################################

if st.session_state['step'] == 3:

    st.success("高解像度化処理を開始します。")

    # 標準画像の保存場所と高解像度化画像の保存場所を定義
    st.session_state['save_dir_temp'] = save_dir_temp
    
    # 高解像度化処理を2回実行
    for j in range(2):
        # print(f"jの値：{j}")
        
        # 高解像度化用画像の定義
        hiresImage= []

        imgFilename = save_dir_temp + '/output' + str(j+1) + '.png'
        src_img = Image.open(imgFilename)
        img_bytes = io.BytesIO()
        src_img.save(img_bytes, format='png')
        image_b64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        img_bytes.close()
        src_img.close()
        hiresImage = (image_b64)

        api_url = st.session_state['api_url']
        height1 = st.session_state['height1']
        width1 = st.session_state['width1']

        upscale_payload = {
            "batch_size": 1,
            "cfg_scale": 1,
            "denoising_strength": 0.09,
            "height": height1,
            "init_images": [hiresImage], #--- 高解像度化する画像 output.png を指定
            "n_iter": 1,  # batch count
            "negative_prompt": mynegativeprompt,
            "prompt": myprompt,
            "sampler_name": "LCM",
            "scheduler": "Automatic", # "Karass",
            "script_args": [
                "<p style=\"margin-bottom:0.75em\">Will upscale the image by the selected scale factor; use width and height sliders to set tile size</p>",
                64,
                "4x-UltraSharp", #--- 【注意】APIで 4x-UltraSharp、SwinIR 4x が動作せず（要検証）
                2.0
            ],
            "script_name": "sd upscale",
            "seed": -1,
            "steps": 12,
            "width": width1,
            "alwayson_scripts": {
                "ControlNet": {
                    "args": [
                        {  ##### tileを適用 #############################
                            #"advanced_weighting": None,
                            #"animatediff_batch": False,
                            #"batch_image_files": [],
                            #"batch_images": "",
                            #"batch_keyframe_idx": None,
                            #"batch_mask_dir": None,
                            #"batch_modifiers": [],
                            "control_mode": "Balanced",
                            #"effective_region_mask": None,
                            "enabled": True,
                            "guidance_end": 1.0,
                            "guidance_start": 0.0,
                            "hr_option": "Both",
                            "image": None,
                            "inpaint_crop_input_image": False,
                            "input_mode": "simple",
                            #"ipadapter_input": None,
                            "is_ui": True,
                            #"loopback": False,
                            "low_vram": False,
                            "mask": None,
                            "model": "control_v11f1e_sd15_tile",
                            "module": "tile_resample",
                            #"output_dir": "",
                            "pixel_perfect": True,
                            "processor_res": 768,
                            "pulid_mode": "Fidelity",
                            "resize_mode": "Crop and Resize",
                            #"save_detected_map": True,
                            "threshold_a": 1.0,
                            "threshold_b": 0.5,
                            "union_control_type": "Tile",
                            "weight": 1.0
                        },

                    ]
                },
                "Dynamic Prompts v2.17.1": {
                    "args": [
                        True,
                        False,
                        1,
                        False,
                        False,
                        False,
                        1.1,
                        1.5,
                        100,
                        0.7,
                        False,
                        False,
                        True,
                        False,
                        False,
                        0,
                        "Gustavosta/MagicPrompt-Stable-Diffusion",
                        ""
                    ]
                },
                # "Soft Inpainting": {
                #         "args": [
                #             True,
                #             1,
                #             0.5,
                #             4,
                #             0,
                #             0.5,
                #             2
                #         ] 
                #     }
                }
        }

        # APIリクエストの送信
        if st.session_state['step'] != 3:

            st.error(st.session_state['step'])
            st.error("高解像度化処理を中止しました。セッションステートの値が3ではありません。")

        else:
            
            upscale_response = requests.post(api_url+'/sdapi/v1/img2img', json=upscale_payload, timeout=3000)

            # ステータスコードが404の場合にURLを出力
            if response.status_code == 404:
                st.error(f"404 Not Found: {api_url+'/sdapi/v1/img2img'}")

            # 画像保存処理
            if upscale_response.status_code == 200:

                # st.write("6秒待機")        
                # time.sleep(6)
            
                # 生成された画像を取得
                hires_result = upscale_response.json()

                # 生成した高解像度化画像変数を定義
                hires_generated_images = hires_result['images']

                # 保存先のパス
                save_dir = st.session_state['save_dir_temp']

                # 画像の保存処理
                hires_image_name = f"output_hires{j+1}.png"
                hires_full_path = os.path.join(save_dir_temp, hires_image_name)

                # st.write("7秒待機")
                # time.sleep(7)
                
                try:
                    with open(hires_full_path, 'wb') as f:
                        f.write(base64.b64decode(hires_generated_images[0]))
                        st.write(f"{j+3}/6：{j+1}枚目の高解像度化処理が終了しました。")

                except Exception as e:
                    st.error(f"画像の保存に失敗しました。: {e}") 
                    st.stop()
                    
            else:
                st.error(f"タイムアウトのため{j+1}枚目の高解像度化に失敗しました。再度、画像を生成してください。: {upscale_response.text}")
                st.stop()
            

    # Adetailer処理開始のフラグ
    st.session_state['step'] = 4

    # st.write("5秒待機")
    # time.sleep(5)


################################################################################################
#    処理(4):ADtetailerで顔を修正して完成画像を保存
################################################################################################

if st.session_state['step'] == 4:

    st.success("最終処理を開始します。")

    seq_digit = 5

    # 高解像度化画像の保存場所を読み込み
    st.session_state['save_dir_temp'] = save_dir_temp

    # 画像の保存パスを定義
    st.session_state['save_dir_outputs'] = save_dir_outputs

    # 顔修正処理を2回実行
    for k in range(2):

        # 顔修正用画像の読み込み
        adImage= []

        adimgFilename = save_dir_temp + '/output_hires' + str(k+1) + '.png'
        src_img = Image.open(adimgFilename)
        img_bytes = io.BytesIO()
        src_img.save(img_bytes, format='png')
        image_b64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        img_bytes.close()
        src_img.close()
        adImage = [image_b64]

        adetailer_payload = {
            "batch_size": 1,
            "cfg_scale": 2,
            #"denoising_strength": 0.35,
            "init_images": adImage,
            "n_iter": 1,  # batch count
            "negative_prompt": mynegativeprompt,
            "prompt": myprompt,
            "sampler_name": "LCM",
            "scheduler": "Automatic",
            # "seed" : myseed,
            "steps": 12,
            #"hight": 2066,
            #"width": 1024,
                "alwayson_scripts": {
                "ADetailer": {
                    "args": [
                        True,
                        True,
                        {   # 顔の修正
                            # "ad_cfg_scale": 7,
                            #"ad_checkpoint": "Use same checkpoint",
                            # "ad_clip_skip": 1,
                            "ad_confidence": 0.3,
                            "ad_controlnet_guidance_end": 1,
                            "ad_controlnet_guidance_start": 0,
                            #"ad_controlnet_model": "None",
                            #"ad_controlnet_module": "None",
                            #"ad_controlnet_weight": 1,
                            "ad_denoising_strength": 0.4,
                            "ad_dilate_erode": 4,
                            "ad_inpaint_height": 512,
                            "ad_inpaint_only_masked": True,
                            "ad_inpaint_only_masked_padding": 32,
                            "ad_inpaint_width": 512,
                            "ad_mask_blur": 4,
                            "ad_mask_k_largest": 0,
                            "ad_mask_max_ratio": 1,
                            "ad_mask_merge_invert": "None",
                            "ad_mask_min_ratio": 0,
                            "ad_model": "mediapipe_face_full",
                            #"ad_model_classes": "",
                            "ad_negative_prompt": "",
                            #"ad_noise_multiplier": 1,
                            "ad_prompt": "",
                            # "ad_restore_face": False,
                            # "ad_sampler": "DPM++ 2M",
                            # "ad_scheduler": "Use same scheduler",
                            # "ad_steps": 20,
                            "ad_tab_enable": True,
                            #"ad_use_cfg_scale": False,
                            #"ad_use_checkpoint": False,
                            #"ad_use_clip_skip": False,
                            #"ad_use_inpaint_width_height": False,
                            #"ad_use_noise_multiplier": False,
                            #"ad_use_sampler": False,
                            #"ad_use_steps": False,
                            #"ad_use_vae": False,
                            #"ad_vae": "Use same VAE",
                            "ad_x_offset": 0,
                            "ad_y_offset": 0,
                            "is_api": []
                        },
                        {   # 手の修正
                            # "ad_cfg_scale": 2, ###---> 7
                            #"ad_checkpoint": "Use same checkpoint",
                            # "ad_clip_skip": 1,
                            "ad_confidence": 0.3,
                            "ad_controlnet_guidance_end": 1.0,  #0.88,
                            "ad_controlnet_guidance_start": adetailer_start_value,  #0,
                            "ad_controlnet_model": "control_v11f1p_sd15_depth",
                            "ad_controlnet_module": "depth_hand_refiner",
                            "ad_controlnet_weight": adetailer_weight_value, ###---> 1.0
                            "ad_denoising_strength": 0.4, ###---> 0.4
                            "ad_dilate_erode": 4,
                            "ad_inpaint_height": 512,
                            "ad_inpaint_only_masked": True,
                            "ad_inpaint_only_masked_padding": 32, ###---> 32
                            "ad_inpaint_width": 512,
                            "ad_mask_blur": 4, ###---> 4
                            "ad_mask_k_largest": 0,
                            "ad_mask_max_ratio": 1,
                            "ad_mask_merge_invert": "None",
                            "ad_mask_min_ratio": 0,
                            "ad_model": "hand_yolov8n.pt",
                            # "ad_model_classes": "",
                            "ad_negative_prompt": "shoes, footwear",
                            # "ad_noise_multiplier": 1,
                            "ad_prompt": "",  # "beautiful hands, beautiful fingers, detailed fingers,",
                            # "ad_restore_face": False,
                            # "ad_sampler": "DPM++ SDE",
                            # "ad_scheduler": "Karass",
                            # "ad_steps": 12,
                            "ad_tab_enable": True,
                            # "ad_use_cfg_scale": False,
                            # "ad_use_checkpoint": False,
                            # "ad_use_clip_skip": False,
                            # "ad_use_inpaint_width_height": False,
                            # "ad_use_noise_multiplier": False,
                            # "ad_use_sampler": False,
                            # "ad_use_steps": False,
                            # "ad_use_vae": False,
                            # "ad_vae": "Use same VAE",
                            "ad_x_offset": 0,
                            "ad_y_offset": 0,
                            "is_api": []
                        }
                    ]
                }
            }
        }

        st.write(f"{k+5}/6：{k+1}枚目の完成画像が表示されるまでお待ちください。")
        adetailer_response = requests.post(st.session_state['api_url']+'/sdapi/v1/img2img', json=adetailer_payload,timeout=3000)

        # 画像保存処理とプレビュー・ダウンロードリンクの表示
        if adetailer_response.status_code == 200:          

            # st.write("5秒待機")
            # time.sleep(5)
            
            # 生成された画像を取得
            ad_result = adetailer_response.json() #['images']

            # 生成した完成画像変数を定義
            last_generated_images = ad_result['images']

            # '/tmp/outputs内のファイル数をカウント
            file_count = sum(os.path.isfile(os.path.join(save_dir_outputs, name)) for name in os.listdir(save_dir_outputs))
            
            # ファイル名に追加する連番
            renban = f"{file_count + 1 - 1:0{seq_digit}}"

            # 完成画像のファイル名
            ad_image_name = renban + '-compImg.png'
            ad_full_path = os.path.join(save_dir_outputs, ad_image_name)

            #  画像保存処理とプレビュー・ダウンロードリンクの表示
            try:
                with open(ad_full_path, 'wb') as f:
                    f.write(base64.b64decode(last_generated_images[0]))

                    # 完成画像を表示
                    st.image(ad_full_path, caption=ad_image_name,  width=500, clamp=True)#use_column_width=True)

                    # 完成画像のダウンロードリンクを作成
                    def get_image_download_link(ad_full_path, ad_image_name):
                        with open(ad_full_path, "rb") as file:
                            img_bytes = file.read()
                        b64 = base64.b64encode(img_bytes).decode()
                        href = f'<a href="data:file/png;base64,{b64}" download="{ad_image_name}">📥Download Image</a>'
                        return href

                    # ダウンロードリンクを表示
                    download_link = get_image_download_link(ad_full_path, "downloaded_image.png")
                    st.markdown(download_link, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"画像の保存に失敗しました。: {e}")
                st.stop()
        else:
            st.error(f"Adetailerでの処理に失敗しました。再度、画像を生成してください。: {adetailer_response.text}")
            st.stop()

    # 処理開始フラグをリセット
    st.session_state['step'] = 0


#--------------------------------------------------------------------------// 画像生成終了 //-----


###################################################################
#   既存ファイルの削除処理を定義
###################################################################

    def clear_files_in_directory(directory):

        # ディレクトリが存在する場合
        if os.path.exists(directory):

            # ディレクトリ内のすべてのファイルとフォルダをループ
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)

                try:
                    # ファイルの場合、削除
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)

                    # サブディレクトリの場合、削除
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)

                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')


###################################################################
#    既存ファイルの削除を実行
###################################################################

# ディレクトリ内のファイルを削除
# clear_files_in_directory(save_dir_temp)
# clear_files_in_directory(save_dir_outputs)
# clear_files_in_directory(save_dir_materials)
