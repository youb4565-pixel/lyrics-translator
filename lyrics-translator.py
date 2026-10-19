import google.generativeai as genai
import os
import sys
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

# 確保設定了 API Key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("錯誤：找不到 GEMINI_API_KEY 環境變數。請先設定您的 API 金鑰。")
    sys.exit(1)

genai.configure(api_key=api_key)

def search_lyrics_url(song_query: str) -> str:
    """自動搜尋並回傳第一個歌詞網頁的網址"""
    print(f"\n🔍 正在網路上尋找 '{song_query}' 的歌詞...")
    try:
        # 搜尋關鍵字加上 "lyrics"，只取第一筆結果
        results = DDGS().text(f"{song_query} lyrics", max_results=1)
        for r in results:
            url = r['href']
            print(f"✅ 找到可能包含歌詞的網址: {url}")
            return url
    except Exception as e:
        print(f"❌ 搜尋失敗: {e}")
    return None

def translate_from_url(url: str, target_language: str = "繁體中文"):
    print(f"📥 正在讀取網頁內容...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        webpage_text = soup.get_text(separator='\n', strip=True)
        
    except Exception as e:
        print(f"❌ 抓取網頁失敗: {e}")
        return

    print("🧠 正在請 AI 提取歌詞並進行專業翻譯 (這可能需要幾秒鐘)...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    你是一位專業的音樂翻譯家。以下是我從某個歌詞網站抓取下來的純文字。
    裡面可能夾雜了大量的網站選單、廣告或版權聲明等雜訊。
    
    任務：
    1. 從這些雜亂的文字中，自動判斷並提取出「真正的原文歌詞」。
    2. 將這首歌詞翻譯成{target_language}，具備流行音樂的詩意與順暢語感。
    3. 完全保留歌詞原本的段落與換行結構。
    
    請直接輸出「翻譯後的歌詞結果」，不需要附上原文，也不要輸出任何網頁雜訊或解釋。
    
    網頁原始文字擷取：
    {webpage_text[:15000]}
    """

    try:
        response = model.generate_content(prompt)
        translated_text = response.text.strip()
        
        output_file = "auto_translated_lyrics.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated_text)
        print(f"🎉 翻譯大功告成！結果已自動儲存為 '{output_file}'\n")
        
    except Exception as e:
        print(f"❌ 翻譯過程中發生錯誤: {e}")

if __name__ == "__main__":
    print("="*40)
    print("   🎶 AI 全自動歌詞搜尋與翻譯機 🎶   ")
    print("="*40)
    
    user_query = input("請輸入歌手與歌曲名稱 (例如: Coldplay Yellow): ")
    
    if user_query.strip():
        # 1. 先搜尋網址
        found_url = search_lyrics_url(user_query.strip())
        
        # 2. 如果有找到網址，就進行抓取與翻譯
        if found_url:
            translate_from_url(found_url)
        else:
            print("找不到這首歌的相關網頁，請嘗試更換關鍵字。")
    else:
        print("未輸入，程式結束。")
if __name__ == "__main__":
    print("="*40)
    print("   🎶 AI 全自動歌詞搜尋與翻譯機 🎶   ")
    print("="*40)
    
    user_query = input("請輸入歌手與歌曲名稱 (例如: Coldplay Yellow): ")
    
    if user_query.strip():
        found_url = search_lyrics_url(user_query.strip())
        if found_url:
            translate_from_url(found_url)
        else:
            print("找不到這首歌的相關網頁，請嘗試更換關鍵字。")
    else:
        print("未輸入，程式結束。")

    # 在最後一行加上這句，視窗就會等待按鍵不會自動關閉
    input("\n按下 Enter 鍵結束程式...")
