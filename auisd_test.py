import streamlit as st
import requests
from PIL import Image
import numpy as np
import base64
import mimetypes
import io
import os
import sys

# Add the project's root directory to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

##############################################################
#   画像の保存先ディレクトリのパスを定義
##############################################################

#####---> Streamlit Clour(Linux Server)
# ホームディレクトリを取得してから定義
# home_dir = os.path.expanduser('~') 
# save_dir = save_dir = os.path.join(home_dir, 'tmp')

save_dir = '/tmp'

#####---> Windwos Local
# save_dir = 'c:/tmp'

#####---> Mac Local or Linux Local
# ホームディレクトリを取得してから定義
# home_dir = os.path.expanduser('~') 
# save_dir = os.path.join(home_dir, 'tmp')

# セッションステートに保存
st.session_state['save_dir'] = save_dir

# ディレクトリが存在しない場合は作成
# os.makedirs(save_dir, exist_ok=True)


###################################################################
#   Session Stateを初期化
###################################################################

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


st.title('Aui for SD AUTOMATIC1111')
st.markdown("<br>", unsafe_allow_html=True)
st.write('Google Colabで起動したAUTOMATIC1111でAIモデル化画像を2枚生成します。\n\r(1)img2img - Inpaint Upload　>　(2)img2img - Upscale　>　(3)img2img - Adetailer(Skip img2img)')

st.markdown("<br>", unsafe_allow_html=True)


##### URL入力エリア ####################

# リクエスト先URLを入力するテキストボックス
st.markdown('<p style="font-size:18px;color:#00ffff;">手順1：Stable Diffusion WebUIのURLを入力してください。</P>', unsafe_allow_html=True)
api_url_tmp = st.text_input("https://~~~.gradio.live　※http: //0.0.0.0：7860ではありません。")

# urlの末尾に'/'がある場合は削除
api_url = api_url_tmp.rstrip("/")
st.session_state['api_url'] = api_url

st.markdown("<br>", unsafe_allow_html=True)


##### 画像選択エリア ####################

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p style="font-size:18px;color:#00ffff;">手順2：衣装画像、マスク画像、マネキン画像を選択してください。</P>', unsafe_allow_html=True)
st.markdown('<div style="color:#ff0000;font-size:14px;line-height:0;">※衣装画像とマスク画像は、幅と高さが同じ画像を使用して下さい。</div><br><br>', unsafe_allow_html=True)

# アップロード可能な画像サイズを定義
MAX_SIZE_MB = 2  # 最大ファイルサイズ (MB)
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 2048  # バイト単位での制限

# 3つのカラムを作成
col1, col2, col3 = st.columns([1, 1, 1])

# 各カラムに画像アップロードとプレビューのウィジェットを追加
with col1:

    #st.header("画像 1")
    uploaded_file1 = st.file_uploader("衣装画像", type=["jpg", "jpeg", "png"], key="1")

    if uploaded_file1 is not None:
        
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
        
        else:
        
            # ファイルサイズが制限内の場合、画像を表示
            st.image(uploaded_file1, caption= str(width1)+' x '+str(height1), use_column_width=True) 

            # 保存するファイルのフルパスを定義
            img1_path = f"{save_dir}/cloth{img1_ext}"

            # 画像を保存
            with open(img1_path, "wb") as f:
                f.write(img1_data)

            # セッションステートに保存
            st.session_state['width1'] = width1
            st.session_state['height1'] = height1

with col2:

    #st.header("画像 2")
    uploaded_file2 = st.file_uploader("マスク画像", type=["jpg", "jpeg", "png"], key="2")
    
    if uploaded_file2 is not None:
        
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
        else:
            # ファイルサイズが制限内の場合、画像を表示
            st.image(uploaded_file2, caption= str(width2)+' x '+str(height2), use_column_width=True)

            # 保存するファイルのフルパスを定義
            img2_path = f"{save_dir}/mask{img2_ext}"

            # 画像を保存
            with open(img2_path, "wb") as f:
                f.write(img2_data)

            # セッションステートに保存
            st.session_state['width2'] = width2
            st.session_state['height2'] = height2

            #画像サイズの比較とメッセージ表示
            if uploaded_file1 is not None and uploaded_file2 is not None:
                if (width1 != width2) or (height1 != height2): 
                    st.error("衣装とマスクの画像サイズが違います。幅と高さが同じサイズの画像を選択してください。")
                    #st.stop()

with col3:

    #st.header("画像 3")
    uploaded_file3 = st.file_uploader("マネキン画像", type=["jpg", "jpeg", "png"], key="3")

    if uploaded_file3 is not None:
        
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
        else:
            # ファイルサイズが制限内の場合、画像を表示
            st.image(uploaded_file3, caption='', use_column_width=True)
            
            # 保存するファイルのフルパスを定義
            img3_path = f"{save_dir}/body{img3_ext}"

            # 画像を保存
            with open(img3_path, "wb") as f:
                f.write(img3_data)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


##### プロンプト選択エリア #######################################################

# プロンプトとネガティブプロンプトを定義
################################################################################

st.markdown('<p style="font-size:18px;color:#00ffff;">手順3：画像の背景を選択してください。</P>', unsafe_allow_html=True)

# 室内のプロンプト
myprompt_room = "Portrait MagMix Girl, { brown long hair | bob cut | ponytail }, { high heels | shoes }, indoors, white wall, white ceiling, white floor, white background, Hand, detailed, perfect, perfection,>"
# <lora:hand 4:0.31>"

# 屋外（街中）のプロンプト
myprompt_street = "Portrait MagMix Girl, { brown long hair | bob cut | ponytail }, { high heels | shoes }, street, Hand, detailed, perfect, perfection,>"
# <lora:hand 4:0.31>"

# 屋外（公園）のプロンプト
myprompt_cafe = "Portrait MagMix Girl, { brown long hair | bob cut | ponytail }, { high heels | shoes }, cafe, Hand, detailed, perfect, perfection,>"
# <lora:hand 4:0.31>"

# ネガティブプロンプト
mynegativeprompt0 = "bad hand, bad fingers, clothes, from behind, gloves, arm cover, long sleeves, sandals"

mynegativeprompt = "(worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch),bad hands, too many fingers, fused fingers, mutated hands and fingers, malformed hands,extra legs, missing fingers, oorly drawn hands, mutated hands, malformed limbs, missing limb, floating limbs, disconnected limbs, bad feet, long body, bad body ,extra arms, extra limb, pubic hair, text,disfigured, mutated, deformed, long neck, clothes, from behind, gloves, arm cover, long sleeves, sandals,"

################################################################################

# ラジオボタンを作成
# プロンプトラジオボタンを定義
prompt_options = {
    "背景 1：室内": myprompt_room,
    "背景 2：屋外（街中）": myprompt_street,
    "背景 3：屋外（公園）": myprompt_cafe
}

# ネガティブプロンプトラジオボタンを定義
negative_prompt_options = {
    "Option 1": "No people, no buildings",
    "Option 2": "No cars, no roads",
    "Option 3": "No animals, no vegetation"
}

# プロンプト選択ラジオボタンを作成
selected_prompt = st.radio("Choose a prompt", list(prompt_options.keys()))
st.markdown("<br>", unsafe_allow_html=True)

# ネガティブプロンプト選択ラジオボタンを作成
# selected_negative_prompt = st.radio("Choose a negative prompt", list(negative_prompt_options.keys()))

# プロンプト選択結果（payloadに引き渡し）
myprompt = prompt_options[selected_prompt]

# ネガティブプロンプト選択結果
# chosen_negative_prompt = negative_prompt_options[selected_negative_prompt]

# 選択したプロンプト・ネガティブプロンプトを表示
st.write("適用するプロンプト:\n\r", myprompt)
st.markdown("<br>", unsafe_allow_html=True)
st.write("適用するネガティブプロンプト:\n\r", mynegativeprompt)


# フッターを挿入
st.markdown(footer, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


with st.container():

    # 画像生成ボタン
    if st.button("画像を生成"):

        api_url = st.session_state['api_url']
        
        # 生成情報の確認
        if not api_url:
            st.error('"URL"が入力されていません。')
            st.stop()

        elif not uploaded_file1 or not uploaded_file2 or not uploaded_file3:

            st.error("全ての画像を選択してください。")
            st.stop()

        else:
            st.success(f"{api_url} にリクエストを送信します。")


###################################################################
#   img2img Inpaint Upload + Canny で　output.png を生成
###################################################################

            if uploaded_file1 and uploaded_file2 and uploaded_file3 is not None:

                # inpaintuoload用画像とContorolnet用画像を定義
                cloth_image = []
                with open(img1_path, 'rb') as f:
                    img_data_cloth = f.read()
                    cloth_file = base64.b64encode(f.read()).decode('utf-8')
                    cloth_image = [f"data:image/png;base64,{cloth_file}"]
            
                mask_image = []
                with open(img2_path, 'rb') as f:
                    img_data_body = f.read()
                    mask_file = base64.b64encode(f.read()).decode('utf-8')
                    mask_image = [f"data:image/png;base64,{mask_file}"]

                body_image = []
                with open(img3_path, 'rb') as f:
                    img_data = f.read()
                    body_file = base64.b64encode(f.read()).decode('utf-8')
                    body_image = [f"data:image/png;base64,{body_file}"]

                # Payloadにそれぞれの画像パスを含める
                files = {
                    "cloth": open(img1_path, "rb"),
                    "mask": open(img2_path, "rb"),
                    "body": open(img3_path, "rb")
                }

                with open(img1_path, "rb") as f:
                    img1_base64 = base64.b64encode(f.read()).decode('utf-8')

                with open(img2_path, "rb") as f:
                    img2_base64 = base64.b64encode(f.read()).decode('utf-8')

                with open(img3_path, "rb") as f:
                    img3_base64 = base64.b64encode(f.read()).decode('utf-8')
        
                for i in range(2):
                    #print("iの値：",i)
                    payload = {
                        "batch_size" :1,
                        "cfg_scale": 1,
                        "denoising_strength": 0.75,
                        "height": height1,  #読み込んだ高さを使用
                        "init_images": [img1_base64],
                        "inpaint_full_res": 1,  # Inpaint area - 0:Whole picture, 1:Only masked
                        "inpaint_full_res_padding": 32,
                        "inpainting_fill": 3,  # Masked content - 0:fill, 1:original, 2:latent noise, 3:latent nothing
                        "inpainting_mask_invert": 1,  # Mask mode - 0:inpaint not masked, 1:inpaint not masked
                        "mask": img2_base64,  # マスク画像を指定
                        #"n": 2,
                        "negative_prompt": mynegativeprompt,
                        "prompt": myprompt,
                        "resize_mode": 0,  # Resize mode
                        "sampler_name": "DPM++ SDE",
                        "scheduler": "Karras",
                        "steps": 12,
                        "width": width1,  # 読み込んだ幅を使用
                        "alwayson_scripts": {
                            "ControlNet": {  # canny を適用
                                "args": [
                                    {
                                        "control_mode": "Balanced",
                                        "enabled": True,
                                        "guidance_end": 1.0,
                                        "guidance_start": 0.0,
                                        "image": {
                                            "image": img3_base64,  # 衣装を着たマネキン画像を指定
                                            "mask": img3_base64    # 衣装を着たマネキン画像を指定
                                        },
                                        "input_mode": "simple",
                                        "is_ui": True,
                                        "loopback": False,
                                        "low_vram": False,
                                        "mask": None,
                                        "model": "sdxl_cannyv2",
                                        "module": "canny",
                                        "output_dir": "",
                                        "pixel_perfect": True,
                                        "processor_res": 512,
                                        "pulid_mode": "Fidelity",
                                        "resize_mode": "Crop and Resize",
                                        "save_detected_map": True,
                                        "threshold_a": 100,
                                        "threshold_b": 200,
                                        "weight": 0.4
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
                        
                    # APIリクエストを送信
                    response = requests.post(api_url+'/sdapi/v1/img2img', json=payload)

                    if response.status_code == 200:

                        # 生成された画像を取得
                        result = response.json()
                        # 生成した標準画像変数を定義
                        generated_images = result['images']

                        # 画像の保存処理
                        image_name = f"output{i}.png"
                        full_path = os.path.join(save_dir, image_name)

                        try:
                            with open(full_path, 'wb') as f:
                                f.write(base64.b64decode(generated_images[0]))
                                st.write(f"{i+1}枚目の標準画像を生成しました。")

                                # 画像を表示
                                st.image(full_path, caption=image_name, use_column_width=True)

                                i += 1

                        except Exception as e:
                            st.error(f"画像の保存に失敗しました。: {e}")
                            st.stop()  
                        
                    else:
                        st.error(f"Request failed with status code {response.status_code}")
                        #st.error(response.text)
                        st.error(f"画像生成に失敗しました。: {response.text}")
                        st.stop()

                #i += 1
            
                st.success("標準画像の生成が完了しました。高解像度化処理を開始します。")


###################################################################
#   img2img + Tile + R-ESRGAN 4x+ で高解像度化
###################################################################

# if uploaded_file1 and uploaded_file2 and uploaded_file3 is not None:

    if 'api_url' in st.session_state:

        for j in range(2):
            
            # 高解像度化用画像の定義
            hiresImage= []

            imgFilename = save_dir + '/output' + str(j) + '.png'
            src_img = Image.open(imgFilename)
            img_bytes = io.BytesIO()
            src_img.save(img_bytes, format='png')
            image_b64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
            img_bytes.close()
            src_img.close()
            hiresImage = (image_b64)

            # Payloadにそれぞれの画像パスを含める
            files = {
                "hiresImage0": open(save_dir + '/output0.png', "rb"),
                "hiresImage1": open(save_dir + '/output1.png', "rb"),
            }

            height1 = st.session_state['height1']
            width1 = st.session_state['width1']

            upscale_payload = {
                "batch_size": 1,
                "cfg_scale": 2,
                "denoising_strength": 0.4,
                "height": height1,
                "init_images": [hiresImage], #--- 高解像度化する画像 output.png を指定
                "n": 2,
                "negative_prompt": mynegativeprompt,
                "prompt": myprompt,
                "sampler_name": "DPM++ SDE",
                "scheduler": "Karass",
                "script_args": [
                    "<p style=\"margin-bottom:0.75em\">Will upscale the image by the selected scale factor; use width and height sliders to set tile size</p>",
                    64,
                    "R-ESRGAN 4x+", #--- 【注意】APIで 4x-UltraSharp、SwinIR 4x が動作せず（要検証）
                    1.5
                ],
                "script_name": "sd upscale",
                "seed": -1,
                "steps": 12,
                "width": width1,
                "alwayson_scripts": {
                    "ControlNet": {     #--- tile を適用
                        "args": [
                            {
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
                                "model": "sdxl_tile",
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

            upscale_response = requests.post(st.session_state['api_url']+'/sdapi/v1/img2img', json=upscale_payload)

            if upscale_response.status_code == 200:
                
                # 生成された画像を取得
                hires_result = upscale_response.json()

                # 生成した高解像度化画像変数を定義
                hires_generated_images = hires_result['images']

                # 保存先のパス
                save_dir = st.session_state['save_dir']

                # 画像の保存処理
                hires_image_name = f"output_hires{j}.png"
                hires_full_path = os.path.join(save_dir, hires_image_name)
                
                try:
                    with open(hires_full_path, 'wb') as f:
                        f.write(base64.b64decode(hires_generated_images[0]))
                        st.write(f"{j+1}枚目の高解像度化処理が終了しました。")
                        j += 1
                except Exception as e:
                    st.error(f"画像の保存に失敗しました。: {e}") 
                    
            else:
                st.error(f"高解像度化に失敗しました。: {upscale_response.text}")
        #j += 1


###################################################################
#   ADtetailerで顔を修正して完成画像を保存
###################################################################

    if 'api_url' in st.session_state:

        seq_digit = 5
        
        # 画像の保存パスを定義
        st.session_state['save_dir'] = save_dir

        for k in range(2):

            # 顔修正用画像の定義
            adImage= []

            adimgFilename = save_dir + '/output_hires' + str(k) + '.png'
            src_img = Image.open(adimgFilename)
            img_bytes = io.BytesIO()
            src_img.save(img_bytes, format='png')
            image_b64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
            img_bytes.close()
            src_img.close()
            adImage = [image_b64]

            adetailer_payload = {
                "batch_size": 1,
                #"cfg_scale": 5,
                #"denoising_strength": 0.35,
                "init_images": adImage,
                "n": 2,
                "negative_prompt": mynegativeprompt,
                "prompt": myprompt,
                # "sampler_name": "DPM++ SDE",
                # "scheduler": "Karass",
                # "seed" : myseed,
                #"hight": 2066,
                #"width": 1024,
                    "alwayson_scripts": {
                    "ADetailer": {
                        "args": [
                            True,
                            True,
                            {
                                "ad_cfg_scale": 7,
                                # "ad_checkpoint": "Use same checkpoint",
                                #"ad_clip_skip": 1,
                                "ad_confidence": 0.3,
                                "ad_controlnet_guidance_end": 1,
                                "ad_controlnet_guidance_start": 0,
                                #"ad_controlnet_model": "None",
                                #"ad_controlnet_module": "None",
                                #"ad_controlnet_weight": 1,
                                #"ad_denoising_strength": 0.4,
                                "ad_dilate_erode": 4,
                                "ad_inpaint_height": 512,
                                "ad_inpaint_only_masked": True,
                                "ad_inpaint_only_masked_padding": 32,
                                "ad_inpaint_width": 512,
                                "ad_mask_blur": 4,
                                "ad_mask_k_largest": 0,
                                "ad_mask_max_ratio": 1,
                                #"ad_mask_merge_invert": "None",
                                "ad_mask_min_ratio": 0,
                                "ad_model": "mediapipe_face_full",
                                #"ad_model_classes": "",
                                #"ad_negative_prompt": "",
                                #"ad_noise_multiplier": 1,
                                #"ad_prompt": "",
                                #"ad_restore_face": False,
                                #"ad_sampler": "DPM++ 2M",
                                #"ad_scheduler": "Use same scheduler",
                                "ad_steps": 28,
                                #"ad_tab_enable": True,
                                #"ad_use_cfg_scale": False,
                                #"ad_use_checkpoint": False,
                                #"ad_use_clip_skip": False,
                                #"ad_use_inpaint_width_height": False,
                                #"ad_use_noise_multiplier": False,
                                #"ad_use_sampler": False,
                                #"ad_use_steps": False,
                                #"ad_use_vae": False,
                                #"ad_vae": "Use same VAE",
                                #"ad_x_offset": 0,
                                #"ad_y_offset": 0,
                                #"is_api": []
                            }
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

            st.write(f"{k+1}枚目の最終処理をしています。")
            adetailer_response = requests.post(st.session_state['api_url']+'/sdapi/v1/img2img', json=adetailer_payload)
            
            if adetailer_response.status_code == 200:

                # 生成された画像を取得
                ad_result = adetailer_response.json() #['images']

                # 生成した完成画像変数を定義
                last_generated_images = ad_result['images']

                # 完成画像の保存パス
                save_dir_outputs = '/tmp/outputs'

                # ディレクトリが存在しない場合は作成
                os.makedirs(save_dir_outputs, exist_ok=True)

                # '/tmp/outputs内のファイル数をカウント
                file_count = sum(os.path.isfile(os.path.join(save_dir_outputs, name)) for name in os.listdir(save_dir_outputs))
                
                # ファイル名に追加する連番
                renban = f"{file_count + 1 - 1:0{seq_digit}}"

                # 完成画像のファイル名
                ad_image_name = renban + '-compimg.png'
                ad_full_path = os.path.join(save_dir_outputs, ad_image_name)

                try:
                    with open(ad_full_path, 'wb') as f:
                        f.write(base64.b64decode(last_generated_images[0]))
                        st.write(f"{k+1}枚目が完成しました。")
                        k += 1

                except Exception as e:
                    st.error(f"画像の保存に失敗しました。: {e}")

                # 完成画像を表示
                st.image(ad_full_path, caption=ad_image_name, use_column_width=True)

                # 完成画像のダウンロードリンクを作成
                def get_image_download_link(ad_full_path, ad_image_name):
                    with open(ad_full_path, "rb") as file:
                        img_bytes = file.read()
                    b64 = base64.b64encode(img_bytes).decode()
                    href = f'<a href="data:file/png;base64,{b64}" download="{ad_image_name}">📥 Download Image</a>'
                    return href

                # ダウンロードリンクを表示
                download_link = get_image_download_link(ad_full_path, "downloaded_image.png")
                st.markdown(download_link, unsafe_allow_html=True)

                # base64でエンコードされた画像を表示
                #with open(ad_full_path, "rb") as f:
                #    img_base64 = base64.b64encode(f.read()).decode("utf-8")
                    
                #    st.markdown(
                #        f'<img src="data:image/png;base64,{img_base64}" alt="Generated Image" />',
                #        unsafe_allow_html=True
                #    )

            else:
                st.error(f"Adetailerでの処理に失敗しました。: {adetailer_response.text}")

            # k += 1