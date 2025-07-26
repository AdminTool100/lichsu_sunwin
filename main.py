from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio

app = FastAPI()

# Cho phép tất cả CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

data100 = []

# Hàm fetch 100 phiên gần nhất
async def fetch_data():
    global data100
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://saobody-lopq.onrender.com/api/taixiu/history")
            response.raise_for_status()
            raw_data = response.json()

            data100 = [
                {
                    "Phien": item["session"],
                    "Xuc_xac_1": item["dice"][0],
                    "Xuc_xac_2": item["dice"][1],
                    "Xuc_xac_3": item["dice"][2],
                    "Tong": item["total"],
                    "Ket_qua": item["result"]
                }
                for item in raw_data[:100]
            ]
            print("✅ Đã cập nhật 100 phiên gần nhất.")
    except Exception as e:
        print("❌ Lỗi khi fetch dữ liệu:", str(e))


# Tự động fetch mỗi 3 giây
async def start_fetch_loop():
    while True:
        await fetch_data()
        await asyncio.sleep(3)

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(start_fetch_loop())

@app.get("/api/history")
async def get_history():
    return data100