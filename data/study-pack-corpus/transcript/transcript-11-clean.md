# Study Pack corpus - Day 01 - AI & LLM Foundation

> Corpus version: `study-pack-corpus-v1`
> Combined source SHA-256: `d9ff0da80192992871546bbffaf0f79567c061d3be189272d715a0811f1055a2`
> Original source lines: 162-314
> Transformation: one non-empty source line equals one citation segment;
> no source text is summarized, paraphrased, or silently truncated.

**[T11-001]** [Day-01]TÀI LIỆU TÓM TẮT CHUYÊN SÂU: AI & LLM FOUNDATION(Tối ưu hóa cấu trúc cho AI Agent)

**[T11-002]** Phát triển dựa trên Nội dung Chương trình Đào tạo AI Thực chiến (Ngày 1)

**[T11-003]** 1. BỨC TRANH AI 2025: TỪ MACHINE LEARNING ĐẾN AGENTIC AI

**[T11-004]** Xu hướng công nghệ AI năm 2025 đánh dấu bước chuyển mình quan trọng từ việc tối ưu hóa khả năng phản hồi ngôn ngữ thông thường (Generative AI) sang các hệ thống tự động hóa lập kế hoạch và thực thi hành động độc lập (Agentic AI). Doanh nghiệp hiện tại không còn chỉ chú trọng vào câu trả lời 'hay', mà chuyển dịch mạnh mẽ sang AI biết hành động, tích hợp công cụ ngoại vi và tạo ra tỷ suất hoàn vốn đầu tư (ROI) rõ ràng.

**[T11-005]** Các chỉ số đo lường hiệu quả ứng dụng AI trong doanh nghiệp tính đến năm 2025:

**[T11-006]** Tỷ lệ áp dụng: 78% doanh nghiệp đã chính thức sử dụng AI trong các quy trình nghiệp vụ.

**[T11-007]** Tác động kinh tế: Dự báo đóng góp 15.7 nghìn tỷ USD (15.7T) vào GDP toàn cầu tính đến năm 2030.

**[T11-008]** Hiệu quả đầu tư (ROI): Đạt trung bình 3.7 lần (3.7x) trên mỗi 1 USD chi phí đầu tư ban đầu.

**[T11-009]** Sơ đồ Phân loại AI (AI Taxonomy) & Trọng tâm học thuật

**[T11-010]** Cấu trúc phân tầng của Trí tuệ Nhân tạo được biểu diễn dưới dạng bao hàm từ ngoài vào trong như sau:

**[T11-011]** ✦ Artificial Intelligence (AI): Các hệ thống máy móc có khả năng thực hiện các tác vụ đòi hỏi trí thông minh nhân tạo.

**[T11-012]** ✦ Machine Learning (ML): Các thuật toán học hỏi trực tiếp từ dữ liệu thực tế mà không cần lập trình các quy tắc tường minh.

**[T11-013]** ✦ Deep Learning (DL): Phân nhánh ML sử dụng các mạng nơ-ron nhân tạo nhiều tầng sâu (multi-layered neural networks) để xử lý dữ liệu phức tạp.

**[T11-014]** ✦ Foundation Models: Mô hình nền tảng được huấn luyện trên khối lượng dữ liệu khổng lồ nhằm phục vụ cho đa tác vụ hạ nguồn.

**[T11-015]** ✦ Large Language Models (LLM): Foundation Model chuyên biệt về ngôn ngữ - đóng vai trò là động cơ cốt lõi (Engine) cho cả Generative AI và Agentic AI.

**[T11-016]** ☞ Trọng tâm phát triển cốt lõi: Xây dựng hệ thống Agentic AI dựa trên nền tảng năng lực suy luận của các mô hình ngôn ngữ lớn (LLM Engine).

**[T11-017]** Phân loại Ba Nhóm AI Chính

**[T11-018]** Nhóm AI

**[T11-019]** Chức năng Cốt lõi

**[T11-020]** Ví dụ Thực tế & Công thức

**[T11-021]** Discriminative AI (AI Phân loại)

**[T11-022]** Phân loại dữ liệu, nhận diện mẫu và đưa ra dự đoán dựa trên nhãn học được.

**[T11-023]** • Công thức: Input → Label• Ví dụ: Spam filter, Image classifier, Fraud detection

**[T11-024]** Generative AI (AI Kiến tạo)

**[T11-025]** Tạo mới các nội dung văn bản, mã nguồn, hình ảnh hoặc âm thanh dựa trên phân phối xác suất.

**[T11-026]** • Công thức: Prompt → Content• Ví dụ: ChatGPT, Claude, DALL-E, GitHub Copilot

**[T11-027]** Agentic AI (AI Tác nhân)

**[T11-028]** Tự động phân tích mục tiêu, tự lập kế hoạch hành động chi tiết và kết nối công cụ ngoại vi để thực hiện.

**[T11-029]** • Công thức: Goal → Plan → Action• Ví dụ: AI coding agents, Auto customer support, Research agents

**[T11-030]** 2. LLM — TRÁI TIM CỦA AI HIỆN ĐẠI: KIẾN TRÚC, CƠ CHẾ VÀ GIỚI HẠN BẨN SINH

**[T11-031]** Large Language Model (LLM) là mô hình ngôn ngữ lớn dựa trên kiến trúc Transformer đột phá, được huấn luyện thông qua quá trình tự học có giám sát (Self-supervised pre-training) trên hàng nghìn tỷ tokens dữ liệu văn bản, sau đó được tinh chỉnh bằng các kỹ thuật căn chỉnh phản hồi con người (SFT + RLHF/DPO) để tương tác an toàn và hữu ích.

**[T11-032]** Đặc điểm kỹ thuật chính của LLM hiện đại:

**[T11-033]** Kiến trúc Decoder-only Transformer: Đọc văn bản từ trái sang phải để dự đoán token tiếp theo một cách tuần tự (Autoregressive). Đây là kiến trúc thắng thế hiện nay nhờ khả năng mở rộng (scaling) vượt trội so với kiến trúc Encoder-Decoder (như BERT, T5).

**[T11-034]** Dự đoán Token tiếp theo (Next-Token Prediction): LLM không thực sự hiểu nghĩa ngôn ngữ như con người mà tính toán phân phối xác suất của token tiếp theo dựa trên toàn bộ ngữ cảnh đầu vào (Context window).

**[T11-035]** Khả năng đột phá (Emergent Capabilities): Các năng lực suy luận phức tạp chỉ bắt đầu xuất hiện khi mô hình được mở rộng quy mô (Scale) về số lượng tham số, kích thước tập dữ liệu và năng lực tính toán.

**[T11-036]** Cơ chế Core: Self-Attention và Quy trình xử lý của Transformer

**[T11-037]** Sơ đồ luồng xử lý thông tin vật lý của một khối Transformer:

**[T11-038]** Input Tokens ⟶ Embedding + Position Embedding ⟶ Self-Attention Layer (×N) ⟶ Feed-Forward Network (×N) ⟶ Next Token Probability Output

**[T11-039]** Self-Attention là cơ chế toán học cho phép mô hình gán trọng số liên kết giữa các phần khác nhau của chuỗi đầu vào khi xử lý một token cụ thể. Ví dụ, trong câu 'Con mèo ngồi trên bàn. Nó rất đáng yêu', khi xử lý từ 'Nó', cơ chế Attention sẽ gán trọng số cao nhất cho thực thể 'mèo' thay vì 'bàn', giúp mô hình duy trì ngữ cảnh chuẩn xác.

**[T11-040]** Công thức tính toán Attention (Scaled Dot-Product Attention):Attention(Q, K, V) = softmax( (Q * Kᵀ) / √d_k ) * V

**[T11-041]** Trong đó: Q (Query) là vectơ truy vấn; K (Key) là vectơ khóa; V (Value) là vectơ giá trị; d_k đại diện cho số chiều của không gian vectơ khóa nhằm chuẩn hóa dữ liệu đầu vào.

**[T11-042]** Khái niệm về Token và Ngôn ngữ học trong LLM

**[T11-043]** Token là đơn vị xử lý ngôn ngữ cơ bản nhất của LLM. Quy trình Tokenization chia nhỏ văn bản thành các phân đoạn subword. Trung bình, 1 token tương đương khoảng 0.75 từ tiếng Anh, nhưng chỉ tương đương khoảng 0.5 từ đối với tiếng Việt. Tiếng Việt tốn nhiều token hơn do đặc thù sử dụng dấu thanh và hệ thống mã hóa ký tự Unicode đa ký tự. Điều này khiến cho chi phí API call của tiếng Việt tăng gấp 1.5 - 2 lần so với cùng một độ dài thông tin bằng tiếng Anh.

**[T11-044]** Ba Giai đoạn Huấn luyện Mô hình LLM hoàn chỉnh

**[T11-045]** 1. Pre-training (Huấn luyện sơ khởi): Mô hình đọc và phân tích một lượng lớn văn bản thô từ internet nhằm xây dựng vốn ngôn ngữ, kiến thức tổng quát và khả năng liên kết ngữ cảnh.

**[T11-046]** 2. Supervised Fine-Tuning - SFT (Tinh chỉnh có giám sát): Mô hình được huấn luyện dựa trên các bộ dữ liệu dạng cặp câu hỏi - câu trả lời mẫu chất lượng cao để hiểu cách phản hồi theo đúng cấu trúc yêu cầu.

**[T11-047]** 3. RLHF / DPO (Căn chỉnh phản hồi & Trực tiếp so sánh sở thích): Sử dụng kỹ thuật học tăng cường từ phản hồi của con người (RLHF) hoặc tối ưu hóa so sánh trực tiếp (DPO) để uốn nắn mô hình hành xử an toàn, trung thực, tránh phản hồi độc hại.

**[T11-048]** Các Giới hạn bẩm sinh của LLM

**[T11-049]** Knowledge Cutoff (Điểm giới hạn tri thức): Mô hình hoàn toàn không nhận biết được các thông tin, sự kiện xảy ra sau thời điểm hoàn thành huấn luyện trừ khi được cung cấp các công cụ tìm kiếm ngoại vi hoặc kỹ thuật RAG.

**[T11-050]** Hallucination (Sự ảo tưởng/Hiện tượng bịa đặt thông tin): Mô hình tối ưu hóa dựa trên xác suất chuỗi token tiếp theo chứ không tối ưu hóa dựa trên tính đúng đắn logic của sự thật thực tế, dẫn đến việc đưa ra các tuyên bố sai lệch một cách rất tự tin.

**[T11-051]** Context Window Limits (Giới hạn cửa sổ ngữ cảnh): Sức chứa bộ nhớ của mô hình trong mỗi phiên làm việc có giới hạn vật lý. Khi ngữ cảnh quá dài, chi phí tăng vọt và mô hình dễ gặp hiện tượng 'Lost in the Middle' (quên mất thông tin nằm ở phần giữa của prompt đầu vào).

**[T11-052]** 3. TOKEN ECONOMY: BẢNG SO SÁNH CHI PHÍ VÀ KHUNG CHỌN MÔ HÌNH

**[T11-053]** Hệ kinh tế Token (Token Economy) quy định cấu trúc chi phí vận hành ứng dụng AI. Chi phí của một API call được tính độc lập dựa trên số lượng Input Tokens (câu hỏi và tài liệu ngữ cảnh gửi đi) và Output Tokens (câu trả lời do mô hình sinh ra). Thông thường, chi phí sinh Output luôn đắt hơn từ 3 đến 5 lần so với chi phí nạp Input.

**[T11-054]** Bảng So sánh Chi phí & Cửa sổ Ngữ cảnh các LLM Phổ biến (Dữ liệu Tháng 03/2026)

**[T11-055]** Tên Mô hình

**[T11-056]** Loại

**[T11-057]** Cửa sổ Ngữ cảnh

**[T11-058]** Giá Input ($/1M)

**[T11-059]** Giá Output ($/1M)

**[T11-060]** Ứng dụng Phù hợp nhất

**[T11-061]** Claude 3.5 Opus (v4.6)

**[T11-062]** Closed

**[T11-063]** 1.000.000 tokens

**[T11-064]** $5.00

**[T11-065]** $25.00

**[T11-066]** Lập luận phức tạp, lập kế hoạch, code khó

**[T11-067]** Claude 3.5 Sonnet (v4)

**[T11-068]** Closed

**[T11-069]** 1.000.000 tokens

**[T11-070]** $3.00

**[T11-071]** $15.00

**[T11-072]** Sự lựa chọn cân bằng tốt nhất cho Agent

**[T11-073]** Claude 3.5 Haiku (v4.5)

**[T11-074]** Closed

**[T11-075]** 200.000 tokens

**[T11-076]** $0.80

**[T11-077]** $4.00

**[T11-078]** Phân loại nhanh, điều phối, độ trễ thấp

**[T11-079]** GPT-4o

**[T11-080]** Closed

**[T11-081]** 128.000 tokens

**[T11-082]** $5.00

**[T11-083]** $20.00

**[T11-084]** Xử lý đa phương tiện (Multimodal)

**[T11-085]** Gemini 2.5 Pro

**[T11-086]** Closed

**[T11-087]** 1.000.000 tokens

**[T11-088]** $1.25

**[T11-089]** $10.00

**[T11-090]** Xử lý ngữ cảnh cực dài và tài liệu lớn

**[T11-091]** Llama 4 Scout

**[T11-092]** Open

**[T11-093]** 1.000.000 tokens

**[T11-094]** Free (Self-host)

**[T11-095]** Free (Self-host)

**[T11-096]** Hệ thống bảo mật nội bộ, tự host

**[T11-097]** Khung Quyết định Chọn Mô hình (Model Selection Framework)

**[T11-098]** Nguyên tắc cốt lõi (Rule of Thumb): Hãy luôn bắt đầu với mô hình ĐỦ TỐT và ĐỦ RẺ. Chỉ nâng cấp lên mô hình cao cấp hơn khi chất lượng của mô hình nhỏ hơn thực sự trở thành nút thắt cổ chai cho bài toán nghiệp vụ.

**[T11-099]** 1. Ưu tiên tối ưu hóa Chi phí và Độ trễ (Cost/Latency Focus):

**[T11-100]** Các tác vụ: Trả lời FAQ, phân loại dữ liệu, trích xuất thực thể đơn giản, xử lý dữ liệu hàng loạt (Batch jobs).

**[T11-101]** Đầu ra yêu cầu độ dài ngắn, không đòi hỏi khả năng tư duy suy luận logic nhiều tầng.

**[T11-102]** Mô hình khuyên dùng: Claude Haiku, Gemini Flash hoặc các mô hình mã nguồn mở kích thước nhỏ.

**[T11-103]** 2. Ưu tiên tối ưu hóa Chất lượng và Lập luận (Quality/Reasoning Focus):

**[T11-104]** Các tác vụ: Phân tích quy trình nhiều bước, lập kế hoạch tự động (Planning), kiểm tra mã nguồn (Debugging/Coding).

**[T11-105]** Đầu vào phức tạp, tài liệu ngữ cảnh cực dài hoặc yêu cầu độ tin cậy và chính xác tuyệt đối.

**[T11-106]** Mô hình khuyên dùng: Claude Sonnet, Claude Opus, GPT-4o hoặc Gemini Pro.

**[T11-107]** Bài toán Tính toán Chi phí Vận hành Thực tế

**[T11-108]** Kịch bản thiết lập: Xây dựng Chatbot hỗ trợ khách hàng tự động với tần suất vận hành trung bình 1.000 lượt tương tác mỗi ngày.• Dung lượng Input trung bình: 500 tokens/lượt (bao gồm câu hỏi và ngữ cảnh nạp vào).• Dung lượng Output trung bình: 200 tokens/lượt (phần nội dung câu trả lời do mô hình sinh ra).

**[T11-109]** Kết quả so sánh chi phí vận hành giữa hai phân tầng mô hình khác nhau:

**[T11-110]** Nếu sử dụng Claude 3.5 Sonnet (v4):• Chi phí Input/ngày: 500.000 tokens × $3.00/1M tokens = $1.50• Chi phí Output/ngày: 200.000 tokens × $15.00/1M tokens = $3.00• Tổng chi phí: $4.50/ngày ~ $135.00/tháng (Xấp xỉ 3.350.000 VNĐ).

**[T11-111]** Nếu sử dụng Claude 3.5 Haiku (v4.5):• Chi phí Input/ngày: 500.000 tokens × $0.80/1M tokens = $0.40• Chi phí Output/ngày: 200.000 tokens × $4.00/1M tokens = $0.80• Tổng chi phí: $1.20/ngày ~ $36.00/tháng (Xấp xỉ 900.000 VNĐ).

**[T11-112]** 4. QUY TRÌNH GỌI API VÀ CÁC THAM SỐ ĐIỀU KHIỂN ĐẦU RA

**[T11-113]** Vòng tuần hoàn đầy đủ của một lượt gọi API (API Call Flow):

**[T11-114]** 1. Prompt (System + User Input + Context) ⟶ 2. Gửi API Request ⟶ 3. Nhận Token Stream ⟶ 4. Trả về Response hoàn chỉnh + Số liệu Usage + Stop Reason

**[T11-115]** Các Tham số Tinh chỉnh Quan trọng

**[T11-116]** Temperature (Độ sáng tạo/Độ ngẫu nhiên): Nhận giá trị từ 0 đến 1. Thiết lập mức 0 cho các tác vụ đòi hỏi sự ổn định, chính xác tuyệt đối như viết code hoặc phân tích tài chính. Tăng dần lên mức cao (0.7 - 1.0) khi cần sinh nội dung mang tính sáng tạo hoặc đa dạng hóa câu trả lời.

**[T11-117]** Top_p (Nucleus Sampling - Trích chọn nhân xác suất): Nhận giá trị từ 0 đến 1. Chỉ cho phép mô hình cân nhắc lựa chọn từ các từ vựng tiềm năng có tổng xác suất tích lũy đạt p% (Thường cấu hình mức 0.9 đến 0.95 để giữ sự tự nhiên).

**[T11-118]** Stop Sequences (Chuỗi ký tự ngắt): Xác định chuỗi văn bản cụ thể mà khi mô hình sinh tới chuỗi này, quá trình tạo từ sẽ lập tức kết thúc. Thường dùng để kiểm soát và định dạng dữ liệu đầu ra có cấu trúc cố định.

**[T11-119]** So sánh Cú pháp Gọi API giữa các Provider hàng đầu

**[T11-120]** Đặc tính

**[T11-121]** Anthropic

**[T11-122]** OpenAI

**[T11-123]** Google Gemini

**[T11-124]** Hàm gọi chính

**[T11-125]** messages.create()

**[T11-126]** chat.completions.create()

**[T11-127]** generate_content()

**[T11-128]** Cấu hình max_tokens

**[T11-129]** Bắt buộc (Required)

**[T11-130]** Tùy chọn (Optional)

**[T11-131]** Tùy chọn (Optional)

**[T11-132]** Cú pháp truy xuất kết quả

**[T11-133]** .content[0].text

**[T11-134]** .choices[0].message.content

**[T11-135]** .text

**[T11-136]** 5. VIBE CODING VÀ TIẾN TRÌNH THỰC HÀNH KỸ THUẬT

**[T11-137]** Vibe Coding là tư duy phát triển phần mềm thế hệ mới: Con người đóng vai trò là 'Đạo diễn AI' thay vì người gõ code thủ công. Tư duy này chuyển dịch trọng tâm công việc từ việc viết từng dòng mã sang định hình mục tiêu hệ thống (Intent-driven), chuẩn bị dữ liệu ngữ cảnh (Context-first) và thẩm định kết quả (Human review).

**[T11-138]** Ba Nguyên tắc Vàng của Vibe Coding:

**[T11-139]** Intent-driven (Định hình mục tiêu rõ ràng): Mô tả chuẩn xác kết quả đầu ra mong muốn, đặt ra các tiêu chuẩn nghiệm thu và chỉ số đánh giá thành công cụ thể trước khi yêu cầu AI viết code.

**[T11-140]** Context-first (Cung cấp ngữ cảnh đầy đủ): Luôn nạp đầy đủ cấu trúc thư mục, tệp tin định cấu hình, các ràng buộc kỹ thuật của dự án cũng như lịch sử thông báo lỗi chi tiết để AI hiểu sâu sắc thực trạng hệ thống.

**[T11-141]** Human review (Con người chịu trách nhiệm kiểm duyệt): AI có tốc độ tạo lập mã nguồn nhanh chóng, nhưng con người bắt buộc phải là lớp phòng vệ cuối cùng để kiểm tra tính logic, độ an toàn và bấm nút vận hành chính thức.

**[T11-142]** Lab Thực hành Thực chiến #1: Xây dựng Chatbot Đa kết nối

**[T11-143]** Mục tiêu bài Lab: Thực hiện kết nối trực tiếp đến 3 nhà cung cấp API lớn (Anthropic, OpenAI, Google Gemini) để viết một chương trình chatbot chạy trực tiếp trên Terminal có hỗ trợ Streaming phản hồi dữ liệu thời gian thực và đo lường độ trễ (latency) thực tế.

**[T11-144]** Môi trường chuẩn bị: Cài đặt Python 3.10+, VS Code/Cursor IDE, thiết lập biến môi trường API keys cho cả 3 nền tảng.

**[T11-145]** Tiến trình triển khai:

**[T11-146]** 1. Tạo môi trường ảo: python -m venv .venv và kích hoạt.

**[T11-147]** 2. Cài đặt các thư viện lõi: pip install anthropic openai google-generativeai.

**[T11-148]** 3. Triển khai cấu trúc script gọi API đồng thời từ 3 providers.

**[T11-149]** 4. Thực hiện so sánh hiệu quả về mặt: Latency, Cost và Quality dựa trên 3 prompts thử nghiệm khác nhau.
