# AI-assisted semantic audit — run_20260731_103502

## Phạm vi và giới hạn

- Đã đọc 16 Study Pack được sinh trong full-run CP3, gồm 160 item cuối
  (5 key point + 5 question/answer mỗi case).
- Mỗi `content` và `answer` được đối chiếu với đúng đoạn `[Txx-NNN]` đã cite.
- Một item chỉ đạt groundedness khi chính các đoạn đã cite hỗ trợ trực tiếp
  toàn bộ mệnh đề quan trọng. Đoạn đúng nằm gần citation nhưng không được cite
  không được dùng để cứu kết quả.
- Một case chỉ đạt semantic precheck khi groundedness, relevance và
  active-recall đều đạt.
- Đây là **AI-assisted precheck**, không phải xác nhận của người chấm thật.
  File `manual-review-run_20260731_103502.csv` vẫn để trống để người thật xác
  nhận hoặc phản biện từng kết luận.

## Kết quả

| Chiều | Kết quả AI-assisted |
|---|---:|
| Groundedness | 3/16 case pass |
| Relevance | 16/16 case pass |
| Active recall | 16/16 case pass |
| Đạt đồng thời cả ba chiều | 3/16 case |

Ba case qua precheck là `GS-03`, `GS-07`, `GS-18`. Mười ba case còn lại có ít
nhất một item không được chính citation đã chọn hỗ trợ trực tiếp. Pattern chính
là model cite tiêu đề mục hoặc câu dẫn, trong khi chi tiết chứng minh nằm ở
segment kế tiếp nhưng không được cite.

Nếu dùng precheck này như nhãn tạm thời, cộng với 6 case `needs_input/rejected`
đã đạt deterministic gate, tổng tạm tính là `9/22 = 40,91%`. Kết quả này thấp
hơn bar 85% và cũng chưa đạt điều kiện `0 mệnh đề không có căn cứ hiện như sự
thật`. Tuy nhiên, đây không phải kết luận quality bar cuối cho đến khi có người
thật xác nhận bảng manual review.

## Hành động sửa được bằng evidence

1. Prompt phải yêu cầu cite đoạn chứa chi tiết, không cite riêng heading/câu
   dẫn kết thúc bằng dấu hai chấm.
2. Thêm semantic citation review ở HITL: giảng viên mở từng citation và sửa mã
   trước khi phê duyệt.
3. Sau khi sửa prompt/validator, chạy lại đủ 22 case; không ghi đè hai full-run
   hiện tại.
4. Người thật vẫn cần xác nhận `manual-review-run_20260731_103502.csv`.

Chi tiết từng case nằm trong
`ai-semantic-audit-run_20260731_103502.csv`.
