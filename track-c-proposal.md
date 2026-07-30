# De xuat Huong C - Study Pack sau buoi hoc

> Trang thai: gia thuyet san pham co evidence lexical tu data pack, chua qua manual audit va khao sat nguoi dung, chua thay the `spec.md` chinh thuc.
> Ngay ra soat nguon ngoai: 30/07/2026.

## 1. Quyet dinh de xuat

**Ten tam:** Study Pack 10 phut.

**Huong:** C - Lan mo.

**Problem statement (khong co chu AI):** Hoc vien sau mot buoi hoc dai can on trong tam va chuan bi quiz, nhung phai tu tong hop nhieu trang tai lieu va thuong khong nhan duoc ban tom tat du pham vi, dan den kho biet nen nho va tu kiem tra dieu gi.

**Core JTBD:** On lai kien thuc trong tam cua mot buoi hoc de biet minh da hieu gi va con hong o dau truoc quiz.

**Lat cat mot cau:** Mot hoc vien vua hoc xong mot buoi chon muc tieu "on quiz trong 10 phut"; he thong quyet dinh 5 y trong tam va 5 cau tu kiem tra tu transcript; hoc vien nhan mot study pack mot trang, moi y va dap an deu co ma doan nguon.

**Ly do day la Huong C:** San pham tao mot artifact on tap chu dong sau buoi hoc, khong toi uu flow hoi-dap cua VLearn tutor va khong phai tro ly Discord.

## 2. Evidence trong data pack

### 2.1 Pham vi du lieu

- `2.522` dong, tuong ung `1.261` cap tin nhan hoc vien-tutor.
- `369` hoc vien an danh, `585` hoi thoai, trong khoang 22-29/07/2026.
- `6` transcript sach, dung `700` doan co ma `[Txx-NNN]`.

### 2.2 Ket qua mining

- `146/1.261` turn (`11,58%`) khop rule lexical Study Pack.
- Cac turn khop rule den tu `103/369` user an danh (`27,91%`) va `125/585` hoi thoai (`21,37%`).
- Trong 146 turn, rule `tom_tat` khop 125 lan, `y_chinh` 17 lan, `tong_hop` 12 lan, `noi_dung_chinh` 8 lan, `note` 7 lan, `tom_gon` 2 lan va `mindmap` 1 lan. Mot turn co the khop nhieu rule, nen khong cong cac so nay thanh tong.
- `47/146` turn co phan hoi tutor khop heuristic failure o 300 ky tu dau (`32,19%`); day la tin hieu lexical, khong phai danh gia chat luong ngu nghia.
- Nguon so lieu may sinh: `evidence/mining-results.json`, voi SHA-256 file data `400ce4ce5c1c58189be9ca0630bd517ca69cfcac637f0f802edec70f4f796cad`.

Nam vi du ngan, da an danh va giu nguyen van:

- `[C0018/T0699]`: "tóm tắt toàn bộ slide sau đó đưa ra các ý chính"
- `[C0057/T0415]`: "tóm tắt nội dung, đưa ra keyword cần nhớ"
- `[C0089/T0952]`: "Tóm tắt kiến thức trọng tâm của ngày hôm nay"
- `[C0093/T0411]`: "tóm tắt nội dung cần học trong ngày hôm nay cho toio"
- `[C0573/T0257]`: "tóm tắt những ý chính, chi tiết để tôi có thể làm quiz kahoot cuối giờ"

### 2.3 Phuong phap dem co the kiem lai

1. Chay `python evidence/mine_chatlog.py`; script doc CSV bang `utf-8-sig` va parser CSV chuan.
2. Chi phan tich `turn_id` co dung mot message student va mot message tutor; lan chay hien tai co 1.261/1.261 turn hop le.
3. Bo mot wrapper doan duoc chon o dau noi dung student neu khop dung mau khai bao trong code.
4. Danh dau mot turn theo cac regex cong khai trong `evidence/mine_chatlog.py`; khong dung model AI de phan loai.
5. Moi turn chi tinh mot lan cho moi candidate; dem them `user_id` va `conversation_id` duy nhat.
6. Danh dau failure heuristic neu 300 ky tu dau cua tutor bat dau bang `xin loi`, `rat tiec`, hoac mau `hien tai... khong tim/khong the`.

### 2.4 Gioi han cua evidence

- Log chi co tam ngay va `100%` o che do `in_class`; khong dai dien chac chan cho toan bo khoang 1.000 hoc vien.
- Log chung minh nhu cau xuat hien, chua chung minh so phut bi mat, tac dong len diem quiz hay san sang dung san pham.
- Phan loai bang tu khoa co the bo sot cach dien dat khac hoac bat nham; can kiem tra tay mot mau truoc khi nop evidence chinh thuc.
- `47/146` la heuristic theo cach mo dau cau tra loi, khong du de ket luan tutor tra loi sai.
- Tat ca con so lexical phai cho ket qua manual audit truoc khi duoc dung de ket luan ve nhu cau that.

## 3. Bang impact ba ung vien

| Ung vien | So nguoi gap trong log | Tan suat quan sat | Ton moi lan | Kha thi 1,5 ngay | Quyet dinh |
|---|---:|---:|---|---|---|
| Study Pack 10 phut | 103 user, 146 turn khop rule | 1,42 turn/user khop rule | Chua co so phut/diem; can khao sat | Cao: 1 man hinh, 1 AI call, transcript co san | Ung vien uu tien, chua chot |
| Course Action Hub | 28 user, 29 turn khop rule | 1,04 turn/user khop rule | Chua co so phut; co nguy co bo sot nguon | Trung binh: can catalog link/deadline chinh thong va integration | Tam xep sau |
| Concept-to-Micro-Lab | 18 user, 22 turn khop rule | 1,22 turn/user khop rule | Chua co so lieu | Kha cao, nhung can duyet do dung cua lab/code | Tam xep sau |

**Tin hieu dinh luong hien co:** Study Pack co so user khop rule cao gap `3,68` lan Course Action Hub va `5,72` lan Concept-to-Micro-Lab. Day chua phai quyet dinh chot cho den khi manual audit va khao sat dat nguong.

**Dieu chua duoc phep tuyen bo:** "tiet kiem X phut", "tang Y diem", "cai thien ket qua hoc" cho den khi co du lieu validation.

## 4. Rasoat thuc te va gia tri cua AI

### 4.1 Workflow hien tai gia dinh can xac minh

1. Hoc vien mo lai slide, transcript hoac video.
2. Tu tim noi dung co kha nang vao quiz.
3. Ghi lai y chinh va keyword.
4. Tu nghi cau hoi hoac nhờ cong cu tong quat tao quiz.
5. Quay lai nguon khi gap noi dung khong chac.

AI co gia tri o buoc 2-4 vi phai hieu ngon ngu tu nhien, nen y chinh tren nhieu doan va tao cau hoi theo ngu canh. Viec mo citation, an/hien dap an va dieu huong phai dung logic tat dinh, khong giao cho AI.

### 4.2 Muc automation

**Augment**, khong automate viec hoc.

- He thong tu dong tao ban nhap study pack.
- Hoc vien quyet dinh y nao dung de on, mo nguon de kiem tra, sua muc tieu va tao lai.
- Sai kien thuc co the lam hoc vien hoc sai; vi vay moi menh de phai truy duoc ve transcript va khong duoc tu cham diem/nang luc.

### 4.3 Pham vi prototype

Phan that:

- Chon mot trong sau transcript co san.
- Chon muc tieu co dinh: `On quiz trong 10 phut`.
- Mot loi goi LLM o quyet dinh trung tam de tao output co cau truc.
- Kiem tra citation bang code: ma doan phai ton tai trong corpus da dua vao model.
- Hien 5 y trong tam, toi da 8 keyword, 5 cau active recall, dap an an va citation co the mo.

Phan co the mock:

- Dang nhap, lich su, dong bo VLearn va analytics.
- Luu feedback lau dai.

Non-goals:

- Khong chat tu do va khong tra loi moi mon hoc.
- Khong tu cham diem quiz hoac gan nhan nang luc hoc vien.
- Khong ca nhan hoa dai han.
- Khong tich hop that voi VLearn/Discord trong hackathon.
- Khong sinh them kien thuc ngoai transcript.

## 5. Nguyen tac PAIR ap dung cu the

| Nguyen tac | Ap dung vao prototype |
|---|---|
| User needs truoc cong nghe | Uu tien kiem chung job on quiz tu 146 turn khop rule, thay vi xuat phat tu y tuong chatbot tong quat. |
| Automation vs augmentation | AI soan ban nhap; hoc vien van tu recall, mo nguon va quyet dinh co tin hay khong. |
| Mental models | Dau flow ghi ro: "Tao tu transcript da chon; co the bo sot y; khong thay the tai lieu goc." |
| Calibrated trust | Moi y va dap an hien `Dua tren [Txx-NNN]`; khong dung confidence % gia. |
| Feedback and control | Co `Chua dung`, ly do `sai nguon/khong trong tam/qua kho`, `Tao lai`, va doi muc tieu. Feedback chi ghi log, khong noi rang model hoc ngay. |
| Graceful failure | Khong du nguon thi abstain, noi ro thieu gi va cho hoc vien mo transcript/chon buoi khac. |
| Human oversight | Khong dua ra diem so hay ket luan hoc vien da hieu; dap an chi hien sau khi hoc vien tu tra loi. |

Thiet ke nay phu hop voi Google PAIR: AI chi nen duoc dung khi tao gia tri rieng so voi rule; task co gia tri ca nhan hoac cost-of-error dang ke nen augment; nguon du lieu va gioi han phai ro; failure phai co duong di tiep. UNESCO va NIST cung ung ho cach tiep can lay con nguoi lam trung tam, quan tri rui ro va danh gia thay vi mac dinh output la dung.

## 6. Bon lop cho kho va kich ban rui ro

| Tinh huong | Lop | Hanh vi mong muon |
|---|---|---|
| Model tao mot y khong co trong transcript | 1 - Nguon su that | Loai y do; khong hien neu khong co citation hop le. |
| Citation ton tai nhung khong ho tro menh de | 1 - Nguon su that | Danh fail trong eval; cho user bao `Sai nguon` va mo doan de kiem tra. |
| User khong chon buoi hoc | 2 - Mo ho | Hoi lai mot cau de chon transcript; khong tu doan. |
| User chon muc tieu qua chung nhu "hoc tat ca" | 2 - Mo ho | De nghi muc tieu ho tro `On quiz trong 10 phut` va neu gioi han output. |
| User yeu cau dap an quiz chinh thuc | 3 - Ngoai pham vi | Tu choi, de nghi cau active recall dua tren transcript. |
| User yeu cau danh gia mot hoc vien khac | 3 - Ngoai pham vi | Tu choi gan nhan; giai thich san pham khong danh gia con nguoi. |
| Tom tat lam mat ngoai le quan trong cua khai niem | 4 - Domain | Uu tien tinh dung va citation hon du so luong; neu khong the nen an toan thi bao thieu can cu. |
| Cau hoi co nhieu dap an dung nhung output chi chap nhan mot | 4 - Domain | Hien rubric/dap an goi y, khong cham dat/truot; cho mo nguon va sua cau hoi. |
| Transcript co `[khong nghe ro]` trong doan can dung | 1 + 4 | Khong dung doan do lam can cu duy nhat; thong bao chat luong nguon han che. |
| Prompt injection nam trong transcript | 1 + 3 | Xem transcript la du lieu, khong la lenh; chi sinh schema study pack. |

Kich ban dang lo nhat: citation dung cu phap nhung khong thuc su chung minh dap an. Kiem tra ma doan ton tai la can nhung chua du; golden set phai cham semantic groundedness bang nguoi.

## 7. Cac duong di trai nghiem

- **Happy path:** chon transcript -> tao pack -> tu tra loi -> hien dap an va citation -> mo dung doan nguon.
- **Low-confidence:** nguon co nhieu doan `[khong nghe ro]` hoac khong du noi dung -> hien `Can kiem tra`, giam so cau va de nghi mo tai lieu goc.
- **Failure/khong can cu:** khong co citation hop le -> khong hien menh de, noi ro khong du nguon va cho chon transcript khac.
- **Correction:** hoc vien bam `Chua dung`, chon ly do, sua muc tieu hoac tao lai; van co the mo transcript de on thu cong.

## 8. Dinh nghia chat luong va ke hoach eval

### 8.1 Chieu chat luong

- **Groundedness:** moi menh de kien thuc va dap an phai co it nhat mot citation; nguoi cham doc doan nguon va xac nhan no ho tro truc tiep menh de.
- **Citation validity:** 100% ma citation ton tai trong transcript da chon va link mo dung doan.
- **Relevance:** moi y phuc vu muc tieu on quiz cua buoi da chon; khong lan sang noi dung ngoai buoi.
- **Active recall:** cau hoi yeu cau nguoi hoc tu nho/giai thich/ap dung truoc khi hien dap an, khong chi la chep lai cau trong tom tat.
- **Graceful failure:** input thieu, ngoai pham vi hoac khong co can cu phai duoc tu choi/hoi lai va co buoc tiep theo.
- **Do gon:** dung 5 y, toi da 8 keyword va 5 cau; pack doc duoc trong mot man hinh dai hop ly.

### 8.2 Golden set toi thieu 20 case

- 8 case thuong tu 4-6 transcript.
- 8 case cho kho, moi lop it nhat 2 case.
- 2 case hiem co `[khong nghe ro]` hoac citation chong cheo.
- 2 case tan cong/ngoai pham vi.
- It nhat 10 case phat trien tu chatlog that va chi luu ma conversation/turn cung trich ngan can thiet.

**Quality bar de xuat, chua duoc chot thay nhom:** it nhat `85%` case dat toan bo tieu chi, `100%` citation hop le ve cu phap, va `0` menh de khong co can cu duoc hien nhu su that. Nhom phai chot bar trong `spec.md` truoc 23:59 ngay 1 va khong doi sau do.

## 9. Kha thi ky thuat

### Kien truc toi thieu

1. Parser tach transcript thanh `{id, text}`.
2. Chon transcript va dua cac chunk can thiet vao prompt trong gioi han context.
3. LLM tra JSON schema co `key_points`, `keywords`, `questions`, `answers`, `citations`.
4. Validator tu choi item co citation khong ton tai, trung lap hoac sai schema.
5. UI render study pack, dap an an, link citation va feedback.
6. Luu trace da loai noi dung data nhay cam de chung minh AI call that.

### Phuong an khi context qua dai

- Prototype chi ho tro mot transcript moi lan.
- Neu van qua dai, chia chunk va lay candidate bang mot buoc, sau do synthesis bang buoc hai; khong can vector database trong hackathon.
- Uu tien deterministic validator va output schema hon them framework RAG phuc tap.

### Uoc luong 1,5 ngay

- 2-3 gio: chot flow, schema, 20 golden cases va prompt dau.
- 3-4 gio: parser, AI call, validator va trace.
- 3-4 gio: UI happy path + low-confidence + failure + correction.
- 2-3 gio: chay golden set, sua mot failure nghiem trong, chay lai toan bo.
- 5 phien x 10 phut: validation voi nguoi ngoai nhom, sau do sua 1-2 diem.

Kha thi o muc **Mock co loi AI that**. Working integration voi VLearn khong kha thi va khong can cho diem prototype.

## 10. Validation bat buoc truoc khi chot

Can khao sat it nhat 20 hoc vien ngoai nhom va log tung cau tra loi nguyen van. Hoi ve hanh vi gan nhat, khong hoi dan dat ve feature:

1. Lan gan nhat on quiz sau mot buoi hoc, ban da lam theo cac buoc nao?
2. Ban mat bao lau de tim va ghi lai phan trong tam?
3. Phan nao kho nhat: tim dung nguon, chon y quan trong, hay tu kiem tra?
4. Lan do ban co bo qua buoc nao khong? Hau qua cu the la gi?
5. Ban da dung tutor/ChatGPT/cong cu nao? No fail o dau?
6. Neu co mot ban on 10 phut kem citation, dieu gi khien ban khong tin hoac khong dung no?
7. Ban co san sang thu prototype truoc demo khong? Ghi ten/vai tro neu dong y.

Tieu chi chot tiep:

- It nhat 10/20 nguoi xac nhan da gap pain trong lan on gan nhat.
- Co du lieu thoi gian thuc te de dien cot `ton moi lan`, khong tu uoc luong.
- It nhat 3 nguoi co ten dong y thu prototype; validation cuoi can it nhat 5 nguoi va co toi thieu 2 willing users tu CP1.

Neu khao sat khong dat nguong, khong nen co chon Study Pack chi vi log co nhieu request; quay lai bang impact va xem xet Concept-to-Micro-Lab.

## 11. Demo 5 phut de xuat

1. Neu manual audit xac nhan rule du tin cay, cho con so lexical `146/1.261 turn`, `103/369 user` cung ket qua audit va mot quote ngan.
2. Cho bang impact ba ung vien va ly do loai hai ung vien.
3. Demo case chuan: tao pack va mo citation.
4. Demo case kho: transcript thieu can cu; he thong khong bia va tra user ve nguon.
5. Cho ket qua golden set so voi quality bar da chot va mot failure that.
6. Cho hai quote validation va thay doi da lam tu feedback.

## 12. Nguon chinh thong tham khao

- Google PAIR, People + AI Guidebook v2 - User Needs + Defining Success: <https://pair.withgoogle.com/guidebook-v2/chapter/user-needs/>
- Google PAIR - Mental Models: <https://pair.withgoogle.com/guidebook-v2/chapter/mental-models/>
- Google PAIR - Explainability + Trust: <https://pair.withgoogle.com/guidebook-v2/chapter/explainability-trust/>
- Google PAIR - Feedback + Control: <https://pair.withgoogle.com/guidebook-v2/chapter/feedback-controls/>
- Google PAIR - Errors + Graceful Failure: <https://pair.withgoogle.com/guidebook-v2/chapter/errors-failing/>
- UNESCO, Guidance for Generative AI in Education and Research, 2023: <https://unesdoc.unesco.org/ark:/48223/pf0000386693>
- NIST AI Risk Management Framework; trang hien tai xac nhan AI RMF 1.0 dang duoc sua doi va GenAI Profile NIST AI 600-1 phat hanh 26/07/2024: <https://www.nist.gov/itl/ai-risk-management-framework>
- U.S. Department of Education AI Guidance, page last reviewed 10/02/2026; inventory co cac use case summarization/RAG nhung khong phai bang chung ve hieu qua hoc tap: <https://www.ed.gov/about/ed-overview/artificial-intelligence-ai-guidance>

## 13. Ket luan thuc tien

Study Pack la ung vien manh nhat trong data hien co va co the build trong 1,5 ngay neu giu dung lat cat. Rui ro lon nhat khong nam o UI hay kha nang goi model, ma o viec lua chon sai trong tam va tao citation co ve hop le nhung khong ho tro menh de. Vi vay san pham chi dang **augment**, citation phai mo kiem tra duoc, failure phai tra quyen kiem soat cho hoc vien, va claim ve tac dong hoc tap chi duoc dua ra sau validation.
