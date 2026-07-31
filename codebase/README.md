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
├── review_store.py            ← bản nháp HITL, revision, approval và audit log
├── main.py                    ← entry point chạy end-to-end
├── web_app.py                 ← local HTTP server, API và clickable flow
├── web/                       ← HTML/CSS/JS, không có output dựng sẵn
├── test_transcript_parser.py  ← regression test trên data pack thật
├── test_objective_guard.py    ← test scope guard từ golden set thật
├── test_review_store.py       ← test vòng đời review trên corpus thật
├── test_recall_evaluator.py   ← test semantic matcher chỉ dùng citation của câu
└── test_web_app.py            ← HTTP smoke test trên data pack thật
```

Luồng xử lý: transcript Markdown → parser `[Txx-NNN]` → prompt có toàn bộ
đoạn bài giảng → Gemini/OpenAI → JSON Schema Draft 2020-12 → citation
validator → trạng thái `ok`, `limited` hoặc `abstain` → bản nháp giảng viên
→ sửa/thêm/xóa/sắp xếp hoặc tạo lại riêng một câu → kiểm tra lại schema và
citation → phê duyệt/khóa bản. Mỗi bước review có revision và audit log.
Objective khác lát cắt `Ôn quiz trong 10 phút` bị chặn tất định trước API call.

Giao diện học viên chạy một **recall session** cục bộ trong tab: chỉ hiện một
câu và buộc nhập câu trả lời trước khi mở đáp án/citation. Backend dùng model
để so khớp linh hoạt câu trả lời với **đáp án/citation của bản nháp HITL hiện
hành** (hoặc bản đã phê duyệt) và chỉ các đoạn citation của chính câu đó; đạt
từ 60% sẽ đi tiếp, chưa đạt sẽ được chèn lại sau đúng một câu khác. Phản hồi
luôn hiện đáp án và mã căn cứ để người học kiểm tra.
`Đúng ngay lần đầu` là tỷ lệ câu đạt ngưỡng trong phiên hiện tại, không phải
điểm quiz, đánh giá năng lực, lịch sử học tập hay hồ sơ của người học. Thuật
toán hàng đợi có test ở `web/recall_session.test.js`; đối chiếu ngữ nghĩa có
test ở `test_recall_evaluator.py`.

## Trạng thái triển khai

| Thành phần | Trạng thái | Ghi chú |
|---|---|---|
| Transcript parser | **Thật** | Runtime đọc Paper + Day 01-05 trong `data/study-pack-corpus/transcript/`; corpus VLearn cũ được giữ để regression |
| LLM call | **Thật, đã chạy** | `LLM_PROVIDER` là primary; nếu cả hai key có mặt thì provider còn lại là backup cho lỗi API/quota/network; key chỉ đọc từ environment |
| Citation validator | **Thật** | Chỉ chấp nhận mã `[Txx-NNN]` thuộc lecture đã gửi model |
| JSON schema | **Thật** | Enforce field bắt buộc, kiểu, giới hạn và citation không rỗng |
| Trace | **Thật** | Lưu model, source hash, prompt hash, response và kết quả validator; không lưu API key |
| HITL giảng viên | **Thật** | Output AI là bản nháp; hỗ trợ sửa, thêm, xóa, đổi thứ tự, tạo lại một câu và phê duyệt |
| Đối chiếu active recall | **Thật, source-bounded** | Model chỉ nhận câu hỏi, đáp án đã duyệt, câu trả lời và citation của câu; schema chặn output sai cấu trúc/citation ngoài phạm vi |
| UI / Frontend | **Đã nối backend** | Local web flow gọi generator và review API thật; dashboard học viên chỉ có recall, dashboard giảng viên thêm HITL review |
| Đăng nhập / Lịch sử | Ngoài phạm vi | Không triển khai hoặc mô phỏng |
| Access gate | **Thật** | Public/non-loopback bind bắt buộc bearer token; API dữ liệu trả `401` nếu thiếu/sai token |

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

### Thiết lập API key và xác nhận data policy

```bash
# Gemini là primary
set LLM_PROVIDER=gemini
set EXTERNAL_AI_DATA_POLICY_CONFIRMED=true
set GOOGLE_API_KEY=your-key-here

# OpenAI là backup khi Gemini call lỗi
set OPENAI_API_KEY=your-openai-key-here
```

PowerShell dùng `$env:GOOGLE_API_KEY = "..."` và
`$env:OPENAI_API_KEY = "..."`. Khi cả hai key tồn tại, `LLM_PROVIDER` quyết
định provider chính; provider còn lại được thử đúng một lần nếu lời gọi chính
lỗi API, quota hoặc network. Output đã nhận nhưng sai JSON/schema/citation
không kích hoạt fallback để tránh che failure chất lượng. Trace và metadata
ghi lại từng attempt, không ghi API key.

**Không hard-code API key trong code. Không commit file `.env` vào repo.**
Không đặt `EXTERNAL_AI_DATA_POLICY_CONFIRMED=true` trước khi đã kiểm tra policy
cho đúng các account/project đang dùng, bao gồm provider dự phòng. Theo
`02-guide.md` §3.4, Gemini free tier
được dùng với data giả hoặc data pack; tuy vậy vẫn phải gửi tối thiểu cần thiết
và hiểu chính sách dùng/lưu giữ dữ liệu của account/API. Tham khảo:
[Gemini API Terms](https://ai.google.dev/gemini-api/terms),
[Gemini logging policy](https://ai.google.dev/gemini-api/docs/logs-policy) và
[OpenAI business data privacy](https://openai.com/business-data/).

### Chạy

```bash
python codebase/main.py --transcript data/study-pack-corpus/transcript/transcript-10-clean.md
```

Chạy đủ 22 golden case qua đúng runtime local đã cấu hình provider:

```bash
python eval/run_golden_set.py --base-url http://127.0.0.1:8000
```

Runner giữ full output trong `eval/private-results/` bị gitignore và chỉ ghi
summary đã redact vào `eval/results/`. Automated gate không thay thế bước người
chấm đọc groundedness, relevance và active recall.

Clickable flow CP2:

```bash
python codebase/web_app.py --host 127.0.0.1 --port 8000
```

Mở `http://127.0.0.1:8000`. Flow web không có response mẫu: nút tạo pack gọi
thẳng generator thật; thiếu API key sẽ hiện lỗi cấu hình từ backend. Sau khi
tạo, Study Pack luôn ở trạng thái **Bản nháp AI**. Giảng viên chọn **Chỉnh sửa
câu hỏi** để sửa nội dung/đáp án/citation, thêm, xóa, đổi thứ tự hoặc gọi model
tạo lại riêng một câu. Nút **Phê duyệt Study Pack** chỉ thành công khi đủ số
câu yêu cầu và toàn bộ citation hợp lệ; bản đã duyệt chuyển sang chỉ đọc.

Header cho phép đổi giữa **Học viên** và **Giảng viên**. Đây là tách giao diện
để demo flow: cả hai thấy cùng Study Pack, còn giảng viên có thêm HITL panel.
Nó **không** thay cho login hoặc phân quyền backend; không được dùng để bảo vệ
dữ liệu hay khẳng định student không thể gọi review API.

Runtime lưu generation trace ở `codebase/traces/` và review audit ở
`codebase/traces/reviews/`. Hai thư mục này bị gitignore; không chứa API key.
Full eval output phải lưu trong `eval/private-results/` (bị gitignore); repo
chỉ giữ summary đã redaction, hash và số liệu kiểm tra.

### Public bind / Docker

Public bind luôn yêu cầu `APP_ACCESS_TOKEN` dài ít nhất 24 ký tự. Frontend yêu
cầu người dùng nhập token và chỉ giữ nó trong `sessionStorage` của tab.

Docker image không chứa data pack. Corpus phải nằm ở private read-only mount và
được trỏ bằng `STUDY_PACK_DATA_ROOT` sau khi policy lưu trữ của host được duyệt:

```bash
docker run --rm -p 127.0.0.1:8000:8000 \
  -e APP_ACCESS_TOKEN=<random-24+-chars> \
  -e STUDY_PACK_DATA_ROOT=/protected-data/transcript \
  -v <authorized-local-transcript-dir>:/protected-data/transcript:ro \
  study-pack
```

Không deploy Render với data pack nằm trong Git/Docker image. `render.yaml`
chỉ là scaffold fail-closed; service cần private corpus mount và access token
trước khi có thể phục vụ dữ liệu.

Ghi kết quả JSON để chấm:

```bash
python codebase/main.py --transcript data/study-pack-corpus/transcript/transcript-10-clean.md --output eval/private-results/run_manual.json
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
