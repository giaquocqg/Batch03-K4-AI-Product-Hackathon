# Study Pack 10 phút — Backend

## Kiến trúc

```
codebase/
├── README.md                  ← tài liệu này
├── requirements.txt           ← dependencies
├── schema.py                  ← JSON schema cho Study Pack output
├── transcript_parser.py       ← parser tách transcript thành {id, text}
├── citation_validator.py      ← kiểm tra mã citation tồn tại trong corpus
├── study_pack_generator.py    ← module gọi LLM sinh Study Pack
├── main.py                    ← entry point chạy end-to-end
├── web_app.py                 ← local HTTP server, API và clickable flow
├── web/                       ← HTML/CSS/JS, không có output dựng sẵn
├── test_transcript_parser.py  ← regression test trên data pack thật
├── test_objective_guard.py    ← test scope guard từ golden set thật
└── test_web_app.py            ← HTTP smoke test trên data pack thật
```

Luồng xử lý: transcript Markdown → parser `[Txx-NNN]` → prompt có toàn bộ
đoạn bài giảng → Gemini/OpenAI → JSON Schema Draft 2020-12 → citation
validator → trạng thái `ok`, `limited` hoặc `abstain` → JSON/CLI + trace.
Objective khác lát cắt `Ôn quiz trong 10 phút` bị chặn tất định trước API call.

## Trạng thái triển khai

| Thành phần | Trạng thái | Ghi chú |
|---|---|---|
| Transcript parser | **Thật** | Runtime đọc Paper + Day 01-05 trong `data/study-pack-corpus/transcript/`; corpus VLearn cũ được giữ để regression |
| LLM call | **Thật, đã chạy** | OpenAI run `20260730_075616_069051`; key chỉ đọc từ environment |
| Citation validator | **Thật** | Chỉ chấp nhận mã `[Txx-NNN]` thuộc lecture đã gửi model |
| JSON schema | **Thật** | Enforce field bắt buộc, kiểu, giới hạn và citation không rỗng |
| Trace | **Thật** | Lưu model, source hash, prompt hash, response và kết quả validator; không lưu API key |
| UI / Frontend | CP2 đã nối | Local web flow gọi backend thật; chưa có successful AI run artifact |
| Đăng nhập / Lịch sử | Ngoài phạm vi | Không triển khai hoặc mô phỏng |

Validator tự động chặn item thiếu citation, citation không thuộc lecture đã gửi
model, item chỉ dựa trên đoạn `[không nghe rõ]`, và keyword không xuất hiện
trong nguồn. Độ đúng ngữ nghĩa vẫn phải được người chấm đối chiếu với đoạn
nguồn trong eval.

## Cách chạy

### Cài đặt

Chạy từ thư mục gốc repository với Python 3.10+:

```bash
python -m pip install -r codebase/requirements.txt
```

### Thiết lập API key

```bash
# Gemini (ưu tiên)
set GOOGLE_API_KEY=your-key-here

# Hoặc OpenAI
set OPENAI_API_KEY=your-key-here
```

PowerShell dùng `$env:GOOGLE_API_KEY = "..."` hoặc
`$env:OPENAI_API_KEY = "..."`.

**Không hard-code API key trong code. Không commit file `.env` vào repo.**

### Chạy

```bash
python codebase/main.py --transcript data/study-pack-corpus/transcript/transcript-10-clean.md
```

Clickable flow CP2:

```bash
python codebase/web_app.py
```

Mở `http://127.0.0.1:8000`. Flow web không có response mẫu: nút tạo pack gọi
thẳng generator thật; thiếu API key sẽ hiện lỗi cấu hình từ backend.

Ghi kết quả JSON để chấm:

```bash
python codebase/main.py --transcript data/study-pack-corpus/transcript/transcript-10-clean.md --output eval/results/run_manual.json
```

Nếu không có `GOOGLE_API_KEY` hoặc `OPENAI_API_KEY`, chương trình dừng trước
lời gọi model. Repository hiện không chứa API key hay output AI dựng sẵn.

Run OpenAI đầu tiên được giữ tại
`eval/results/run_cp2_openai_transcript01_attempt3.json`: schema pass, 10/10
citation occurrence hợp lệ, 1 keyword ngoài nguồn bị loại và status
`limited`. Hai attempt fail trước đó cũng được giữ để audit, không bị xoá.

### Chạy test parser

```bash
python -m pytest codebase/ -v
```

Test dùng trực tiếp corpus active, bộ VLearn cũ cho regression và input từ
`golden_set.json`; không dùng response AI giả. Bộ test xác nhận đủ 1.456
segment từ Paper + Day 01-05, hash nội dung khớp manifest, web chỉ liệt kê
corpus mới, parser không cắt ngầm transcript dài và objective ngoài lát cắt bị
chặn trước khi gọi API.

## Quy tắc phát triển

Theo `PROJECT_RULES.md`:
1. Không dùng mock response hoặc hard-coded AI output.
2. Nếu thiếu API key → dừng và yêu cầu đầu vào; không dùng giá trị thay thế.
3. Mọi lần gọi API giữ trace kiểm tra lại, kể cả API/JSON/schema error.
4. Không commit API key, `.env`, hoặc bản sao data pack vào repo nộp bài.
5. Không xoá/ghi đè `data/vlearn-pack/transcript/`; runtime chỉ dùng
   `data/study-pack-corpus/transcript/` theo quy tắc trong `AGENTS.md`.
