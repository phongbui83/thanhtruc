import pandas as pd
import re
import shutil
from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_col(df, col):
    # Nếu nhập là ký tự cột (A, B, C...), lấy theo index
    if len(col) == 1 and col.isalpha():
        idx = ord(col.upper()) - ord('A')
        return df.iloc[:, idx]
    # Nếu nhập là tên cột, lấy theo tên
    return df[col]

@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/compare", response_class=HTMLResponse)
async def compare(
    request: Request,
    file1: UploadFile,
    file2: UploadFile,
    clientid_col1: str = Form(...),
    qty_col1: str = Form(...),
    skiprows1: int = Form(...),
    acc_col2: str = Form(...),
    qty_col2: str = Form(...),
    skiprows2: int = Form(...),
    ty_le: int = Form(...),
):
    if ty_le < 1:
        return templates.TemplateResponse("result.html", {"request": request, "download_url": None, "table_data": [], "headers": [], "error": "Tỷ lệ chuyển đổi phải lớn hơn hoặc bằng 1!"})

    # Lưu file tạm
    file1_path = os.path.join(UPLOAD_DIR, file1.filename)
    file2_path = os.path.join(UPLOAD_DIR, file2.filename)
    with open(file1_path, "wb") as f1:
        shutil.copyfileobj(file1.file, f1)
    with open(file2_path, "wb") as f2:
        shutil.copyfileobj(file2.file, f2)

    # Đọc file 1
    df1 = pd.read_excel(file1_path, skiprows=skiprows1)
    df1['C_MA'] = get_col(df1, clientid_col1).astype(str)
    def extract_qty(text):
        match = re.search(r'Exercise Qty: (\d+)', str(text))
        return int(match.group(1)) if match else None
    df1['Exercise_Qty'] = get_col(df1, qty_col1).apply(extract_qty)
    df1_grouped = df1.groupby('C_MA', as_index=False)['Exercise_Qty'].sum()
    df1_grouped['Qty_div_tyle'] = (df1_grouped['Exercise_Qty'] // ty_le).astype(int)

    # Đọc file 2
    df2 = pd.read_excel(file2_path, skiprows=skiprows2)
    df2['C_MA'] = get_col(df2, acc_col2).astype(str).str[3:10]
    df2['J'] = get_col(df2, qty_col2)
    df2_grouped = df2.groupby('C_MA', as_index=False)['J'].sum()

    # So sánh
    merged = pd.merge(df1_grouped, df2_grouped, on='C_MA', how='inner')
    merged['Match'] = merged['Qty_div_tyle'] == merged['J']
    nguyen_nhan = []
    for idx, row in merged[merged['Match'] == False].iterrows():
        if pd.isna(row['Qty_div_tyle']) or pd.isna(row['J']):
            nguyen_nhan.append('Thiếu dữ liệu số lượng ở một trong hai file')
        elif row['Qty_div_tyle'] > row['J']:
            nguyen_nhan.append(f'Tổng Exercise Qty/{ty_le} (lấy nguyên) lớn hơn tổng số lượng đặt mua')
        elif row['Qty_div_tyle'] < row['J']:
            nguyen_nhan.append(f'Tổng Exercise Qty/{ty_le} (lấy nguyên) nhỏ hơn tổng số lượng đặt mua')
        else:
            nguyen_nhan.append('Lệch không xác định')
    diff = merged[merged['Match'] == False].copy()
    diff['Nguyên nhân lệch'] = nguyen_nhan
    bao_cao = diff[['C_MA', 'Exercise_Qty', 'Qty_div_tyle', 'J', 'Nguyên nhân lệch']].copy()
    bao_cao.columns = [
        'Mã CXXXXX',
        'Tổng Exercise Qty (file1)',
        f'Tổng Exercise Qty / {ty_le} (lấy nguyên)',
        'Tổng số lượng đặt mua (file2)',
        'Nguyên nhân lệch'
    ]
    report_path = os.path.join(UPLOAD_DIR, 'bao_cao_sai_khac.xlsx')
    bao_cao.to_excel(report_path, index=False)

    # Truyền dữ liệu bảng cho HTML
    table_data = bao_cao.to_dict(orient='records')
    headers = bao_cao.columns.tolist()
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "download_url": f"/download",
            "table_data": table_data,
            "headers": headers,
            "error": None
        }
    )

@app.get("/download")
def download_report():
    report_path = os.path.join(UPLOAD_DIR, 'bao_cao_sai_khac.xlsx')
    return FileResponse(report_path, filename="bao_cao_sai_khac.xlsx") 