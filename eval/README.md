# Eval — Golden Set & Kết quả đánh giá

## Cấu trúc

```
eval/
├── README.md           ← tài liệu này
├── golden_set.json     ← 22 case kiểm thử theo cơ cấu guide §2.6
├── ai-semantic-audit-run_20260731_103502.csv/.md
│                       ← AI-assisted precheck, không giả làm human review
├── manual-review-run_20260731_103502.csv
│                       ← nhãn semantic do Gia Quốc chấm cho full-run CP3
├── private-results/    ← full output chạy thật, local-only và bị gitignore
└── results/            ← summary đã redaction: hash, count, citation code
```

## Golden set

File `golden_set.json` v2 chứa 22 case cho corpus
`study-pack-corpus-v1` (`T10` Paper, `T11`-`T15` Day 01-05).
`expected_behavior` là tiêu chí chấm đã chốt, còn trường `result` được giữ ở
trạng thái chờ cho đến khi có run thật.

| Nhóm | Số case | Mô tả |
|---|---|---|
| Thường + thường từ chatlog | 10 | Input chuẩn từ 6 nguồn active |
| Lớp ① Nguồn sự thật | 2 | Citation không tồn tại và sai ngữ nghĩa |
| Lớp ② Mơ hồ | 2 | Chưa chọn buổi, mục tiêu quá chung |
| Lớp ③ Ngoài phạm vi | 2 | Đáp án quiz chính thức, đánh giá người khác |
| Lớp ④ Domain | 2 | Khái niệm có ngoại lệ, câu hỏi nhiều đáp án |
| Hiếm | 2 | Nguồn không rõ, citation chồng chéo |
| Tấn công | 2 | Prompt injection trong objective |

Ít nhất 10 case phát triển từ chatlog thật (mã conversation/turn, trích ngắn cần thiết).

## Chiều chất lượng

Mỗi case được chấm theo 6 chiều (xem `spec.md §7`):

1. **Groundedness** — mọi mệnh đề có citation hỗ trợ trực tiếp
2. **Citation validity** — 100% mã citation tồn tại và mở đúng đoạn
3. **Relevance** — mọi ý phục vụ mục tiêu ôn quiz của buổi đã chọn
4. **Active recall** — câu hỏi yêu cầu tự nhớ/giải thích, không chép lại
5. **Graceful failure** — input thiếu/ngoài phạm vi được xử lý đúng
6. **Độ gọn** — đúng giới hạn 5 ý + 8 keyword + 5 câu

## Quality bar

> **Đạt khi ≥85% case đạt toàn bộ tiêu chí, 100% citation hợp lệ về cú pháp, và 0 mệnh đề không có căn cứ được hiện như sự thật.**

Bar đã được ghi trong `spec.md`. Thời điểm commit cần được xác nhận bằng Git;
README này không tự tuyên bố checkpoint đã đạt.

## Cách chạy eval

```bash
# Chạy một case thật trực tiếp trên backend
python codebase/main.py --transcript <transcript_path> --output eval/private-results/run_<timestamp>.json

# Chạy đủ golden set qua app local đã cấu hình provider
python eval/run_golden_set.py --base-url http://127.0.0.1:8000

# Chạy test tất định trước eval
python -m pytest codebase/ -v
```

Không tự điền kết quả hàng loạt khi chưa có API key. Một lượt đánh giá hoàn
chỉnh cần giữ full output và trace local trong thư mục bị gitignore, sau đó
chấm đủ sáu
chiều. `groundedness`, `relevance`, `active_recall` và các case có
`eval_note` phải được người chấm đọc nguồn; validator code không thay thế bước
này.

## Checklist một lượt thật

1. Tạo thư mục private `eval/private-results/<run-id>/`; runner chỉ ghi summary
   đã redaction vào `eval/results/<run-id>/`.
2. Chạy từng case có transcript bằng backend thật, không dùng response giả.
3. Với case không có transcript hoặc ngoài phạm vi, ghi đúng hành vi sản phẩm.
4. Đối chiếu từng citation với đoạn `[Txx-NNN]` và chấm sáu chiều.
5. Giữ cả case fail; tính tỷ lệ qua và so với quality bar 85%.
6. Ghi người chấm, thời điểm, model và trace ID trong bảng kết quả.

GS-09 là invariant áp lên output thật; không inject citation hoặc dựng response
để tạo kết quả. Các case cần hành vi chưa có trong CLI phải được ghi fail/chưa
triển khai, không diễn giải thành pass.

## Full-run CP3 trên corpus active

Ngày 31/07/2026 đã chạy đủ 22/22 case qua app local và lời gọi Gemini thật.
Full output được giữ trong `private-results/run_20260731_103502/`; artifact
public đã redact nội dung học tại `results/run_20260731_103502/`.

| Thuộc tính | Kết quả |
|---|---|
| Provider / model | Gemini / `gemini-3.5-flash-lite` |
| Tổng case đã thực thi | 22/22; 0 lỗi provider; 0 skip |
| Trạng thái | 14 `ok`; 2 `limited`; 1 `needs_input`; 5 `rejected` |
| Automated gate | 22/22 = 100% |
| Citation trên 16 Study Pack | 352 total; 0 invalid; 0 item thiếu citation |
| Semantic review | Gia Quốc: 16/16 case `pass` cả groundedness, relevance, active recall; khoảng 11:00–12:45 ICT (ước lượng) |
| Quality bar cuối | **Đạt: 22/22 = 100%** theo nhãn human + deterministic gate |

Hai case `limited` vẫn đạt automated gate vì validator đã loại keyword không
có trong nguồn trước khi hiển thị, còn Study Pack cuối vẫn đủ 5 ý, 5 câu,
keyword và toàn bộ citation hợp lệ. Warning và removed-item count vẫn được giữ
trong artifact; không đổi `limited` thành `ok`.

Run `run_20260731_103239` là full-run đầu tiên theo evaluator cũ, đạt automated
21/22 (95,45%) vì mọi trạng thái `limited` bị chấm fail dù output cuối đã sạch
và đủ. Run này được giữ để audit lý do đổi rule chấm; không bị xóa hoặc ghi đè.

`manual-review-run_20260731_103502.csv` ghi nhãn human do Gia Quốc chấm: 16/16
Study Pack đạt cả groundedness, relevance và active recall. Kết hợp với 6 case
`needs_input/rejected` đã đạt deterministic gate, full set đạt `22/22 = 100%`;
citation syntax là `352` total, `0` invalid và `0` item thiếu citation. Do đó,
theo nhãn manual hiện có, run này đạt quality bar 85%.

AI-assisted precheck vẫn được giữ nguyên để audit: nó flag 13/16 case do tiêu
chí rất chặt về citation heading/câu dẫn, trong khi reviewer human đánh giá
16/16 pass sau khi đọc nguồn. Nhãn human là kết luận chính thức của run; không
xóa precheck hoặc che bất đồng. Xem
`ai-semantic-audit-run_20260731_103502.md` và `.csv`.

## Run thật đầu tiên trên corpus legacy

Ngày 30/07/2026 đã chạy OpenAI trên GS-01/transcript-01 của golden set v1 và
giữ đủ ba attempt. Các artifact này là lịch sử của corpus VLearn cũ, không
được diễn giải thành kết quả cho golden set v2:

| Artifact | Kết quả |
|---|---|
| `results/run_cp2_openai_transcript01_attempt1.json` | Fail schema: model lặp lại schema thay vì trả object Study Pack |
| `results/run_cp2_openai_transcript01_attempt2.json` | Fail provider: OpenAI Structured Outputs không hỗ trợ `uniqueItems` |
| `results/run_cp2_openai_transcript01_attempt3.json` | `limited`: schema pass, 10/10 citation occurrence hợp lệ, loại 1 keyword ngoài nguồn |

Attempt 3 dùng provider `openai`, trace ID `20260730_075616_069051`. Đây mới là
một case thật của corpus legacy, không phải lượt chạy trọn bộ và không được
dùng để tính tỷ lệ của corpus active so với quality bar 85%.

## Lưu ý

- Chưa đạt quality bar nhưng phân tích được nguyên nhân vẫn được tính đủ điểm.
- Số liệu bị chỉnh sửa hoặc che giấu sẽ không được tính.
- Mỗi lượt chạy giữ đủ mọi case kể cả case chưa đạt.
