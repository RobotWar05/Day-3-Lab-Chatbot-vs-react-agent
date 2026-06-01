# Báo Cáo Nhóm: Lab 3 - Hệ Thống Agentic Chuẩn Production

- **Tên Nhóm**: [Tên]
- **Thành Viên Nhóm**: [Thành viên 1, Thành viên 2, ...]
- **Ngày Triển Khai**: [YYYY-MM-DD]

---

## 1. Tóm Tắt Điều Hành

*Tổng quan ngắn gọn về mục tiêu của agent và tỷ lệ thành công so với chatbot baseline.*

- **Tỷ Lệ Thành Công**: [ví dụ: 85% trên 20 test cases]
- **Kết Quả Chính**: [ví dụ: “Agent của nhóm giải được nhiều hơn 40% truy vấn nhiều bước so với chatbot baseline nhờ sử dụng đúng Search tool.”]

---

## 2. Kiến Trúc Hệ Thống & Tooling

### 2.1 Triển Khai ReAct Loop
*Sơ đồ hoặc mô tả vòng lặp Thought-Action-Observation.*

### 2.2 Định Nghĩa Tool (Danh Sách Tool)
| Tên Tool | Định Dạng Input | Use Case |
| :--- | :--- | :--- |
| `calc_tax` | `json` | Tính VAT dựa trên mã quốc gia. |
| `search_api` | `string` | Truy xuất thông tin thời gian thực từ Google Search. |

### 2.3 Các LLM Provider Đã Dùng
- **Chính**: [ví dụ: GPT-4o]
- **Phụ / Dự Phòng**: [ví dụ: Gemini 1.5 Flash]

---

## 3. Telemetry & Performance Dashboard

*Phân tích các metric chuẩn công nghiệp thu thập được trong lần chạy test cuối cùng.*

- **Độ Trễ Trung Bình (P50)**: [ví dụ: 1200ms]
- **Độ Trễ Tối Đa (P99)**: [ví dụ: 4500ms]
- **Token Trung Bình Mỗi Task**: [ví dụ: 350 tokens]
- **Tổng Chi Phí Của Test Suite**: [ví dụ: $0.05]

---

## 4. Phân Tích Nguyên Nhân Gốc (RCA) - Failure Traces

*Phân tích sâu vì sao agent thất bại.*

### Case Study: [ví dụ: Hallucinated Argument]
- **Input**: “How much is the tax for 500 in Vietnam?”
- **Observation**: Agent gọi `calc_tax(amount=500, region="Asia")` trong khi tool chỉ chấp nhận mã quốc gia 2 chữ cái.
- **Nguyên Nhân Gốc**: System prompt thiếu đủ ví dụ `Few-Shot` cho định dạng argument nghiêm ngặt của tool.

---

## 5. Ablation Studies & Experiments

### Experiment 1: Prompt v1 vs Prompt v2
- **Diff**: [ví dụ: Thêm “Always double check the tool arguments before calling”.]
- **Result**: Giảm lỗi tool call không hợp lệ [ví dụ: 30%].

### Experiment 2 (Bonus): Chatbot vs Agent
| Case | Kết Quả Chatbot | Kết Quả Agent | Bên Thắng |
| :--- | :--- | :--- | :--- |
| Simple Q | Đúng | Đúng | Hòa |
| Multi-step | Hallucinated | Đúng | **Agent** |

---

## 6. Đánh Giá Mức Độ Sẵn Sàng Production

*Các cân nhắc khi đưa hệ thống này vào môi trường thực tế.*

- **Security**: [ví dụ: Input sanitization cho tool arguments.]
- **Guardrails**: [ví dụ: Tối đa 5 loops để tránh chi phí billing vô hạn.]
- **Scaling**: [ví dụ: Chuyển sang LangGraph cho branching phức tạp hơn.]

---

> [!NOTE]
> Nộp báo cáo này bằng cách đổi tên thành `GROUP_REPORT_[TEAM_NAME].md` và đặt trong thư mục này.
