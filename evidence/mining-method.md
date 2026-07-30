# Phương pháp mining chatlog cho Hướng C

## Mục đích

Tài liệu này mô tả cách tạo bằng chứng định lượng từ chatlog VLearn. Kết quả chỉ phản ánh các chuỗi ký tự khớp rule trong dữ liệu được cấp; chưa phải kết luận về ý định, mức đau hoặc chất lượng câu trả lời.

## Nguồn dữ liệu

- File đầu vào: `data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv`.
- Data dictionary: `data/vlearn-pack/chatlog/DATA_DICTIONARY.md`.
- Script: `evidence/mine_chatlog.py`.
- Kết quả máy sinh từ file thật: `evidence/mining-results.json`.
- Mẫu cần hai người kiểm tra độc lập: `evidence/manual-audit.csv`.
- Khóa nhóm mẫu, chỉ mở sau khi cả hai người chấm xong: `evidence/manual-audit-key.json`.
- Phiếu độc lập cho reviewer 1: `evidence/manual-audit-reviewer-1.csv`.
- Phiếu độc lập cho reviewer 2: `evidence/manual-audit-reviewer-2.csv`.

Script lưu SHA-256 của file nguồn trong kết quả để xác định chính xác phiên bản dữ liệu đã được phân tích.

## Đơn vị phân tích

Một đơn vị là một `turn_id` có đúng một message `student` và một message `tutor`. Script báo riêng turn không đúng cấu trúc này và không đưa chúng vào phân tích.

Mỗi candidate được báo theo ba chỉ số độc lập:

- Số turn khớp rule.
- Số `conversation_id` duy nhất có turn khớp.
- Số `user_id` duy nhất có turn khớp.

Các candidate có thể chồng lấn. Không cộng số của các candidate để tạo tổng chung.

## Tiền xử lý

1. Đọc CSV bằng `utf-8-sig` và parser CSV chuẩn để giữ đúng content nhiều dòng.
2. Chuẩn hóa Unicode về NFC.
3. Với message student, loại một wrapper đầu chuỗi có dạng `(Trang N, đoạn được chọn: "...")` nếu tồn tại.
4. Không sửa chính tả, không dịch và không gọi mô hình AI.

## Rule phân loại

### Study Pack

Một turn khớp khi nội dung student sau tiền xử lý chứa ít nhất một nhóm từ khóa được khai báo trong `STUDY_PACK_PATTERNS`, gồm các dạng của:

- `tóm tắt`, `tóm gọn`, `tổng hợp`;
- `ý chính`, `nội dung chính`;
- `ghi chú`, `note`;
- `mindmap`, `sơ đồ tư duy`, `hệ thống hóa`.

### Course Action Hub

Một turn chỉ khớp khi đồng thời có:

- Từ chỉ tài nguyên: `slide`, `tài liệu`, `PDF`, `file`, `link`.
- Từ chỉ hành động hoặc lỗi: `tải`, `download`, `lấy`, `read_file`, không xem/mở/tải được, hoặc `failed to fetch`.

### Concept-to-Micro-Lab

Một turn khớp khi có một trong các cấu trúc hẹp:

- Yêu cầu cho/lấy/nêu ví dụ.
- Ví dụ cụ thể, thực tế hoặc dễ hiểu.
- Gợi ý use case.
- Hướng dẫn hoặc bắt đầu lab/thực hành.
- Hỏi bài lab làm gì hoặc yêu cầu gì.

## Heuristic phản hồi không đáp ứng

Với các turn Study Pack, script đánh dấu tín hiệu failure nếu 300 ký tự đầu của tutor bắt đầu bằng `xin lỗi`, `rất tiếc`, hoặc cấu trúc `hiện tại ... không tìm/không thể`.

Đây chỉ là tín hiệu từ vựng. Không được diễn giải nó thành “tutor trả lời sai” trước khi đọc và chấm thủ công.

## Manual audit

Script chọn ổn định 60 turn thật bằng SHA-256 của nhóm mẫu và ID, không dùng random không seed:

- 30 `rule_positive`: khớp Study Pack.
- 10 `near_boundary_unlabeled`: không khớp Study Pack nhưng có từ gần chủ đề như quiz, ôn tập, trọng tâm, keyword, kiến thức, nội dung, bài học hoặc slide.
- 20 `rule_negative`: không khớp Study Pack và không thuộc nhóm near-boundary trên.

`near_boundary_unlabeled` không phải nhãn đúng/sai. Worksheet không hiển thị nhóm mẫu hoặc rule đã khớp, được xáo thứ tự ổn định, và để trống toàn bộ cột reviewer. Mapping kỹ thuật nằm trong `manual-audit-key.json`; không được mở file key trước khi cả hai reviewer nộp nhãn.

Nhãn người chấm được phép dùng:

- `positive`: user thực sự yêu cầu tóm tắt hoặc hệ thống hóa nội dung học.
- `negative`: user không yêu cầu công việc trên.
- `unclear`: không đủ ngữ cảnh để quyết định.

Hai reviewer điền hai file riêng được chuẩn bị sẵn và không xem nhãn của nhau trước khi hoàn tất. Sau khi nhận đủ hai bản, ghép nhãn theo `audit_id`. Nếu bất đồng, cùng đọc lại định nghĩa label rồi ghi `final_label` và lý do trong `review_note`; không sửa nhãn ban đầu.

Script từ chối chạy đè nếu phát hiện `reviewer_label` hoặc `reviewer_note` đã có dữ liệu trong một phiếu reviewer. Điều này bảo vệ kết quả do con người nhập. Muốn chạy lại rule sau audit, trước tiên phải giữ nguyên hai phiếu đã hoàn tất ở vị trí khác có kiểm soát.

## Cách chạy

Từ thư mục gốc repository:

```bash
python evidence/mine_chatlog.py
```

Script ghi đè hai artifact máy sinh:

```text
evidence/mining-results.json
evidence/manual-audit.csv
evidence/manual-audit-key.json
evidence/manual-audit-reviewer-1.csv
evidence/manual-audit-reviewer-2.csv
```

## Giới hạn

- Phương pháp lexical có thể bỏ sót cách diễn đạt không chứa từ khóa và có thể bắt nhầm câu chứa từ khóa nhưng có ý định khác.
- Log chỉ bao phủ thời gian và chế độ sử dụng ghi trong data pack; không được tự suy rộng sang toàn bộ học viên.
- Số turn không chứng minh hậu quả, thời gian bị mất, cải thiện điểm số hoặc willingness-to-use.
- Manual audit và khảo sát người dùng là bắt buộc trước khi khóa problem statement và impact.
