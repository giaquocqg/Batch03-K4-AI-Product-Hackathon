# AI SPEC — Study Pack 10 phút · Nhóm D304 · Zone C
Hướng: [ ] A — VLearn  [ ] B — Trợ lý Học viên  [x] C — Làn mở
Loại: [x] Tính năng mới

## §1. User & Job

### Job executor + workflow

**Job executor:** Học viên khoá AI Thực Chiến, vừa kết thúc một buổi học dài (60–120 phút bài giảng), cần ôn trọng tâm và chuẩn bị quiz Kahoot cuối giờ hoặc quiz tuần.

**Workflow hiện tại (giả định — cần xác minh qua khảo sát):**

1. Mở lại slide, transcript hoặc video bài giảng.
2. Tự đọc lướt và tìm nội dung có khả năng vào quiz.
3. Ghi lại ý chính và keyword bằng tay.
4. Tự nghĩ câu hỏi hoặc nhờ công cụ tổng quát (ChatGPT, VLearn tutor) tạo quiz.
5. Quay lại nguồn khi gặp nội dung không chắc.

AI có giá trị ở bước 2–4 vì phải hiểu ngôn ngữ tự nhiên, nén ý chính trên nhiều đoạn và tạo câu hỏi theo ngữ cảnh. Việc mở citation, ẩn/hiện đáp án và điều hướng phải dùng logic tất định, không giao cho AI.

### Core JTBD

Ôn lại kiến thức trọng tâm của một buổi học để biết mình đã hiểu gì và còn hổng ở đâu trước quiz.

### Problem statement (KHÔNG chữ AI)

Học viên sau một buổi học dài cần ôn trọng tâm và chuẩn bị quiz, nhưng phải tự tổng hợp nhiều trang tài liệu và thường không nhận được bản tóm tắt đủ phạm vi, dẫn đến khó biết nên nhớ và tự kiểm tra điều gì.

### Evidence

**Đường B — Mining data (đạt chuẩn):**

Phân tích `1.261` turn hợp lệ từ `2.522` message chatlog VLearn tutor (369 user ẩn danh, 585 hội thoại, khoảng 22–29/07/2026).

- `146/1.261` turn (`11,58%`) khớp rule lexical Study Pack.
- Các turn khớp rule đến từ `103/369` user ẩn danh (`27,91%`) và `125/585` hội thoại (`21,37%`).
- Trong 146 turn, rule `tom_tat` khớp 125 lần, `y_chinh` 17, `tong_hop` 12, `noi_dung_chinh` 8, `note` 7, `tom_gon` 2, `mindmap` 1. Một turn có thể khớp nhiều rule.
- `47/146` turn có phản hồi tutor khớp heuristic failure ở 300 ký tự đầu (`32,19%`); đây là tín hiệu lexical, không phải đánh giá chất lượng ngữ nghĩa.

Nguồn số liệu máy sinh: `evidence/mining-results.json`, SHA-256 file nguồn `400ce4ce5c1c58189be9ca0630bd517ca69cfcac637f0f802edec70f4f796cad`. Phương pháp đếm: `evidence/mining-method.md`. Script tái lập: `evidence/mine_chatlog.py`.

**5 quote nguyên văn (đã ẩn danh, giữ nguyên văn):**

1. `[C0018/T0699]`: "tóm tắt toàn bộ slide sau đó đưa ra các ý chính"
2. `[C0057/T0415]`: "tóm tắt nội dung, đưa ra keyword cần nhớ"
3. `[C0089/T0952]`: "Tóm tắt kiến thức trọng tâm của ngày hôm nay"
4. `[C0093/T0411]`: "tóm tắt nội dung cần học trong ngày hôm nay cho toio"
5. `[C0573/T0257]`: "tóm tắt những ý chính, chi tiết để tôi có thể làm quiz kahoot cuối giờ"

**Đường A — Khảo sát:** `[chờ khảo sát ≥20 người ngoài nhóm]`

**Kết quả manual audit:** `[chờ 2 reviewer hoàn thành manual-audit-reviewer-1.csv và manual-audit-reviewer-2.csv]`

### Giới hạn của evidence

- Log chỉ có 8 ngày và 100% ở chế độ `in_class`; không đại diện chắc chắn cho toàn bộ ~1.000 học viên.
- Log chứng minh nhu cầu xuất hiện, chưa chứng minh số phút bị mất, tác động lên điểm quiz hay sẵn sàng dùng sản phẩm.
- Phân loại bằng từ khoá có thể bỏ sót cách diễn đạt khác hoặc bắt nhầm; cần kiểm tra tay trước khi nộp evidence chính thức.
- Tất cả con số lexical phải chờ kết quả manual audit trước khi được dùng để kết luận về nhu cầu thật.

---

## §2. Impact & quyết định chọn

### Bảng impact ≥3 ứng viên

| Ứng viên | Số người gặp trong log | Tần suất quan sát | Tốn mỗi lần | Khả thi 1,5 ngày | Quyết định |
|---|---:|---:|---|---|---|
| **Study Pack 10 phút** | 103 user, 146 turn khớp rule | 1,42 turn/user khớp rule | `[chờ khảo sát — chưa có số phút/điểm]` | Cao: 1 màn hình, 1 AI call, transcript có sẵn | Ứng viên ưu tiên |
| Course Action Hub | 28 user, 29 turn khớp rule | 1,04 turn/user khớp rule | `[chờ khảo sát]` | Trung bình: cần catalog link/deadline chính thống và integration | Tạm xếp sau |
| Concept-to-Micro-Lab | 18 user, 22 turn khớp rule | 1,22 turn/user khớp rule | `[chờ khảo sát]` | Khá cao, nhưng cần duyệt độ đúng của lab/code | Tạm xếp sau |

### Ứng viên ĐÃ LOẠI + vì sao

- **Course Action Hub:** Số user khớp rule chỉ bằng `27,18%` so với Study Pack (28 vs 103). Cần catalog link/deadline chính thống từ VLearn — không có API/data trong hackathon. Rủi ro trả sai deadline gây hậu quả trực tiếp cho học viên.
- **Concept-to-Micro-Lab:** Số user khớp rule chỉ bằng `17,48%` so với Study Pack (18 vs 103). Cần duyệt độ đúng của lab/code sinh ra — chi phí kiểm thử cao hơn đáng kể trong 1,5 ngày.

### Ứng viên CHỌN + vì sao

Study Pack có số user khớp rule cao gấp `3,68×` Course Action Hub và `5,72×` Concept-to-Micro-Lab. Phạm vi prototype nhỏ (1 màn hình, 1 AI call trung tâm, transcript có sẵn) khả thi trong thời gian sự kiện nên đây là hướng đã chọn và đã khóa. Manual audit vẫn bắt buộc để xác nhận độ tin cậy của evidence, không phải để âm thầm đổi hướng hoặc mở rộng sản phẩm sau CP4.

**Điều chưa được phép tuyên bố:** "tiết kiệm X phút", "tăng Y điểm", "cải thiện kết quả học" cho đến khi có dữ liệu validation.

---

## §3. Giải pháp tương tự đã nghiên cứu

### Google NotebookLM

- **Flow:** Upload tài liệu → AI tạo study guide, timeline, FAQ tự động → user đọc và hỏi thêm.
- **Đáng học:** Mọi câu trả lời có trích dẫn nguồn inline, bấm vào mở đúng đoạn — tạo calibrated trust.
- **Đáng né:** Output dài, dạng văn xuôi, khó dùng để tự kiểm tra nhanh; không có cơ chế active recall.
- **Mình khác gì:** Study Pack tập trung vào active recall (5 câu hỏi tự kiểm tra, đáp án ẩn), không chỉ tóm tắt thụ động. Citation trỏ về mã đoạn `[Txx-NNN]` cụ thể, không chỉ "nguồn 1".

### Quizlet AI (Magic Notes)

- **Flow:** Paste notes → AI sinh flashcard và practice test.
- **Đáng học:** Cơ chế spaced repetition và tự kiểm tra bằng flashcard rất hiệu quả cho ghi nhớ.
- **Đáng né:** Không kiểm soát nguồn — AI có thể sinh flashcard từ kiến thức ngoài tài liệu người dùng đưa vào; không có citation.
- **Mình khác gì:** Mọi ý và đáp án trong Study Pack bắt buộc có citation kiểm chứng được; nếu không có căn cứ thì không hiện — chọn thiếu hơn chọn sai.

### ChatGPT (Study mode / Custom instructions)

- **Flow:** Paste transcript hoặc nội dung → yêu cầu tóm tắt, tạo quiz.
- **Đáng học:** Linh hoạt, user có toàn quyền điều khiển prompt, output đa dạng.
- **Đáng né:** Không có cơ chế citation bắt buộc — AI có thể bịa kiến thức ngoài nguồn mà user không nhận ra; output phụ thuộc vào kỹ năng prompting của user.
- **Mình khác gì:** Study Pack có schema cố định (5 ý + 8 keyword + 5 câu), citation validator tự động loại item không có căn cứ, và graceful failure khi thiếu nguồn — user không cần biết prompt.

---

## §4. Thiết kế

### Lát cắt MỘT CÂU

Một học viên vừa học xong một buổi chọn mục tiêu "ôn quiz trong 10 phút"; hệ thống quyết định 5 ý trọng tâm và 5 câu active recall từ transcript; học viên nhận một study pack một trang, trả lời từng câu trước khi mở đáp án/citation, hệ thống so khớp linh hoạt câu trả lời với đáp án/citation trong bản nháp HITL hiện hành, rồi cho ôn lại câu chưa đạt ngưỡng sau một câu khác.

### Non-goals (≥3 thứ KHÔNG build)

1. **Không chat tự do** — sản phẩm tạo artifact có cấu trúc, không phải chatbot.
2. **Không tự chấm năng lực** — không gán nhãn "đã hiểu" / "chưa hiểu" cho học viên. AI chỉ so khớp từng câu trả lời với đáp án và citation đã khoanh vùng trong bản nháp HITL hiện hành; tỷ lệ của phiên không phải điểm quiz, không phải hồ sơ năng lực và không lưu lịch sử.
3. **Không tạo đáp án quiz chính thức** — chỉ sinh câu hỏi active recall để tự kiểm tra.
4. **Không cá nhân hoá dài hạn** — không lưu lịch sử học tập hay theo dõi tiến độ.
5. **Không tích hợp VLearn hoặc Discord** — prototype độc lập.
6. **Không sinh kiến thức ngoài transcript** — mọi mệnh đề phải truy về transcript đã chọn.

### Mức prototype nhắm tới

[x] Working — Flow chính chạy end-to-end bằng corpus được cấp và model thật;
không dùng response mock hoặc output dựng sẵn.

**Phần thật:** Chọn transcript → LLM sinh JSON study pack → validator kiểm
citation → tạo bản nháp HITL → giảng viên sửa/thêm/xóa/sắp xếp hoặc tạo lại
riêng một câu → kiểm tra lại schema/citation → phê duyệt/khóa bản → học viên
nhập câu trả lời cho từng câu trước khi mở đáp án/citation → AI so khớp có căn
cứ với đáp án/citation của câu → câu chưa đạt ngưỡng xuất hiện lại sau một câu khác.

**Hai dashboard cùng một flow:** Cả học viên và giảng viên xem cùng nội dung
Study Pack; active recall vẫn chỉ hiện một câu tại một thời điểm. Giảng viên có
thêm panel HITL để sửa, thêm, xóa, đổi thứ tự, tạo lại và phê duyệt. Đây mới là
tách giao diện demo; chưa có đăng nhập hay phân quyền backend, nên không được
mô tả như kiểm soát truy cập theo vai trò.

**Không triển khai:** Đăng nhập người dùng, lịch sử học tập, đồng bộ VLearn,
analytics và feedback dài hạn. Những phần này là non-goal, không được mô phỏng
như tính năng đang chạy.

### Automation

[x] Augment — AI gợi ý, người quyết.

**Lý do theo cost-of-error:** Chọn sai trọng tâm hoặc tạo đáp án sai có thể khiến học viên học sai kiến thức trước quiz — hậu quả trực tiếp (mất điểm, mất niềm tin vào tài liệu). Học viên phải tự recall, mở nguồn và quyết định có tin kết quả không. Sản phẩm không tự kết luận học viên đã hiểu hoặc chưa hiểu.

### §4b. Nguyên tắc đã áp dụng (7 nguyên tắc — ≥4 yêu cầu)

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G1 — Làm rõ hệ thống làm được gì** | Đầu flow ghi rõ: "Tạo từ transcript đã chọn; có thể bỏ sót ý; không thay thế tài liệu gốc." |
| **G2 — Làm rõ nó làm tốt đến đâu** | Mỗi ý và đáp án hiện `Dựa trên [Txx-NNN]`; không dùng confidence % giả. Khi nguồn có nhiều `[không nghe rõ]` thì hiện `Cần kiểm tra — nguồn hạn chế`. |
| **G8 — Gạt bỏ dễ dàng** | Trong review HITL, giảng viên có thể xóa câu hỏi không phù hợp; UI cảnh báo phải thêm câu thay thế trước khi phê duyệt. Học viên có thể đóng pack mà không bị ép hoàn thành. |
| **G9 — Sửa dễ dàng** | Nút "Tạo lại" cho phép đổi mục tiêu hoặc chọn transcript khác và sinh pack mới. |
| **G10 — Thu hẹp phạm vi khi nghi ngờ** | Không đủ nguồn thì abstain — giảm số câu, nói rõ thiếu gì và cho học viên mở transcript/chọn buổi khác. |
| **G11 — Giải thích vì sao** | Mỗi citation bấm mở đúng đoạn transcript; học viên thấy ngay cơ sở của mệnh đề. |
| **G15 — Mời feedback chi tiết** | Trong review HITL, giảng viên sửa trực tiếp câu hỏi, đáp án, citation; có thể ghi yêu cầu khi tạo lại riêng một câu. Thay đổi được lưu bằng revision/audit log, không tuyên bố model tự học. |

### Phân tích GAP (Importance − Satisfaction)

- **Importance cao:** Ôn đúng trọng tâm và tự kiểm tra kiến thức nhanh trước quiz Kahoot là nhu cầu cấp bách, lặp lại mỗi buổi học.
- **Satisfaction hiện tại thấp:** Phải tự lội qua 70+ slide hoặc 700 đoạn transcript thô, không biết kiến thức nào sẽ vào quiz, dễ học lệch. VLearn tutor chưa có tính năng tạo artifact ôn tập có cấu trúc.
- **Khoảng GAP trọng tâm:** Tạo ra một artifact Active Recall có trích dẫn nguồn kiểm chứng được — giá trị khác biệt so với ChatGPT tóm tắt chung chung (không citation) hoặc VLearn tutor (trả lời dạng văn xuôi).

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (10 kịch bản, ≥8 yêu cầu)

| # | Tình huống cụ thể | Lớp | Hành vi mong muốn | Nguyên tắc |
|---|---|---|---|---|
| 1 | Model tạo một ý không có trong transcript | ① Nguồn sự thật | Validator loại ý đó; không hiện nếu không có citation hợp lệ. | G10, PAIR Explainability |
| 2 | Citation tồn tại nhưng không hỗ trợ mệnh đề (sai ngữ nghĩa) | ① Nguồn sự thật | Đánh fail trong eval; cho user bấm "Sai nguồn" và mở đoạn để kiểm tra. | G15, G11 |
| 3 | Transcript có `[không nghe rõ]` trong đoạn cần dùng | ① + ④ | Không dùng đoạn đó làm căn cứ duy nhất; thông báo chất lượng nguồn hạn chế. | G2, G10 |
| 4 | User chưa chọn buổi học | ② Mơ hồ | Hỏi lại một câu để chọn transcript; không tự đoán. | G10 |
| 5 | User chọn mục tiêu quá chung "học tất cả" | ② Mơ hồ | Đề nghị mục tiêu hỗ trợ "Ôn quiz trong 10 phút" và nêu giới hạn output. | G1, G10 |
| 6 | User yêu cầu đáp án quiz chính thức | ③ Ngoài phạm vi | Từ chối, đề nghị câu active recall dựa trên transcript. | G1 |
| 7 | User yêu cầu đánh giá một học viên khác | ③ Ngoài phạm vi | Từ chối gán nhãn; giải thích sản phẩm không đánh giá con người. | G1 |
| 8 | Tóm tắt làm mất ngoại lệ quan trọng của khái niệm | ④ Domain | Ưu tiên tính đúng và citation hơn đủ số lượng; nếu không thể nén an toàn thì báo thiếu căn cứ. | G2, G10 |
| 9 | Câu hỏi có nhiều cách trả lời đúng nhưng học viên diễn đạt khác đáp án gợi ý | ④ Domain | So khớp ngữ nghĩa linh hoạt nhưng chỉ với đáp án đã duyệt và citation của câu; hiển thị score, feedback, citation để kiểm tra. Model trả citation ngoài phạm vi bị chặn; mơ hồ thì cho mở nguồn và ôn lại, không gán nhãn năng lực. | G9, G11 |
| 10 | Prompt injection nằm trong transcript | ① + ③ | Xem transcript là dữ liệu, không là lệnh; chỉ sinh schema study pack, không thực thi. | G10, PAIR Safety |

**Kịch bản đáng lo nhất khi demo:** Kịch bản #2 — citation đúng cú pháp nhưng không thực sự chứng minh đáp án. Kiểm tra mã đoạn tồn tại là cần nhưng chưa đủ; golden set phải chấm semantic groundedness bằng người.

---

## §6. Bốn đường đi của trải nghiệm

### Happy path
Chọn transcript → chọn mục tiêu "Ôn quiz trong 10 phút" → hệ thống gọi LLM sinh study pack → validator xác nhận citation → hiển thị 5 ý trọng tâm + tối đa 8 keyword + 5 câu active recall → chỉ hiện một câu, học viên nhập câu trả lời → bấm đối chiếu đáp án/citation → AI trả mức khớp, feedback và citation của câu → câu dưới 60% quay lại sau một câu khác → hiển thị tỷ lệ đạt ngưỡng của phiên ôn.

### Low-confidence (②)
Nguồn có nhiều đoạn `[không nghe rõ]` hoặc transcript quá ngắn không đủ nội dung → hiện `Cần kiểm tra — nguồn hạn chế`, giảm số câu hỏi (từ 5 xuống 3), đề nghị mở tài liệu gốc để bổ sung.

### Failure / không căn cứ (①)
Không có citation hợp lệ cho bất kỳ mệnh đề nào → không hiện study pack, nói rõ "Không đủ nguồn từ transcript đã chọn để tạo study pack" và cho chọn transcript khác hoặc mở tài liệu gốc để ôn thủ công.

### Correction (user sửa)
Giảng viên mở chế độ review → sửa câu hỏi, đáp án hoặc citation; thêm, xóa,
đổi thứ tự hoặc yêu cầu model tạo lại riêng một câu → backend kiểm tra schema
và citation khi lưu → chỉ cho phê duyệt khi đủ số câu và nguồn hợp lệ. Bản đã
phê duyệt chuyển sang chỉ đọc.

### Khi bị đòi ngoài phạm vi (③)
Từ chối lịch sự, giải thích giới hạn sản phẩm, đề nghị hành động thay thế trong phạm vi (ví dụ: "Mình chỉ tạo câu active recall từ transcript — không có đáp án quiz chính thức. Bạn có muốn tạo study pack để tự ôn không?").

### Case đặc thù domain (④)
Khi khái niệm có ngoại lệ quan trọng mà tóm tắt có thể bỏ sót → ưu tiên giữ caveat kèm citation hơn là nén cho gọn. Nếu phải bỏ → ghi chú "Nội dung đầy đủ hơn tại [Txx-NNN]".

---

## §7. Kiểm thử

### Chiều chất lượng + định nghĩa kiểm chứng được

| Chiều | Định nghĩa pass/fail |
|---|---|
| **Groundedness** | Mọi mệnh đề kiến thức và đáp án phải có ít nhất một citation; người chấm đọc đoạn nguồn và xác nhận nó hỗ trợ trực tiếp mệnh đề. Fail = mệnh đề không có căn cứ trong transcript. |
| **Citation validity** | 100% mã citation tồn tại trong transcript đã chọn và link mở đúng đoạn. Fail = mã không tồn tại hoặc mở sai đoạn. |
| **Relevance** | Mọi ý phục vụ mục tiêu ôn quiz của buổi đã chọn; không lẫn sang nội dung ngoài buổi. Fail = ý không liên quan đến buổi học. |
| **Active recall** | Câu hỏi yêu cầu người học tự nhớ/giải thích/áp dụng và nhập câu trả lời trước khi hiện đáp án. Sau đó AI so khớp linh hoạt nhưng bị giới hạn bởi đáp án đã duyệt và citation của câu; câu dưới 60% phải quay lại sau một câu khác. Fail = cho hiện đáp án trước khi nhập, làm rơi câu chưa đạt, dùng nguồn ngoài citation, hoặc chấm năng lực từ free-text. |
| **Graceful failure** | Input thiếu, ngoài phạm vi hoặc không có căn cứ phải được từ chối/hỏi lại và có bước tiếp theo. Fail = hệ thống bịa output hoặc trả dead-end. |
| **Độ gọn** | Đúng 5 ý, tối đa 8 keyword và 5 câu; pack đọc được trong một màn hình dài hợp lý. Fail = vượt giới hạn số lượng hoặc quá dài. |

### Golden set (≥20 case, file trong `eval/`)

**Cơ cấu:**

- **10 case thường** từ 6 transcript active: 8 case `normal` và 2 case `normal_from_chatlog`, mục tiêu "ôn quiz 10 phút".
- **8 case chỗ khó** (≥2 case/lớp):
  - Lớp ①: 2 case — model bịa ý + citation sai ngữ nghĩa.
  - Lớp ②: 2 case — user chưa chọn buổi + mục tiêu quá chung.
  - Lớp ③: 2 case — yêu cầu đáp án quiz chính thức + yêu cầu đánh giá người khác.
  - Lớp ④: 2 case — khái niệm có ngoại lệ + câu hỏi nhiều đáp án.
- **2 case hiếm:** transcript dài 550 segment không được cắt ngầm + cô lập citation giữa hai nguồn có nội dung gần nhau.
- **2 case tấn công/ngoài phạm vi:** prompt injection trong input.

**11 case phát triển từ chatlog thật** (lưu mã conversation/turn, trích ngắn cần thiết).

### Direction update — source-bounded Recall session (31/07/2026, before CP4)

**Decision:** The team changed the learner side of the slice after identifying
that hidden answers alone cannot show whether a learner has practiced recall.
The product remains Track C / Study Pack 10 minutes for one learner and one
lecture. It does **not** add an official quiz, learner profile, long-term
personalization, or AI capability assessment.

- **§1 User & Job:** the learner now types an answer before checking the cited
  answer, then sees an AI-produced answer-match result (`Đúng ngay lần đầu`)
  that is bounded to the reviewed answer and the cited source segments. This
  makes the JTBD observable without claiming learning gain.
- **§2 Decision:** this reinforces the chosen candidate's advantage over a
  generic prompt-to-questions tool: a grounded, source-linked recall loop.
- **§4 Design:** one question is shown at a time; the evaluator receives only
  that question, its current HITL-draft answer, the learner answer and its cited source
  segments. On a below-60% match, the card is reinserted after one other
  question. The rate stays local to the tab and is explicitly not a quiz score
  or proficiency label.
- **§5 Failure handling:** the schema requires score, feedback and citation;
  a citation outside the question evidence is rejected. A below-threshold
  question is never silently dropped, including when it is the final queued
  question.
- **§6 Experience:** answer input is required before reveal; then the learner
  sees the source-bounded score, feedback and citation, and repeats missed
  cards until they meet the threshold.

### Recall-session interaction check

`codebase/web/recall_session.test.js` checks retry order, first-try score
accounting, and final-card retention. `codebase/test_recall_evaluator.py`
checks evidence minimization, schema output and rejection of an out-of-scope
citation. The earlier Gemini
`run_20260731_103502` still measures generator quality only; it does not
measure this later evaluator/UI behavior. CP5 must validate whether real
learners understand the 60% match feedback, can complete the retry loop
uncoached, and trust the citation-based comparison. This is a changelogged
scope correction before CP4, not a claim of learner improvement.

### Quality bar

> **Đạt khi ≥85% case đạt toàn bộ tiêu chí, 100% citation hợp lệ về cú pháp, và 0 mệnh đề không có căn cứ được hiện như sự thật.**

*Bar này chốt tại thời điểm commit spec.md trước 23:59 Ngày 1 và giữ nguyên sau đó. Không đạt quality bar nhưng phân tích được nguyên nhân vẫn được tính đủ điểm; số liệu bị chỉnh sửa sẽ không được tính.*

### Kết quả các lượt chạy

| Run | Provider / model | Phạm vi | Automated gate | Citation | Semantic review | Kết luận bar 85% |
|---|---|---:|---:|---:|---:|---|
| `run_20260731_103239` | Gemini / `gemini-3.5-flash-lite` | 22/22 | 21/22 (95,45%) | Output public đã redact; full output private | Chưa chấm | Chưa kết luận; evaluator cũ chấm mọi `limited` là fail |
| `run_20260731_103502` | Gemini / `gemini-3.5-flash-lite` | 22/22 | 22/22 (100%) | 352 total; 0 invalid; 0 item thiếu citation | Gia Quốc: 16/16 `pass` cả 3 chiều; 11:00–12:45 ICT (ước lượng) | **Đạt: 22/22 (100%)** theo nhãn human + deterministic gate |

Run thứ hai gồm 14 `ok`, 2 `limited`, 1 `needs_input`, 5 `rejected`, không lỗi
provider và không skip. Hai case `limited` chỉ được tính đạt automated gate khi
validator đã loại item không có căn cứ, còn output cuối vẫn đủ cấu trúc và
citation hợp lệ; trạng thái cùng warning vẫn được giữ nguyên để audit.

Full output và trace chứa nội dung được bảo vệ nằm trong thư mục local bị
gitignore. Summary public chỉ giữ hash, count, citation code, provider/model,
trace ID và kết quả gate. Các cột semantic trong
`eval/manual-review-run_20260731_103502.csv` đã được Gia Quốc chấm trực tiếp:
16/16 case `pass` ở groundedness, relevance và active recall, với khoảng thời
gian tự khai 11:00–12:45 ICT (ước lượng, không có timestamp riêng từng case).
Kết hợp với six deterministic case, đó là cơ sở kết luận 22/22 pass ở trên.
AI-assisted audit riêng vẫn được giữ nguyên: nó flag 13/16 case theo tiêu chí
rất chặt về citation heading/câu dẫn. Kết quả human là kết luận chính thức,
còn precheck là bằng chứng bất đồng cần theo dõi khi cải thiện prompt; không
xóa hoặc viết lại artifact đó.

---

## §8. Phân công & kế hoạch

### Phân công có tên

`[chờ nhập tên thành viên nhóm]`

| Phần việc | Người phụ trách |
|---|---|
| Spec + evidence | `[tên]` |
| Prompt + golden set | `[tên]` |
| Backend (parser, LLM call, validator) | `[tên]` |
| Frontend (UI study pack) | `[tên]` |
| Demo + validation | `[tên]` |

### Willing users

`[chờ khảo sát — cần ≥3 người thật ngoài nhóm đồng ý thử prototype trước demo, tên cụ thể]`

### Kế hoạch vòng validation CP5

**Đối tượng:** ≥5 người ngoài nhóm (ưu tiên 3 willing users đã khai + thành viên zone khác).

**Một phiên 10 phút/người:**
1. Giao task thật: "Hãy dùng cái này để ôn quiz buổi [X]" → im lặng quan sát, ghi lại bấm gì, kẹt đâu.
2. Hỏi đúng 3 câu:
   - "Điều gì khó hiểu hoặc khó chịu nhất?"
   - "Kết quả này bạn có tin không — vì sao?"
   - "Bạn có dùng thật không — vì sao / vì sao chưa?"
3. Log nguyên văn vào `validation/`.

**Phân biệt Usability vs PMF feedback:**
- Usability: "Nút mở citation có dễ bấm không?", "Đáp án ẩn có dễ tương tác không?"
- PMF: "5 câu Active Recall có giúp phát hiện phần kiến thức bị hổng trước quiz không?", "Nếu buổi học sau có Study Pack này, bạn có tiếp tục dùng không?"

### Chiến lược thử nghiệm theo vòng

- **Vòng 1 (nội bộ nhóm — 0,5h):** Test thủ công trên 1 transcript với 3 thành viên nhóm.
- **Vòng 2 (validation CP5 — 2h):** Mang prototype AI chạy thật test với 5–10 học viên ngoài nhóm, ghi nhận phản ứng và chỉnh sửa 1–2 điểm nghẽn lớn trước CP6 Demo.

---

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 30/07/2026 12:40 | Tạo spec.md v1 từ track-c-proposal.md + bản thảo 12 mục | Khởi tạo spec chính thức theo template, chốt quality bar, chuẩn bị cho CP4 |
| 30/07/2026 07:56 UTC | Nối clickable flow CP2 với backend thật; chạy OpenAI transcript-01, giữ 2 failure và 1 run `limited` | Chứng minh AI call không hard-code, enforce schema/citation và không che failure trước khi chạy full golden set |
| 31/07/2026 | Nâng prototype lên Working với review HITL thật; loại feedback giả; thêm access gate và external-data policy gate | Khớp implementation hiện tại và fail-closed theo quy định bảo mật data pack |
| 30/07/2026 23:34 ICT | Chuyển corpus runtime sang Paper + Day 01-05 (`T10`-`T15`), giữ nguyên 6 transcript VLearn cũ | Dùng toàn bộ nội dung nguồn mới theo yêu cầu chủ dự án; manifest + test bảo toàn 1.456 segment và không cắt ngầm |
| 31/07/2026 10:32 ICT | Chạy full golden set active lần 1: 22/22 case, automated 21/22; giữ nguyên case `limited` và toàn bộ failure/status | Hoàn thành lượt đo CP3 đầu tiên bằng Gemini thật, không cherry-pick |
| 31/07/2026 10:35 ICT | Sửa rule evaluator để `limited` chỉ đạt khi output sau lọc vẫn đủ mọi gate; chạy lại 22/22, automated 22/22, semantic 16 case còn chờ | Phân biệt xử lý an toàn của validator với model output hoàn hảo; không tuyên bố quality bar khi chưa chấm semantic |
| 31/07/2026 | Đối chiếu bản spec “Multi-Agent Learning Platform” với repo và giữ lát cắt Track C hiện hành; sửa title, trạng thái quyết định, G8 và cơ cấu golden set | Loại các claim không có implementation/artifact: Track A, upload PDF, 10 MCQ, Socratic/Feynman chatbot, SQLite/ChromaDB và kết quả 81,8% với bar 80% |
| 31/07/2026 | AI-assisted semantic audit đủ 16 Study Pack/160 item: groundedness 3/16, relevance 16/16, active recall 16/16; human CSV vẫn để trống | Phát hiện automated citation validity không chứng minh semantic support; giữ kết quả thấp trung thực và chỉ ra pattern cite heading |
| 31/07/2026 | Gia Quốc hoàn tất manual review: 16/16 Study Pack pass cả ba chiều; ghi khoảng review 11:00–12:45 ICT là ước lượng | Hoàn tất nhãn human CP3; giữ AI precheck bất đồng để audit thay vì che kết quả |
| 31/07/2026 | Bổ sung recall session: nhập câu trả lời → đối chiếu đáp án/citation → tự đánh dấu → lặp câu chưa đúng sau một câu | Hidden-answer-only flow không cho người học thấy kết quả của lượt tự ôn và quá giống công cụ hỏi đáp tổng quát; không chấm năng lực hay tạo điểm quiz chính thức |
| 31/07/2026 | Thay tự đánh dấu bằng AI so khớp source-bounded: chỉ gửi đáp án/citation của bản nháp HITL hiện hành, đạt ngưỡng 60% mới đi tiếp | Chấp nhận diễn đạt tương đương mà vẫn để người học kiểm tra feedback/citation; không đọc toàn transcript, không tạo điểm quiz hay hồ sơ năng lực |
| 31/07/2026 | Thêm OpenAI backup khi Gemini lỗi API/quota/network; sửa Gemini recall schema không gửi `minimum`/`maximum` SDK không hỗ trợ | Giữ flow demo hoạt động khi provider chính gián đoạn nhưng không dùng fallback để che output sai JSON/schema/citation; trace ghi đủ từng attempt |
