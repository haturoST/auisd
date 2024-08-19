import streamlit as st
import requests
from PIL import Image
import numpy as np
import base64
import mimetypes
import io
#from io import BytesIO
import os
import platform
import datetime

MAX_SIZE_MB = 2  # 最大ファイルサイズ (MB)
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 2048  # バイト単位での制限

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
    .custom-header {
        font-size: 15px;
        color: #ffffff;
        font-weight: bold;
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
##############################################################
#   StreamlitでUIを作成
##############################################################
st.title('Aui for SD AUTOMATIC1111')
st.markdown("<br>", unsafe_allow_html=True)
st.write('Google Colabで起動したAUTOMATIC1111でAIモデル化画像を2枚生成します。\n\r(1)img2img - Inpaint Upload　>　(2)img2img - Upscale　>　(3)img2img - Adetailer(Skip img2img)')

st.markdown("<br>", unsafe_allow_html=True)

# リクエスト先URLを入力するテキストボックス
st.markdown('<p style="font-size:18px;color:#00ffff;">手順1：Stable Diffusion WebUIのURLを入力してください。</P>', unsafe_allow_html=True)
api_url_tmp = st.text_input("https://~~~.gradio.live　※http: //0.0.0.0：7860ではありません。")

api_url = api_url_tmp.rstrip("/")
st.session_state['api_url'] = api_url

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p style="font-size:18px;color:#00ffff;">手順2：衣装画像、マスク画像、マネキン画像を選択してください。</P>', unsafe_allow_html=True)
st.markdown('<div style="color:#ff0000;font-size:14px;line-height:0;">※衣装画像とマスク画像は、幅と高さが同じ画像を使用して下さい。</div><br><br>', unsafe_allow_html=True)

# 3つのカラムを作成
col1, col2, col3 = st.columns([1, 1, 1])

# 各カラムに画像アップロードとプレビューのウィジェットを追加
with col1:
    #st.header("画像 1")
    #st.markdown('<div class="custom-header">衣装画像</div>', unsafe_allow_html=True)
    uploaded_file1 = st.file_uploader("衣装画像", type=["jpg", "jpeg", "png"], key="1")

    if uploaded_file1 is not None:
        file_size1 = uploaded_file1.size

        # 画像のサイズを取得
        img1 = Image.open(uploaded_file1)
        width1, height1 = img1.size

        # ファイルサイズのチェック
        if file_size1 > MAX_SIZE_BYTES:
            st.error(f"ファイルサイズが{MAX_SIZE_MB}MBを超えています。別のファイルを選択してください。")
        else:
            # ファイルサイズが制限内の場合、画像を表示
            st.image(uploaded_file1, caption= str(width1)+' x '+str(height1), use_column_width=True) 

            # セッションステートに保存
            st.session_state['width1'] = width1
            st.session_state['height1'] = height1

with col2:
    if 'width1' in st.session_state and 'height1' in st.session_state:
        # セッションステートから幅と高さを取得
        width1 = st.session_state['width1']
        height1 = st.session_state['height1']

    #st.header("画像 2")
    #st.markdown('<div class="custom-header">マスク画像</div>', unsafe_allow_html=True)
    uploaded_file2 = st.file_uploader("マスク画像", type=["jpg", "jpeg", "png"], key="2")
    
    if uploaded_file2 is not None:
        file_size2 = uploaded_file2.size

        # 画像のサイズを取得
        img2 = Image.open(uploaded_file2)
        width2, height2 = img2.size

        # ファイルサイズのチェック
        if file_size2 > MAX_SIZE_BYTES:
            st.error(f"ファイルサイズが{MAX_SIZE_MB}MBを超えています。別のファイルを選択してください。")
        else:
            # ファイルサイズが制限内の場合、画像を表示
            st.image(uploaded_file2, caption= str(width2)+' x '+str(height2), use_column_width=True)

            # サイズの比較
            if (width1 != width2) or (height1 != height2):
                st.error("画像サイズが違います。幅と高さが同じサイズの画像を選択してください。")
                st.session_state['image1'] = None
                st.session_state['image2'] = None
            else:
                # サイズが同じ場合、画像を表示
                #st.image(img1, caption='画像 1', use_column_width=True)
                #st.image(img2, caption='画像 2', use_column_width=True)

                # セッションステートに画像を保存（プレビューの初期化のため）
                st.session_state['image1'] = img1
                st.session_state['image2'] = img2
                st.session_state['height1'] = height1
                st.session_state['width1'] = width1

            # プレビューの初期化
            if 'image1' not in st.session_state or 'image2' not in st.session_state:
                st.session_state['image1'] = None
                st.session_state['imaeg2'] = None

with col3:
    #st.header("画像 3")
    #st.markdown('<div class="custom-header">マネキン画像</div>', unsafe_allow_html=True)
    uploaded_file3 = st.file_uploader("マネキン画像", type=["jpg", "jpeg", "png"], key="3")

    if uploaded_file3 is not None:
        file_size3 = uploaded_file3.size

        # ファイルサイズのチェック
        if file_size3 > MAX_SIZE_BYTES:
            st.error(f"ファイルサイズが{MAX_SIZE_MB}MBを超えています。別のファイルを選択してください。")
        else:
            # ファイルサイズが制限内の場合、画像を表示
            st.image(uploaded_file3, caption='', use_column_width=True)

            img3 = Image.open(uploaded_file3)
            st.session_state['image3'] = img3

with st.container():

    st.markdown("<br>", unsafe_allow_html=True)

    # OSの種類を取得
    #os_type = platform.system()

    # OSに応じたディレクトリを設定
    #if os_type == 'Windows':

        # 画像の保存先ディレクトリのパスを定義
    #    save_dir = 'C:/auisd/temp'
    #    st.session_state['save_dir'] = save_dir

    #elif os_type == 'Darwin':  # MacOSの場合

        #save_dir = '/Users/your_username/auisd/outputs'

        # ホームディレクトリを取得
    #    home_dir = os.path.expanduser('~') 
    #    save_dir = os.path.join(home_dir, 'auisd', 'temp')

        # 画像の保存先ディレクトリのパスを定義
    #    st.session_state['save_dir'] = save_dir
    
    #elif os_type == 'Linux':  # Linuxの場合

        # ホームディレクトリを取得
    #    home_dir = os.path.expanduser('~')
    #    save_dir = os.path.join(home_dir, 'auisd', 'temp')

        # 画像の保存先ディレクトリのパスを定義
    #    st.session_state['save_dir'] = save_dir
        
    #else:
    #    raise Exception("Unsupported OS")

    # ディレクトリが存在しない場合は作成
    #os.makedirs(save_dir, exist_ok=True)

    save_dir = '/tmp'
    st.session_state['save_dir'] = save_dir

# 画像生成ボタン
    if st.button("画像を生成"):

        if img1 and img2 and img3:
            # 画像データを取得
            img1_data = uploaded_file1.getvalue()
            img2_data = uploaded_file2.getvalue()
            img3_data = uploaded_file3.getvalue()

            # ファイル拡張子を取得
            img1_ext = mimetypes.guess_extension(uploaded_file1.type)
            img2_ext = mimetypes.guess_extension(uploaded_file2.type)
            img3_ext = mimetypes.guess_extension(uploaded_file3.type)

            # ローカルに保存
            img1_path = f"{save_dir}/cloth{img1_ext}"
            img2_path = f"{save_dir}/mask{img2_ext}"
            img3_path = f"{save_dir}/body{img3_ext}"

            with open(img1_path, "wb") as f:
                f.write(img1_data)
                #st.success(f"{img1_path} を保存しました。")

            with open(img2_path, "wb") as f:
                f.write(img2_data)
                #st.success(f"{img2_path} を保存しました。")

            with open(img3_path, "wb") as f:
                f.write(img3_data)
                #st.success(f"{img3_path} を保存しました。")

        #input("Enterキーを押すと処理が再開されます...")

        ###################################################
        # ここにプレースホルダを作成してメッセージを切り替える
        ###################################################
        st.success("Stable Doffusion WebUIにリクエストを送信しました。")

        myprompt = "Portrait MagMix Girl, brown long hair, high heels, indoors, white wall, white ceiling, white floor, white background, Hand, detailed, perfect, perfection, <lora:hand 4:0.3>"
        mynegativeprompt = "clothes, from behind, gloves, arm cover, long sleeves,"

    
    # フッターを挿入
    st.markdown(footer, unsafe_allow_html=True)
    #st.markdown('<p style="font-size:small;text-align:center;">©2023 Habanero Groove AI art Studio All rights reserved</P>', unsafe_allow_html=True)


##############################################################
#   img2img Inpaint Upload + Canny で　output.png を生成
##############################################################

    if uploaded_file1 and uploaded_file2 and uploaded_file3 is not None:
            
        cloth_image = []
        with open(img1_path, 'rb') as f:
            img_data = f.read()
            cloth_file = base64.b64encode(f.read()).decode('utf-8')
            cloth_image = [f"data:image/png;base64,{cloth_file}"]
        
        mask_image = []
        with open(img2_path, 'rb') as f:
            img_data = f.read()
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
                #"batch_size" :2,
                "cfg_scale": 2,
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
                generated_images = result['images']  # ここで正しく変数を定義

                # 画像の保存処理
                image_name = f"output{i}.png"
                full_path = os.path.join(save_dir, image_name)

                try:
                    with open(full_path, 'wb') as f:
                        f.write(base64.b64decode(generated_images[0]))
                except Exception as e:
                    st.error(f"Failed to save image: {e}")  

                #print(f"Images saved: {image_name}")
                
            else:
                st.error(f"Request failed with status code {response.status_code}")
                #st.error(response.text)
                st.error(f"Image generation failed: {response.text}")

        i += 1
    
        st.success("標準画像の生成が完了しました。高解像度化処理を開始します。")

#input("1回目の生成処理が完了。Enterキーを押すと処理が再開されます...")  

##############################################################
#   img2img + Tile + R-ESRGAN 4x+ で高解像度化
##############################################################

if uploaded_file1 and uploaded_file2 and uploaded_file3 is not None:

    #if 'Upscale_images' in locals():
    if 'api_url' in st.session_state:

        for j in range(2):
        #print('i値： ',i)

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
                    "R-ESRGAN 4x+", #--- 【注意】APIで SwinIR 4x が動作せず（要検証）
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
                hires_result = upscale_response.json() #['images']
                hires_generated_images = hires_result['images']

                save_dir = st.session_state['save_dir']

                # 画像の保存処理
                hires_image_name = f"output_hires{j}.png"
                hires_full_path = os.path.join(save_dir, hires_image_name)
                
                try:
                    with open(hires_full_path, 'wb') as f:
                        f.write(base64.b64decode(hires_generated_images[0]))
                except Exception as e:
                    st.error(f"Failed to save image: {e}") 
                    
            else:
                st.error(f"Upscale failed: {upscale_response.text}")
        j += 1

#input("2回目の生成処理が完了。Enterキーを押すと処理が再開されます...")

##############################################################
#   ADtetailerで顔を修正して完成画像を保存
##############################################################

    #if 'Adetailer_images' in locals():
    if 'api_url' in st.session_state:

        seq_digit = 5
        
        # 画像の保存先ディレクトリのパスを定義
        st.session_state['save_dir'] = save_dir

        for k in range(2):

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

            adetailer_response = requests.post(st.session_state['api_url']+'/sdapi/v1/img2img', json=adetailer_payload)
            #response = requests.post(api_url+'/sdapi/v1/img2img', files=files)

            if adetailer_response.status_code == 200:
                #st.success("Images refined with Adetailer successfully")

                # OSに応じたディレクトリを設定
                #if os_type == 'Windows':

                    # 画像の保存先ディレクトリのパスを定義
                #    save_dir_comp = 'C:/auisd/outputs'
                    #st.session_state['save_dir'] = save_dir_comp

                #elif os_type == 'Darwin':  # MacOSの場合

                    # ホームディレクトリを取得
                #    home_dir = os.path.expanduser('~') 
                #    save_dir_comp = os.path.join(home_dir, 'auisd', 'outputs')

                #elif os_type == 'Linux':  # Linuxの場合

                    # ホームディレクトリを取得
                #    home_dir = os.path.expanduser('~')
                #    save_dir = os.path.join(home_dir, 'auisd', 'temp')

                    # 画像の保存先ディレクトリのパスを定義
                #    st.session_state['save_dir'] = save_dir
                    
                #else:
                #    raise Exception("Unsupported OS")


                # 生成された画像を取得
                ad_result = adetailer_response.json() #['images']
                last_generated_images = ad_result['images']

                # 現在の日付を取得し、ディレクトリ名を作成
                today = datetime.date.today()
                date_folder_name = today.strftime('%Y-%m-%d')  # YYYY-MM-DD format
                
                save_dir_outputs = '/tmp/outputs' #os.path.join(save_dir_comp, date_folder_name)

                # ディレクトリが存在しない場合は作成
                os.makedirs(save_dir_outputs, exist_ok=True)

                file_count = sum(os.path.isfile(os.path.join(save_dir_outputs, name)) for name in os.listdir(save_dir_outputs))
                
                #st.success(f"{save_dir_date} 内にあるファイル数は、{file_count} 個")

                renban = f"{file_count + 1 - 1:0{seq_digit}}"

                ad_image_name = renban + '-compimg.png'
                ad_full_path = os.path.join(save_dir_outputs, ad_image_name)

                #st.success(ad_image_name)

                try:
                    with open(ad_full_path, 'wb') as f:
                        f.write(base64.b64decode(last_generated_images[0]))
                except Exception as e:
                    st.error(f"Failed to save image: {e}")

                # 画像を表示
                st.image(ad_full_path, caption=ad_image_name, use_column_width=True)

                # ダウンロードリンクを作成
                def get_image_download_link(ad_full_path, ad_image_name):
                    with open(ad_full_path, "rb") as file:
                        img_bytes = file.read()
                    b64 = base64.b64encode(img_bytes).decode()
                    href = f'<a href="data:file/png;base64,{b64}" download="{ad_image_name}">📥 Download Image</a>'
                    return href

                # ダウンロードリンクを表示
                download_link = get_image_download_link(ad_full_path, "downloaded_image.png")
                st.markdown(download_link, unsafe_allow_html=True)

                # さらにbase64でエンコードされた画像を表示したい場合
                #with open(ad_full_path, "rb") as f:
                #    img_base64 = base64.b64encode(f.read()).decode("utf-8")
                    
                #    st.markdown(
                #        f'<img src="data:image/png;base64,{img_base64}" alt="Generated Image" />',
                #        unsafe_allow_html=True
                #    )

            else:
                st.error(f"Adetailer failed: {adetailer_response.text}")

            i += 1

    #st.success("全ての処理が終了しました。")