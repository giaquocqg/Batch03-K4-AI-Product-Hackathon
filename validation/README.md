# Validation — Feedback log từ user test

## Cấu trúc

```
validation/
├── README.md              ← tài liệu này
└── feedback_log.md        ← bảng log nguyên văn từ phiên validation (tạo khi có dữ liệu thật)
```

## Quy trình validation (theo guide §4.2)

### Đối tượng
≥5 người ngoài nhóm, ưu tiên willing users đã khai ở CP1 + thành viên zone khác.

### Một phiên 10 phút/người

1. **Giao task thật** — "Hãy dùng cái này để ôn quiz buổi [X]" → im lặng quan sát, ghi lại bấm gì, kẹt đâu.
2. **Hỏi đúng 3 câu:**
   - "Điều gì khó hiểu hoặc khó chịu nhất?"
   - "Kết quả này bạn có tin không — vì sao?"
   - "Bạn có dùng thật không — vì sao / vì sao chưa?"
3. **Log nguyên văn** — không tóm tắt, không sửa.

### Scaffold bảng log

| # | Người thử (tên/vai) | Willing user? | Task giao | Quan sát (bấm gì, kẹt đâu) | Quote nguyên văn | Mức nghiêm trọng |
|---|---|---|---|---|---|---|
| 1 | `[chờ validation thật]` | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

### Tổng hợp (điền sau khi có đủ ≥5 phiên)

- **Chủ đề lặp nhiều nhất:** `[chờ dữ liệu]`
- **1–2 thay đổi làm trước demo:** `[chờ dữ liệu]` → ghi vào Changelog spec §9
- **Giữ nguyên có lý do:** `[chờ dữ liệu]`
- **Đưa vào backlog:** `[chờ dữ liệu]`

## Lưu ý

- Nếu mọi phản hồi đều là lời khen → phiên test chưa đạt — giao lại task khó hơn hoặc đổi người thử.
- Bảng log phải giữ nguyên văn, không sửa, không tóm tắt.
- Theo PROJECT_RULES: không tự điền survey response, quote, hoặc kết quả validation.
- Chỉ tạo `feedback_log.md` khi bắt đầu phiên thật; mỗi dòng phải truy được về
  người ghi và phiên test tương ứng.
- Scaffold được xem là hoàn tất khi quy trình, câu hỏi và bảng log đã sẵn sàng;
  checkpoint validation chỉ hoàn tất sau khi có ít nhất 5 phiên thật.
