from fastapi import FastAPI, Response, StreamingResponse
import time

app = FastAPI()

# Hàm generator để tạo dữ liệu stream
def generate_data():
    for i in range(10):
        yield f"Data {i}\n"
        # Thêm sleep để mô phỏng việc sinh dữ liệu chậm hơn
        # Thực tế bạn có thể thay thế vòng lặp này bằng việc đọc dữ liệu từ một tập tin hoặc một nguồn dữ liệu khác.
        # Đảm bảo là bạn không block main thread trong khi sinh dữ liệu trong ứng dụng thực tế.
        time.sleep(1)

@app.get("/stream")
async def get_stream():
    # Tạo một response streaming
    return StreamingResponse(generate_data(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
