# Hướng Dẫn Giảng Viên: Lab 3 - Từ Chatbot đến ReAct Agentic

Tài liệu hướng dẫn này được thiết kế cho giảng viên để dẫn dắt một buổi lab chuyên sâu kéo dài 240 phút (4 giờ). Mục tiêu là đưa sinh viên từ “viết code chạy được” sang “xây dựng các hệ thống biết suy luận và tiến hóa”.

---

## Mục Tiêu Học Tập Cốt Lõi
1.  **Cơ chế ReAct**: Hiểu chu kỳ *Thought -> Action -> Observation*.
2.  **Khả năng quan sát theo chuẩn công nghiệp**: Học cách debug “bộ não” LLM bằng JSON log có cấu trúc.
3.  **Cải tiến lặp lại**: Cải thiện hiệu năng bằng cách chẩn đoán failure trace, không chỉ đoán prompt.

---

## Dòng Thời Gian & Luồng Buổi Học

### 01. Mở Đầu: Vì sao cần Agent? (15 phút)
- **Demo**: Cho thấy một chatbot đơn giản thất bại với truy vấn nhiều bước, ví dụ: “Tìm giá rẻ nhất và tính tổng chi phí với 10% thuế”.
- **Ý chính**: Chatbot giỏi trò chuyện; Agent giỏi *hành động*.

### 02. Phase 1: Thiết Kế Tool (30 phút)
- **Hoạt động**: Sinh viên định nghĩa tools trong `src/tools/`.
- **Điểm giảng dạy**: Nhấn mạnh tầm quan trọng của **Tool Descriptions**. LLM chỉ biết một tool thông qua phần mô tả dạng chuỗi của tool đó.
- **Ví dụ**: So sánh mô tả mơ hồ (“Calculates tax”) với mô tả chính xác (“Calculates 10% VAT for EU countries only, takes float amount”).

### 03. Phase 2: Chatbot Baseline (30 phút)
- **Hoạt động**: Chạy `chatbot.py` với các test case phức tạp.
- **Quan sát**: Nhiều sinh viên sẽ cố “prompt engineer” chatbot để giải các bài toán nhiều bước. Hãy để họ thất bại. Việc này tạo tiền đề cho ReAct.

### 04. Phase 3: Xây Dựng Agent v1 (60 phút) - Phần Cốt Lõi Của Lab
- **Hoạt động**: Triển khai `agent/agent.py`.
- **Vai trò của giảng viên**: Hỗ trợ Regex/JSON parsing, đây là nút thắt phổ biến nhất. Đảm bảo sinh viên hiểu rằng `Observation` phải được đưa ngược lại vào prompt cho bước tiếp theo.

### 05. Phase 4: Phân Tích Lỗi (45 phút) - CỰC KỲ QUAN TRỌNG
- **Hoạt động**: Mở thư mục `logs/`. Tìm `LOG_EVENT: LLM_METRIC`.
- **Case giảng dạy**: Tìm một trường hợp agent chọn sai tool hoặc bịa argument.
- **Cách sửa**: Hướng dẫn sinh viên cập nhật system prompt (v1 -> v2) hoặc tool specs dựa trên các *sự thật* này, không dựa trên trực giác.

### 06. Phase 5: Đánh Giá Nhóm (30 phút)
- **Hoạt động**: Chạy toàn bộ test suite. Tạo các bảng cho `GROUP_REPORT`.
- **Thảo luận**: Vì sao Agent thắng trong các kịch bản nhiều bước? Vì sao Chatbot thắng trong các câu hỏi đơn giản?

---

## Mẹo Giảng Dạy & Ví Dụ

### Kịch Bản Khuyến Nghị: “Trợ Lý Thương Mại Điện Tử Thông Minh”
- **Tool 1**: `check_stock(item_name)` -> Trả về số lượng tồn kho.
- **Tool 2**: `get_discount(coupon_code)` -> Trả về phần trăm giảm giá.
- **Tool 3**: `calc_shipping(weight, destination)` -> Trả về chi phí vận chuyển.
- **Test Case**: “I want to buy 2 iPhones using code 'WINNER' and ship to Hanoi. What is the total price?”

### Các Lỗi Phổ Biến Cần Theo Dõi
1.  **Vòng lặp vô hạn**: Agent lặp lại cùng một “Thought” mãi.
    - *Cách sửa*: Kiểm tra triển khai `max_steps` và cơ chế phát hiện “Final Answer”.
2.  **Lỗi JSON**: LLM xuất markdown backticks, ví dụ ```json ... ```, khiến parser có thể bỏ qua.
    - *Cách sửa*: Dạy sinh viên dùng cơ chế trích xuất robust hơn hoặc chỉ dẫn LLM rõ ràng: “Only output raw JSON.”
3.  **Observation rỗng**: Tool trả về “No data found”.
    - *Cách sửa*: Agent phản ứng với thất bại như thế nào? Nó thử tool khác hay bỏ cuộc?

---

## Chỉ Số Thành Công Cho Giảng Viên
Buổi lab được xem là thành công nếu:
- Sinh viên có thể cho bạn xem một **Failed Trace** và giải thích *vì sao* nó thất bại.
- Sinh viên có thể demo **Provider Switching** (OpenAI -> Gemini) và so sánh latency.
- Mỗi sinh viên có một **Individual Report** phản ánh đóng góp kỹ thuật cá nhân.

---

*“Trong thế giới AI, trace là sự thật. Hãy dạy sinh viên biết đọc log.”*
