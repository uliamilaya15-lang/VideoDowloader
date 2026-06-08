#!/usr/bin/env python3
"""
GitHub Auto-Uploader для загрузки файлов landing на GitHub через API
Использование:
    python3 upload_to_github.py
    
Потребуется:
    1. GitHub personal access token (создать: https://github.com/settings/tokens)
    2. GitHub username
"""

import os
import base64
import json
import requests
from pathlib import Path

# КОНФИГУРАЦИЯ (заполни нужные значения)
GITHUB_TOKEN = "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"
GITHUB_USERNAME = "uliamilaya15-lang"
REPO_NAME = "videodowloader"

# Пути к файлам
LANDING_DIR = Path(__file__).parent
FILES_TO_UPLOAD = [
    "index.html",
    "style.css", 
    "script.js",
    "robots.txt",
    "sitemap.xml",
    "google2fd91d89dfc71f3e.html"
]

# GitHub API URLs
GITHUB_API = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

def create_repo():
    """Создает репо на GitHub"""
    print(f"\n📦 Создаю репо '{REPO_NAME}'...")
    
    url = f"{GITHUB_API}/user/repos"
    data = {
        "name": REPO_NAME,
        "description": "Landing page for Video Downloader Telegram Bot",
        "homepage": "https://script-wine-seven.vercel.app",
        "public": True,
        "auto_init": True,
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code in [201, 422]:  # 422 = уже существует
        print(f"✅ Репо '{REPO_NAME}' готово!")
        return True
    else:
        print(f"❌ Ошибка: {response.status_code}")
        print(response.text)
        return False

def upload_file(file_name):
    """Загружает файл на GitHub"""
    file_path = LANDING_DIR / file_name
    
    if not file_path.exists():
        print(f"⚠️  Файл {file_name} не найден!")
        return False
    
    # Читаем файл
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Кодируем в base64
    encoded_content = base64.b64encode(content).decode('utf-8')
    
    # GitHub API URL для этого файла
    url = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{file_name}"
    
    # Проверяем, существует ли файл (для получения SHA)
    get_response = requests.get(url, headers=HEADERS)
    sha = None
    if get_response.status_code == 200:
        sha = get_response.json().get('sha')
    
    # Подготавливаем данные для загрузки
    data = {
        "message": f"Add {file_name} - Landing page files with Google verification",
        "content": encoded_content,
        "branch": "main"
    }
    
    if sha:
        data["sha"] = sha
    
    # Загружаем
    response = requests.put(url, headers=HEADERS, json=data)
    
    if response.status_code in [201, 200]:
        print(f"✅ Загружен: {file_name}")
        return True
    else:
        print(f"❌ Ошибка загрузки {file_name}: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 60)
    print("🚀 GitHub Auto-Uploader для Vercel Landing")
    print("=" * 60)
    print(f"👤 GitHub User: {GITHUB_USERNAME}")
    print(f"📁 Repo: {REPO_NAME}")
    
    # Проверяем token
    print("\n🔍 Проверяю токен...")
    check_url = f"{GITHUB_API}/user"
    check_response = requests.get(check_url, headers=HEADERS)
    
    if check_response.status_code != 200:
        print("❌ Ошибка: Неверный token или нет интернета!")
        return False
    
    print(f"✅ Токен валиден! Залогинен как: {check_response.json().get('login')}")
    
    # Создаем репо
    if not create_repo():
        return False
    
    # Загружаем файлы
    print(f"\n📤 Загружаю файлы на GitHub...")
    success_count = 0
    
    for file_name in FILES_TO_UPLOAD:
        if upload_file(file_name):
            success_count += 1
    
    print(f"\n{'=' * 50}")
    print(f"✅ Загружено файлов: {success_count}/{len(FILES_TO_UPLOAD)}")
    print(f"{'=' * 50}")
    
    # Инструкции
    if success_count == len(FILES_TO_UPLOAD):
        print(f"\n🎉 ВСЁ ГОТОВО!")
        print(f"\n📋 СЛЕДУЮЩИЕ ШАГИ:")
        print(f"1️⃣  Откройте: https://vercel.com/dashboard")
        print(f"2️⃣  Найдите проект script-wine-seven")
        print(f"3️⃣  Нажмите Settings → Git")
        print(f"4️⃣  Подключите GitHub репо: {GITHUB_USERNAME}/{REPO_NAME}")
        print(f"5️⃣  Vercel автоматически перестроит сайт!")
        print(f"\n📍 Файл верификации Google доступен по адресу:")
        print(f"https://script-wine-seven.vercel.app/google2fd91d89dfc71f3e.html")
        print(f"\n✨ Затем зарегистрируйте в Google Search Console!")
        return True
    
    return False

if __name__ == "__main__":
    main()
