# Eval — Golden Set & Kết quả đánh giá

## Cấu trúc

```
eval/
├── README.md           ← tài liệu này
├── golden_set.json     ← 22 case kiểm thử theo cơ cấu guide §2.6
└── results/            ← artifact mỗi lượt chạy thật (tạo khi có API key)
```

## Golden set

File `golden_set.json` chứa 22 case. `expected_behavior` là tiêu chí chấm đã
chốt, còn trường `result` được giữ ở trạng thái chờ cho đến khi có run thật.

| Nhóm | Số case | Mô tả |
|---|---|---|
| Thường + thường từ chatlog | 10 | Input chuẩn từ 6 transcript |
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
# Chạy một case thật trên backend
python codebase/main.py --transcript <transcript_path> --output eval/results/run_<timestamp>.json

# Chạy test tất định trước eval
python -m pytest codebase/ -v
```

Không tự điền kết quả hàng loạt khi chưa có API key. Một lượt đánh giá hoàn
chỉnh cần giữ output và trace của mọi case đã gọi model, sau đó chấm đủ sáu
chiều. `groundedness`, `relevance`, `active_recall` và các case có
`eval_note` phải được người chấm đọc nguồn; validator code không thay thế bước
này.

## Checklist một lượt thật

1. Tạo thư mục `eval/results/<run-id>/`.
2. Chạy từng case có transcript bằng backend thật, không dùng response giả.
3. Với case không có transcript hoặc ngoài phạm vi, ghi đúng hành vi sản phẩm.
4. Đối chiếu từng citation với đoạn `[Txx-NNN]` và chấm sáu chiều.
5. Giữ cả case fail; tính tỷ lệ qua và so với quality bar 85%.
6. Ghi người chấm, thời điểm, model và trace ID trong bảng kết quả.

GS-09 là invariant áp lên output thật; không inject citation hoặc dựng response
để tạo kết quả. Các case cần hành vi chưa có trong CLI phải được ghi fail/chưa
triển khai, không diễn giải thành pass.

## Lưu ý

- Chưa đạt quality bar nhưng phân tích được nguyên nhân vẫn được tính đủ điểm.
- Số liệu bị chỉnh sửa hoặc che giấu sẽ không được tính.
- Mỗi lượt chạy giữ đủ mọi case kể cả case chưa đạt.
