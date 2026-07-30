# Active Study Pack corpus

Đây là corpus mặc định của web app, gồm đúng 6 nguồn do chủ dự án cung cấp:

| Transcript | Nguồn |
|---|---|
| `T10` | Paper - AI & LLM Foundation |
| `T11` | Day 01 - AI & LLM Foundation |
| `T12` | Day 02 - Từ yêu cầu mơ hồ đến Problem Statement |
| `T13` | Day 03 - Agentic AI và ReAct |
| `T14` | Day 04 - Prompt Engineering và Tool Calling |
| `T15` | Day 05 - AI Product Thinking và Requirements |

`transcript/` chứa bản đã gắn citation `[Txx-NNN]`. `manifest.json` là bằng
chứng kiểm tra độ phủ: SHA-256 của nguồn kết hợp, ranh giới từng tài liệu, số
dòng nguồn, số segment và hash nội dung chuẩn hoá của từng transcript.

## Quy tắc bảo toàn

- Mỗi dòng nguồn không rỗng được giữ đúng một lần, đúng thứ tự, thành một
  segment citation.
- Không tóm tắt, diễn giải, bổ sung hoặc cắt ngầm nội dung trong bước chuyển
  đổi.
- Dòng rỗng chỉ là định dạng, không được coi là nội dung; khoảng trắng ở hai
  đầu dòng được chuẩn hoá giống parser.
- Sáu transcript cũ trong `data/vlearn-pack/transcript/` phải được giữ nguyên
  để audit và đối chiếu, nhưng không nằm trong danh sách nguồn mặc định của
  web app.

## Tái tạo corpus

Từ thư mục gốc repo:

```bash
python tools/build_study_corpus.py <combined-source.txt>
```

Script chỉ ghi sáu file `transcript-10-clean.md` đến
`transcript-15-clean.md` và `manifest.json`; không xoá corpus cũ.
