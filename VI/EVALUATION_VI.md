# Các Chỉ Số Đánh Giá cho Lab 3: Suy luận Agentic

Trong lab này, chúng ta không chỉ hỏi “Nó có chạy không?”. Chúng ta hỏi **“Nó hoạt động tốt đến mức nào?”**.

## Các Chỉ Số Công Nghiệp Quan Trọng

### 1. Hiệu Quả Token (Số lượng token)
- **Prompt vs. Completion**: System prompt của bạn có quá dài không? Agent có tạo ra phần “nói lan man” không cần thiết trước khi gọi tool không?
- **Phân Tích Chi Phí**: Số token thấp hơn = Chi phí thấp hơn = ROI cao hơn.

### 2. Độ Trễ (Thời gian phản hồi)
- **Time-to-First-Token (TTFT)**: LLM bắt đầu phản hồi nhanh đến mức nào?
- **Tổng Thời Gian**: Với ReAct agent, chỉ số này bao gồm toàn bộ các vòng lặp + thời gian thực thi tool.
- **Mục Tiêu**: Trong môi trường “production”, người dùng kỳ vọng phản hồi trong khoảng 200ms-2s.

### 3. Số Vòng Lặp (Số bước)
- **Suy Luận Nhiều Bước**: Agent cần bao nhiêu chu kỳ `Thought->Action` để giải quyết nhiệm vụ?
- **Chất Lượng Kết Thúc**: Agent có xác định đúng thời điểm gọi “Final Answer” không, hay bị kẹt trong “vòng lặp vô hạn”?

### 4. Phân Tích Lỗi (Mã lỗi)
- **JSON Parser Error**: LLM xuất `Action` theo định dạng mà code của bạn không parse được.
- **Hallucination Error**: LLM bịa ra một tool không tồn tại.
- **Timeout**: Agent vượt quá `max_steps`.

## Cách Sử Dụng Logs
Tất cả các metric này được tự động ghi lại trong thư mục `logs/`. Hãy dùng script để parse các file JSON này và tính **Độ Tin Cậy Tổng Hợp** của agent phiên bản 1 so với phiên bản 2.
