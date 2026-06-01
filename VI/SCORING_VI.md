# Rubric chấm điểm Lab: Chatbot vs ReAct Agent

Tài liệu này mô tả tiêu chí chấm điểm cho Lab 3. Mục tiêu của lab là thể hiện sự hiểu biết sâu về reasoning của agent, khả năng monitoring chắc chắn, và quá trình cải tiến lặp lại dựa trên dữ liệu.

## 1. Điểm nhóm (45 điểm cơ bản + 15 điểm thưởng = tối đa 60)

Điểm này phản ánh kết quả chung của cả nhóm. Tổng điểm nhóm, bao gồm điểm cơ bản và điểm thưởng, được giới hạn tối đa ở **60 điểm**.

| Hạng mục | Mô tả | Điểm |
| :--- | :--- | :--- |
| **Chatbot Baseline** | Cài đặt một chatbot baseline tối giản, sạch và dễ hiểu. | 2 |
| **Agent v1 (Working)** | Cài đặt thành công vòng lặp ReAct với ít nhất 2 công cụ. | 7 |
| **Agent v2 (Improved)** | Cải thiện logic của agent dựa trên các lỗi đã phát hiện ở v1. | 7 |
| **Tool Design Evolution** | Tài liệu hóa rõ quá trình tiến hóa của đặc tả công cụ. | 4 |
| **Trace Quality** | Ghi lại đầy đủ cả trace thành công và trace thất bại. | 9 |
| **Evaluation & Analysis** | So sánh Chatbot vs Agent dựa trên dữ liệu, không dựa trên cảm tính. | 7 |
| **Flowchart & Insight** | Có sơ đồ logic trực quan và các bài học rút ra của nhóm. | 5 |
| **Code Quality** | Code sạch, có module rõ ràng, và tích hợp telemetry. | 4 |

> [!TIP]
> **Bài nộp nhóm**: Các nhóm phải dùng [TEMPLATE_GROUP_REPORT.md] trong thư mục `report/group_report/` cho bài nộp cuối cùng.

### Điểm thưởng nhóm (tối đa +15)

Điểm thưởng có thể được dùng để đạt giới hạn **60 điểm** hoặc để bù cho các điểm cơ bản bị mất:

| Hạng mục thưởng | Mô tả | Điểm |
| :--- | :--- | :--- |
| **Extra Monitoring** | Bổ sung các metric nâng cao theo hướng thực tế công nghiệp, ví dụ cost, token ratio, v.v. | +3 |
| **Extra Tools** | Cài đặt các công cụ nâng cao, ví dụ browsing, search, v.v. | +2 |
| **Failure Handling** | Có retry logic hoặc guardrail xử lý lỗi ở mức tốt. | +3 |
| **Live System Demo** | Demo hệ thống chạy trực tiếp thành công cho giảng viên. | +5 |
| **Ablation Experiments** | So sánh các biến thể prompt hoặc công cụ. | +2 |

---

## 2. Điểm cá nhân (40 điểm)

Để đạt đủ 40 điểm, mỗi sinh viên phải nộp file `individual_report.md` trong thư mục `report/individual_reports/`.

| Thành phần | Rubric / Yêu cầu | Điểm |
| :--- | :--- | :--- |
| **I. Đóng góp kỹ thuật** | Liệt kê các module code, công cụ, hoặc test cụ thể đã triển khai. Có bằng chứng về chất lượng và độ rõ ràng của code. | 15 |
| **II. Case study debug** | Phân tích chi tiết ít nhất một lỗi, ví dụ hallucination, vòng lặp, lỗi parser, và cách lỗi đó được xử lý bằng telemetry/log. | 10 |
| **III. Nhận thức cá nhân** | Phản tư sâu về khác biệt nền tảng giữa LLM Chatbot và ReAct Agent dựa trên kết quả lab. | 10 |
| **IV. Cải tiến trong tương lai** | Đề xuất hướng mở rộng agent lên hệ thống production-level RAG hoặc multi-agent. | 5 |

---

## 3. Cách tính tổng điểm

Điểm cuối cùng của mỗi sinh viên được tính như sau:

**Tổng điểm = MIN(60, Điểm nhóm cơ bản + Điểm thưởng nhóm) + Điểm cá nhân (tối đa 40) = tối đa 100 điểm**

> [!IMPORTANT]
> **Minh bạch điểm số**: Template chi tiết cho báo cáo cá nhân nằm tại `report/individual_reports/TEMPLATE_INDIVIDUAL_REPORT.md`.

> [!IMPORTANT]
> **Trách nhiệm cá nhân**: Tỷ trọng 40% điểm cá nhân được thiết kế để đảm bảo mỗi sinh viên đều đóng góp đáng kể và hiểu cơ chế bên trong của agentic loop.

---

> [!IMPORTANT]
> **"Fail Early, Learn Fast"**: Chất lượng của phần **phân tích lỗi** được đánh giá quan trọng không kém code chạy được cuối cùng. Một failure trace được tài liệu hóa tốt có giá trị hơn một hệ thống "hoàn hảo" nhưng không có giải thích.
