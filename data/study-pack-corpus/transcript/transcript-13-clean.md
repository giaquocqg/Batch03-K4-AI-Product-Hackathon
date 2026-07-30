# Study Pack corpus - Day 03 - Agentic AI và ReAct

> Corpus version: `study-pack-corpus-v1`
> Combined source SHA-256: `d9ff0da80192992871546bbffaf0f79567c061d3be189272d715a0811f1055a2`
> Original source lines: 478-677
> Transformation: one non-empty source line equals one citation segment;
> no source text is summarized, paraphrased, or silently truncated.

**[T13-001]** [Day-03]XÂY DỰNG HỆ THỐNG AGENTIC AI & MẪU THIẾT KẾ REACT

**[T13-002]** Tài liệu Tóm tắt Chuyên sâu và Hệ thống hóa Kiến thức Ngày 3 (Design Pattern ReAct)Tối ưu hóa cấu trúc dữ liệu cho AI Agent đọc hiểu

**[T13-003]** MỤC TIÊU VÀ ĐỊNH HƯỚNG TÀI LIỆUTài liệu này tổng hợp toàn bộ nội dung lý thuyết, khung đánh giá thực chiến, kiến trúc kỹ thuật và hướng dẫn lập trình vòng lặp ReAct Agent. Nội dung được trích xuất hoàn chỉnh từ chương trình Đào tạo AI Thực chiến (AICB-P1) của VinUniversity. Mọi thông tin cá nhân và quảng cáo không liên quan của giảng viên đã được lược bỏ để đảm bảo tính cô đọng tối đa, sẵn sàng làm tài nguyên dữ liệu tham chiếu hiệu năng cao cho các hệ thống AI Agent khác.

**[T13-004]** MỤC LỤC TỰ ĐỘNG

**[T13-005]** Danh mục các đề mục chính trong tài liệu. Người đọc có thể cập nhật mục lục này trực tiếp bằng cách nhấn chuột phải vào vùng mục lục trong Microsoft Word hoặc Google Docs và chọn 'Update Field'.

**[T13-006]** 1. PHÂN LOẠI BA KIỂU HỆ THỐNG AI TRONG THỰC TẾ

**[T13-007]** Mô hình phổ phát triển AI (AI Spectrum): Sự tiến hóa của các hệ thống AI từ dạng bot tĩnh có quy tắc cứng đến các tác nhân tự chủ có khả năng lập kế hoạch dài hạn được biểu diễn qua một phổ phát triển (Spectrum): Rule-based Bot → LLM Chatbot → Reactive Agent → Autonomous Agent. Khả năng thích nghi, khả năng sử dụng công cụ, dung lượng bộ nhớ và mức độ rủi ro tăng dần theo chiều tiến hóa này.

**[T13-008]** • Rule-based Bot: Hoạt động dựa trên các cấu trúc điều kiện if/else cứng nhắc, có tính chất dự đoán tuyệt đối (predictable) nhưng không linh hoạt.

**[T13-009]** • LLM Chatbot: Có khả năng sinh câu trả lời thông minh, linh hoạt theo ngữ cảnh, nhưng chủ yếu hoạt động theo cơ chế tương tác một lượt (single-turn).

**[T13-010]** • Reactive Agent: Sử dụng các công cụ bên ngoài kết hợp với vòng lặp quan sát (observe-loop) để thực thi hành động theo từng bước phản hồi.

**[T13-011]** • Autonomous Agent: Định hướng mục tiêu dài hạn (long-horizon goal), có khả năng đưa ra chuỗi nhiều quyết định liên tiếp một cách tự chủ.

**[T13-012]** ĐỊNH NGHĨA CỐT LÕI VỀ AGENTNguyên tắc phân định Agent: Không phải mọi hệ thống sử dụng Mô hình ngôn ngữ lớn (LLM) đều được coi là một Agent. Agent thực sự chỉ xuất hiện khi hệ thống có khả năng tự đưa ra quyết định, thực thi hành động, quan sát kết quả phản hồi từ môi trường, và lặp lại vòng lặp này để đạt mục tiêu.

**[T13-013]** Bảng So Sánh Chi Tiết Ba Kiểu Hệ Thống AI

**[T13-014]** Tiêu chí

**[T13-015]** Rule-based Bot

**[T13-016]** LLM Chatbot

**[T13-017]** Agent

**[T13-018]** Cách xử lý

**[T13-019]** Cấu trúc If/else cố định

**[T13-020]** Sinh câu trả lời thông minh theo context

**[T13-021]** Chu trình: Plan -> Act -> Observe -> Adapt

**[T13-022]** Sự linh hoạt (Flexibility)

**[T13-023]** Rất thấp

**[T13-024]** Trung bình

**[T13-025]** Cao

**[T13-026]** Bộ nhớ (Memory)

**[T13-027]** Gần như không có

**[T13-028]** Ngắn hạn (trong context window)

**[T13-029]** Ngắn hạn + Bộ nhớ dài hạn (Long-term memory)

**[T13-030]** Sử dụng công cụ (Tool use)

**[T13-031]** Hard-coded (tích hợp cứng)

**[T13-032]** Có thể gọi công cụ theo chỉ định sẵn

**[T13-033]** Chủ động lựa chọn công cụ phù hợp bước tiếp theo

**[T13-034]** Chi phí (Cost)

**[T13-035]** Thấp nhất

**[T13-036]** Trung bình

**[T13-037]** Cao hơn đáng kể (do vòng lặp và nhiều lượt gọi LLM)

**[T13-038]** Rủi ro (Risk)

**[T13-039]** Dễ kiểm soát logic

**[T13-040]** Ảo tưởng (Hallucination) / Trôi lệch định dạng

**[T13-041]** Ảo tưởng + Lạm dụng công cụ + Lặp vô hạn (Loop)

**[T13-042]** Ví dụ thực tế phù hợp

**[T13-043]** Menu IVR điện thoại, biểu mẫu xác thực dữ liệu

**[T13-044]** Hệ thống hỏi đáp FAQ, hỗ trợ khách hàng cơ bản

**[T13-045]** Hệ thống đặt chỗ (Booking), nghiên cứu (Research), trợ lý code

**[T13-046]** Bảng 1: So sánh đặc tính vận hành giữa Rule-based Bot, LLM Chatbot và AI Agent

**[T13-047]** Ví Dụ Thực Nghiệm So Sánh Qua Cùng Một Câu Hỏi

**[T13-048]** Tình huống thực tế: Để làm rõ sự khác biệt trong năng lực xử lý, hãy xem xét bài toán yêu cầu: 'Tìm vé máy bay từ Hà Nội (HAN) đi TP. Hồ Chí Minh (HCM) dưới 2 triệu đồng, sau đó gợi ý hành lý mang theo nếu dự báo có mưa'.

**[T13-049]** 1. Rule-based Bot: Chỉ hiển thị một danh mục lựa chọn cố định (menu tĩnh); không thể truy vấn thông tin mới tại thời điểm thực tế; không có khả năng tổng hợp nhiều điều kiện phức tạp cùng lúc.

**[T13-050]** 2. LLM Chatbot: Có khả năng viết câu trả lời rất trôi chảy, mượt mà về mặt ngôn ngữ; tuy nhiên, hệ thống không thể tự động kết nối và thực hiện truy vấn cơ sở dữ liệu thật để kiểm tra giá vé thực tế tại thời điểm hỏi.

**[T13-051]** 3. Reactive Agent: Tự động phân tách mục tiêu lớn thành hai nhiệm vụ con độc lập: (1) Gọi công cụ tìm kiếm vé máy bay trực tuyến để truy vấn giá vé thực tế, và (2) Gọi công cụ thời tiết để kiểm tra khả năng mưa. Sau đó, Agent tổng hợp dữ liệu, so sánh giá, đối chiếu điều kiện thời tiết và trả về câu trả lời tối ưu tích hợp.

**[T13-052]** LƯU Ý QUAN TRỌNG KHI TRIỂN KHAIKhuyến nghị thiết kế: Nếu bài toán nghiệp vụ không đòi hỏi tích hợp dữ liệu thời gian thực, không yêu cầu thực thi chuỗi nhiều bước phức tạp, hoặc không cần đưa ra các quyết định động dựa trên kết quả phản hồi, việc triển khai hệ thống Agent là một sự lãng phí tài nguyên và chi phí không cần thiết (Overkill).

**[T13-053]** 2. KHUNG ĐÁNH GIÁ ĐỘ PHÙ HỢP AGENTIC FIT (AGENTIC FIT FRAMEWORK)

**[T13-054]** Khái niệm: Agentic Fit Framework cung cấp một tập hợp các tiêu chí và ma trận chấm điểm khoa học nhằm giúp các kỹ sư hệ thống xác định chính xác liệu bài toán nghiệp vụ hiện tại có thực sự cần nâng cấp lên kiến trúc Agent hay không.

**[T13-055]** 4 Tiêu Chí Cốt Lõi Xác Định Agentic Fit

**[T13-056]** 1. Multi-step Reasoning (Suy luận nhiều bước): Bài toán có đòi hỏi việc chia nhỏ thành nhiều bước trung gian phụ thuộc lẫn nhau để giải quyết hay không?

**[T13-057]** 2. Tool Interaction (Tương tác công cụ): Hệ thống có cần tương tác trực tiếp với các công cụ bên ngoài như công cụ tìm kiếm (Search), API bên thứ ba, cơ sở dữ liệu (Database), máy tính (Calculator), trình duyệt web (Browser), hoặc hệ thống tệp tin (File system) hay không?

**[T13-058]** 3. Dynamic Decision (Quyết định động): Mỗi bước hành động tiếp theo của hệ thống có phụ thuộc chặt chẽ vào kết quả quan sát (observation) thu được từ bước hành động ngay trước đó hay không?

**[T13-059]** 4. Long Horizon (Tầm nhìn dài hạn): Hệ thống có cần phải duy trì, bảo toàn mục tiêu cốt lõi xuyên suốt một chuỗi nhiều vòng lặp tương tác hoặc qua nhiều trạng thái (state) phức tạp khác nhau hay không?

**[T13-060]** Ma Trận Chấm Điểm Thang Đo Quyết Định

**[T13-061]** Quy tắc đánh giá: Mỗi tiêu chí được đánh giá theo thang điểm từ 1 đến 5 (với 1 là mức độ đơn giản nhất, 5 là phức tạp nhất). Tổng số điểm của 3 tiêu chí chính (Reasoning, Tool Use, Dynamic Decision) sẽ định hướng kiến trúc hệ thống phù hợp.

**[T13-062]** Nghiệp vụ ứng dụng (Use Case)

**[T13-063]** Reasoning

**[T13-064]** Tool Use

**[T13-065]** Dynamic Decision

**[T13-066]** Tổng điểm

**[T13-067]** Hỏi đáp FAQ nội bộ bộ phận Nhân sự (HR FAQ)

**[T13-068]** 1

**[T13-069]** 1

**[T13-070]** 1

**[T13-071]** 3

**[T13-072]** Tóm tắt hợp đồng kinh tế và cảnh báo rủi ro (Risk Highlight)

**[T13-073]** 3

**[T13-074]** 2

**[T13-075]** 2

**[T13-076]** 7

**[T13-077]** Trợ lý hỗ trợ đặt lịch trình du lịch tự động (Booking Assistant)

**[T13-078]** 4

**[T13-079]** 5

**[T13-080]** 4

**[T13-081]** 13

**[T13-082]** Tác nhân nghiên cứu thị trường & đối thủ cạnh tranh (Research Agent)

**[T13-083]** 4

**[T13-084]** 4

**[T13-085]** 4

**[T13-086]** 12

**[T13-087]** Trợ lý lập trình có vòng lặp tự động chạy thử và sửa lỗi (Code Assistant)

**[T13-088]** 5

**[T13-089]** 5

**[T13-090]** 4

**[T13-091]** 14

**[T13-092]** Bảng 2: Ma trận chấm điểm Agentic Fit áp dụng cho các Use Case

**[T13-093]** Định hướng kiến trúc dựa trên tổng điểm: • Từ 0 đến 5 điểm: Lựa chọn tối ưu là thiết kế Chatbot thông thường hoặc hệ thống dựa trên quy tắc (Rule/Workflow).• Từ 6 đến 10 điểm: Phù hợp với mô hình Chatbot tăng cường (Augmented Chatbot - Chatbot có bổ sung RAG hoặc công cụ cơ bản).• Từ 11 điểm trở lên: Kiến trúc hệ thống Agent là giải pháp rất đáng để đầu tư và thử nghiệm.

**[T13-094]** Các Phản Mẫu (Anti-Patterns) Cần Tránh

**[T13-095]** Cảnh báo thiết kế: Triển khai kiến trúc Agent sẽ trở nên phản tác dụng và gây lãng phí lớn nếu rơi vào các trường hợp sau đây:

**[T13-096]** • Bài toán một bước (Single-step): Nghiệp vụ bản chất là hỏi đáp trực tiếp một bước, tra cứu tài liệu FAQ hoặc phân loại dữ liệu cơ bản.

**[T13-097]** • Thiếu công cụ hành động (No tools): Agent được thiết lập để thực hiện các suy luận trừu tượng nhưng không được cung cấp bất kỳ công cụ thực tế nào để tương tác và phản hồi môi trường.

**[T13-098]** • Nghiệp vụ đòi hỏi tính chính xác tuyệt đối: Yêu cầu hệ thống phải hoạt động chính xác 100% theo logic định sẵn (deterministic); nơi mà mỗi sai số nhỏ của mô hình ngôn ngữ đều phải trả giá rất đắt.

**[T13-099]** • Giới hạn nghiêm ngặt về thời gian phản hồi (Latency constraint): Hệ thống không chấp nhận độ trễ lớn (latency); việc chạy vòng lặp agent từ 3 đến 5 bước sẽ tốn thời gian quá dài và không thể đáp ứng yêu cầu thời gian thực.

**[T13-100]** 3. KIẾN TRÚC TỔNG QUAN CỦA MỘT AGENT

**[T13-101]** Mô hình kiến trúc tổng quát: Một hệ thống Agent hoàn chỉnh được xây dựng dựa trên sự liên kết chặt chẽ của loa bốn khối kiến trúc cơ bản (Perception, Reasoning, Action, Memory). Luồng thông tin tương tác tuần hoàn giữa các khối này giúp Agent nhận biết, suy luận và hành động hiệu quả trong môi trường thực tế.

**[T13-102]** Bốn Khối Thành Phần Cốt Lõi

**[T13-103]** 1. Nhận thức (Perception): Đóng vai trò tiếp nhận thông tin đầu vào từ người dùng (user input), kết quả phản hồi từ việc gọi công cụ (tool results) hoặc các phản hồi trực tiếp từ môi trường xung quanh.

**[T13-104]** 2. Suy luận (Reasoning): Được đảm nhiệm bởi Mô hình ngôn ngữ lớn Core (LLM Core). Đóng vai trò bộ não trung tâm để phân tích trạng thái hiện tại, suy luận logic và quyết định bước hành động tiếp theo.

**[T13-105]** 3. Hành động (Action): Thực thi các quyết định bằng cách gọi các API bên ngoài, thực hiện tìm kiếm (Search), truy vấn dữ liệu hoặc trả về câu trả lời cuối cùng cho người dùng (Final Answer).

**[T13-106]** 4. Bộ nhớ (Memory): Hệ thống lưu trữ giúp duy trì tính liên tục của mục tiêu, lưu giữ các sự kiện quan trọng và kết quả trung gian để tránh việc Agent bị mất mạch suy luận.

**[T13-107]** LƯU Ý VỀ CHI PHÍ VẬN HÀNHPhân tích Chi phí: Bốn khối kiến trúc này là nguồn gốc trực tiếp dẫn tới bốn nhóm chi phí chính trong vận hành Agent, bao gồm: chi phí số lượng token tiêu thụ, chi phí lưu trữ dữ liệu (storage), chi phí gọi các API bên thứ ba, và độ trễ hệ thống (latency).

**[T13-108]** Cơ Chế Bộ Nhớ: Ngắn Hạn (Short-Term) vs Dài Hạn (Long-Term)

**[T13-109]** • Bộ nhớ ngắn hạn (Short-term memory): Bộ nhớ ngắn hạn nằm trực tiếp trong cửa sổ ngữ cảnh (context window) của mô hình. Bộ nhớ này cực kỳ tối ưu cho việc xử lý tác vụ hiện tại, chi phí triển khai thấp nhưng nhược điểm lớn nhất là dễ bị đầy khi chuỗi hội thoại kéo dài. Thích hợp nhất cho các cuộc hội thoại ngắn và các mục tiêu chỉ kéo dài trong vài bước lặp.

**[T13-110]** • Bộ nhớ dài hạn (Long-term memory): Bộ nhớ dài hạn được lưu trữ ngoài cửa sổ ngữ cảnh của mô hình thông qua các hệ thống cơ sở dữ liệu chuyên dụng, Vector Store, hoặc Key-Value Store. Bộ nhớ này cho phép lưu giữ thông tin lâu dài về người dùng (preferences, facts) hoặc các trạng thái phức tạp, tuy nhiên nó đòi hỏi phải có chiến lược truy xuất dữ liệu (retrieval strategy) và mô hình phân quyền truy cập (permission model) cực kỳ chặt chẽ.

**[T13-111]** Cơ Chế Gọi Công Cụ (Tool Calling)

**[T13-112]** Nguyên lý hoạt động: Cơ chế gọi công cụ đóng vai trò như 'tay chân' giúp Agent tương tác vật lý với thế giới thực. Sơ đồ luồng xử lý chuẩn hóa diễn ra như sau:

**[T13-113]** Luồng dữ liệu: User Goal → LLM Core (Phân tích) → Trả về định dạng JSON / Arguments chỉ định công cụ → Gọi API/Database/Search thực tế → Trả về kết quả quan sát (Observation) → LLM Core (Tổng hợp) → Trả về Câu trả lời cuối cùng (Final Answer).

**[T13-114]** • Định nghĩa công cụ (Tool Definitions) phải cực kỳ tường minh về đầu vào (input), đầu ra (output) và các chế độ xử lý lỗi (error modes).

**[T13-115]** • Mặc dù công cụ giúp mở rộng đáng kể năng lực của Agent, chúng cũng làm tăng xác suất lỗi hệ thống do các phụ thuộc bên ngoài (external dependencies).

**[T13-116]** Nấc Thang Phát Triển Mẫu Thiết Kế Agent (Theo Khảo Sát Từ Anthropic)

**[T13-117]** Độ phức tạp tăng dần: Năng lực và cấu trúc của các mẫu thiết kế Agent nên được gia tăng dần theo nhu cầu thực tế để đảm bảo hiệu quả chi phí và dễ kiểm soát:

**[T13-118]** 1. Augmented LLM (Mô hình tăng cường): Sử dụng mô hình ngôn ngữ lớn kết hợp Prompt tinh chỉnh, tài liệu hướng dẫn và các công cụ được định nghĩa sẵn.

**[T13-119]** 2. Prompt Chaining (Chuỗi Prompt): Chuỗi các bước thực thi được kết nối tuần tự một cách rõ ràng và cố định.

**[T13-120]** 3. Routing (Điều hướng): Phân loại ý định của người dùng để điều hướng luồng xử lý tới các nhánh chuyên biệt hoặc các mô hình chuyên gia phù hợp.

**[T13-121]** 4. Orchestrator-Worker (Điều phối - Thực thi): Một tác nhân điều phối (Orchestrator) thực hiện phân chia công việc cho các tác nhân thực thi (Workers), sau đó tổng hợp lại kết quả.

**[T13-122]** 5. Autonomous Agent (Tác nhân tự chủ): Hệ thống tự đưa ra quyết định thực thi chuỗi nhiều bước lặp động độc lập để đạt mục tiêu.

**[T13-123]** 4. MẪU THIẾT KẾ REACT (REASONING & ACTING)

**[T13-124]** Định nghĩa: ReAct (Reasoning + Acting) là mẫu thiết kế (design pattern) kinh điển và dễ tiếp cận nhất để chuyển đổi một mô hình ngôn ngữ lớn thông thường thành một Agent có khả năng tự động giải quyết các bài toán phức tạp và hỗ trợ khả năng gỡ lỗi (debug) trực quan cho con người.

**[T13-125]** Chu Trình Vòng Lặp ReAct (Thought → Action → Observation)

**[T13-126]** Các bước lặp tuần hoàn: Trong mẫu thiết kế ReAct, thay vì ngay lập tức đưa ra câu trả lời cuối cùng cho người dùng, Agent sẽ thực hiện một vòng lặp tuần hoàn qua ba trạng thái cốt lõi cho đến khi tích lũy đủ thông tin cần thiết:

**[T13-127]** 1. Thought (Suy nghĩ): Tự vấn bản thân về trạng thái hiện tại: 'Mình đang thiếu thông tin gì? Mình nên thực hiện hành động nào tiếp theo?'

**[T13-128]** 2. Action (Hành động): Quyết định gọi công cụ cụ thể nào và truyền vào các tham số (arguments) tương ứng là gì?

**[T13-129]** 3. Observation (Quan sát): Tiếp nhận và phân tích kết quả dữ liệu phản hồi trả về từ công cụ vừa thực thi.

**[T13-130]** ĐIỂM MẠNH GỠ LỖI CỦA REACTGiá trị cốt lõi: ReAct cực kỳ mạnh mẽ vì toàn bộ vết suy luận (trace) và lý do dẫn tới hành động đều được bộc lộ ra ngoài dưới dạng văn bản. Điều này giúp các kỹ sư hệ thống dễ dàng theo dõi, kiểm thử, phát hiện lỗi và can thiệp kịp thời vào quá trình xử lý của Agent.

**[T13-131]** Phân Tích Trace Ví Dụ Thực Tế: Tìm Chuyến Bay Khứ Hồi

**[T13-132]** Hành trình trace chi tiết: Dưới đây là vết xử lý thực tế của một ReAct Agent khi tiếp nhận yêu cầu tìm vé máy bay từ HAN đi HCM và kiểm tra thời tiết để gợi ý trang phục:

**[T13-133]** • Thought 1: Tôi cần tìm kiếm các chuyến bay khởi hành sáng mai từ sân bay Hà Nội (HAN) tới sân bay Tân Sơn Nhất (SGN) có mức giá dưới 2.000.000 VNĐ.

**[T13-134]** • Action 1: Gọi công cụ search_flights(origin="HAN", destination="SGN", date="2026-03-18", max_price=2000000)

**[T13-135]** • Observation 1: Trả về kết quả có 2 lựa chọn phù hợp: VietJet 06:10 giá 1.750.000 VNĐ; Vietnam Airlines 08:20 giá 1.950.000 VNĐ.

**[T13-136]** • Thought 2: Người dùng có yêu cầu gợi ý trang phục mang theo trong trường hợp có mưa. Do đó, tôi cần phải thực hiện kiểm tra tình hình thời tiết thực tế tại Thành phố Hồ Chí Minh.

**[T13-137]** • Action 2: Gọi công cụ get_weather(city="Ho Chi Minh City", date="2026-03-18")

**[T13-138]** • Observation 2: Dữ liệu thời tiết trả về: Nhiệt độ dao động 27–32°C, xác suất xuất hiện mưa đạt 70%.

**[T13-139]** • Thought 3: Tôi hiện tại đã thu thập đầy đủ cả hai luồng thông tin bao gồm danh sách chuyến bay thỏa mãn ngân sách và dự báo thời tiết chi tiết tại điểm đến. Tôi có thể tiến hành tổng hợp để đưa ra kết luận cuối cùng.

**[T13-140]** • Final Answer: Gợi ý người dùng lựa chọn chuyến bay VietJet lúc 06:10 với mức giá tối ưu 1.75M VNĐ. Về trang phục tại TP. HCM do có xác suất mưa cao, khuyến nghị chuẩn bị áo quần mỏng nhẹ thoáng mát, mang theo giày dễ làm khô, ô gập cá nhân hoặc áo mưa tiện lợi.

**[T13-141]** Đánh Giá Ưu Điểm Và Giới Hạn Của ReAct Pattern

**[T13-142]** • Ưu điểm: Dễ dàng đọc hiểu toàn bộ vết suy luận (trace) và thực hiện debug; Agent có khả năng tự động đưa ra quyết định tối ưu cho bước tiếp theo dựa trên kết quả quan sát thực tế; Rất thích hợp cho các bài toán mang tính chất điều tra, tìm kiếm thông tin, lập trình hoặc đặt chỗ; Cho phép dễ dàng cài đặt các bộ lọc an toàn (safeguard) tại từng vòng lặp.

**[T13-143]** • Giới hạn: Tiêu tốn số lượng token lớn và làm gia tăng độ trễ hệ thống (latency) nhiều lần so với chatbot thông thường; Dễ rơi vào trạng thái lặp vô hạn (infinite loop) hoặc gọi sai lệch công cụ; Đòi hỏi phải có hệ thống đánh giá (evaluation) phức tạp dựa trên toàn bộ vết suy luận (trace) thay vì chỉ kiểm tra câu trả lời cuối cùng; Không phù hợp cho các bài toán đơn giản hoặc đòi hỏi tính định sẵn cao.

**[T13-144]** 5. GIẢI PHẪU MÃ NGUỒN VÒNG LẶP AGENT (AGENT LOOP: CODE ANATOMY)

**[T13-145]** Kiến trúc lập trình: Để hiện thực hóa lý thuyết ReAct thành một hệ thống phần mềm hoạt động ổn định, cấu trúc mã nguồn cần phải quản trị tốt trạng thái vòng lặp, đăng ký các công cụ và thiết lập các chốt chặn an toàn (safeguards).

**[T13-146]** Cấu Trúc Mã Giả Vòng Lặp Agent Tối Thiểu (Pseudocode)

**[T13-147]** Mã nguồn tham khảo: Dưới đây là logic lập trình cốt lõi của một vòng lặp ReAct Agent thủ công bằng Python để minh họa bản chất vận hành:

**[T13-148]** def run_agent_loop(user_query, max_iterations=5): history = [] current_input = user_query for iteration in range(max_iterations): # 1. LLM Core sinh Thought và Action từ ngữ cảnh hội thoại response = llm_core.generate(system_prompt, current_input, history) thought, action, action_args = parse_llm_output(response) log(f"[Vòng {iteration+1}] Thought: {thought}") history.append({"role": "assistant", "content": response}) if is_final_answer(response): return extract_final_answer(response) # 2. Thực thi Action bằng cách gọi công cụ tương ứng try: tool_func = tool_registry.get(action) observation = tool_func(**action_args) except Exception as e: observation = f"Lỗi thực thi công cụ: {str(e)}" log(f"[Vòng {iteration+1}] Observation: {observation}") history.append({"role": "user", "content": f"Observation: {observation}"}) return fallback_to_chatbot(user_query, "Vượt quá số vòng lặp tối đa cho phép.")

**[T13-149]** Thiết Lập System Prompt Production-Grade Cho ReAct

**[T13-150]** Cấu trúc System Prompt: Một trong những cấu phần quan trọng nhất của ReAct Agent là System Prompt. System Prompt phải quy định cực kỳ chặt chẽ định dạng đầu ra để tránh hiện tượng vỡ định dạng (format drift). Prompt chuẩn hóa thường có cấu trúc như sau:

**[T13-151]** MẪU SYSTEM PROMPT CHUẨN HÓABạn là một trợ lý AI hữu ích có khả năng sử dụng các công cụ để giải quyết bài toán. Bạn phải tuân thủ nghiêm ngặt quy trình suy luận sau:1. Thought: Ghi lại suy nghĩ của bạn về việc cần làm tiếp theo.2. Action: Tên công cụ cần gọi (phải thuộc danh sách công cụ được cung cấp).3. Action Input: Các tham số truyền vào công cụ dưới định dạng JSON chuẩn.4. Observation: Kết quả trả về từ công cụ (sẽ do hệ thống cung cấp cho bạn).Lặp lại quy trình trên cho đến khi bạn tích lũy đủ thông tin. Khi đó, hãy kết thúc bằng:5. Final Answer: Câu trả lời chi tiết và hoàn chỉnh nhất dành cho người dùng.

**[T13-152]** Các Bộ Lọc An Toàn (Safeguards) Ngăn Chặn Vòng Lặp Vô Hạn

**[T13-153]** Các tham số chốt chặn cần thiết: Trong môi trường vận hành thực tế (production), các bộ lọc an toàn (guardrails) đóng vai trò sống còn để bảo vệ hệ thống khỏi việc tiêu tốn tài nguyên vô ích:

**[T13-154]** • Max Iterations Safeguard: Bắt buộc phải giới hạn cứng số vòng lặp tối đa (Max Iterations), thông thường cấu hình ở mức 3 đến 5 vòng lặp tùy thuộc use case cụ thể.

**[T13-155]** • Timeout Safeguard: Đặt giới hạn thời gian phản hồi tối đa (Timeout) cho từng công cụ/API độc lập để tránh hệ thống bị treo khi dịch vụ bên ngoài gặp sự cố.

**[T13-156]** • Token/Cost Budget: Thiết lập ngưỡng chi phí tối đa (Budget) về số lượng token hoặc chi phí tài chính cho mỗi phiên xử lý của người dùng.

**[T13-157]** • Kiểm soát tái thử nghiệp (Controlled Retry): Quản lý việc gọi lại công cụ khi xảy ra lỗi kết nối với số lần thử lại (retry) có giới hạn và cơ chế lùi bước (backoff).

**[T13-158]** Dấu hiệu nhận biết vòng lặp lỗi (Loop Detection): Hệ thống cần phải giám sát liên tục vết suy luận và thực hiện dừng khẩn cấp (break loop) kèm theo kích hoạt cơ chế chuyển hướng dự phòng (fallback) khi phát hiện các dấu hiệu sau:1. Agent liên tục thực hiện gọi lặp lại cùng một công cụ với cùng một tham số đầu vào.2. Agent liên tục hỏi lại các thông tin mà hệ thống đã cung cấp ở các bước trước.3. Bước suy luận (Thought) của Agent không tiến triển thêm về mặt logic.4. Kết quả quan sát (Observation) trả về không thay đổi nhưng Agent vẫn tiếp tục vòng lặp.

**[T13-159]** Sự Dịch Chuyển Từ Vòng Lặp Thủ Công Đến LangGraph

**[T13-160]** Quá trình tối ưu kiến trúc: Mặc dù việc lập trình vòng lặp bằng tay (bằng cấu trúc vòng lặp for/while thông thường) rất phù hợp để giúp các kỹ sư hiểu rõ bản chất cơ chế hoạt động, tuy nhiên khi hệ thống nghiệp vụ phát triển phức tạp hơn với nhiều nhánh rẽ, việc duy trì mã nguồn ad-hoc sẽ trở nên vô cùng khó khăn.

**[T13-161]** • Ưu thế của Graph Approach: LangGraph cho phép các nhà phát triển biểu diễn chu trình hoạt động của Agent dưới dạng một Đồ thị có trạng thái (Stateful Graph), bao gồm các thành phần: các Nút đại diện cho hành động (Nodes), các Cạnh đại diện cho luồng di chuyển (Edges), các Cạnh có điều kiện để điều hướng dựa trên kết quả (Conditional Edges), và bộ lưu trữ trạng thái xuyên suốt (State). Cách tiếp cận này giúp hệ thống dễ bảo trì, dễ mở rộng quy mô và quản trị trạng thái hoàn hảo.

**[T13-162]** 6. KỊCH BẢN KIỂM THỬ VÀ HƯỚNG DẪN GỠ LỖI

**[T13-163]** Nguyên tắc kiểm thử: Để đảm bảo chất lượng vận hành của Agent trước khi triển khai, các kỹ sư cần xây dựng các kịch bản kiểm thử trực quan và tuân thủ quy trình gỡ lỗi khoa học dựa trên vết suy luận (trace).

**[T13-164]** Kịch Bản Live Demo Tra Cứu Thời Tiết Và Gợi Ý Trang Phục

**[T13-165]** Nội dung kịch bản: Quy trình thực hiện kịch bản thử nghiệm trực tiếp tại lớp học bao gồm 5 bước tiêu chuẩn:

**[T13-166]** Bước 1: Định nghĩa rõ ràng hai công cụ cốt lõi: get_weather (lấy dữ liệu thời tiết thực tế) và recommend_outfit (gợi ý trang phục phù hợp dựa trên thông số đầu vào).

**[T13-167]** Bước 2: Xây dựng System Prompt ràng buộc nghiêm ngặt: Agent tuyệt đối không được đưa ra câu trả lời cuối cùng nếu chưa hoàn thành việc gọi công cụ tra cứu thời tiết.

**[T13-168]** Bước 3: Thực thi vòng lặp và ghi nhận chi tiết toàn bộ các bước Thought / Action / Observation hiển thị trực quan ra màn hình log.

**[T13-169]** Bước 4: Chủ động giả lập các lỗi kỹ thuật thực tế như: đặt thời gian chờ (timeout) cho công cụ hoặc tinh chỉnh để Agent trả về gợi ý trang phục sai lệch hoàn toàn với thời tiết quan sát.

**[T13-170]** Bước 5: Tiến hành gỡ lỗi (debugging) bằng cách sửa đổi mô tả công cụ (tool description), điều chỉnh hệ thống Prompt, hoặc bổ sung các bộ lọc an toàn.

**[T13-171]** Bảng Kiểm Tra Gỡ Lỗi Khi Agent Gặp Sự Cố (Debug Checklist)

**[T13-172]** Hướng tiếp cận hệ thống: Khi Agent hoạt động không đúng kỳ vọng, nguyên tắc tối thượng là phải phân tích toàn bộ vết suy luận (trace log) đầu tiên, thay vì chỉ đánh giá câu trả lời cuối cùng. Bảng kiểm tra dưới đây định hướng quy trình kiểm vết:

**[T13-173]** 1. Sửa đổi mô tả công cụ (Tool Description): Mô tả hoạt động của công cụ được viết quá mơ hồ khiến mô hình ngôn ngữ lớn Core không thể nhận biết chính xác khi nào nên kích hoạt công cụ đó.

**[T13-174]** 2. Bổ sung quy tắc dừng trong System Prompt: System Prompt bị thiếu các quy tắc ràng buộc nghiêm ngặt về điều kiện dừng vòng lặp hoặc định dạng trả về.

**[T13-175]** 3. Thiết lập Safeguards dự phòng: Hệ thống thiếu các tham số chốt chặn an toàn cho các trường hợp gọi lỗi hoặc rơi vào vòng lặp vô hạn.

**[T13-176]** 4. Cải tiến quy trình đánh giá chất lượng (Evaluation): Hệ thống đánh giá chất lượng chỉ thực hiện chấm điểm dựa trên câu trả lời cuối cùng (Final Answer) mà bỏ qua việc đánh giá tính logic của toàn bộ vết suy luận (Trace Evaluation).

**[T13-177]** BẢN CHẤT CỦA AGENT DEBUGGINGNhận định chuyên gia: Việc gỡ lỗi cho một hệ thống Agentic AI có tính chất phức tạp tương đồng với việc gỡ lỗi cho một hệ thống phân tán (distributed system) hơn là việc tinh chỉnh prompt thông thường (prompt tuning). Lập trình viên bắt buộc phải kiểm soát toàn diện từ mô hình ngôn ngữ Core, các công cụ tích hợp, trạng thái của luồng xử lý (state) cho đến bộ máy điều phối (orchestration).

**[T13-178]** Mô Hình Lai Trực Dụng (Hybrid Pattern: Chatbot & Agent)

**[T13-179]** Kiến trúc tối ưu: Trong các hệ thống thương mại thực tế, việc sử dụng kiến trúc Agent cho mọi yêu cầu của người dùng là một phương án cực kỳ tốn kém và làm tăng độ trễ không đáng có. Giải pháp tối ưu và thực dụng nhất là triển khai Mô hình Lai (Hybrid Pattern):

**[T13-180]** Sơ đồ luồng xử lý lai: Yêu cầu đầu vào của người dùng (User Query) → Bộ phận phân loại ý định (Intent/Triage Node) →• Nhánh 1 (Câu hỏi đơn giản, FAQ lặp lại): Chuyển hướng xử lý qua Chatbot thông thường (Simple Chatbot Path) để phản hồi nhanh chóng với chi phí tối thiểu.• Nhánh 2 (Yêu cầu phức tạp, nhiều bước): Chuyển hướng xử lý vào Vòng lặp Agent (Agent Path) để gọi công cụ và xử lý động.• Nhánh 3 (Sự cố hoặc yêu cầu đặc biệt): Chuyển hướng hỗ trợ trực tiếp từ con người (Human/Escalation Path).

**[T13-181]** 7. NỘI DUNG THỰC HÀNH VÀ BÀI TẬP BẮT BUỘC

**[T13-182]** Tổng quan phần thực hành: Nội dung thực hành thực tế được thiết kế nhằm giúp người học có sự đối chiếu trực quan và sâu sắc giữa năng lực của Chatbot thông thường và Agent in việc giải quyết cùng một bài toán nghiệp vụ.

**[T13-183]** Hướng Dẫn Thực Hiện Lab #3: Chatbot vs Agent — Hands-on Comparison

**[T13-184]** Bước 1: Chọn lại một bài toán nghiệp vụ (use case) đã xây dựng từ Ngày học số 2 hoặc lựa chọn một use case tương đương có độ phức tạp trung bình.

**[T13-185]** Bước 2: Xây dựng phiên bản Chatbot Baseline cho bài toán đó để làm mốc đối chứng hiệu năng.

**[T13-186]** Bước 3: Nâng cấp hệ thống Chatbot lên kiến trúc ReAct Agent, tích hợp tối thiểu từ 1 đến 2 công cụ (tools) thực tế.

**[T13-187]** Bước 4: Thiết lập và chạy thử nghiệm đồng thời 5 trường hợp kiểm thử (test cases) giống nhau trên cả hai hệ thống.

**[T13-188]** Bước 5: Vẽ sơ đồ luồng xử lý (flowchart) và ghi chép chi tiết các trường hợp thực tế mà hệ thống Agent mang lại giá trị vượt trội so với phiên bản Baseline.

**[T13-189]** Yêu cầu sản phẩm đầu ra (Deliverable Checklist): • Thời gian thực hiện quy định: 150 phút.• Sản phẩm bàn giao bắt buộc (Deliverables): Mã nguồn hệ thống Chatbot Baseline + Mã nguồn ReAct Agent + Tập hợp 5 ca kiểm thử thực tế + 1 File Log ghi nhận Trace của Agent + 1 Sơ đồ luồng xử lý Flowchart.• Điểm thưởng (Bonus): Triển khai thành công đường dẫn dự phòng (fallback path) hoặc cơ chế chuyển hướng con người (human escalation).
