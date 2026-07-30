Dưới đây là nội dung của tài liệu `day_1_slide_summary.docx` (được trích xuất từ nguồn `day1.docx`) đã được chuyển đổi sang định dạng Markdown (`.md`):

```markdown
# TÀI LIỆU TÓM TẮT CHUYÊN SÂU: AI & LLM FOUNDATION (Tối ưu hóa cấu trúc cho AI Agent)

*Phát triển dựa trên Nội dung Chương trình Đào tạo AI Thực chiến (Ngày 1)*

## 1. BỨC TRANH AI 2025: TỪ MACHINE LEARNING ĐẾN AGENTIC AI
Xu hướng công nghệ AI năm 2025 đánh dấu bước chuyển mình quan trọng từ việc tối ưu hóa khả năng phản hồi ngôn ngữ thông thường (Generative AI) sang các hệ thống tự động hóa lập kế hoạch và thực thi hành động độc lập (Agentic AI). Doanh nghiệp hiện tại không còn chỉ chú trọng vào câu trả lời 'hay', mà chuyển dịch mạnh mẽ sang AI biết hành động, tích hợp công cụ ngoại vi và tạo ra tỷ suất hoàn vốn đầu tư (ROI) rõ ràng.

**Các chỉ số đo lường hiệu quả ứng dụng AI trong doanh nghiệp tính đến năm 2025:**
- **Tỷ lệ áp dụng:** 78% doanh nghiệp đã chính thức sử dụng AI trong các quy trình nghiệp vụ.
- **Tác động kinh tế:** Dự báo đóng góp 15.7 nghìn tỷ USD (15.7T) vào GDP toàn cầu tính đến năm 2030.
- **Hiệu quả đầu tư (ROI):** Đạt trung bình 3.7 lần (3.7x) trên mỗi 1 USD chi phí đầu tư ban đầu.

**Sơ đồ Phân loại AI (AI Taxonomy) & Trọng tâm học thuật**
Cấu trúc phân tầng của Trí tuệ Nhân tạo được biểu diễn dưới dạng bao hàm từ ngoài vào trong như sau:
- **✦ Artificial Intelligence (AI):** Các hệ thống máy móc có khả năng thực hiện các tác vụ đòi hỏi trí thông minh nhân tạo.
- **✦ Machine Learning (ML):** Các thuật toán học hỏi trực tiếp từ dữ liệu thực tế mà không cần lập trình các quy tắc tường minh.
- **✦ Deep Learning (DL):** Phân nhánh ML sử dụng các mạng nơ-ron nhân tạo nhiều tầng sâu (multi-layered neural networks) để xử lý dữ liệu phức tạp.
- **✦ Foundation Models:** Mô hình nền tảng được huấn luyện trên khối lượng dữ liệu khổng lồ nhằm phục vụ cho đa tác vụ hạ nguồn.
- **✦ Large Language Models (LLM):** Foundation Model chuyên biệt về ngôn ngữ - đóng vai trò là động cơ cốt lõi (Engine) cho cả Generative AI và Agentic AI.

*☞ Trọng tâm phát triển cốt lõi: Xây dựng hệ thống Agentic AI dựa trên nền tảng năng lực suy luận của các mô hình ngôn ngữ lớn (LLM Engine).*

**Phân loại Ba Nhóm AI Chính**

| **Nhóm AI** | **Chức năng Cốt lõi** | **Ví dụ Thực tế & Công thức** |
| ------ | ------ | ------ |
| Discriminative AI (AI Phân loại) | Phân loại dữ liệu, nhận diện mẫu và đưa ra dự đoán dựa trên nhãn học được. | • Công thức: Input → Label<br>• Ví dụ: Spam filter, Image classifier, Fraud detection |
| Generative AI (AI Kiến tạo) | Tạo mới các nội dung văn bản, mã nguồn, hình ảnh hoặc âm thanh dựa trên phân phối xác suất. | • Công thức: Prompt → Content<br>• Ví dụ: ChatGPT, Claude, DALL-E, GitHub Copilot |
| Agentic AI (AI Tác nhân) | Tự động phân tích mục tiêu, tự lập kế hoạch hành động chi tiết và kết nối công cụ ngoại vi để thực hiện. | • Công thức: Goal → Plan → Action<br>• Ví dụ: AI coding agents, Auto customer support, Research agents |

## 2. LLM — TRÁI TIM CỦA AI HIỆN ĐẠI: KIẾN TRÚC, CƠ CHẾ VÀ GIỚI HẠN BẨN SINH
Large Language Model (LLM) là mô hình ngôn ngữ lớn dựa trên kiến trúc Transformer đột phá, được huấn luyện thông qua quá trình tự học có giám sát (Self-supervised pre-training) trên hàng nghìn tỷ tokens dữ liệu văn bản, sau đó được tinh chỉnh bằng các kỹ thuật căn chỉnh phản hồi con người (SFT + RLHF/DPO) để tương tác an toàn và hữu ích.

**Đặc điểm kỹ thuật chính của LLM hiện đại:**
- **Kiến trúc Decoder-only Transformer:** Đọc văn bản từ trái sang phải để dự đoán token tiếp theo một cách tuần tự (Autoregressive). Đây là kiến trúc thắng thế hiện nay nhờ khả năng mở rộng (scaling) vượt trội so với kiến trúc Encoder-Decoder (như BERT, T5).
- **Dự đoán Token tiếp theo (Next-Token Prediction):** LLM không thực sự hiểu nghĩa ngôn ngữ như con người mà tính toán phân phối xác suất của token tiếp theo dựa trên toàn bộ ngữ cảnh đầu vào (Context window).
- **Khả năng đột phá (Emergent Capabilities):** Các năng lực suy luận phức tạp chỉ bắt đầu xuất hiện khi mô hình được mở rộng quy mô (Scale) về số lượng tham số, kích thước tập dữ liệu và năng lực tính toán.

**Cơ chế Core: Self-Attention và Quy trình xử lý của Transformer**
*Sơ đồ luồng xử lý thông tin vật lý của một khối Transformer:*
`Input Tokens ⟶ Embedding + Position Embedding ⟶ Self-Attention Layer (×N) ⟶ Feed-Forward Network (×N) ⟶ Next Token Probability Output`

**Self-Attention** là cơ chế toán học cho phép mô hình gán trọng số liên kết giữa các phần khác nhau của chuỗi đầu vào khi xử lý một token cụ thể. Ví dụ, trong câu 'Con mèo ngồi trên bàn. Nó rất đáng yêu', khi xử lý từ 'Nó', cơ chế Attention sẽ gán trọng số cao nhất cho thực thể 'mèo' thay vì 'bàn', giúp mô hình duy trì ngữ cảnh chuẩn xác.
*Công thức tính toán Attention (Scaled Dot-Product Attention):* **Attention(Q, K, V) = softmax( (Q * Kᵀ) / √d_k ) * V**
Trong đó: Q (Query) là vectơ truy vấn; K (Key) là vectơ khóa; V (Value) là vectơ giá trị; d_k đại diện cho số chiều của không gian vectơ khóa nhằm chuẩn hóa dữ liệu đầu vào.

**Khái niệm về Token và Ngôn ngữ học trong LLM**
Token là đơn vị xử lý ngôn ngữ cơ bản nhất của LLM. Quy trình Tokenization chia nhỏ văn bản thành các phân đoạn subword. Trung bình, 1 token tương đương khoảng 0.75 từ tiếng Anh, nhưng chỉ tương đương khoảng 0.5 từ đối với tiếng Việt. Tiếng Việt tốn nhiều token hơn do đặc thù sử dụng dấu thanh và hệ thống mã hóa ký tự Unicode đa ký tự. Điều này khiến cho chi phí API call của tiếng Việt tăng gấp 1.5 - 2 lần so với cùng một độ dài thông tin bằng tiếng Anh.

**Ba Giai đoạn Huấn luyện Mô hình LLM hoàn chỉnh**
1. **Pre-training (Huấn luyện sơ khởi):** Mô hình đọc và phân tích một lượng lớn văn bản thô từ internet nhằm xây dựng vốn ngôn ngữ, kiến thức tổng quát và khả năng liên kết ngữ cảnh.
2. **Supervised Fine-Tuning - SFT (Tinh chỉnh có giám sát):** Mô hình được huấn luyện dựa trên các bộ dữ liệu dạng cặp câu hỏi - câu trả lời mẫu chất lượng cao để hiểu cách phản hồi theo đúng cấu trúc yêu cầu.
3. **RLHF / DPO (Căn chỉnh phản hồi & Trực tiếp so sánh sở thích):** Sử dụng kỹ thuật học tăng cường từ phản hồi của con người (RLHF) hoặc tối ưu hóa so sánh trực tiếp (DPO) để uốn nắn mô hình hành xử an toàn, trung thực, tránh phản hồi độc hại.

**Các Giới hạn bẩm sinh của LLM**
- **Knowledge Cutoff (Điểm giới hạn tri thức):** Mô hình hoàn toàn không nhận biết được các thông tin, sự kiện xảy ra sau thời điểm hoàn thành huấn luyện trừ khi được cung cấp các công cụ tìm kiếm ngoại vi hoặc kỹ thuật RAG.
- **Hallucination (Sự ảo tưởng/Hiện tượng bịa đặt thông tin):** Mô hình tối ưu hóa dựa trên xác suất chuỗi token tiếp theo chứ không tối ưu hóa dựa trên tính đúng đắn logic của sự thật thực tế, dẫn đến việc đưa ra các tuyên bố sai lệch một cách rất tự tin.
- **Context Window Limits (Giới hạn cửa sổ ngữ cảnh):** Sức chứa bộ nhớ của mô hình trong mỗi phiên làm việc có giới hạn vật lý. Khi ngữ cảnh quá dài, chi phí tăng vọt và mô hình dễ gặp hiện tượng 'Lost in the Middle' (quên mất thông tin nằm ở phần giữa của prompt đầu vào).

## 3. TOKEN ECONOMY: BẢNG SO SÁNH CHI PHÍ VÀ KHUNG CHỌN MÔ HÌNH
Hệ kinh tế Token (Token Economy) quy định cấu trúc chi phí vận hành ứng dụng AI. Chi phí của một API call được tính độc lập dựa trên số lượng Input Tokens (câu hỏi và tài liệu ngữ cảnh gửi đi) và Output Tokens (câu trả lời do mô hình sinh ra). Thông thường, chi phí sinh Output luôn đắt hơn từ 3 đến 5 lần so với chi phí nạp Input.

**Bảng So sánh Chi phí & Cửa sổ Ngữ cảnh các LLM Phổ biến (Dữ liệu Tháng 03/2026)**

| **Tên Mô hình** | **Loại** | **Cửa sổ Ngữ cảnh** | **Giá Input ($/1M)** | **Giá Output ($/1M)** | **Ứng dụng Phù hợp nhất** |
| ------ | ------ | ------ | ------ | ------ | ------ |
| Claude 3.5 Opus (v4.6) | Closed | 1.000.000 tokens | $5.00 | $25.00 | Lập luận phức tạp, lập kế hoạch, code khó |
| Claude 3.5 Sonnet (v4) | Closed | 1.000.000 tokens | $3.00 | $15.00 | Sự lựa chọn cân bằng tốt nhất cho Agent |
| Claude 3.5 Haiku (v4.5) | Closed | 200.000 tokens | $0.80 | $4.00 | Phân loại nhanh, điều phối, độ trễ thấp |
| GPT-4o | Closed | 128.000 tokens | $5.00 | $20.00 | Xử lý đa phương tiện (Multimodal) |
| Gemini 2.5 Pro | Closed | 1.000.000 tokens | $1.25 | $10.00 | Xử lý ngữ cảnh cực dài và tài liệu lớn |
| Llama 4 Scout | Open | 1.000.000 tokens | Free (Self-host) | Free (Self-host) | Hệ thống bảo mật nội bộ, tự host |

**Khung Quyết định Chọn Mô hình (Model Selection Framework)**
Nguyên tắc cốt lõi (Rule of Thumb): Hãy luôn bắt đầu với mô hình ĐỦ TỐT và ĐỦ RẺ. Chỉ nâng cấp lên mô hình cao cấp hơn khi chất lượng của mô hình nhỏ hơn thực sự trở thành nút thắt cổ chai cho bài toán nghiệp vụ.

**1. Ưu tiên tối ưu hóa Chi phí và Độ trễ (Cost/Latency Focus):**
- Các tác vụ: Trả lời FAQ, phân loại dữ liệu, trích xuất thực thể đơn giản, xử lý dữ liệu hàng loạt (Batch jobs).
- Đầu ra yêu cầu độ dài ngắn, không đòi hỏi khả năng tư duy suy luận logic nhiều tầng.
- Mô hình khuyên dùng: Claude Haiku, Gemini Flash hoặc các mô hình mã nguồn mở kích thước nhỏ.

**2. Ưu tiên tối ưu hóa Chất lượng và Lập luận (Quality/Reasoning Focus):**
- Các tác vụ: Phân tích quy trình nhiều bước, lập kế hoạch tự động (Planning), kiểm tra mã nguồn (Debugging/Coding).
- Đầu vào phức tạp, tài liệu ngữ cảnh cực dài hoặc yêu cầu độ tin cậy và chính xác tuyệt đối.
- Mô hình khuyên dùng: Claude Sonnet, Claude Opus, GPT-4o hoặc Gemini Pro.

**Bài toán Tính toán Chi phí Vận hành Thực tế**
**Kịch bản thiết lập:** Xây dựng Chatbot hỗ trợ khách hàng tự động với tần suất vận hành trung bình 1.000 lượt tương tác mỗi ngày.
• Dung lượng Input trung bình: 500 tokens/lượt (bao gồm câu hỏi và ngữ cảnh nạp vào).
• Dung lượng Output trung bình: 200 tokens/lượt (phần nội dung câu trả lời do mô hình sinh ra).

*Kết quả so sánh chi phí vận hành giữa hai phân tầng mô hình khác nhau:*
- **Nếu sử dụng Claude 3.5 Sonnet (v4):**
  • Chi phí Input/ngày: 500.000 tokens × $3.00/1M tokens = $1.50
  • Chi phí Output/ngày: 200.000 tokens × $15.00/1M tokens = $3.00
  • Tổng chi phí: $4.50/ngày ~ $135.00/tháng (Xấp xỉ 3.350.000 VNĐ).
- **Nếu sử dụng Claude 3.5 Haiku (v4.5):**
  • Chi phí Input/ngày: 500.000 tokens × $0.80/1M tokens = $0.40
  • Chi phí Output/ngày: 200.000 tokens × $4.00/1M tokens = $0.80
  • Tổng chi phí: $1.20/ngày ~ $36.00/tháng (Xấp xỉ 900.000 VNĐ).

## 4. QUY TRÌNH GỌI API VÀ CÁC THAM SỐ ĐIỀU KHIỂN ĐẦU RA
**Vòng tuần hoàn đầy đủ của một lượt gọi API (API Call Flow):**
`1. Prompt (System + User Input + Context) ⟶ 2. Gửi API Request ⟶ 3. Nhận Token Stream ⟶ 4. Trả về Response hoàn chỉnh + Số liệu Usage + Stop Reason`

**Các Tham số Tinh chỉnh Quan trọng**
- **Temperature (Độ sáng tạo/Độ ngẫu nhiên):** Nhận giá trị từ 0 đến 1. Thiết lập mức 0 cho các tác vụ đòi hỏi sự ổn định, chính xác tuyệt đối như viết code hoặc phân tích tài chính. Tăng dần lên mức cao (0.7 - 1.0) khi cần sinh nội dung mang tính sáng tạo hoặc đa dạng hóa câu trả lời.
- **Top_p (Nucleus Sampling - Trích chọn nhân xác suất):** Nhận giá trị từ 0 đến 1. Chỉ cho phép mô hình cân nhắc lựa chọn từ các từ vựng tiềm năng có tổng xác suất tích lũy đạt p% (Thường cấu hình mức 0.9 đến 0.95 để giữ sự tự nhiên).
- **Stop Sequences (Chuỗi ký tự ngắt):** Xác định chuỗi văn bản cụ thể mà khi mô hình sinh tới chuỗi này, quá trình tạo từ sẽ lập tức kết thúc. Thường dùng để kiểm soát và định dạng dữ liệu đầu ra có cấu trúc cố định.

**So sánh Cú pháp Gọi API giữa các Provider hàng đầu**

| **Đặc tính** | **Anthropic** | **OpenAI** | **Google Gemini** |
| ------ | ------ | ------ | ------ |
| Hàm gọi chính | messages.create() | chat.completions.create() | generate_content() |
| Cấu hình max_tokens | Bắt buộc (Required) | Tùy chọn (Optional) | Tùy chọn (Optional) |
| Cú pháp truy xuất kết quả | .content.text | .choices.message.content | .text |

## 5. VIBE CODING VÀ TIẾN TRÌNH THỰC HÀNH KỸ THUẬT
**Vibe Coding** là tư duy phát triển phần mềm thế hệ mới: Con người đóng vai trò là 'Đạo diễn AI' thay vì người gõ code thủ công. Tư duy này chuyển dịch trọng tâm công việc từ việc viết từng dòng mã sang định hình mục tiêu hệ thống (Intent-driven), chuẩn bị dữ liệu ngữ cảnh (Context-first) và thẩm định kết quả (Human review).

*Ba Nguyên tắc Vàng của Vibe Coding:*
1. **Intent-driven (Định hình mục tiêu rõ ràng):** Mô tả chuẩn xác kết quả đầu ra mong muốn, đặt ra các tiêu chuẩn nghiệm thu và chỉ số đánh giá thành công cụ thể trước khi yêu cầu AI viết code.
2. **Context-first (Cung cấp ngữ cảnh đầy đủ):** Luôn nạp đầy đủ cấu trúc thư mục, tệp tin định cấu hình, các ràng buộc kỹ thuật của dự án cũng như lịch sử thông báo lỗi chi tiết để AI hiểu sâu sắc thực trạng hệ thống.
3. **Human review (Con người chịu trách nhiệm kiểm duyệt):** AI có tốc độ tạo lập mã nguồn nhanh chóng, nhưng con người bắt buộc phải là lớp phòng vệ cuối cùng để kiểm tra tính logic, độ an toàn và bấm nút vận hành chính thức.

**Lab Thực hành Thực chiến #1: Xây dựng Chatbot Đa kết nối**
- **Mục tiêu bài Lab:** Thực hiện kết nối trực tiếp đến 3 nhà cung cấp API lớn (Anthropic, OpenAI, Google Gemini) để viết một chương trình chatbot chạy trực tiếp trên Terminal có hỗ trợ Streaming phản hồi dữ liệu thời gian thực và đo lường độ trễ (latency) thực tế.
- **Môi trường chuẩn bị:** Cài đặt Python 3.10+, VS Code/Cursor IDE, thiết lập biến môi trường API keys cho cả 3 nền tảng.
- **Tiến trình triển khai:**
  1. Tạo môi trường ảo: `python -m venv .venv` và kích hoạt.
  2. Cài đặt các thư viện lõi: `pip install anthropic openai google-generativeai`.
  3. Triển khai cấu trúc script gọi API đồng thời từ 3 providers.
  4. Thực hiện so sánh hiệu quả về mặt: Latency, Cost và Quality dựa trên 3 prompts thử nghiệm khác nhau.

## 6. TÀI LIỆU THAM KHẢO & LIÊN KẾT NGUỒN CỐT LÕI
Các liên kết tài liệu nghiên cứu khoa học và tài nguyên chuẩn hóa phục vụ huấn luyện Agent đọc học máy sâu sắc:
- **■ Vaswani et al. (2017) — 'Attention Is All You Need':** Nghiên cứu nền tảng khai sinh ra kiến trúc Transformer thay đổi toàn bộ thế giới AI (Link bài báo khoa học: arXiv:1706.03762).
- **■ Ouyang et al. (2022) — 'InstructGPT / RLHF':** Phương pháp tối ưu hóa hành vi mô hình dựa trên phản hồi của con người (Link bài báo khoa học: arXiv:2203.02155).
- **■ Rafailov et al. (2023) — 'Direct Preference Optimization (DPO)':** Phương pháp căn chỉnh trực tiếp sở thích bỏ qua bước huấn luyện mô hình phần thưởng phức tạp của RLHF (Link bài báo khoa học: arXiv:2305.18290).
- **■ Andrej Karpathy (2023) — 'State of GPT':** Bài thuyết giảng chuẩn hóa quy trình huấn luyện và vận hành mô hình ngôn ngữ lớn từ chuyên gia AI hàng đầu.
- **■ Công cụ Tokenizer của OpenAI:** Công cụ hỗ trợ phân tách và tính toán số lượng tokens trực quan thực tế (platform.openai.com/tokenizer).
- **■ Anthropic API / OpenAI API / Google AI Studio Quickstarts:** Hệ thống tài liệu hướng dẫn gọi API chính thức từ các nhà cung cấp dịch vụ mô hình lớn hàng đầu.
```