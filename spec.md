# AI SPEC — Study Pack 10 phút · Nhóm [XX] · Zone [X]
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

Study Pack có số user khớp rule cao gấp `3,68×` Course Action Hub và `5,72×` Concept-to-Micro-Lab. Phạm vi prototype nhỏ (1 màn hình, 1 AI call, transcript có sẵn) khả thi trong thời gian sự kiện. Tuy nhiên, quyết định chưa phải chốt cuối cùng — cần manual audit xác nhận rule đủ tin cậy và khảo sát đạt ngưỡng trước khi khóa.

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

Một học viên vừa học xong một buổi chọn mục tiêu "ôn quiz trong 10 phút"; hệ thống quyết định 5 ý trọng tâm và 5 câu tự kiểm tra từ transcript; học viên nhận một study pack một trang, mỗi ý và đáp án đều có mã đoạn nguồn.

### Non-goals (≥3 thứ KHÔNG build)

1. **Không chat tự do** — sản phẩm tạo artifact có cấu trúc, không phải chatbot.
2. **Không tự chấm năng lực** — không gán nhãn "đã hiểu" / "chưa hiểu" cho học viên.
3. **Không tạo đáp án quiz chính thức** — chỉ sinh câu hỏi active recall để tự kiểm tra.
4. **Không cá nhân hoá dài hạn** — không lưu lịch sử học tập hay theo dõi tiến độ.
5. **Không tích hợp VLearn hoặc Discord** — prototype độc lập.
6. **Không sinh kiến thức ngoài transcript** — mọi mệnh đề phải truy về transcript đã chọn.

### Mức prototype nhắm tới

[x] Mock có lời AI thật — Flow bấm được, AI thật ở lõi, data giả cho phần login/lịch sử/analytics.

**Phần thật:** Chọn transcript → LLM sinh JSON study pack → validator kiểm citation → hiển thị study pack + đáp án ẩn + citation mở được + failure state + nút feedback.

**Phần mock:** Đăng nhập, lịch sử, đồng bộ VLearn, analytics, lưu feedback lâu dài.

### Automation

[x] Augment — AI gợi ý, người quyết.

**Lý do theo cost-of-error:** Chọn sai trọng tâm hoặc tạo đáp án sai có thể khiến học viên học sai kiến thức trước quiz — hậu quả trực tiếp (mất điểm, mất niềm tin vào tài liệu). Học viên phải tự recall, mở nguồn và quyết định có tin kết quả không. Sản phẩm không tự kết luận học viên đã hiểu hoặc chưa hiểu.

### §4b. Nguyên tắc đã áp dụng (7 nguyên tắc — ≥4 yêu cầu)

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G1 — Làm rõ hệ thống làm được gì** | Đầu flow ghi rõ: "Tạo từ transcript đã chọn; có thể bỏ sót ý; không thay thế tài liệu gốc." |
| **G2 — Làm rõ nó làm tốt đến đâu** | Mỗi ý và đáp án hiện `Dựa trên [Txx-NNN]`; không dùng confidence % giả. Khi nguồn có nhiều `[không nghe rõ]` thì hiện `Cần kiểm tra — nguồn hạn chế`. |
| **G8 — Gạt bỏ dễ dàng** | User bấm "Bỏ qua" bất kỳ ý nào hoặc đóng pack mà không bị chặn flow. |
| **G9 — Sửa dễ dàng** | Nút "Tạo lại" cho phép đổi mục tiêu hoặc chọn transcript khác và sinh pack mới. |
| **G10 — Thu hẹp phạm vi khi nghi ngờ** | Không đủ nguồn thì abstain — giảm số câu, nói rõ thiếu gì và cho học viên mở transcript/chọn buổi khác. |
| **G11 — Giải thích vì sao** | Mỗi citation bấm mở đúng đoạn transcript; học viên thấy ngay cơ sở của mệnh đề. |
| **G15 — Mời feedback chi tiết** | Nút "Chưa đúng" kèm lý do (sai nguồn / không trọng tâm / quá khó). Feedback chỉ ghi log, không nói rằng model học ngay. |

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
| 9 | Câu hỏi có nhiều đáp án đúng nhưng output chỉ chấp nhận một | ④ Domain | Hiện rubric/đáp án gợi ý, không chấm đạt/trượt; cho mở nguồn và sửa câu hỏi. | G9, G11 |
| 10 | Prompt injection nằm trong transcript | ① + ③ | Xem transcript là dữ liệu, không là lệnh; chỉ sinh schema study pack, không thực thi. | G10, PAIR Safety |

**Kịch bản đáng lo nhất khi demo:** Kịch bản #2 — citation đúng cú pháp nhưng không thực sự chứng minh đáp án. Kiểm tra mã đoạn tồn tại là cần nhưng chưa đủ; golden set phải chấm semantic groundedness bằng người.

---

## §6. Bốn đường đi của trải nghiệm

### Happy path
Chọn transcript → chọn mục tiêu "Ôn quiz trong 10 phút" → hệ thống gọi LLM sinh study pack → validator xác nhận citation → hiển thị 5 ý trọng tâm + tối đa 8 keyword + 5 câu active recall → học viên tự trả lời → bấm mở đáp án ẩn → bấm citation mở đúng đoạn transcript nguồn.

### Low-confidence (②)
Nguồn có nhiều đoạn `[không nghe rõ]` hoặc transcript quá ngắn không đủ nội dung → hiện `Cần kiểm tra — nguồn hạn chế`, giảm số câu hỏi (từ 5 xuống 3), đề nghị mở tài liệu gốc để bổ sung.

### Failure / không căn cứ (①)
Không có citation hợp lệ cho bất kỳ mệnh đề nào → không hiện study pack, nói rõ "Không đủ nguồn từ transcript đã chọn để tạo study pack" và cho chọn transcript khác hoặc mở tài liệu gốc để ôn thủ công.

### Correction (user sửa)
Học viên bấm "Chưa đúng" trên bất kỳ ý hoặc câu hỏi nào → chọn lý do (sai nguồn / không trọng tâm / quá khó) → có thể đổi mục tiêu hoặc bấm "Tạo lại" → hệ thống sinh pack mới. Feedback được ghi log nhưng không tuyên bố model học ngay.

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
| **Active recall** | Câu hỏi yêu cầu người học tự nhớ/giải thích/áp dụng trước khi hiện đáp án, không chỉ là chép lại câu trong tóm tắt. Fail = câu hỏi chỉ đòi nhận diện hoặc chép lại. |
| **Graceful failure** | Input thiếu, ngoài phạm vi hoặc không có căn cứ phải được từ chối/hỏi lại và có bước tiếp theo. Fail = hệ thống bịa output hoặc trả dead-end. |
| **Độ gọn** | Đúng 5 ý, tối đa 8 keyword và 5 câu; pack đọc được trong một màn hình dài hợp lý. Fail = vượt giới hạn số lượng hoặc quá dài. |

### Golden set (≥20 case, file trong `eval/`)

**Cơ cấu:**

- **8 case thường** từ 4–6 transcript (mỗi transcript 1–2 case): input chuẩn, mục tiêu "ôn quiz 10 phút".
- **8 case chỗ khó** (≥2 case/lớp):
  - Lớp ①: 2 case — model bịa ý + citation sai ngữ nghĩa.
  - Lớp ②: 2 case — user chưa chọn buổi + mục tiêu quá chung.
  - Lớp ③: 2 case — yêu cầu đáp án quiz chính thức + yêu cầu đánh giá người khác.
  - Lớp ④: 2 case — khái niệm có ngoại lệ + câu hỏi nhiều đáp án.
- **2 case hiếm:** transcript có `[không nghe rõ]` nhiều + citation chồng chéo.
- **2 case tấn công/ngoài phạm vi:** prompt injection trong input.

**Ít nhất 10 case phát triển từ chatlog thật** (lưu mã conversation/turn, trích ngắn cần thiết).

### Quality bar

> **Đạt khi ≥85% case đạt toàn bộ tiêu chí, 100% citation hợp lệ về cú pháp, và 0 mệnh đề không có căn cứ được hiện như sự thật.**

*Bar này chốt tại thời điểm commit spec.md trước 23:59 Ngày 1 và giữ nguyên sau đó. Không đạt quality bar nhưng phân tích được nguyên nhân vẫn được tính đủ điểm; số liệu bị chỉnh sửa sẽ không được tính.*

### Kết quả các lượt chạy

`[chờ chạy prototype — sẽ cập nhật bảng % sau mỗi lượt chạy golden set, đủ mọi case kể cả case chưa đạt]`

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
| 30/07/2026 23:34 ICT | Chuyển corpus runtime sang Paper + Day 01-05 (`T10`-`T15`), giữ nguyên 6 transcript VLearn cũ | Dùng toàn bộ nội dung nguồn mới theo yêu cầu chủ dự án; manifest + test bảo toàn 1.456 segment và không cắt ngầm |
