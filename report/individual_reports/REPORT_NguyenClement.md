# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Nguyen Clement
- **Student ID**: SV2026-0001
- **Date**: 2026-06-01

---

## I. Technical Contribution (15 Points)

*Quá trình tham gia thiết kế, phát triển và tối ưu hóa hệ thống Trợ lý ảo gợi ý địa điểm ăn uống quanh VinUni / Ocean Park / Gia Lâm.*

- **Modules Implemented**:
  1. **Tích hợp LLM Summarizer vào Agent** ([react_agent.py](file:///E:/vin_ai_k2_2026/Documents/Day3/web/backend/agent/react_agent.py)): Thiết kế và cài đặt các Prompt chuyên biệt (`SUMMARIZER_PROMPT`, `SUMMARIZER_NO_RESULTS_PROMPT`, `CLARIFY_LOCATION_PROMPT`, `UNSUPPORTED_LOCATION_PROMPT`) để Agent gọi LLM sinh Thought và phản hồi tự nhiên ở bước cuối cùng, thay vì dùng chuỗi tĩnh cứng nhắc.
  2. **Mở rộng cơ sở dữ liệu và xử lý danh mục trống** ([nearby_tools.py](file:///E:/vin_ai_k2_2026/Documents/Day3/web/backend/tools/nearby_tools.py)): Bổ sung danh mục món nước/canh (`soup`) với các địa điểm nổi tiếng (Lẩu Phan, Cháo sườn sụn, Canh cá Gia Lâm) giúp sửa lỗi không tìm thấy kết quả khi hỏi về lẩu/canh.
  3. **Khắc phục lỗi hiển thị Tiếng Việt trên Windows console**: Sửa lỗi mã hóa ký tự khi gọi API uvicorn thông qua việc đồng bộ kiểu dữ liệu UTF-8 trên toàn hệ thống backend.
- **Code Highlights**:
  Tích hợp hàm sinh Thought và Answer tự nhiên thông qua LLM:
  ```python
  # Trích đoạn xử lý LLM trong react_agent.py:
  try:
      prompt = SUMMARIZER_PROMPT.format(places_summary=places_summary)
      result = await provider.generate(message=candidate_message, system_prompt=prompt)
      thought, answer = _parse_thought_and_answer(result.text)
  except Exception as exc:
      answer = _fallback_build_answer(recommendations, parsed["category"])
      thought = f"Lỗi gọi LLM ({exc}). Rơi về chế độ trả lời mẫu."
  ```
- **Documentation**: Đặc tả quy trình ReAct loop 5 bước rõ ràng trong logs giúp UI hiển thị đầy đủ thông tin telemetry và trace của bước suy luận cuối cùng của LLM.

---

## II. Debugging Case Study (10 Points)

*Phân tích lỗi Agent phản hồi quá nhanh giống như lấy sẵn dữ liệu từ database thay vì Agent suy nghĩ.*

- **Problem Description**: Khi chạy thử nghiệm Agent ở phiên bản cũ, người dùng nhận thấy câu trả lời xuất hiện ngay lập tức (<100ms) với văn phong khô khan, giống hệt một câu lệnh `print` của Python ghép các từ khóa thô, mất đi tính "agentic" (khả năng suy nghĩ tự nhiên) của hệ thống AI.
- **Log Source**: (Trích đoạn log từ `web/backend/app.py` và `react_agent.py` trước nâng cấp)
  ```json
  {"metrics": {"latency_ms": 0, "steps": 4, "provider": "opencode", "model": "deepseek-v4-flash"}}
  ```
  Quan sát log cho thấy mặc dù cấu hình provider là `opencode` và mô hình là `deepseek-v4-flash`, thời gian phản hồi (latency) của Agent lại bằng **0ms**, chứng tỏ hệ thống hoàn toàn không gọi LLM để xử lý câu trả lời mà chỉ chạy code Python thuần túy.
- **Diagnosis**: Đi sâu vào mã nguồn của `react_agent.py`, tôi phát hiện ra hàm `run_react_agent` trả về kết quả bằng cách gọi trực tiếp hàm ghép chuỗi tĩnh `_build_answer(recommendations)`. Hệ thống hoàn toàn bỏ qua việc gọi API của LLM, dẫn đến việc Agent chạy rất nhanh nhưng thô ráp và thiếu thông minh.
- **Solution**: 
  1. Tôi đã viết lại hàm `run_react_agent` thành hàm bất đồng bộ (`async def`) để có thể gọi `await provider.generate()`.
  2. Xây dựng một prompt cấu trúc (`SUMMARIZER_PROMPT`) hướng dẫn LLM cách lấy thông tin từ database nội bộ và viết lại câu trả lời theo đúng định dạng:
     - `Thought`: <Dòng suy nghĩ tự nhiên của Agent>
     - `Final Answer`: <Câu trả lời hoàn chỉnh sinh động>
  3. Cài đặt hàm `_parse_thought_and_answer` để tách biệt hai phần này, đưa `Thought` vào danh sách trace bước 5 để hiển thị lên UI, và trả `Final Answer` về cho người dùng. Kế hoạch này giúp Agent phản hồi thông minh, có độ trễ thực tế và quy trình suy luận trực quan.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning (Năng lực suy luận)**: Khối `Thought` giúp tách biệt quá trình "suy nghĩ/lên kế hoạch" và "hành động". Trong Agent v2 của chúng tôi, việc LLM có bước `Thought` trước khi đưa ra câu trả lời cuối cùng giúp nó xâu chuỗi thông tin tốt hơn, điều chỉnh giọng điệu phù hợp với câu hỏi của người dùng và làm rõ lý do tại sao nó lại gợi ý địa điểm đó.
2. **Reliability (Độ tin cậy)**: Agent có độ tin cậy tuyệt đối về mặt dữ liệu vì nó bị giới hạn (grounded) trong cơ sở dữ liệu `PLACE_DB` đã qua xác minh. Chatbot baseline tuy nói chuyện trôi chảy và nhanh hơn nhưng rất dễ bịa ra tên quán không tồn tại hoặc sai khoảng cách địa lý. Tuy nhiên, Agent lại chịu nhược điểm về thời gian phản hồi (latency cao hơn do phải gọi LLM nhiều lần hoặc qua các bước trung gian) và tốn tài nguyên token hơn.
3. **Observation (Phản hồi môi trường)**: Nhận phản hồi từ công cụ (ví dụ: `ERROR_MISSING_LOCATION` hoặc `NO_RESULTS`) giúp Agent biết chính xác trạng thái của hệ thống để đưa ra hành động tiếp theo (hỏi lại vị trí hoặc đề xuất mở rộng bán kính) thay vì bối rối và trả lời sai lệch.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Khi cơ sở dữ liệu địa điểm tăng lên hàng ngàn quán, ta không thể nhét toàn bộ database vào prompt. Hướng giải quyết là sử dụng **Vector Database (RAG)** để tìm kiếm ngữ nghĩa các địa điểm trước, sau đó chỉ ném top 5-10 địa điểm tiềm năng nhất vào ngữ cảnh cho LLM Agent chọn lọc và tổng hợp.
- **Safety**: Bổ sung cơ chế lọc nội dung độc hại (content moderation) ở cả đầu vào lẫn đầu ra để đảm bảo Agent không phản hồi các nội dung không lành mạnh hoặc bị bẻ khóa prompt (jailbreak) tinh vi hơn.
- **Performance**: Áp dụng kỹ thuật streaming câu trả lời từ LLM ở bước cuối cùng (synthesize) để hiển thị chữ chạy dần trên giao diện chat. Điều này giúp giảm cảm giác chờ đợi của người dùng (perceived latency) xuống dưới 1 giây, mặc dù tổng thời gian sinh câu trả lời vẫn là 5-6 giây.
