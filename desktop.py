import webview
import uvicorn
import threading
import sys
import os
import main

# Hàm lấy đường dẫn tuyệt đối khi đóng gói
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Hàm chạy FastAPI server
def start_server():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="error")

if __name__ == '__main__':
    # Tạo thư mục uploads nếu chưa có
    os.makedirs("uploads", exist_ok=True)
    
    # Chạy FastAPI server trong thread riêng
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Tạo cửa sổ desktop app
    window = webview.create_window(
        "Đối chiếu File Excel", 
        "http://127.0.0.1:8000",
        width=1280,
        height=720,
        min_size=(1280, 720),
        resizable=True
    )
    webview.start()