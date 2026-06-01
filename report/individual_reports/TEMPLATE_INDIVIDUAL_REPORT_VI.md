# Báo Cáo Cá Nhân: Lab 3 - Chatbot vs ReAct Agent

- **Tên Sinh Viên**: [Tên của bạn ở đây]
- **Mã Số Sinh Viên**: [Mã số của bạn ở đây]
- **Ngày**: [Ngày ở đây]

---

## I. Đóng Góp Kỹ Thuật (15 điểm)

*Mô tả đóng góp cụ thể của bạn vào codebase, ví dụ: triển khai một tool cụ thể, sửa parser, v.v.*

- **Các Module Đã Triển Khai**: [ví dụ: `src/tools/search_tool.py`]
- **Điểm Nổi Bật Trong Code**: [Copy snippet hoặc dẫn link dòng code]
- **Tài Liệu Hóa**: [Giải thích ngắn gọn code của bạn tương tác với ReAct loop như thế nào]

---

## II. Case Study Debugging (10 điểm)

*Phân tích một lỗi cụ thể bạn gặp trong lab bằng hệ thống logging.*

- **Mô Tả Vấn Đề**: [ví dụ: Agent bị kẹt trong vòng lặp vô hạn với `Action: search(None)`]
- **Nguồn Log**: [Link hoặc snippet từ `logs/YYYY-MM-DD.log`]
- **Chẩn Đoán**: [Vì sao LLM làm như vậy? Do prompt, do model, hay do tool spec?]
- **Giải Pháp**: [Bạn đã sửa như thế nào? Ví dụ: cập nhật ví dụ `Thought` trong system prompt]

---

## III. Nhận Thức Cá Nhân: Chatbot vs ReAct (10 điểm)

*Suy ngẫm về sự khác biệt trong năng lực suy luận.*

1.  **Suy Luận**: Khối `Thought` đã giúp agent như thế nào so với một câu trả lời Chatbot trực tiếp?
2.  **Độ Tin Cậy**: Trong những trường hợp nào Agent thực sự hoạt động *tệ hơn* Chatbot?
3.  **Observation**: Phản hồi từ môi trường (observations) đã ảnh hưởng đến các bước tiếp theo như thế nào?

---

## IV. Cải Tiến Tương Lai (5 điểm)

*Bạn sẽ mở rộng hệ thống này thành một AI agent production-level như thế nào?*

- **Khả Năng Mở Rộng**: [ví dụ: Dùng hàng đợi bất đồng bộ cho các tool call]
- **An Toàn**: [ví dụ: Triển khai một LLM 'Supervisor' để kiểm tra các hành động của agent]
- **Hiệu Năng**: [ví dụ: Dùng Vector DB cho tool retrieval trong hệ thống có nhiều tool]

---

> [!NOTE]
> Nộp báo cáo này bằng cách đổi tên thành `REPORT_[YOUR_NAME].md` và đặt trong thư mục này.
