# Study Pack corpus - Day 05 - AI Product Thinking và Requirements

> Corpus version: `study-pack-corpus-v1`
> Combined source SHA-256: `d9ff0da80192992871546bbffaf0f79567c061d3be189272d715a0811f1055a2`
> Original source lines: 1497-1751
> Transformation: one non-empty source line equals one citation segment;
> no source text is summarized, paraphrased, or silently truncated.

**[T15-001]** [Day-05] BẢN TÓM TẮT CHUYÊN SÂU NỘI DUNG ĐÀO TẠO

**[T15-002]** NGÀY 5: TƯ DUY SẢN PHẨM AI & QUẢN TRỊ YÊU CẦU(AI PRODUCT THINKING & REQUIREMENTS)

**[T15-003]** ★ CÂU HỎI SỐNG CÒN CỦA NGÀY 5

**[T15-004]** "Bạn đã xây dựng một Agent rất đẹp, thông minh và phức tạp. Nhưng tại sao người dùng lại không chịu sử dụng?" Giữ nguyên câu hỏi mang tính định hướng cốt lõi này trong đầu suốt quá trình tiếp cận đặc tả yêu cầu cho sản phẩm AI.

**[T15-005]** MỤC LỤC TỰ ĐỘNG

**[T15-006]** Danh mục các đề mục chính trong tài liệu. Người đọc có thể cập nhật mục lục này trực tiếp bằng cách nhấn chuột phải vào vùng mục lục trong Microsoft Word hoặc Google Docs và chọn 'Update Field'.

**[T15-007]** 1. TỔNG QUAN CHƯƠNG TRÌNH & MỤC TIÊU NGÀY 5

**[T15-008]** Buổi học thứ 5 tập trung vào việc định hình tư duy sản phẩm khi thiết kế các giải pháp Trí tuệ Nhân tạo (AI), chuyển hóa các nhu cầu của người dùng thành các yêu cầu kỹ thuật đo lường được và quản trị rủi ro toàn diện.

**[T15-009]** Mục tiêu chi tiết: Mục tiêu cốt lõi của ngày học bao gồm bốn khía cạnh then chốt giúp định hình năng lực cho các Product Manager (PM), Business Analyst (BA), Kỹ sư phát triển (Engineer) và các bên liên quan (Stakeholders):

**[T15-010]** • Hiểu rõ và phân biệt sự khác biệt sâu sắc giữa một sản phẩm AI (AI Product) và một tính năng phần mềm truyền thống (Software Feature).

**[T15-011]** • Nắm vững phương pháp chuyển hóa nhu cầu mơ hồ của người dùng (User Needs) thành các yêu cầu kỹ thuật đặc thù và đo lường được (Testable Requirements).

**[T15-012]** • Biết cách soạn thảo một tài liệu Đặc tả Yêu cầu Sản phẩm (PRD - Product Requirements Document) có cấu trúc chuẩn hóa, làm cầu nối đồng thuận giữa các bên liên quan.

**[T15-013]** • Lập và quản trị được một Danh mục Rủi ro (Risk Register) toàn diện cho sản phẩm AI dựa trên logic định lượng rõ ràng: Khả năng xảy ra (Likelihood) nhân với Mức độ ảnh hưởng (Impact).

**[T15-014]** Hệ câu hỏi nghiệm thu: Kết thúc ngày học, học viên bắt buộc phải trả lời mạch lạc 5 câu hỏi cốt lõi: Sản phẩm này được làm cho ai? Mang lại giá trị gì? Đo lường thành công bằng gì? Gặp phải rủi ro nào? Và khi nào thì kích hoạt điều kiện Go/No-Go?

**[T15-015]** Yêu cầu bàn giao (Deliverables): Bộ hồ sơ nghiệm thu cuối buổi (Deliverables) yêu cầu học viên phải bàn giao: 1 tài liệu PRD hoàn chỉnh dài từ 3-5 trang bám sát vào hệ thống Multi-agent đã phát triển ở Ngày 4, kết hợp với 1 Ma trận Rủi ro (Risk Matrix) chứa ít nhất 5 rủi ro bắt buộc (Hallucination, Bias, Privacy, Cost, Adoption).

**[T15-016]** 2. PRODUCT THINKING CHO AI

**[T15-017]** Xây dựng thành công một hệ thống Agent thông minh mới chỉ là điều kiện cần. Điều kiện đủ để sản phẩm tồn tại và phát triển là nó phải giải quyết đúng nỗi đau thực tế của đúng nhóm khách hàng mục tiêu.

**[T15-018]** 2.1. Hai Kiểu Thất Bại Phổ Biến Trong Phát Triển AI

**[T15-019]** Quá trình nghiên cứu và triển khai sản phẩm AI thực tế thường vấp phải hai vết xe đổ nghiêm trọng:

**[T15-020]** • Build the wrong thing (Xây dựng sai sản phẩm): Xảy ra khi đội ngũ phát triển không thấu hiểu hành trình công việc thực tế của người dùng (Jobs-to-be-Done - JTBD), lựa chọn sai chân dung người dùng mục tiêu (Persona) hoặc giá trị mang lại không đủ lớn để giữ chân người dùng quay lại sử dụng lần thứ hai.

**[T15-021]** • Build the thing wrong (Xây dựng sản phẩm sai cách): Xảy ra khi tài liệu yêu cầu (Requirements) quá mơ hồ, không đưa ra được các tiêu chí nghiệm thu (Acceptance Criteria) đo lường được bằng số liệu và hoàn toàn không lường trước các trường hợp rủi ro, biên (Edge Cases).

**[T15-022]** ★ NGUYÊN TẮC VÀNG VỀ GIÁ TRỊ SẢN PHẨM

**[T15-023]** Đối với một sản phẩm tích hợp AI, việc làm rõ giá trị mang lại (Value Clarity) và chất lượng của đặc tả yêu cầu (Requirement Quality) đóng vai trò quan trọng không kém gì chất lượng của mô hình toán học (Model Quality).

**[T15-024]** 2.2. Sự Khác Biệt Giữa Software Feature Thường Và AI Product

**[T15-025]** Việc cố gắng viết yêu cầu cho một sản phẩm AI theo cách viết đặc tả cho một biểu mẫu CRUD (Create-Read-Update-Delete) truyền thống là nguyên nhân hàng đầu dẫn đến thất bại. Bản chất của AI yêu cầu việc thiết kế thêm các dải chất lượng (Quality Bands), cơ chế dự phòng (Fallbacks) và thiết kế trải nghiệm tin cậy (Trust Design).

**[T15-026]** Khía cạnh so sánh

**[T15-027]** Software Feature truyền thống

**[T15-028]** AI Product thực tế

**[T15-029]** Kết quả đầu ra (Output)

**[T15-030]** Deterministic (Có tính xác định, 1+1 luôn bằng 2, có quy tắc cứng)

**[T15-031]** Probabilistic (Có tính xác suất, có sự biến thiên và không đồng nhất)

**[T15-032]** Kỳ vọng người dùng

**[T15-033]** Rõ ràng, ít mơ hồ, hành vi của hệ thống được định hình sẵn

**[T15-034]** Dễ kỳ vọng quá mức (Over-expectation) hoặc hiểu sai bản chất

**[T15-035]** Định nghĩa hoàn thành (DoD)

**[T15-036]** Đạt/Không đạt (Pass/Fail) phân định rất rõ ràng

**[T15-037]** Yêu cầu dải ngưỡng chất lượng, cam kết dịch vụ (SLA) và fallback

**[T15-038]** Vòng lặp cải tiến (Loop)

**[T15-039]** Build rồi Ship (Xây dựng xong là bàn giao, bảo trì cơ bản)

**[T15-040]** Build -> Test -> Observe -> Calibrate -> Re-ship (Cần giám sát liên tục)

**[T15-041]** Sơ đồ: So sánh bản chất Software Feature truyền thống và AI Product

**[T15-042]** 2.3. Khung Tư Duy Jobs-to-be-Done (JTBD) Cho Sản Phẩm AI

**[T15-043]** Để tránh việc xây dựng một hệ thống Agent đúng chức năng kỹ thuật nhưng không bao giờ được dùng lại, nhà phát triển cần phân tích nhu cầu người dùng qua ba khía cạnh của lý thuyết JTBD:

**[T15-044]** • Functional Job (Mục tiêu chức năng): Công việc bề nổi người dùng muốn hoàn thành. Ví dụ: Trả lời các yêu cầu hỗ trợ (ticket) của khách hàng nhanh hơn.

**[T15-045]** • Emotional Job (Cảm xúc nội tại): Cảm giác của người dùng khi thực hiện công việc. Ví dụ: Cảm thấy tự tin hơn trong quyết định xử lý, bớt lo sợ việc trả lời sai chính sách.

**[T15-046]** • Social Job (Vị thế xã hội): Cách người dùng muốn được đồng nghiệp, khách hàng nhìn nhận. Ví dụ: Trông chuyên nghiệp hơn trong mắt khách hàng, phản hồi thông tin mạch lạc, nhanh chóng.

**[T15-047]** 2.4. Phân Tích Các Use Cases Điển Hình Xác Định Giá Trị Thực Tế

**[T15-048]** Một sản phẩm AI tốt cần định vị rõ rệt giá trị của nó thông qua 4 câu hỏi: Ai là người dùng? Họ đau ở đâu (Pain points)? Thành công của họ được đo bằng gì? Và nếu hệ thống thất bại thì hậu quả gây hại lớn thế nào?

**[T15-049]** Danh mục Use Cases thực tế: Bốn trường hợp ứng dụng (Use Cases) phổ biến nhất được đúc rút bao gồm:

**[T15-050]** 1. • AI Support Agent: Tập trung giảm thời gian phản hồi trung bình và tăng tính nhất quán của câu trả lời cho khách hàng.

**[T15-051]** 2. • Trợ lý tra cứu chính sách nội bộ (Internal Policy Assistant): Giảm thời gian tìm kiếm văn bản pháp lý, giảm tần suất hỏi lặp lại các câu hỏi phổ biến.

**[T15-052]** 3. • Ticket Routing Agent (Tác nhân phân luồng công việc): Tự động phân loại và chuyển tiếp ticket đến đúng phòng ban chuyên môn, giảm thiểu tình trạng nghẽn hàng đợi.

**[T15-053]** 4. • Trợ lý bán hàng (AI Sales Assistant): Sàng lọc thông minh các khách hàng tiềm năng (Leads), tóm tắt nhu cầu và tự động gợi ý bước tiếp theo cho nhân viên sales.

**[T15-054]** 2.5. Chỉ Số Định Hướng Thành Công (North Star Metrics)

**[T15-055]** Nguyên lý cốt lõi trước khi đi vào xây dựng phạm vi tính năng là phải định nghĩa được chỉ số thành công (Define success before scope):

**[T15-056]** • Đối với AI Support Agent: Đo lường bằng Tỷ lệ xử lý thành công ngay từ lần phản hồi đầu tiên (First-response resolution rate) – Đừng chỉ đo thuần túy số lượng câu trả lời phát ra.

**[T15-057]** • Đối với Tra cứu văn bản chính sách: Đo lường bằng Thời gian trả lời đúng nguồn trích dẫn chính thức (Time-to-answer) – Đừng chỉ đo độ dài của câu trả lời sinh ra.

**[T15-058]** • Đối với Ticket Routing Agent: Đo lường bằng Tỷ lệ phân luồng chính xác ngay từ lần đầu tiên (Correct queue rate) – Đừng chỉ đo tốc độ phân loại thô.

**[T15-059]** • Đối với AI Sales Assistant: Đo lường bằng Tỷ lệ khách hàng tiềm năng đủ điều kiện chuyển đổi thực tế (Qualified lead rate) – Đừng chỉ đo số lượng lead được chấm điểm tự động.

**[T15-060]** 3. NGUYÊN LÝ RESPONSIBLE AI CỐT LÕI (RESPONSIBLE AI FUNDAMENTALS)

**[T15-061]** Phát triển AI có trách nhiệm (Responsible AI) không đơn thuần là một khẩu hiệu đạo đức mang tính lý thuyết, mà trực tiếp đóng vai trò là một rào chắn giảm thiểu rủi ro pháp lý và vận hành cho doanh nghiệp.

**[T15-062]** 3.1. 5 Trụ Cột Cốt Lõi Của Responsible AI

**[T15-063]** • Công bằng (Fairness): Mô hình không được phép đưa ra các kết quả thiên vị bất hợp lý hoặc phân biệt đối xử đối với các nhóm đối tượng người dùng khác nhau.

**[T15-064]** • Tin cậy & An toàn (Reliability & Safety): Đảm bảo hệ thống vận hành đủ ổn định, có khả năng chống chịu lỗi tốt để người dùng có thể an tâm tin tưởng.

**[T15-065]** • Bảo mật & Riêng tư (Privacy & Security): Chỉ thu thập và xử lý những phần dữ liệu thực sự cần thiết cho tác vụ (Data Minimization).

**[T15-066]** • Toàn diện (Inclusiveness): Thiết kế giao diện và khả năng của sản phẩm phù hợp với nhiều nhóm người dùng có năng lực và điều kiện tiếp cận khác nhau.

**[T15-067]** • Minh bạch (Transparency): Giúp người dùng hiểu rõ AI đang làm gì, giới hạn khả năng của nó nằm ở đâu và cung cấp nguồn trích dẫn rõ ràng.

**[T15-068]** 3.2. Chuyển Hóa Trụ Cột Responsible AI Thành Đặc Tả Kỹ Thuật

**[T15-069]** Đối với các BA và PM, các nguyên lý Responsible AI chung chung cần phải được dịch thuật sang ngôn ngữ của đặc tả yêu cầu sản phẩm:

**[T15-070]** Vấn đề Responsible AI

**[T15-071]** Câu hỏi cần đặt ra khi phát hiện yêu cầu (Discovery)

**[T15-072]** Yêu cầu kỹ thuật bắt buộc phải tích hợp trong PRD

**[T15-073]** Thiên lệch (Bias)

**[T15-074]** AI có đối xử khác biệt hoặc đưa ra kết quả không đồng đều giữa các nhóm người dùng không?

**[T15-075]** Yêu cầu xây dựng Test Set đa dạng; thiết lập quy trình kiểm duyệt thủ công (Human Review) cho các trường hợp nhạy cảm.

**[T15-076]** Riêng tư (Privacy)

**[T15-077]** Sản phẩm có xử lý thông tin định danh cá nhân (PII) hay dữ liệu nhạy cảm nào của người dùng không?

**[T15-078]** Áp dụng nguyên tắc giảm thiểu dữ liệu (Data Minimization), che giấu thông tin nhạy cảm (Masking), và chính sách lưu trữ/xóa dữ liệu rõ ràng.

**[T15-079]** Minh bạch (Transparency)

**[T15-080]** Người dùng có biết họ đang tương tác với AI không? Làm sao để họ biết khi nào cần ghi đè kết quả của AI?

**[T15-081]** Tích hợp thông báo tuyên bố rõ (Disclosure), hiển thị dẫn nguồn tài liệu trích dẫn (Citation), và thiết lập luồng chuyển hướng lên người thật (Escalation Path).

**[T15-082]** 3.3. Đạo Luật AI Act Của Liên Minh Châu Âu (EU AI Act 2024)

**[T15-083]** Đạo luật AI Act của EU (có hiệu lực từ năm 2024) phân loại các hệ thống AI theo các cấp độ rủi ro khác nhau. Đối với các PM/BA, tác động thực tế của đạo luật này là buộc đội ngũ phát triển phải thiết kế hệ thống ghi nhật ký (Logging), hiển thị tuyên bố rõ ràng (Disclosure), xử lý ngoại lệ (Exception Handling) và quy trình phê duyệt (Review Process) ngay từ những bước đầu tiên.

**[T15-084]** Khi một sản phẩm AI tham gia vào các lĩnh vực nhạy cảm cao như: Tuyển dụng nhân sự, Chấm điểm tín dụng, Y tế và chăm sóc sức khỏe, Giáo dục và chấm điểm, mức độ cẩn trọng và tính tuân thủ pháp lý phải được nâng lên mức tối đa để giảm thiểu rủi ro pháp lý nặng nề.

**[T15-085]** 4. NGHIÊN CỨU NGƯỜI DÙNG CHO SẢN PHẨM AI (USER RESEARCH FOR AI PRODUCTS)

**[T15-086]** Sản phẩm AI thường thất bại không phải vì mô hình toán học yếu, mà vì đội ngũ phát triển ngầm giả định người dùng muốn tự động hóa hoàn toàn (Full Automation), trong khi thực tế người dùng chỉ có nhu cầu hỗ trợ đưa ra quyết định (Decision Support).

**[T15-087]** 4.1. 4 Câu Hỏi Nghiên Cứu Người Dùng Đặc Thù Cho AI

**[T15-088]** 1. User muốn AI tự động thực hiện đến mức độ nào, và ở những bước cụ thể nào họ muốn giữ lại quyền kiểm soát tối cao?

**[T15-089]** 2. Người dùng đặt niềm tin vào AI dựa trên tiêu chí gì: Tốc độ phản hồi cực nhanh, nguồn trích dẫn minh bạch, độ tự tin của mô hình hay kết quả thực nghiệm thực tế?

**[T15-090]** 3. Khi hệ thống AI đưa ra kết quả sai lệch, người dùng mong muốn cơ chế dự phòng (Fallback) nào: Tự chỉnh sửa bằng tay, chuyển hướng trực tiếp đến nhân viên hỗ trợ, hay yêu cầu Agent thử lại tác vụ?

**[T15-091]** 4. Người dùng đang thực sự kỳ vọng Agent đóng vai trò là một trợ lý thừa hành (Assistant), một người bạn đồng hành (Copilot), hay một thực thể thay thế hoàn toàn công việc của họ?

**[T15-092]** 4.2. Mở Rộng Chân Dung Người Dùng (Persona Dimensions) Cho AI

**[T15-093]** Bên cạnh các thông tin cơ bản của một chân dung người dùng thông thường (Vai trò, Mục tiêu, Nỗi đau, Bối cảnh), một Persona thiết kế cho sản phẩm AI bắt buộc phải mở rộng thêm bốn chiều kích đặc thù:

**[T15-094]** • AI Literacy Level (Trình độ hiểu biết và làm việc với AI): Mức độ am hiểu về công nghệ và cách ra lệnh cho AI của đối tượng người dùng.

**[T15-095]** • Automation Willingness (Mức độ sẵn sàng tin tưởng tự động hóa): Sự cởi mở của họ trong việc giao quyền ra quyết định cho thuật toán.

**[T15-096]** • Error Tolerance (Ngưỡng chấp nhận sai sót): Giới hạn mà người dùng có thể chấp nhận khi mô hình đưa ra câu trả lời chưa chính xác.

**[T15-097]** • Explainability Need (Nhu cầu được giải thích): Yêu cầu của người dùng về việc hệ thống phải giải trình logic tại sao lại đưa ra kết quả đó.

**[T15-098]** 4.3. Thiết Kế Vòng Phản Hồi (Feedback Loops)

**[T15-099]** Một hệ thống AI không thể học tập và cải thiện liên tục nếu thiếu đi thiết kế vòng phản hồi để thu thập tín hiệu từ người dùng ngay sau khi ra mắt sản phẩm (Launch):

**[T15-100]** • Explicit Feedback (Phản hồi trực tiếp): Các hành động chủ động của user như bấm nút Thumbs Up/Down, đánh giá số sao (Rating) -> Dùng để xác định nhanh chất lượng dịch vụ mà người dùng cảm nhận được.

**[T15-101]** • Behavioral Signal (Tín hiệu hành vi): Các chỉ báo ngầm như sao chép câu trả lời (Copy), sửa đổi nội dung sinh ra (Rephrase), ghi đè kết quả (Override), hoặc bỏ ngang phiên làm việc (Abandon) -> Giúp phát hiện mức độ tin cậy, điểm ma sát (Friction) và điểm nghẽn trong trải nghiệm.

**[T15-102]** • Outcome Signal (Tín hiệu kết quả cuối cùng): Kết quả thực tế của phiên làm việc như vấn đề được giải quyết triệt để (Resolved), lịch hẹn được đặt thành công (Booked), hay bị chuyển tiếp lên người thật xử lý (Escalated) -> Giúp kết nối trực tiếp chất lượng kỹ thuật của AI với giá trị kinh doanh thực tế.

**[T15-103]** 5. KỸ NGHỆ ĐẶC TẢ YÊU CẦU (REQUIREMENTS ENGINEERING)

**[T15-104]** Chìa khóa cốt lõi của kỹ nghệ đặc tả yêu cầu cho AI là chuyển hóa từ các tuyên bố mơ hồ (Vague Requirements) sang các chỉ số cụ thể, đo lường được và có thể kiểm thử được (Testable Requirements).

**[T15-105]** Nếu đội ngũ kiểm thử (QA/Tester) hoặc kỹ sư (Engineer) nhìn vào đặc tả yêu cầu mà không biết cách thiết kế kịch bản test để xác minh, thì yêu cầu đó được coi là chưa đủ rõ ràng.

**[T15-106]** 5.1. Ví Dụ Chuyển Hóa Đặc Tả Yêu Cầu Từ Mơ Hồ Sang Đo Lường Được

**[T15-107]** • [MƠ HỒ] Yêu cầu mơ hồ: "Agent phải phản hồi nhanh chóng, chính xác và có câu trả lời thông minh."

**[T15-108]** • [ĐO LƯỜNG ĐƯỢC] Yêu cầu đo lường được: "Agent phải trả lời trong thời gian dưới 5 giây ở phân vị p95, trích dẫn chính xác nguồn văn bản nội bộ và tự động escalate sang người thật khi điểm tự tin (confidence score) của mô hình dưới mức 0.7."

**[T15-109]** 5.2. Ba Nhóm Yêu Cầu Bắt Buộc Cho AI Product

**[T15-110]** • Functional Requirements (Yêu cầu chức năng): Mô tả những tác vụ nghiệp vụ cụ thể mà hệ thống AI phải thực hiện. Ví dụ: Tóm tắt nội dung ticket hỗ trợ, phân loại và dán nhãn khách hàng tiềm năng, tra cứu cơ sở tri thức nội bộ.

**[T15-111]** • Non-functional Requirements (Yêu cầu phi chức năng): Các tiêu chuẩn vận hành và bảo vệ trải nghiệm người dùng. Ví dụ: Cam kết độ trễ (Latency SLA), thời gian hoạt động liên tục (Uptime), giới hạn ngân sách chi phí vận hành (Cost Budget) cho mỗi 1,000 lượt gọi.

**[T15-112]** • AI-Specific Requirements (Yêu cầu đặc thù AI): Phản ánh bản chất rủi ro đặc trưng của công nghệ AI. Ví dụ: Ngưỡng chấp nhận ảo giác (Hallucination Threshold), khả năng giải thích nguồn gốc câu trả lời (Explainability), và kịch bản xử lý lỗi khi mô hình thất bại (Fallback behaviors).

**[T15-113]** 5.3. Công Thức Thiết Kế Tiêu Chí Nghiệm Thu (Acceptance Criteria) Cho AI

**[T15-114]** Mọi tiêu chí nghiệm thu của sản phẩm AI cần phải tuân thủ nghiêm ngặt theo cấu trúc cấu trúc điều kiện mẫu:

**[T15-115]** ★ CẤU TRÚC ACCEPTANCE CRITERIA CHUẨN HÓA

**[T15-116]** When [Sự kiện/Kích hoạt xảy ra]...The agent should [Hành vi mong đợi của AI]...Within [Ngưỡng thời gian / Chỉ số đo lường được]...And if [Điều kiện lỗi/Thất bại xảy ra], it should [Hành vi dự phòng - Fallback].

**[T15-117]** Thành phần cấu thành AC: Một Acceptance Criteria hoàn chỉnh bao gồm bốn yếu tố sống còn: Có trigger rõ rệt; Có hành vi mong đợi cụ thể; Có ngưỡng đo lường chuẩn hóa; và có thiết kế xử lý lỗi dự phòng rõ ràng.

**[T15-118]** 6. CẤU TRÚC HỒ SƠ ĐẶC TẢ SẢN PHẨM (PRD ANATOMY FOR AI)

**[T15-119]** Tài liệu Đặc tả Yêu cầu Sản phẩm (PRD) không phải là một văn bản hành chính viết ra để điền cho đủ thủ tục. PRD đóng vai trò là một bản hợp đồng cam kết và đồng thuận cao nhất giữa PM, BA, Engineer và các bên liên quan.

**[T15-120]** 6.1. 8 Thành Phần Cốt Lõi Của Một Bản PRD AI Chuẩn Hóa

**[T15-121]** 1. Problem Statement (Mô tả nỗi đau/Vấn đề thực tế cần giải quyết)

**[T15-122]** 2. Target User (Xác định rõ ràng chân dung nhóm người dùng mục tiêu)

**[T15-123]** 3. Success Metrics (Hệ thống chỉ số đo lường thành công đa tầng)

**[T15-124]** 4. Technical Architecture (Kiến trúc kỹ thuật và luồng tích hợp hệ thống ở mức cao)

**[T15-125]** 5. Feature Requirements (Mô tả chi tiết các tính năng chức năng của AI)

**[T15-126]** 6. Non-functional Requirements (Các tiêu chuẩn phi chức năng về vận hành và an toàn)

**[T15-127]** 7. Acceptance Criteria (Hệ thống tiêu chí nghiệm thu kiểm thử được)

**[T15-128]** 8. Risks & Mitigations (Bảng quản trị rủi ro kèm giải pháp khắc phục)

**[T15-129]** 6.2. Tháp Chỉ Số Thành Công (Success Metrics Hierarchy)

**[T15-130]** Một trong những lỗi nghiêm trọng nhất của PM/BA khi thiết kế chỉ số là viết chung chung kiểu "độ chính xác càng cao càng tốt". Hệ thống chỉ số cần được cấu trúc phân tầng rõ rệt để định hình giá trị:

**[T15-131]** Tầng chỉ số

**[T15-132]** Ví dụ thực tế

**[T15-133]** Câu hỏi cốt lõi PM/BA phải trả lời

**[T15-134]** Business KPI (Chỉ số kinh doanh)

**[T15-135]** Chi phí tiết kiệm được (Cost saved), Doanh thu tăng thêm (Revenue), Điểm hài lòng khách hàng (CSAT).

**[T15-136]** Sản phẩm AI này mang lại giá trị thực tiễn gì cho tổ chức/doanh nghiệp?

**[T15-137]** Product Metric (Chỉ số sản phẩm)

**[T15-138]** Tỷ lệ hoàn thành tác vụ (Task completion), Tỷ lệ người dùng quay lại (Repeat usage), Tỷ lệ chuyển tiếp lên người thật (Escalation rate).

**[T15-139]** Người dùng có thực sự tương tác, sử dụng và hoàn thành được công việc của họ không?

**[T15-140]** AI Metric (Chỉ số kỹ thuật AI)

**[T15-141]** Độ chính xác (Accuracy), Độ trễ (Latency), Tỷ lệ trích dẫn nguồn đúng (Citation rate).

**[T15-142]** Hệ thống AI có vận hành đủ tốt và ổn định để nâng đỡ cho các chỉ số sản phẩm phía trên không?

**[T15-143]** Sơ đồ: Hệ thống phân tầng chỉ số thành công - Success Metrics Hierarchy

**[T15-144]** 6.3. Các Sai Lầm Phổ Biến (Anti-patterns) Khi Viết PRD Cho AI

**[T15-145]** • Chỉ tập trung mô tả tính năng công nghệ mà hoàn toàn bỏ qua việc định hình vấn đề (Problem) và chân dung người dùng mục tiêu (Target User).

**[T15-146]** • Xác định chỉ số đo lường mơ hồ theo kiểu định tính ("càng cao càng tốt", "nhanh nhất có thể"), không thiết lập được đường cơ sở (Baseline) hay dải ngưỡng tối thiểu (Threshold).

**[T15-147]** • Thiếu hụt hoàn toàn các yêu cầu phi chức năng quan trọng liên quan trực tiếp đến trải nghiệm thực tế như: Độ trễ, chi phí vận hành, bảo mật riêng tư dữ liệu và quy trình escalate.

**[T15-148]** • Bỏ qua hoàn toàn phần quản trị rủi ro (Risk section), dẫn đến việc khi hệ thống gặp lỗi thực tế (bias, privacy leak, adoption thấp) thì đội ngũ mới bắt đầu tranh luận giải pháp chữa cháy.

**[T15-149]** • Vội vã đưa ra giải pháp công nghệ cụ thể quá sớm (ví dụ: chỉ định dùng model GPT-4o) khi chưa chứng minh được giá trị thực tế mang lại cho người dùng và mức độ tương thích với quy trình làm việc (Workflow fit).

**[T15-150]** 7. THIẾT KẾ USER STORIES CHO AI

**[T15-151]** Một User Story tốt cho AI phải đủ rõ ràng để kỹ sư lập trình hiểu cách xây dựng, chuyên viên kiểm thử biết cách thiết kế kịch bản test, và các bên liên quan dễ dàng đạt được sự đồng thuận cao.

**[T15-152]** 7.1. Template Thiết Kế User Story Chuẩn Hóa

**[T15-153]** ★ TEMPLATE USER STORY

**[T15-154]** As a [Persona - Vai trò người dùng thực tế],I want [AI Capability - Khả năng cụ thể của hệ thống AI],So that [Business Value - Giá trị nghiệp vụ mang lại].

**[T15-155]** Lưu ý quan trọng: Vai trò phải là một con người cụ thể trải nghiệm sản phẩm, không được viết là "Hệ thống"; Khả năng của AI phải mô tả hành vi trực quan của hệ thống, không được viết tên model kỹ thuật; Giá trị nghiệp vụ phải liên kết chặt chẽ với KPI hoặc giải quyết trực tiếp một nỗi đau cụ thể.

**[T15-156]** 7.2. Phân Tích Các Ví Dụ User Story Thực Tế Theo Use Cases

**[T15-157]** Dưới đây là đặc tả chi tiết 3 User Stories chuẩn hóa cho các trường hợp ứng dụng phổ biến:

**[T15-158]** Use Case 1 (AI Support Agent): "As a Support Agent (Nhân viên hỗ trợ), I want AI to draft the first response based on past policy and ticket context, so that I can resolve routine cases faster."

**[T15-159]** • • Happy path: Agent tự động soạn bản thảo câu trả lời nháp bám sát nguồn tài liệu trong vòng dưới 6 giây.

**[T15-160]** • • Edge case: Nhận diện và xử lý tốt các câu hỏi mơ hồ, câu hỏi thiếu thông tin ngữ cảnh hoặc sử dụng tiếng lóng từ khách hàng.

**[T15-161]** • • Error state: Trường hợp không tìm thấy tài liệu nguồn phù hợp hoặc công cụ bị timeout, hệ thống tự động đưa ra câu trả lời xin lỗi và chuyển thẳng cho nhân viên hỗ trợ xử lý.

**[T15-162]** Use Case 2 (Tra cứu chính sách nội bộ): "As an HR Staff Member (Nhân viên nhân sự), I want AI to answer HR policy questions with precise source citations, so that I can respond consistently and reduce manual lookup time."

**[T15-163]** • • Happy path: Agent trả lời chính xác, hiển thị rõ ràng đường dẫn liên kết và số trang của văn bản gốc trích dẫn trong vòng dưới 5 giây.

**[T15-164]** • • Edge case: Người dùng hỏi các chính sách cũ đã hết hiệu lực hoặc hỏi các câu hỏi so sánh giữa hai văn bản chính sách khác nhau.

**[T15-165]** • • Error state: Khi độ tự tin của câu trả lời dưới ngưỡng thiết lập (ví dụ < 80%), Agent hiển thị thông báo giới hạn tri thức và đề xuất người dùng liên hệ với phòng ban pháp chế.

**[T15-166]** Use Case 3 (Ticket Routing Agent): "As an Operations Lead (Trưởng bộ phận vận hành), I want AI to suggest the right support queue for incoming requests, so that misrouting drops and overall response time improves."

**[T15-167]** • • Happy path: Tự động phân tích nội dung ticket và đề xuất phân luồng chính xác phòng ban xử lý ngay từ lần đầu tiên với độ trễ dưới 2 giây.

**[T15-168]** • • Edge case: Ticket chứa nội dung hỗn hợp liên quan đến nhiều phòng ban khác nhau hoặc ticket viết bằng ngôn ngữ hỗn hợp.

**[T15-169]** • • Error state: Khi không thể xác định được phân luồng phù hợp, ticket tự động được đẩy vào hàng đợi chung (General Queue) để phân loại thủ công.

**[T15-170]** 8. DANH MỤC QUẢN TRỊ RỦI RO (RISK REGISTER)

**[T15-171]** Thiết lập tư duy quản trị rủi ro một cách tường minh, rõ ràng và có số liệu định lượng (Risk thinking must be explicit) giúp đội ngũ phát triển biết rõ hệ thống đang được xây dựng trong điều kiện rào chắn nào, có thể ship ở mức độ nào và khi nào bắt buộc phải dừng.

**[T15-172]** 8.1. Phân Loại Rủi Ro AI (AI Risk Taxonomy)

**[T15-173]** Hệ thống rủi ro của sản phẩm AI được phân nhóm thành 5 danh mục chính kèm phương án giảm thiểu cụ thể:

**[T15-174]** • Technical Risk (Rủi ro kỹ thuật): Ảo giác mô hình (Hallucination), lỗi gọi công cụ (tool failure), độ trễ phản hồi tăng đột biến (latency spike) -> Giải pháp: Thiết lập hệ thống đánh giá tự động (Evaluation Framework), thiết kế cơ chế dự phòng (fallback), cấu hình thời gian chờ (timeouts) và hệ thống giám sát (monitoring).

**[T15-175]** • Data Risk (Rủi ro dữ liệu): Rò rỉ thông tin định danh cá nhân (PII Leak), dữ liệu tri thức bị lỗi thời (stale source), gán nhãn dữ liệu kém chất lượng (bad labeling) -> Giải pháp: Tích hợp bộ lọc ẩn danh dữ liệu (masking), kiểm soát phân quyền truy cập chặt chẽ (access control), quy trình kiểm định chất lượng dữ liệu đầu vào (data QA).

**[T15-176]** • Business Risk (Rủi ro kinh doanh): Tỷ lệ người dùng chấp nhận sử dụng thấp (adoption), không chứng minh được hiệu quả đầu tư (unclear ROI), thiết kế luồng quy trình nghiệp vụ không tương thích (wrong workflow fit) -> Giải pháp: Tiến hành thử nghiệm giới hạn (pilot), thiết lập bộ chỉ số thành công rõ ràng, xác thực sớm lý thuyết hành trình công việc (JTBD validation).

**[T15-177]** • Ethical Risk (Rủi ro đạo đức): Đưa ra các quyết định bất công, thiên lệch (unfair outcome), mô hình hoạt động như một hộp đen không thể giải thích (opaque decision) -> Giải pháp: Thiết lập quy trình kiểm duyệt có con người tham gia (human review), hiển thị cảnh báo rõ ràng (disclosure), định kỳ lấy mẫu kiểm toán dữ liệu (audit sample).

**[T15-178]** • Regulatory Risk (Rủi ro tuân thủ): Thiếu hụt hệ thống ghi nhật ký hoạt động (logging), vi phạm các quy định pháp lý về dữ liệu và an toàn AI (compliance gap) -> Giải pháp: Thiết kế tài liệu hóa chi tiết hệ thống, xây dựng luồng phê duyệt nghiêm ngặt, định kỳ đánh giá lại chính sách bảo mật.

**[T15-179]** 8.2. Ma Trận Rủi Ro (Risk Matrix: Likelihood x Impact)

**[T15-180]** Mức độ nghiêm trọng của mỗi rủi ro được định lượng bằng công thức: Điểm rủi ro = Khả năng xảy ra (Likelihood) x Mức độ ảnh hưởng (Impact). Cả hai chỉ số đều được đánh giá trên thang điểm từ 1 (Rất thấp) đến 5 (Rất cao).

**[T15-181]** ID rủi ro

**[T15-182]** Mô tả rủi ro cụ thể

**[T15-183]** Khả năng xảy ra (L)

**[T15-184]** Mức độ ảnh hưởng (I)

**[T15-185]** Điểm rủi ro (L x I)

**[T15-186]** Nhóm hành động khuyến nghị

**[T15-187]** R1

**[T15-188]** Privacy leak (Rò rỉ dữ liệu riêng tư của người dùng)

**[T15-189]** 2 (Thấp)

**[T15-190]** 5 (Rất cao)

**[T15-191]** 10

**[T15-192]** Mitigate & Escalate (Giảm thiểu & Báo cáo cấp cao)

**[T15-193]** R2

**[T15-194]** Hallucination on sensitive advice (Ảo giác ở các lời khuyên nhạy cảm)

**[T15-195]** 3 (Trung bình)

**[T15-196]** 5 (Rất cao)

**[T15-197]** 15

**[T15-198]** Reduce & Escalate / Go-No-Go threshold

**[T15-199]** R3

**[T15-200]** Cost spike (Chi phí vận hành mô hình tăng vọt đột biến)

**[T15-201]** 4 (Cao)

**[T15-202]** 3 (Trung bình)

**[T15-203]** 12

**[T15-204]** Mitigate & Monitor (Giảm thiểu & Giám sát chặt)

**[T15-205]** R4

**[T15-206]** Adoption risk (Tỷ lệ người dùng chấp nhận sản phẩm thấp)

**[T15-207]** 3 (Trung bình)

**[T15-208]** 4 (Cao)

**[T15-209]** 12

**[T15-210]** Reduce & Mitigate (Thử nghiệm pilot và tối ưu JTBD)

**[T15-211]** R5

**[T15-212]** Minor wording inconsistency (Không đồng nhất nhỏ trong câu chữ phản hồi)

**[T15-213]** 2 (Thấp)

**[T15-214]** 1 (Rất thấp)

**[T15-215]** 2

**[T15-216]** Monitor (Chỉ cần theo dõi thông thường)

**[T15-217]** Sơ đồ: Ma trận định lượng rủi ro Likelihood x Impact thực tế

**[T15-218]** 8.3. Tiêu Chí Quyết Định Go / No-Go

**[T15-219]** • [GO] Go (Đồng ý triển khai): Áp dụng khi tất cả các rủi ro mức độ cao đều đã có phương án giảm thiểu (mitigation) cực kỳ rõ ràng, các tiêu chí nghiệm thu đo lường được bằng số liệu và xác định rõ chủ sở hữu chịu trách nhiệm (owner) xử lý.

**[T15-220]** • [CONDITIONAL GO] Conditional Go (Đồng ý có điều kiện): Triển khai thử nghiệm trong một phạm vi giới hạn nhỏ (pilot), bắt buộc phải có cơ chế con người kiểm soát (human-in-the-loop), thiết lập các chốt chặn an toàn (guardrails) nghiêm ngặt và thu hẹp bối cảnh sử dụng (scope).

**[T15-221]** • [NO-GO] No-Go (Không triển khai): Kích hoạt khi hệ thống chưa xử lý triệt để các rủi ro lớn liên quan đến bảo mật riêng tư dữ liệu (privacy) hoặc rủi ro pháp lý tuân thủ (compliance gap); hoặc chưa thiết lập được cơ chế dự phòng (fallback) đáng tin cậy; hoặc chưa chứng minh được rõ ràng giá trị mang lại cho người dùng cuối.

**[T15-222]** 9. TIÊU CHUẨN THỰC HÀNH LAB 5 & KHUNG PRD SKELETON

**[T15-223]** Mục tiêu thực hành của bài Lab 5 là giúp học viên chuyển hóa toàn bộ kiến thức lý thuyết sản phẩm thành một bộ tài liệu đặc tả PRD và Ma trận Rủi ro thực tế, có tính hành động cao.

**[T15-224]** 9.1. Yêu Cầu Bàn Giao Của Bài Lab 5 (Deliverable Checklist)

**[T15-225]** • Hồ sơ tài liệu PRD dài từ 3-5 trang, bao gồm đầy đủ 8 phần cấu trúc cốt lõi đã học.

**[T15-226]** • Bảng Ma trận Rủi ro định lượng (Likelihood x Impact) bao phủ ít nhất 5 rủi ro bắt buộc bao gồm: hallucination, bias, privacy, cost, adoption.

**[T15-227]** • Thiết kế tối thiểu 3 User Stories hoàn chỉnh có kèm theo tiêu chí nghiệm thu (Acceptance Criteria) và kịch bản xử lý ngoại lệ (failure handling).

**[T15-228]** • Bản ghi chú quyết định (Decision Note) đề xuất phương án Go / Conditional Go / No-Go kèm theo lập luận chứng minh rõ ràng.

**[T15-229]** 9.2. Khung PRD Tối Thiểu Tham Khảo (PRD Skeleton - Internal Policy Assistant)

**[T15-230]** Dưới đây là cấu trúc khung PRD rút gọn được thiết kế chuẩn mực làm điểm tựa khởi đầu cho dự án:

**[T15-231]** Problem (Vấn đề): Bộ phận Nhân sự (HR Team) hiện đang tốn quá nhiều thời gian và nguồn lực để giải quyết thủ công các câu hỏi lặp đi lặp lại của nhân viên về các chính sách, quy định phúc lợi nội bộ.

**[T15-232]** Target User (Người dùng mục tiêu): Nhân viên phòng HR (HR staff) và các quản lý cấp trung (Line Managers) cần tra cứu thông tin chính sách một cách nhanh chóng, chính xác tuyệt đối và dẫn nguồn tài liệu gốc rõ ràng.

**[T15-233]** Success Metrics (Chỉ số thành công): Hệ chỉ số gồm ba tầng đo lường rõ ràng:

**[T15-234]** • Chỉ số kinh doanh: Thời gian phản hồi trung bình (Time-to-answer) của HR giảm 50%.

**[T15-235]** • Chỉ số sản phẩm: Tỷ lệ câu hỏi tự tra cứu thành công mà không cần chuyển tiếp lên nhân sự (Escalation rate) dưới 15%.

**[T15-236]** • Chỉ số AI: Tỷ lệ phản hồi dẫn chính xác nguồn văn bản gốc (Citation coverage) đạt trên 95%.

**[T15-237]** Risks & Mitigations (Rủi ro & Biện pháp): Bảng quản trị hai rủi ro hàng đầu:

**[T15-238]** • Rủi ro 1: Mô hình ảo giác thông tin chính sách (Hallucination on policy interpretation) -> Giảm thiểu: Áp dụng kỹ thuật RAG giới hạn chặt chẽ tri thức trong văn bản gốc, thiết lập quy trình kiểm duyệt câu trả lời của HR.

**[T15-239]** • Rủi ro 2: Rò rỉ thông tin cá nhân nhạy cảm trong tài liệu được tải lên hệ thống (PII leakage in documents) -> Giảm thiểu: Áp dụng công cụ tự động phát hiện và che giấu thông tin nhạy cảm (PII Masking) trước khi nạp vào vector database.

**[T15-240]** 10. TÀI LIỆU THAM KHẢO & LIÊN KẾT NGUỒN CHÍNH THỨC

**[T15-241]** Để hỗ trợ cho việc tra cứu tự động và mở rộng nghiên cứu chuyên sâu của các hệ thống AI Agent khác, dưới đây là danh mục tổng hợp toàn bộ các đường dẫn liên kết tài nguyên học thuật chính thức được sử dụng trong bài học:

**[T15-242]** 1. Google PAIR: Google PAIR - People + AI Guidebook (Phiên bản cập nhật thiết kế trải nghiệm người dùng với AI):

**[T15-243]** Đường dẫn chính thức: pair.withgoogle.com/guidebook-v2/

**[T15-244]** 2. NIST AI RMF 1.0: NIST - AI Risk Management Framework (Khung quản trị rủi ro AI tiêu chuẩn của Viện Tiêu chuẩn và Công nghệ Quốc gia Hoa Kỳ):

**[T15-245]** Đường dẫn chính thức: nist.gov

**[T15-246]** 3. EU AI Act: Liên minh Châu Âu - European Union AI Act (Văn bản pháp lý và các quy định chính thức về Đạo luật Quản lý AI):

**[T15-247]** Đường dẫn chính thức: eur-lex.europa.eu

**[T15-248]** 4. Duke University: Đại học Duke - Chương trình chuyên sâu về Quản trị Sản phẩm AI (AI Product Management Specialization):

**[T15-249]** Đường dẫn chính thức: coursera.org

**[T15-250]** 5. Kho lưu trữ Slides & Code chính thức: Kho lưu trữ mã nguồn học tập, slides bài giảng và hệ thống tài liệu hướng dẫn thực hành chính thức:

**[T15-251]** Đường dẫn chính thức: github.com/aicb-vinuni

**[T15-252]** 6. Lab 5 Template chính thức: Đường dẫn liên kết tải về tệp tin mẫu (Lab Template) hướng dẫn soạn thảo tài liệu PRD và Risk Matrix của Ngày 5:

**[T15-253]** Đường dẫn chính thức: bit.ly/aicb-day05-lab
