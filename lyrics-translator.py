import google.generativeai as genai
import os
import sys

# 確保設定了 API Key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("錯誤：找不到 GEMINI_API_KEY 環境變數。請先設定您的 API 金鑰。")
    sys.exit(1)

genai.configure(api_key=api_key)

def translate_lyrics_file(input_file: str, output_file: str, target_language: str = "繁體中文"):
    """讀取外部歌詞檔案進行翻譯，並儲存至新檔案。"""
    if not os.path.exists(input_file):
        print(f"錯誤：找不到指定的歌詞檔案 '{input_file}'")
        return

    # 讀取原文歌詞
    with open(input_file, 'r', encoding='utf-8') as f:
        original_lyrics = f.read()

    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
    你是一位精通多國語言的專業音樂翻譯家與作詞人。
    請將以下歌詞翻譯成{target_language}，並務必遵守以下原則：
    
    1. 語意精準：正確理解原文的文化背景、雙關語與隱喻，避免生硬的直譯。
    2. 詩意與流暢：翻譯結果需具備流行音樂的歌詞美感，讀起來順暢自然。
    3. 情感傳遞：完美捕捉原曲的情緒氛圍。
    4. 格式保留：完全維持原本的段落與換行結構，不增減段落。
    
    直接輸出翻譯結果，不需提供任何額外解釋。
    
    原文歌詞：
    {original_lyrics}
    """

    print(f"正在使用 AI 翻譯 '{input_file}' ...")
    try:
        response = model.generate_content(prompt)
        translated_text = response.text.strip()
        
        # 將翻譯結果寫入新檔案
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated_text)
        print(f"翻譯完成！已成功儲存至 '{output_file}'")
        
    except Exception as e:
        print(f"翻譯過程中發生錯誤: {e}")

if __name__ == "__main__":
    # 預設的輸入與輸出檔名
    input_filename = "lyrics_original.txt"
    output_filename = "lyrics_translated.txt"
    
    # 建立一個測試用的假歌詞檔案（如果檔案不存在）
    if not os.path.exists(input_filename):
        print(f"自動建立測試檔案 '{input_filename}'，請將想翻譯的歌詞貼入該檔案中再執行一次。")
        with open(input_filename, 'w', encoding='utf-8') as temp_file:
            temp_file.write("I'm walking on sunshine, whoa\nAnd don't it feel good!")
    else:
        translate_lyrics_file(input_filename, output_filename)
