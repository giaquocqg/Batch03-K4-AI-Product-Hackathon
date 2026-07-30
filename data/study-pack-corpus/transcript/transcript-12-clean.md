# Study Pack corpus - Day 02 - Từ yêu cầu mơ hồ đến Problem Statement

> Corpus version: `study-pack-corpus-v1`
> Combined source SHA-256: `d9ff0da80192992871546bbffaf0f79567c061d3be189272d715a0811f1055a2`
> Original source lines: 315-477
> Transformation: one non-empty source line equals one citation segment;
> no source text is summarized, paraphrased, or silently truncated.

**[T12-001]** [Day-02] Tóm tắt Giáo trình Day 02: Từ Yêu Cầu Mơ Hồ Đến Problem Statement Rõ Ràng

**[T12-002]** 1. Ba Trụ Cột Nền Tảng Của Một Sản Phẩm AI (AI Product)

**[T12-003]** Một sản phẩm tích hợp trí tuệ nhân tạo (AI Product) bản chất vẫn là một sản phẩm hoàn chỉnh, kế thừa chứ không thay thế các nguyên lý phát triển sản phẩm truyền thống. Để xây dựng thành công một sản phẩm AI thực tế, cần sự giao thoa chặt chẽ giữa ba trụ cột cốt lõi:

**[T12-004]** AI Engineering: triển khai các kỹ thuật hệ thống thực tế như Retrieval-Augmented Generation (RAG), AI Agent, Guardrails (hệ thống rào chắn), Evaluation (đánh giá hiệu năng) và vận hành hệ thống AI trong môi trường production.

**[T12-005]** Product Thinking: định hình và xác định đúng bài toán cần giải quyết, thấu hiểu sâu sắc người dùng để tránh xây dựng các tính năng không mang lại giá trị thực tế.

**[T12-006]** Design Thinking: thiết kế trải nghiệm dựa trên mô hình tư duy của người dùng (Mental Model), cơ chế phản hồi tương tác (Feedback) và tối ưu hóa trải nghiệm khi hệ thống AI xảy ra sai sót (Graceful Failure).

**[T12-007]** Các nguồn học liệu và sách giáo khoa chính được sử dụng xuyên suốt chương trình:

**[T12-008]** Tài liệu / Tác giả

**[T12-009]** Phạm vi kiến thức

**[T12-010]** Vai trò trong chương trình

**[T12-011]** People + AI Guidebook(Google PAIR)

**[T12-012]** Cẩm nang 6 chương thiết kế sản phẩm AI lấy con người làm trung tâm (User Needs + Success, Data Collection, Mental Models, Explainability, Feedback, Errors).

**[T12-013]** Xương sống lý thuyết định hình thành công của sản phẩm (Chương 1 là trọng tâm định lượng và thiết kế bài toán).

**[T12-014]** AI Engineering(Chip Huyen, O'Reilly 2025)

**[T12-015]** Kiến trúc hệ thống AI hoàn chỉnh qua các giai đoạn (Planning, Expectations, Model Selection, Architecture Evolution, Eval-Driven Development, Monitoring).

**[T12-016]** Tài liệu kỹ thuật định hướng triển khai hệ thống, rào chắn bảo vệ và vận hành thực tế.

**[T12-017]** Inspired (Marty Cagan) &Design of Everyday Things (Don Norman)

**[T12-018]** Tư duy sản phẩm định giá trị và thiết kế lấy con người làm trung tâm (HCD).

**[T12-019]** Định vị bài toán, tối ưu hóa điểm chạm và cơ chế phản hồi tương tác khi AI sai sót.

**[T12-020]** 2. Problem Discovery: Khám Phá Và Tìm Đúng Vấn Đề Trước Khi Giải Quyết

**[T12-021]** Một trong những sai lầm kinh điển nhất khi phát triển AI là xây dựng giải pháp xuất sắc cho một bài toán sai lệch. Điều này thậm chí còn tồi tệ hơn việc không có giải pháp nào. Triết lý thiết kế lấy con con người làm trung tâm (HCD) của Don Norman nhấn mạnh: 'Do not solve the problem I am asked to solve.' - cần đi sâu tìm ra vấn đề thực sự ẩn sau yêu cầu ban đầu.

**[T12-022]** Mô hình Double Diamond (Kim cương kép)

**[T12-023]** Mô hình Double Diamond chia quá trình thiết kế thành hai giai đoạn lớn với hai vòng lặp phân kỳ (mở rộng góc nhìn) và hội tụ (định nghĩa chính xác):

**[T12-024]** Diamond 1 - Tìm đúng vấn đề (Discover): Khám phá các vấn đề căn bản bằng cách quan sát thực tế (Observation), phỏng vấn người dùng (User Interview), khảo sát (Survey), nhật ký hành vi (Diary Study), phân tích dữ liệu và bản đồ các bên liên quan (Stakeholder Mapping).

**[T12-025]** Diamond 1 - Tìm đúng vấn đề (Define): Định nghĩa và chọn lọc bài toán gốc dựa vào dữ liệu bằng sơ đồ đồng cảm (Affinity Mapping), kỹ thuật 5 Whys, ma trận Tác động - Nỗ lực (Impact-Effort), biểu quyết bằng chấm tròn (Dot Voting) và câu hỏi mở hướng giải quyết (How Might We). Kết quả là một phát biểu bài toán (Problem Statement) hoàn chỉnh.

**[T12-026]** Diamond 2 - Tìm đúng giải pháp (Develop & Deliver): Phát triển nhiều giải pháp tiềm năng, tạo mẫu thử nhanh (Prototype) và kiểm tra (Test) liên tục.

**[T12-027]** Bộ câu hỏi phỏng vấn khai phá bài toán (Discovery Interview)

**[T12-028]** Khi phỏng vấn các bên liên quan (stakeholder) để định hình vấn đề, bộ thẻ câu hỏi #2 cung cấp 5 câu hỏi cốt lõi để thu thập thông tin rành mạch:

**[T12-029]** Vấn đề nhức nhối nhất là gì? Tần suất lặp lại trong ngày hoặc trong tuần ra sao?

**[T12-030]** Quy trình làm việc (workflow) hiện tại như thế nào? Công cụ nào được sử dụng ở từng bước, và ai bàn giao công việc cho ai?

**[T12-031]** Thiệt hại (cost) cụ thể do vấn đề gây ra là gì? Đo lường bằng hao phí thời gian, chi phí tài chính, cam kết dịch vụ (SLA) hay tỷ lệ chuyển đổi?

**[T12-032]** Hậu quả nếu hệ thống AI sai sót là gì? Khâu nào cần con người tham gia kiểm soát (HITL/phê duyệt), hay AI chỉ đưa ra gợi ý?

**[T12-033]** Ai là người có quyền phê duyệt dự án (nói YES)? Chỉ số hiệu quả (metric) và mức độ rủi ro (risk) nào quyết định việc đầu tư?

**[T12-034]** Lưu ý: Nếu đối tác không thể mô tả được quy trình hiện tại và thiệt hại cụ thể khi xảy ra lỗi, mọi đề xuất giải pháp AI đều chỉ là phỏng đoán thiếu căn cứ.

**[T12-035]** 3. Problem Statement: Khung Định Hình Bài Toán Hệ Thống AI

**[T12-036]** Để chuyển đổi một điểm đau (pain point) mơ hồ thành một bài toán rõ ràng sẵn sàng cho triển khai kỹ thuật, chương trình thiết lập khung Problem Statement hoàn chỉnh gồm 9 trường thông tin (chia làm 6 yếu tố bài toán cốt lõi và 3 yếu tố quyết định AI):

**[T12-037]** Yếu tố

**[T12-038]** Định nghĩa trường thông tin

**[T12-039]** Ví dụ mẫu: Case Hỗ trợ Trợ giảng (TA/Lab Coach)

**[T12-040]** 1. Actor(Đối tượng)

**[T12-041]** Đối tượng chịu ảnh hưởng trực tiếp từ vấn đề.

**[T12-042]** Lab Coach hỗ trợ các nhóm học viên trong lớp học quy mô lớn 1000 học viên.

**[T12-043]** 2. Workflow(Quy trình)

**[T12-044]** Quy trình vận hành hiện tại gồm các bước cụ thể nào.

**[T12-045]** Học viên đặt câu hỏi -> Lab Coach nghiên cứu ngữ cảnh -> Phản hồi / yêu cầu làm rõ -> Học viên cập nhật bài.

**[T12-046]** 3. Bottleneck(Nút thắt)

**[T12-047]** Khâu nào gặp tình trạng chậm trễ, lặp lại, dễ sai sót.

**[T12-048]** Nhiều câu hỏi trùng lặp hoặc thiếu thông tin nền tảng; Lab Coach mất nhiều thời gian rà soát thủ công.

**[T12-049]** 4. Impact(Tác động)

**[T12-050]** Tổn thất lượng hóa cụ thể (thời gian, chi phí, SLA, chất lượng).

**[T12-051]** Học viên phải chờ phản hồi lâu; Lab Coach bị quá tải, không có thời gian cho câu hỏi phức tạp hơn.

**[T12-052]** 5. Success Metric(Chỉ số thành công)

**[T12-053]** Chỉ số định lượng đo lường sự cải thiện.

**[T12-054]** Giảm tỷ lệ câu hỏi lặp cần duyệt thủ công; rút ngắn thời gian phản hồi trung bình; không tăng tỷ lệ định hướng sai.

**[T12-055]** 6. Boundary(Ranh giới)

**[T12-056]** Giới hạn những gì AI KHÔNG được phép tự quyết.

**[T12-057]** AI không tự đánh giá hoặc chấm điểm bài tập; chỉ hỗ trợ gợi ý làm rõ và điều phối quy trình hỗ trợ.

**[T12-058]** 7. AI Intervention(Điểm can thiệp)

**[T12-059]** Điểm cụ thể trong quy trình mà AI sẽ nhảy vào hỗ trợ.

**[T12-060]** Ngay sau khi học viên gửi câu hỏi hoặc nộp Problem Card thiếu thông tin ngữ cảnh đầu vào.

**[T12-061]** 8. Decision Level(Cấp độ kỹ thuật)

**[T12-062]** Giải pháp kỹ thuật lựa chọn: Rule, Workflow hay Agent.

**[T12-063]** Workflow: AI tự động phát hiện thông tin còn thiếu; Lab Coach phê duyệt thủ công các câu hỏi chuyên sâu.

**[T12-064]** 9. Risk & HITL(An toàn & Con người)

**[T12-065]** Cách xử lý khi AI sai sót và quy trình con người kiểm soát.

**[T12-066]** Rủi ro: AI định hướng sai hướng thực hành -> Giải pháp: Lab Coach kiểm duyệt trước khi gửi phản hồi cuối cùng.

**[T12-067]** 4. Thẩm Định Ứng Dụng AI: Khung Quyết Định Theo Google PAIR

**[T12-068]** Trí tuệ nhân tạo không phải là lời giải cho mọi bài toán. Theo Google PAIR Guidebook (Chương 1), quyết định có nên ứng dụng AI được thực hiện qua 3 bước chặt chẽ:

**[T12-069]** Bước 1: Giao điểm giữa nhu cầu thực tế và thế mạnh của AI

**[T12-070]** Chỉ nên làm AI khi bài toán nằm trong nhóm các tác vụ mà AI có lợi thế vượt trội so với các quy tắc luật tĩnh (rule/heuristic).

**[T12-071]** ✓ Các trường hợp AI có ưu thế (AI probably better):

**[T12-072]** Gợi ý nội dung theo từng cá nhân (Personalization / Recommendation).

**[T12-073]** Dự đoán các sự kiện tương lai dựa trên dữ liệu lịch sử (Prediction).

**[T12-074]** Hiểu ngôn ngữ tự nhiên viết tự do của người dùng (Natural Language Understanding).

**[T12-075]** Nhận diện cả một lớp thực thể (ví dụ: nhận diện khuôn mặt, vật thể).

**[T12-076]** Phát hiện các sự kiện hiếm và biến đổi theo thời gian (ví dụ: phát hiện gian lận).

**[T12-077]** Hệ thống trợ lý tự chủ (Agent/Bot) cho một lĩnh vực chuyên biệt.

**[T12-078]** Giao diện động thay thế cho các layout cố định, tĩnh.

**[T12-079]** ✗ Các trường hợp AI KHÔNG tốt hơn (AI probably NOT better):

**[T12-080]** Khi cần duy trì tính nhất quán và dự đoán được (ví dụ: vị trí các nút chức năng cốt lõi).

**[T12-081]** Thông tin tĩnh, cố định và ít thay đổi (hiển thị trực tiếp tối ưu hơn).

**[T12-082]** Lỗi sai sót của hệ thống quá tốn kém (chi phí một lần sai lớn hơn nhiều lợi ích của nhiều lần đúng).

**[T12-083]** Yêu cầu tính minh bạch tuyệt đối, truy vết rõ ràng từng bước.

**[T12-084]** Cần tối ưu tốc độ tối đa và chi phí vận hành cực thấp.

**[T12-085]** Các tác vụ mang ý nghĩa cá nhân sâu sắc mà người dùng thực sự muốn tự tay làm.

**[T12-086]** Bước 2: Xác định vai trò - Automate (Tự động hóa) hay Augment (Hỗ trợ)?

**[T12-087]** Automate (AI làm thay): Thay thế hoàn toàn con người. Chọn khi tác vụ nhàm chán, nguy hiểm, cần mở rộng quy mô lớn, hoặc có một đáp án đúng thống nhất. Đo lường thành công bằng hiệu suất tăng, giảm tải công việc tẻ nhạt.

**[T12-088]** Augment (Con người kiểm soát): Hỗ trợ và tăng cường năng lực con người. Chọn khi người dùng thích tự làm, tác vụ có mức độ rủi ro cao (pháp lý, tài chính, sức khỏe), hoặc kết quả cần trách nhiệm cá nhân. Đo lường bằng mức độ hài lòng, cảm giác kiểm soát và sự sáng tạo được tăng lên.

**[T12-089]** Bước 3: Thiết lập hàm thưởng và cơ chế đánh đổi (Precision vs. Recall)

**[T12-090]** Hệ thống AI không bao giờ đạt độ chính xác 100%. Thiết kế hệ thống đòi hỏi phải vặn nút đánh đổi giữa Precision (Độ chính xác) và Recall (Độ phủ):

**[T12-091]** Ưu tiên Precision cao: Đo bằng TP / (TP + FP). Hệ thống ít đưa ra gợi ý, nhưng gợi ý nào cũng chắc chắn đúng. Hệ quả là bỏ sót nhiều trường hợp thực sự cần hỗ trợ (nhiều False Negative).

**[T12-092]** Ưu tiên Recall cao: Đo bằng TP / (TP + FN). Hệ thống bao trọn mọi trường hợp cần trợ giúp để không ai bị bỏ lại phía sau. Hệ quả là sinh ra nhiều cảnh báo giả/gợi ý sai lệch, buộc con người phải lọc thủ công nhiều hơn (nhiều False Positive).

**[T12-093]** 5. Cấp Độ Giải Pháp Kỹ Thuật: Rule, Workflow, Hay Agent

**[T12-094]** Một giải pháp thực tế luôn ưu tiên cấp độ đơn giản nhất đủ để giải quyết bài toán cốt lõi. Tăng độ phức tạp kỹ thuật không đồng nghĩa với tối ưu hiệu quả.

**[T12-095]** Cấp độ 1 - Rule-based (Luật tĩnh): Áp dụng khi logic phân nhánh rành mạch (If/Else), đầu vào ổn định, yêu cầu kết quả dự đoán trước và kiểm soát tuyệt đối 100% (ví dụ: tính thuế, chặn email spam theo từ khóa, auto-reply theo mẫu biểu).

**[T12-096]** Cấp độ 2 - Workflow (Quy trình): Áp dụng khi đầu vào đa dạng không thể viết hết luật tĩnh, nhưng các bước quy trình đã định hình rõ. Từng công đoạn cần AI hỗ trợ xử lý ngôn ngữ hoặc đánh giá, có con người kiểm tra trước khi gửi.

**[T12-097]** Cấp độ 3 - Agent (Tác nhân tự chủ): Áp dụng khi không thể xác định trước toàn bộ các bước thực thi, môi trường nhiều biến số đòi hỏi thay đổi kế hoạch linh hoạt, cần tương tác nhiều công cụ và tự động ra quyết định giữa các bước.

**[T12-098]** Cây quyết định lựa chọn cấp độ giải pháp phù hợp:

**[T12-099]** Bước kiểm tra

**[T12-100]** Điều kiện / Rẽ nhánh

**[T12-101]** Quyết định kỹ thuật

**[T12-102]** 1. Quy mô bài toán

**[T12-103]** Tần suất & Tác động KHÔNG đủ lớn?Tần suất & Tác động CÓ đủ lớn?

**[T12-104]** -> Chưa đáng đầu tư AI - Giải thủ công trước-> Chuyển sang Bước 2

**[T12-105]** 2. Đặc điểm logic

**[T12-106]** Logic xử lý rành mạch, input ổn định?Logic phức tạp, đầu vào biến thiên?

**[T12-107]** -> Sử dụng RULE / Script tĩnh-> Chuyển sang Bước 3

**[T12-108]** 3. Độ linh hoạt quy trình

**[T12-109]** Các bước quy trình cố định?Không thể định trước các bước, cần tự điều phối?

**[T12-110]** -> Xây dựng WORKFLOW tích hợp AI-> Cân nhắc sử dụng AGENT + Chốt chặn

**[T12-111]** 6. Workflow Patterns: Các Mô Hình Kiến Trúc Theo Anthropic

**[T12-112]** Khi xây dựng các hệ thống AI phức tạp hơn mức Prompt đơn lẻ, Anthropic (2024) đề xuất các mẫu thiết kế quy trình (Workflow Patterns). Mỗi pattern là một sự đánh đổi (tradeoff) rõ rệt:

**[T12-113]** Mô hình (Pattern)

**[T12-114]** Được gì (Lợi ích)

**[T12-115]** Mất gì (Đánh đổi)

**[T12-116]** 1. Prompt Chaining(Chuỗi liên kết)

**[T12-117]** Chính xác cao hơn nhờ có các cổng kiểm tra (gate) độc lập giữa từng bước.

**[T12-118]** Chậm hơn, độ trễ cộng dồn qua từng bước gọi mô hình tuần tự.

**[T12-119]** 2. Routing(Định tuyến / Phân luồng)

**[T12-120]** Tối ưu chi phí; phân loại đúng yêu cầu để đưa vào nhánh xử lý chuyên biệt (câu dễ đi model rẻ, câu khó đi model mạnh).

**[T12-121]** Đòi hỏi bộ phân loại (router) phải cực kỳ chính xác ngay từ đầu.

**[T12-122]** 3. Parallelization(Xử lý song song)

**[T12-123]** Độ tin cậy cao hơn nhờ chạy song song các chốt chặn (guardrail) hoặc gom ý kiến biểu quyết (voting).

**[T12-124]** Chi phí nhân lên trực tiếp theo số lượng nhánh chạy song song.

**[T12-125]** 4. Orchestrator-Workers(Điều phối - Thực thi)

**[T12-126]** Giải quyết tốt các bài toán mở, phức tạp khi không thể biết trước các tác vụ con.

**[T12-127]** Khó kiểm thử, hành vi của hệ thống rất khó dự đoán trước.

**[T12-128]** 5. Evaluator-Optimizer(Đánh giá - Tối ưu)

**[T12-129]** Chất lượng đầu ra tăng vượt trội qua vòng lặp phản hồi và hiệu chỉnh liên tục.

**[T12-130]** Yêu cầu tiêu chí đánh giá rất rõ ràng (hàm thưởng); tăng chi phí và độ trễ.

**[T12-131]** 6. Agent(Tác nhân tự chủ)

**[T12-132]** Độ tự chủ cao nhất, xử lý các bài toán mở, đa công cụ và tự động lập kế hoạch linh hoạt.

**[T12-133]** Chi phí vận hành rất lớn, dễ tích tụ sai số dẫn đến lỗi cộng dồn (error propagation).

**[T12-134]** 7. Từ Problem Statement Sang Kế Hoạch Đánh Giá & UX Fallback

**[T12-135]** Một Problem Statement chất lượng phải là bệ phóng trực tiếp để xây dựng Kế hoạch Đánh giá (Eval Plan) và Thiết kế Ranh giới Kiến trúc (Architecture Boundary). Nguyên tắc vàng: 'Nếu từ Problem Statement không suy ra được Test Cases, Eval Metric và Architecture Boundary thì bài toán đó chưa đủ chặt chẽ.'

**[T12-136]** Test Cases (Làm sao biết đúng): Xác định bộ dữ liệu thực tế và các trường hợp biên (edge cases) để kiểm thử mức độ đáp ứng của mô hình.

**[T12-137]** Eval Metric (Đo bằng cái gì): Thiết lập ngưỡng đo lường cụ thể về chất lượng đầu ra (accuracy), độ trễ (latency), chi phí (cost) và mức độ hài lòng (CSAT).

**[T12-138]** Architecture Boundary (Được phép làm gì): Vẽ rõ phạm vi hoạt động, các điểm con người phê duyệt (HITL), cơ chế khôi phục (rollback) và phân quyền (permissions).

**[T12-139]** Thiết kế trải nghiệm UX Fallback nâng đỡ điểm yếu của AI

**[T12-140]** Hệ thống AI không cần phải hoàn hảo tuyệt đối nếu được hỗ trợ bởi thiết kế trải nghiệm người dùng (UX) thông minh tại các điểm ranh giới:

**[T12-141]** Trạng thái không chắc chắn (Low confidence): Yêu cầu người dùng xác nhận rõ ràng trước khi thực hiện hành động.

**[T12-142]** Tác vụ rủi ro cao (High risk): Chỉ đưa ra đề xuất hiển thị (suggest), tuyệt đối không tự động thực thi (no auto-action).

**[T12-143]** Phản hồi quá dài (Overload): Chia nhỏ các tùy chọn thành dạng thẻ (cards) hoặc tóm tắt ngắn để người dùng chủ động lựa chọn.

**[T12-144]** Thiếu ngữ cảnh đầu vào (Ambiguous input): Hỏi lại đúng thông tin còn thiếu thay vì cố tình suy đoán sai lệch bối cảnh.

**[T12-145]** 8. Phụ Lục: Nguồn Gốc Lỗi AI Và Bộ Thẻ Câu Hỏi Thẩm Định

**[T12-146]** Bốn nguồn gốc cốt lõi của lỗi AI (Chương 6 Google PAIR)

**[T12-147]** 1. Lỗi dữ liệu & dự đoán: Dữ liệu gán nhãn sai lệch, suy luận kém của mô hình hoặc thiếu dữ liệu huấn luyện cục bộ.

**[T12-148]** 2. Lỗi đầu vào (Input): Đầu vào bất ngờ, nằm ngoài thiết kế ban đầu hoặc phá vỡ thói quen sử dụng của người dùng.

**[T12-149]** 3. Lỗi liên quan (Context): Độ tin cậy thấp, đề xuất kết quả không liên quan đến bối cảnh thực tế.

**[T12-150]** 4. Lỗi phân cấp hệ thống: Xảy ra khi có nhiều phân cấp hệ thống AI cùng vận hành song song và xung đột tín hiệu.

**[T12-151]** Bộ thẻ câu hỏi thẩm định mức độ sẵn sàng (Gate Quyết định)

**[T12-152]** Trước khi ra quyết định Go, Not Yet hay No-Go, đội ngũ sản phẩm phải cùng trả lời 5 câu hỏi cốt lõi:

**[T12-153]** Nghiệp vụ thực tế có thực sự đòi hỏi xử lý ngôn ngữ, tri thức chuyên môn hoặc khả năng suy luận chuyên sâu của AI không?

**[T12-154]** Dữ liệu đầu vào hiện tại có cung cấp đầy đủ ngữ cảnh để AI phản hồi chính xác không?

**[T12-155]** Đã thiết lập được các chỉ số định lượng cụ thể để đánh giá hiệu quả cải tiến chưa?

**[T12-156]** Hậu quả khi AI xảy ra sai sót có nằm trong phạm vi kiểm soát an toàn của doanh nghiệp không?

**[T12-157]** Có giải pháp thay thế nào đơn giản, tối ưu chi phí và dễ bảo trì hơn việc dùng AI không (như rule, kịch bản tĩnh)?

**[T12-158]** Nếu phần lớn các câu trả lời cho các câu hỏi trên chưa rõ ràng, quyết định tối ưu nhất luôn là: Not Yet (Tạm hoãn để chuẩn hóa quy trình và thu thập thêm dữ liệu).
