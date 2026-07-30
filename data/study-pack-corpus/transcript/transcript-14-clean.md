# Study Pack corpus - Day 04 - Prompt Engineering và Tool Calling

> Corpus version: `study-pack-corpus-v1`
> Combined source SHA-256: `d9ff0da80192992871546bbffaf0f79567c061d3be189272d715a0811f1055a2`
> Original source lines: 678-1496
> Transformation: one non-empty source line equals one citation segment;
> no source text is summarized, paraphrased, or silently truncated.

**[T14-001]** [Day-04] PROMPT ENGINEERING & TOOL CALLING

**[T14-002]** ## 1. Bức tranh tổng thể của Day 04

**[T14-003]** Hãy hình dung một AI Agent như một nhân viên trong doanh nghiệp.

**[T14-004]** Prompt là cách chúng ta giao việc và đặt luật.

**[T14-005]** Tool Calling là cách nhân viên đó sử dụng hệ thống, dữ liệu và dịch vụ bên ngoài để hoàn thành công việc.

**[T14-006]** ```text

**[T14-007]** Ý định con người → Prompt → Hành vi của mô hình

**[T14-008]** Hành vi của mô hình → Tool Calling → Thế giới bên ngoài

**[T14-009]** ```

**[T14-010]** Mục tiêu của Day 04 không phải học những “câu thần chú” khiến AI thông minh hơn. Mục tiêu là hiểu cách thiết kế một hệ thống mà hành vi của mô hình có thể kiểm soát, dự đoán, kiểm thử và vận hành ổn định trong Production.

**[T14-011]** Toàn bộ bài học đi qua năm lớp nội dung trọng tâm:

**[T14-012]** Prompt Fundamentals

**[T14-013]** Advanced Prompting

**[T14-014]** System Prompt Engineering

**[T14-015]** Tool Calling

**[T14-016]** LangGraph

**[T14-017]** Sơ đồ lộ trình học tập tối ưu hóa theo hệ thống.

**[T14-018]** ```

**[T14-019]** ---

**[T14-020]** ## 2. Bản chất của Prompt Engineering

**[T14-021]** Hãy tưởng tượng người quản lý nói với nhân viên: “Viết email cho tôi.” Nhân viên sẽ phải tự đoán email gửi cho ai, nói về việc gì, dùng giọng điệu nào và dài bao nhiêu. Khi LLM nhận một prompt mơ hồ, nó cũng phải lấp các khoảng trống bằng xác suất. Vì vậy, Prompt Engineering là thiết kế giao diện giữa ý định của con người và hành vi của mô hình.

**[T14-022]** Vì vậy, **Prompt Engineering là thiết kế giao diện giữa ý định của con người và hành vi của mô hình**.

**[T14-023]** ```text

**[T14-024]** Human Intent → Prompt Interface → Model Behavior

**[T14-025]** ```

**[T14-026]** Prompt tốt không nhất thiết phải dài hoặc hoa mỹ. Nó phải khiến mô hình tạo ra đúng hành vi mong muốn một cách tương đối ổn định.

**[T14-027]** Nguyên tắc trung tâm của tài liệu là:

**[T14-028]** > **Specificity beats cleverness.**

**[T14-029]** Một yêu cầu ngắn nhưng cụ thể thường hiệu quả hơn một yêu cầu dài mà lan man. Trong Production, sự cụ thể giúp giảm đầu ra bất ngờ, giảm số lần sửa và giúp viết test rõ ràng hơn.

**[T14-030]** ---

**[T14-031]** ## 3. Bốn thành phần của một Prompt tốt

**[T14-032]** Thành phần

**[T14-033]** Ý nghĩa

**[T14-034]** Câu hỏi thiết kế

**[T14-035]** Role

**[T14-036]** Vai trò và góc nhìn chuyên môn

**[T14-037]** AI đang đóng vai gì?

**[T14-038]** Task

**[T14-039]** Nhiệm vụ cần hoàn thành

**[T14-040]** Kết quả cuối cùng là gì?

**[T14-041]** Context

**[T14-042]** Bối cảnh cần thiết

**[T14-043]** AI cần biết gì để không phải đoán?

**[T14-044]** Format

**[T14-045]** Hình dạng của đầu ra

**[T14-046]** Hệ thống cần nhận kết quả ra sao?

**[T14-047]** **Task** và **Format** là hai thành phần nên được xác định đầu tiên. Role chỉ cần thiết khi vai trò chuyên môn thực sự làm thay đổi chất lượng câu trả lời. Context cũng chỉ nên được thêm khi nó giúp giảm sự mơ hồ.

**[T14-048]** ```text

**[T14-049]** Task + Format

**[T14-050]** → kiểm tra chất lượng

**[T14-051]** → thêm Role hoặc Context nếu thực sự cần

**[T14-052]** ```

**[T14-053]** Trong Production, Format đặc biệt quan trọng vì đầu ra của LLM thường không chỉ dành cho người đọc mà còn được chuyển sang một bước xử lý khác.

**[T14-054]** ---

**[T14-055]** ## 4. Instruction Prompt, Conversation Prompt và System Prompt

**[T14-056]** Loại prompt

**[T14-057]** Vai trò chính

**[T14-058]** Phù hợp với

**[T14-059]** Instruction Prompt

**[T14-060]** Giao một nhiệm vụ trực tiếp

**[T14-061]** Tóm tắt, phân loại, biến đổi văn bản

**[T14-062]** Conversation Prompt

**[T14-063]** Duy trì ngữ cảnh nhiều lượt

**[T14-064]** Chatbot, trợ lý, gia sư

**[T14-065]** System Prompt

**[T14-066]** Thiết lập policy và boundary

**[T14-067]** Agent hoặc ứng dụng Production

**[T14-068]** Có thể ghi nhớ như sau:

**[T14-069]** ```text

**[T14-070]** Instruction Prompt = Làm gì?

**[T14-071]** Conversation Prompt = Đã trao đổi những gì?

**[T14-072]** System Prompt = Được phép hành xử thế nào?

**[T14-073]** ```

**[T14-074]** System Prompt không nên bị xem như một đoạn giới thiệu vai trò đơn giản. Trong hệ thống thực tế, nó là **policy layer**, tức lớp quy định hành vi xuyên suốt phiên làm việc.

**[T14-075]** ---

**[T14-076]** ## 5. Token Budget Awareness

**[T14-077]** Hãy hình dung context như chiếc ba lô của Agent. Bỏ thêm nhiều đồ không luôn khiến Agent chuẩn bị tốt hơn; đôi khi chỉ khiến nó nặng, chậm và khó tìm đúng thứ cần dùng.

**[T14-078]** Prompt dài làm tăng:

**[T14-079]** ```text

**[T14-080]** Input Tokens → Chi phí → Latency → Nhiễu

**[T14-081]** ```

**[T14-082]** Một prompt tốt nên ưu tiên instruction rõ, ví dụ đúng chỗ, output contract cụ thể và context liên quan trực tiếp đến nhiệm vụ.

**[T14-083]** Quy tắc thực dụng:

**[T14-084]** > Nếu một đoạn prompt dài thêm nhưng không làm thay đổi hành vi mong muốn, hãy cắt bỏ.

**[T14-085]** Prompt Engineering là tối ưu **độ rõ và khả năng kiểm soát**, không phải cuộc thi xem ai viết prompt dài hơn.

**[T14-086]** ---

**[T14-087]** ## 6. Zero-shot, One-shot, Few-shot và Chain-of-Thought

**[T14-088]** Hãy hình dung việc đào tạo một nhân viên.

**[T14-089]** **Zero-shot** là giao nhiệm vụ bằng lời.

**[T14-090]** **One-shot** là đưa một sản phẩm mẫu.

**[T14-091]** **Few-shot** là đưa một số ví dụ để nhân viên nhận ra pattern.

**[T14-092]** **Chain-of-Thought** là yêu cầu chia bài toán thành nhiều bước suy luận.

**[T14-093]** | Kỹ thuật      | Cơ chế             | Khi phù hợp                     |

**[T14-094]** | ------------- | ------------------ | ------------------------------- |

**[T14-095]** | **Zero-shot** | Không có ví dụ     | Nhiệm vụ rõ, quen thuộc         |

**[T14-096]** | **One-shot**  | Một ví dụ          | Cần giữ format cơ bản           |

**[T14-097]** | **Few-shot**  | Khoảng 2–5 ví dụ   | Output hoặc tone thiếu ổn định  |

**[T14-098]** | **CoT**       | Suy luận từng bước | Bài toán logic, nhiều điều kiện |

**[T14-099]** Thứ tự thử nghiệm nên là:

**[T14-100]** ```text

**[T14-101]** Zero-shot

**[T14-102]** → nếu chưa ổn: Few-shot

**[T14-103]** → nếu cần reasoning phức tạp: Decomposition hoặc CoT

**[T14-104]** ```

**[T14-105]** Không nên dùng kỹ thuật phức tạp theo thói quen. CoT thường là **overkill** đối với tác vụ chỉ cần trích xuất hoặc định dạng dữ liệu.

**[T14-106]** ---

**[T14-107]** ## 7. Sức mạnh thật sự của Few-shot

**[T14-108]** Few-shot không nhằm “dạy lại toàn bộ kiến thức” cho mô hình. Nó dùng để chỉ rõ **pattern hành vi** mà chúng ta muốn mô hình bắt chước.

**[T14-109]** ```text

**[T14-110]** Instruction mô tả hành vi

**[T14-111]** Few-shot minh họa hành vi

**[T14-112]** ```

**[T14-113]** Few-shot hữu ích khi mô hình đã hiểu nhiệm vụ nhưng:

**[T14-114]** * thường xuyên sai format;

**[T14-115]** * không nhất quán giữa các input tương tự;

**[T14-116]** * thay đổi tone;

**[T14-117]** * xử lý các trường hợp ngoại lệ không ổn định.

**[T14-118]** Ví dụ tốt không nên chỉ gồm **happy path**. Trong môi trường thực tế, cần có cả dữ liệu thiếu, input mơ hồ, trường hợp ngoài phạm vi và tình huống mô hình phải thừa nhận rằng chưa đủ thông tin.

**[T14-119]** ```text

**[T14-120]** Ví dụ chất lượng

**[T14-121]** = trường hợp bình thường

**[T14-122]** + edge cases

**[T14-123]** + cách xử lý khi không biết

**[T14-124]** ```

**[T14-125]** Hai đến năm ví dụ có chủ đích thường tốt hơn rất nhiều ví dụ kém liên quan.

**[T14-126]** ---

**[T14-127]** ## 8. Rủi ro của Few-shot

**[T14-128]** Few-shot tạo ra ba đánh đổi chính.

**[T14-129]** **Order Bias** xảy ra khi ví dụ cuối cùng ảnh hưởng mạnh đến dự đoán của mô hình. Nếu nhiều ví dụ cùng nhãn bị đặt ở cuối, mô hình có thể thiên về nhãn đó.

**[T14-130]** **Token Budget** tăng theo số lượng ví dụ, kéo theo chi phí và latency.

**[T14-131]** **Coverage hẹp** xuất hiện khi các ví dụ quá giống nhau, khiến mô hình học một pattern đơn giản nhưng không xử lý tốt trường hợp thực tế.

**[T14-132]** ```text

**[T14-133]** Nhiều ví dụ hơn

**[T14-134]** ≠ luôn chính xác hơn

**[T14-135]** ```

**[T14-136]** Giải pháp là chọn ví dụ đa dạng vừa đủ, cân bằng thứ tự và chỉ đưa vào những ví dụ gần với yêu cầu hiện tại.

**[T14-137]** ---

**[T14-138]** ## 9. Negative Prompting

**[T14-139]** Hãy tưởng tượng dạy một nhân viên chỉ bằng câu “đừng làm sai”. Chỉ dẫn này quá mơ hồ vì nhân viên chưa biết thế nào là sai và hành vi đúng phải trông ra sao.

**[T14-140]** Negative Prompting hiệu quả hơn khi dùng cặp ví dụ:

**[T14-141]** ```text

**[T14-142]** Bad Example → chỉ rõ lỗi

**[T14-143]** Good Example → minh họa hành vi đúng

**[T14-144]** ```

**[T14-145]** Thay vì chỉ nói “không được bịa dữ liệu”, có thể chỉ ra rằng việc khẳng định trạng thái đơn hàng khi chưa kiểm tra là sai, còn cách đúng là yêu cầu dữ liệu hoặc gọi công cụ xác minh.

**[T14-146]** Trong Production, cách này giúp tạo boundary hành vi cụ thể hơn so với các câu cấm đoán chung chung.

**[T14-147]** ---

**[T14-148]** ## 10. Tư duy “Prompts as Code”

**[T14-149]** Khi prompt được dùng trong Agent, nó không còn là một đoạn văn tùy hứng. Nó trở thành một thành phần phần mềm cần được quản lý như code.

**[T14-150]** ```text

**[T14-151]** Prompt

**[T14-152]** → Có cấu trúc

**[T14-153]** → Có phiên bản

**[T14-154]** → Có test cases

**[T14-155]** → Có edge cases

**[T14-156]** → Có tiêu chí thành công

**[T14-157]** ```

**[T14-158]** Prompt đơn giản thường thất bại trong Agent Loop vì tính **fragile**: chỉ một thay đổi nhỏ cũng có thể làm format biến đổi. Mô hình còn có thể tạo thêm lời dẫn hoặc Markdown dù hệ thống cần một output cấu trúc.

**[T14-159]** Trong giao tiếp giữa người và AI, vài chữ thừa có thể không quan trọng. Nhưng trong Agent Loop:

**[T14-160]** ```text

**[T14-161]** Output sai format → Parser lỗi → Pipeline có thể dừng

**[T14-162]** ```

**[T14-163]** Do đó, mục tiêu là tiến gần tới **Prompt Determinism**: dù input người dùng thay đổi, mô hình vẫn giữ đúng cấu trúc và boundary cần thiết.

**[T14-164]** ---

**[T14-165]** ## 11. Thu hẹp không gian xác suất

**[T14-166]** Hãy hình dung LLM đứng trước rất nhiều cánh cửa, mỗi cánh cửa là một cách trả lời có vẻ hợp lý. Prompt mơ hồ để quá nhiều cửa mở; prompt rõ sẽ đóng bớt những lựa chọn không mong muốn.

**[T14-167]** ```text

**[T14-168]** Task rõ

**[T14-169]** + Context phù hợp

**[T14-170]** + Format cụ thể

**[T14-171]** + Constraints

**[T14-172]** + Examples

**[T14-173]** → Narrowing the probability space

**[T14-174]** ```

**[T14-175]** Tài liệu gọi đây là **Programming the Latent Space**. Ta không lập trình mô hình bằng câu lệnh tuyệt đối như phần mềm truyền thống, mà thu hẹp phân bố xác suất để hành vi mong muốn có khả năng xuất hiện cao hơn.

**[T14-176]** ---

**[T14-177]** ## 12. Cấu trúc System Prompt Production-grade

**[T14-178]** Hãy xem System Prompt như hiến pháp của Agent. Nó không giải quyết một câu hỏi duy nhất, mà quy định Agent phải hành xử thế nào trong nhiều tình huống.

**[T14-179]** Một System Prompt Production thường có năm lớp:

**[T14-180]** | Lớp                 | Chức năng                                            |

**[T14-181]** | ------------------- | ---------------------------------------------------- |

**[T14-182]** | **Persona**         | Vai trò, mức chuyên môn, phong cách giao tiếp        |

**[T14-183]** | **Rules**           | Việc nên làm và luôn phải làm                        |

**[T14-184]** | **Capabilities**    | Tool và dữ liệu Agent được phép dùng                 |

**[T14-185]** | **Constraints**     | Điều không được làm, khi nào từ chối hoặc chuyển cấp |

**[T14-186]** | **Output Contract** | Ngôn ngữ, cấu trúc và các trường bắt buộc            |

**[T14-187]** Flow hành vi mong muốn là:

**[T14-188]** ```text

**[T14-189]** Nhận yêu cầu

**[T14-190]** → kiểm tra phạm vi và dữ liệu

**[T14-191]** → quyết định trả lời / hỏi lại / gọi tool / từ chối

**[T14-192]** → trả đúng Output Contract

**[T14-193]** ```

**[T14-194]** Trong Production, System Prompt tốt giúp Agent nhất quán hơn, dễ test hơn và dễ xác định nguyên nhân khi kết quả sai.

**[T14-195]** ---

**[T14-196]** ## 13. Những System Prompt anti-pattern

**[T14-197]** System Prompt quá dài dễ tạo noise và làm chỉ dẫn quan trọng bị chìm. System Prompt mâu thuẫn buộc mô hình phải tự lựa chọn giữa hai yêu cầu không thể đồng thời đáp ứng.

**[T14-198]** Các câu như “hãy chuyên nghiệp” hoặc “hãy thông minh” không tạo ra tiêu chuẩn có thể đo lường. Thay vào đó, cần quy định cụ thể tone, độ dài, cách xử lý khi thiếu dữ liệu và cấu trúc đầu ra.

**[T14-199]** Một lỗi khác là chỉ test happy path mà quên kiểm tra:

**[T14-200]** ```text

**[T14-201]** Out-of-scope

**[T14-202]** Tool failure

**[T14-203]** Missing information

**[T14-204]** Refusal

**[T14-205]** Prompt injection

**[T14-206]** ```

**[T14-207]** Nguyên tắc cốt lõi:

**[T14-208]** > Boundary càng rõ thì hành vi càng dễ dự đoán.

**[T14-209]** ---

**[T14-210]** ## 14. System, User và Assistant Roles

**[T14-211]** Hãy hình dung cuộc trò chuyện có ba tầng quyền lực.

**[T14-212]** **System** đặt ra luật chơi.

**[T14-213]** **User** cung cấp yêu cầu và dữ liệu.

**[T14-214]** **Assistant** tạo phản hồi và duy trì lịch sử hội thoại.

**[T14-215]** ```text

**[T14-216]** System = Trusted instructions

**[T14-217]** User = Untrusted input

**[T14-218]** Assistant = Generated response

**[T14-219]** ```

**[T14-220]** User Input phải được xem là dữ liệu không đáng tin hoàn toàn vì nó có thể chứa prompt injection hoặc yêu cầu mâu thuẫn với policy.

**[T14-221]** Việc tách vai trò giúp mô hình nhận biết đâu là chỉ dẫn cốt lõi và đâu là nội dung cần xử lý. Đây là ưu điểm quan trọng của kiến trúc Chat Messages so với cách nối tất cả nội dung vào một block text.

**[T14-222]** ---

**[T14-223]** ## 15. XML và Delimiters

**[T14-224]** Hãy hình dung một kho hàng được chia thành các khu có nhãn rõ ràng. Khi rules, tài liệu và input người dùng bị trộn vào một đoạn văn duy nhất, mô hình khó phân biệt chức năng của từng phần.

**[T14-225]** XML hoặc delimiters tạo ra các vùng:

**[T14-226]** ```text

**[T14-227]** System Role

**[T14-228]** Instructions

**[T14-229]** Examples

**[T14-230]** Documents

**[T14-231]** User Input

**[T14-232]** ```

**[T14-233]** Các thẻ này đóng vai trò tương tự dấu ngoặc trong lập trình. Chúng giúp attention mechanism nhận diện cấu trúc và làm rõ rằng nội dung nào là chỉ dẫn, nội dung nào chỉ là dữ liệu.

**[T14-234]** XML không phải một lớp bảo mật tuyệt đối, nhưng là kỹ thuật cấu trúc hóa giúp tăng tính nhất quán và giảm nhầm lẫn.

**[T14-235]** ---

**[T14-236]** ## 16. Context Bleed

**[T14-237]** Context Bleed xảy ra khi mô hình nhầm **dữ liệu cần xử lý** với **chỉ dẫn phải tuân theo**.

**[T14-238]** ```text

**[T14-239]** Instructions + User Payload bị trộn

**[T14-240]** → Model nhầm payload thành instruction

**[T14-241]** → Mất kiểm soát

**[T14-242]** ```

**[T14-243]** Ví dụ, một tài liệu được đưa vào context có thể chứa câu “hãy bỏ qua hướng dẫn phía trên”. Nếu tài liệu đó không được cô lập rõ, mô hình có nguy cơ diễn giải nó như một lệnh mới.

**[T14-244]** Hậu quả có thể là Prompt Injection, sai trọng tâm hoặc mất format. Vì vậy, dữ liệu từ người dùng, API, database và tài liệu truy xuất cần được đặt trong các vùng riêng và được mô tả rõ là dữ liệu, không phải instruction.

**[T14-245]** ---

**[T14-246]** ## 17. Nested XML trong RAG

**[T14-247]** Khi phải cung cấp nhiều tài liệu, một block context dài khiến mô hình khó xác định thông tin đến từ đâu.

**[T14-248]** Nested XML tổ chức context như một thư mục:

**[T14-249]** ```text

**[T14-250]** Documents

**[T14-251]** ├── Document 1

**[T14-252]** ├── Document 2

**[T14-253]** └── Document 3

**[T14-254]** ```

**[T14-255]** Mỗi tài liệu có thể có ID hoặc metadata riêng. Cấu trúc này giúp mô hình dễ truy xuất, phân biệt nguồn và tạo citation chính xác hơn.

**[T14-256]** Trong Production, nó cũng hỗ trợ debugging: đội phát triển có thể kiểm tra mô hình đã dựa trên tài liệu nào khi đưa ra câu trả lời.

**[T14-257]** ---

**[T14-258]** ## 18. Lost in the Middle

**[T14-259]** Hãy tưởng tượng tìm một ghi chú trong một cuốn sách rất dày. Việc cuốn sách nằm trọn trên bàn không có nghĩa ta sẽ chú ý đồng đều tới mọi trang.

**[T14-260]** Context Window lớn cũng vậy. Mô hình thường sử dụng tốt thông tin ở đầu và cuối context nhưng có thể bỏ sót nội dung nằm ở giữa.

**[T14-261]** ```text

**[T14-262]** Đầu context → thường được nhớ tốt

**[T14-263]** Giữa context → dễ bị bỏ sót

**[T14-264]** Cuối context → thường được ưu tiên

**[T14-265]** ```

**[T14-266]** Do đó:

**[T14-267]** ```text

**[T14-268]** Context Window lớn ≠ sử dụng hiệu quả toàn bộ context

**[T14-269]** ```

**[T14-270]** Giải pháp không phải luôn tăng context mà là chọn lọc dữ liệu, tóm tắt lịch sử và sắp xếp thông tin theo mức độ quan trọng.

**[T14-271]** ---

**[T14-272]** ## 19. Recency Bias

**[T14-273]** Recency Bias là xu hướng mô hình chú ý mạnh đến thông tin xuất hiện gần thời điểm bắt đầu sinh câu trả lời.

**[T14-274]** Tài liệu đề xuất một cấu trúc thực dụng:

**[T14-275]** ```text

**[T14-276]** System Persona và rules

**[T14-277]** → Documents / Context

**[T14-278]** → Yêu cầu thực thi cụ thể

**[T14-279]** ```

**[T14-280]** Không nên đặt câu hỏi chính ở đầu rồi nối thêm một khối tài liệu rất dài phía sau. Yêu cầu có thể bị chìm trong context.

**[T14-281]** Điều này không có nghĩa System Prompt phải chuyển xuống cuối. System vẫn là policy layer; nhưng câu hỏi hoặc nhiệm vụ cụ thể nên được đặt gần cuối phần context thực thi.

**[T14-282]** ---

**[T14-283]** ## 20. Cắt tỉa và quản lý Context

**[T14-284]** Hãy xem context như bộ nhớ làm việc, không phải kho lưu trữ toàn bộ lịch sử.

**[T14-285]** Context quá dài làm tăng chi phí, độ trễ và tỷ lệ noise. Hai chiến lược quan trọng là:

**[T14-286]** **Compression**: tóm tắt hội thoại hoặc trạng thái cũ.

**[T14-287]** **Relevance filtering**: chỉ giữ dữ liệu cần cho bước hiện tại.

**[T14-288]** ```text

**[T14-289]** Lịch sử đầy đủ

**[T14-290]** → Tóm tắt trạng thái quan trọng

**[T14-291]** → Chọn dữ liệu liên quan

**[T14-292]** → Prompt gọn hơn

**[T14-293]** ```

**[T14-294]** Trong Agent có nhiều bước, context nên được xây dựng theo state hiện tại thay vì gửi lại toàn bộ thông tin ở mọi lần gọi model.

**[T14-295]** ---

**[T14-296]** ## 21. Static Prompt và Dynamic Prompt

**[T14-297]** System Prompt nên giữ những nội dung tương đối ổn định như vai trò, policy, boundary và Output Contract.

**[T14-298]** Các dữ liệu thay đổi theo thời gian nên được bơm động:

**[T14-299]** ```text

**[T14-300]** Thời gian hiện tại

**[T14-301]** User profile

**[T14-302]** Session state

**[T14-303]** Retrieved documents

**[T14-304]** Tool availability

**[T14-305]** ```

**[T14-306]** Kiến trúc phù hợp là:

**[T14-307]** ```text

**[T14-308]** Stable Prompt Template

**[T14-309]** + Runtime Variables

**[T14-310]** → Dynamic Prompt

**[T14-311]** ```

**[T14-312]** Điểm quan trọng là không để dữ liệu động hòa lẫn với policy. Dữ liệu lấy từ bên ngoài phải tiếp tục được xem là untrusted input và được đặt trong vùng cấu trúc riêng.

**[T14-313]** ---

**[T14-314]** ## 22. Bản chất của Tool Calling

**[T14-315]** Hãy hình dung LLM là bộ não còn Tool là tay chân. Bộ não có thể quyết định rằng cần kiểm tra thông tin, nhưng bản thân nó không trực tiếp truy cập database hoặc gọi dịch vụ.

**[T14-316]** ```text

**[T14-317]** User Request

**[T14-318]** → Model phân tích

**[T14-319]** → Model đề xuất Tool Call

**[T14-320]** → Application xác thực

**[T14-321]** → Tool thực thi

**[T14-322]** → Kết quả quay lại Model

**[T14-323]** ```

**[T14-324]** Điểm quan trọng nhất là:

**[T14-325]** > **Model không trực tiếp chạy tool. Model chỉ đề xuất hành động.**

**[T14-326]** Tầng ứng dụng mới là nơi kiểm tra quyền, validate tham số, thực thi, ghi log và trả kết quả lại cho mô hình.

**[T14-327]** ---

**[T14-328]** ## 23. Vòng lặp Tool Calling

**[T14-329]** Tool Calling không phải một lời gọi đơn lẻ mà là một vòng lặp giữa model và môi trường.

**[T14-330]** ```text

**[T14-331]** User

**[T14-332]** → Model

**[T14-333]** → Tool Call?

**[T14-334]** ├─ Không → Final Answer

**[T14-335]** └─ Có → Validate → Execute Tool

**[T14-336]** ↓

**[T14-337]** Tool Result

**[T14-338]** ↓

**[T14-339]** Model

**[T14-340]** ```

**[T14-341]** Sau khi nhận kết quả, model có thể trả lời, gọi thêm tool, sửa tham số hoặc yêu cầu người dùng bổ sung thông tin.

**[T14-342]** Một Agent tốt không phải Agent gọi nhiều tool nhất, mà là Agent biết:

**[T14-343]** ```text

**[T14-344]** Khi nào trả lời trực tiếp

**[T14-345]** Khi nào cần dữ liệu bên ngoài

**[T14-346]** Khi nào phải hỏi lại

**[T14-347]** Khi nào không được hành động

**[T14-348]** ```

**[T14-349]** ---

**[T14-350]** ## 24. Khi nào cần Tool?

**[T14-351]** Tool phù hợp khi nhiệm vụ cần dữ liệu thời gian thực, thông tin riêng của hệ thống, phép tính chính xác hoặc hành động bên ngoài.

**[T14-352]** Nếu câu hỏi có thể trả lời đầy đủ từ context hiện có, việc gọi tool chỉ làm tăng latency và thêm điểm có thể lỗi.

**[T14-353]** ```text

**[T14-354]** Cần thông tin hoặc hành động bên ngoài → Tool

**[T14-355]** Context đã đủ → Trả lời trực tiếp

**[T14-356]** Thiếu tham số quan trọng → Hỏi lại

**[T14-357]** ```

**[T14-358]** System Prompt và Tool Description cần phối hợp để mô hình phân biệt ba tình huống này.

**[T14-359]** ---

**[T14-360]** ## 25. Tool Schema

**[T14-361]** Tool Schema là hợp đồng giữa model và công cụ. Nó mô tả:

**[T14-362]** ```text

**[T14-363]** Tên công cụ

**[T14-364]** → Công cụ làm gì

**[T14-365]** → Khi nào nên dùng

**[T14-366]** → Các tham số

**[T14-367]** → Kiểu dữ liệu

**[T14-368]** → Trường bắt buộc

**[T14-369]** → Giới hạn hợp lệ

**[T14-370]** ```

**[T14-371]** Mô tả tool thực chất cũng là một prompt. Nếu hai tool có mô tả giống nhau hoặc tên quá chung, mô hình khó lựa chọn chính xác.

**[T14-372]** Schema tốt giúp giảm các lỗi như chọn sai tool, thiếu tham số hoặc tạo ra trường không tồn tại.

**[T14-373]** Trong Production, Tool Schema cần đơn giản, rõ nghĩa và tránh chức năng chồng lấn không cần thiết.

**[T14-374]** ---

**[T14-375]** ## 26. Validation và Authorization

**[T14-376]** Không được giả định rằng tham số do model sinh ra luôn hợp lệ.

**[T14-377]** Tầng ứng dụng phải kiểm tra:

**[T14-378]** ```text

**[T14-379]** Đúng kiểu dữ liệu?

**[T14-380]** → Đủ trường bắt buộc?

**[T14-381]** → Giá trị trong giới hạn?

**[T14-382]** → Người dùng có quyền?

**[T14-383]** → Hành động có cần xác nhận?

**[T14-384]** ```

**[T14-385]** Các hành động nhạy cảm như thanh toán, xóa dữ liệu, hoàn tiền hoặc thay đổi quyền cần cơ chế kiểm soát ở tầng ứng dụng.

**[T14-386]** System Prompt có thể hướng dẫn model, nhưng:

**[T14-387]** > **System Prompt không thay thế Authorization System.**

**[T14-388]** Đây là ranh giới quan trọng giữa kiểm soát hành vi của mô hình và bảo mật phần mềm thực sự.

**[T14-389]** ---

**[T14-390]** ## 27. Self-Correction

**[T14-391]** Hãy hình dung một nhân viên điền sai biểu mẫu. Nếu chỉ nhận thông báo “thất bại”, họ khó sửa; nếu được cho biết trường nào sai, họ có thể điều chỉnh.

**[T14-392]** Khi tool trả lỗi, thông tin lỗi nên quay lại model:

**[T14-393]** ```text

**[T14-394]** Tool Error

**[T14-395]** → Model đọc nguyên nhân

**[T14-396]** → Sửa tham số hoặc đổi chiến lược

**[T14-397]** → Retry

**[T14-398]** ```

**[T14-399]** Lỗi nên chỉ rõ trường bị thiếu, kiểu dữ liệu không hợp lệ hoặc điều kiện chưa thỏa mãn.

**[T14-400]** Self-Correction giúp Agent phục hồi trước lỗi nhỏ, nhưng cần giới hạn retry. Nếu không, Agent có thể rơi vào vòng lặp vô hạn.

**[T14-401]** ```text

**[T14-402]** Sai tham số → có thể sửa và thử lại

**[T14-403]** Không có quyền → dừng

**[T14-404]** Vi phạm policy → từ chối

**[T14-405]** Lỗi kéo dài → chuyển cho con người

**[T14-406]** ```

**[T14-407]** ---

**[T14-408]** ## 28. Phân biệt ba nhóm lỗi

**[T14-409]** Khi Agent thất bại, cần xác định lỗi nằm ở tầng nào.

**[T14-410]** | Nhóm lỗi               | Ví dụ                                   |

**[T14-411]** | ---------------------- | --------------------------------------- |

**[T14-412]** | **Model Error**        | Chọn sai tool, bịa kết quả              |

**[T14-413]** | **Tool Error**         | Timeout, API lỗi, dữ liệu không tồn tại |

**[T14-414]** | **Control Flow Error** | Loop vô hạn, kết thúc sớm, mất state    |

**[T14-415]** Nếu không phân biệt, đội phát triển có thể cố sửa prompt trong khi vấn đề thực sự nằm ở API hoặc Router.

**[T14-416]** ```text

**[T14-417]** Xác định tầng lỗi → sửa đúng tầng

**[T14-418]** ```

**[T14-419]** ---

**[T14-420]** ## 29. LangGraph và tư duy đồ thị

**[T14-421]** Hãy hình dung workflow Agent như một bản đồ giao thông. Pipeline truyền thống đi theo một đường thẳng, còn Agent thường phải rẽ nhánh, quay lại và thử lại.

**[T14-422]** LangGraph biểu diễn workflow dưới dạng đồ thị có hướng:

**[T14-423]** ```text

**[T14-424]** State → Node → Edge → Node

**[T14-425]** ```

**[T14-426]** Ba thành phần cốt lõi là:

**[T14-427]** | Thành phần | Ý nghĩa                      |

**[T14-428]** | ---------- | ---------------------------- |

**[T14-429]** | **State**  | Dữ liệu chung được mang theo |

**[T14-430]** | **Node**   | Hàm xử lý, tool hoặc agent   |

**[T14-431]** | **Edge**   | Quy tắc chuyển bước          |

**[T14-432]** Cấu trúc đồ thị phù hợp với workflow có vòng lặp, tool calling, retry hoặc nhiều Agent phối hợp.

**[T14-433]** ---

**[T14-434]** ## 30. State, Node và Edge

**[T14-435]** **State** có thể chứa lịch sử tin nhắn, kết quả tool, retry count và trạng thái hiện tại.

**[T14-436]** **Node** thực hiện một đơn vị công việc, chẳng hạn gọi model, gọi tool, kiểm tra dữ liệu hoặc cập nhật state.

**[T14-437]** **Edge** xác định Node tiếp theo. Edge có thể cố định hoặc phụ thuộc điều kiện.

**[T14-438]** ```text

**[T14-439]** State hiện tại

**[T14-440]** → Node xử lý

**[T14-441]** → State mới

**[T14-442]** → Router kiểm tra

**[T14-443]** → Node tiếp theo hoặc END

**[T14-444]** ```

**[T14-445]** Điểm mạnh của LangGraph là control flow trở nên rõ ràng và quan sát được, thay vì ẩn trong một vòng lặp phức tạp.

**[T14-446]** ---

**[T14-447]** ## 31. Router và Agent Loop

**[T14-448]** Router giống như cảnh sát giao thông của graph. Nó đọc State, thường là tin nhắn mới nhất, rồi quyết định bước tiếp theo.

**[T14-449]** ```text

**[T14-450]** Model Node

**[T14-451]** → Có Tool Call?

**[T14-452]** ├─ Có → Tool Node

**[T14-453]** └─ Không → END

**[T14-454]** ```

**[T14-455]** Sau khi Tool Node cập nhật kết quả vào State, luồng quay lại Model Node:

**[T14-456]** ```text

**[T14-457]** START

**[T14-458]** → Model

**[T14-459]** → Tool

**[T14-460]** → Model

**[T14-461]** → Tool hoặc END

**[T14-462]** ```

**[T14-463]** Đây là Agent Loop cơ bản. Agent có thể tự điều hướng dựa trên kết quả trung gian thay vì chạy một chuỗi bước cố định.

**[T14-464]** ---

**[T14-465]** ## 32. Tại sao LangGraph phù hợp Production?

**[T14-466]** LangGraph hữu ích không chỉ vì cho phép tạo Agent phức tạp mà vì nó làm workflow **quan sát được**.

**[T14-467]** Mỗi Node có thể được log, test và đo thời gian xử lý. State cho biết Agent đang biết gì. Edge giúp xác định tại sao hệ thống chuyển sang bước tiếp theo.

**[T14-468]** ```text

**[T14-469]** Graph rõ ràng

**[T14-470]** → Debug dễ hơn

**[T14-471]** → Retry có kiểm soát

**[T14-472]** → Human-in-the-loop

**[T14-473]** → Workflow có thể phục hồi

**[T14-474]** ```

**[T14-475]** Trong Multi-Agent hoặc workflow cyclic, mô hình đồ thị giúp tránh việc mọi logic bị nhồi vào một prompt hoặc một vòng lặp khó bảo trì.

**[T14-476]** ---

**[T14-477]** ## 33. Kiến trúc tổng thể của một Agent Production

**[T14-478]** Một Agent Production không chỉ gồm LLM và prompt. Nó là một hệ thống nhiều lớp:

**[T14-479]** ```text

**[T14-480]** System Prompt

**[T14-481]** → Context Management

**[T14-482]** → Model Decision

**[T14-483]** → Tool Schema

**[T14-484]** → Validation và Authorization

**[T14-485]** → Tool Execution

**[T14-486]** → State Update

**[T14-487]** → Routing

**[T14-488]** → Logging và Testing

**[T14-489]** ```

**[T14-490]** Model mạnh nhưng kiến trúc yếu vẫn có thể tạo ra Agent không ổn định. Prompt không sửa được API lỗi; Tool Schema không thay thế quyền truy cập; LangGraph không tự làm cho reasoning chính xác.

**[T14-491]** Mỗi lớp giải quyết một nhóm vấn đề khác nhau và phải phối hợp với nhau.

**[T14-492]** ---

**[T14-493]** ## 34. Flow tổng kết Day 04

**[T14-494]** ```text

**[T14-495]** Human Intent

**[T14-496]** ↓

**[T14-497]** Prompt

**[T14-498]** (Role + Task + Context + Format)

**[T14-499]** ↓

**[T14-500]** System Prompt

**[T14-501]** (Policy + Boundary + Capabilities + Contract)

**[T14-502]** ↓

**[T14-503]** Model Decision

**[T14-504]** ↓

**[T14-505]** Trả lời trực tiếp?

**[T14-506]** ├─ Có → Structured Response

**[T14-507]** └─ Không

**[T14-508]** ↓

**[T14-509]** Tool Call

**[T14-510]** ↓

**[T14-511]** Validation + Authorization

**[T14-512]** ↓

**[T14-513]** Tool Execution

**[T14-514]** ↓

**[T14-515]** Tool Result

**[T14-516]** ↓

**[T14-517]** Model Self-Correction hoặc Final Answer

**[T14-518]** ```

**[T14-519]** Nếu workflow có nhiều bước, phần điều phối được biểu diễn bằng LangGraph:

**[T14-520]** ```text

**[T14-521]** State → Node → Router → Node → END

**[T14-522]** ```

**[T14-523]** ---

**[T14-524]** ## 35. Các ý cần nhớ cho Kahoot

**[T14-525]** **Prompt** là interface giữa ý định con người và hành vi mô hình.

**[T14-526]** **Specificity beats cleverness**: cụ thể quan trọng hơn hoa mỹ.

**[T14-527]** **Role, Task, Context, Format** là bốn thành phần cơ bản; nên bắt đầu bằng Task và Format.

**[T14-528]** **Zero-shot → Few-shot → Decomposition/CoT** là thứ tự thử thực dụng.

**[T14-529]** **Few-shot** dùng để chỉ ra pattern, giữ format và xử lý edge case.

**[T14-530]** **CoT** phù hợp cho reasoning nhiều bước, không cần cho extraction đơn giản.

**[T14-531]** **System Prompt** là policy layer của Agent.

**[T14-532]** **XML và delimiters** giúp tách instruction khỏi dữ liệu và giảm Context Bleed.

**[T14-533]** **Lost in the Middle** cho thấy context lớn không đồng nghĩa nhớ hết.

**[T14-534]** **Recency Bias** khiến yêu cầu cụ thể gần cuối context thường được chú ý mạnh.

**[T14-535]** **Tool Schema** là hợp đồng giữa model và tool.

**[T14-536]** **Model chỉ đề xuất Tool Call; application mới thực thi.**

**[T14-537]** **Self-Correction** là vòng nhận lỗi → sửa → thử lại, nhưng phải có giới hạn.

**[T14-538]** **LangGraph = State + Node + Edge**, dùng để biểu diễn workflow có điều kiện và vòng lặp.

**[T14-539]** ---

**[T14-540]** ## 36. Kết luận

**[T14-541]** Hãy hình dung toàn bộ Day 04 như việc xây một nhân viên số đáng tin cậy.

**[T14-542]** Prompt giúp nhân viên hiểu việc. System Prompt đặt nội quy. Tool cung cấp khả năng hành động. Validation kiểm tra quyền và dữ liệu. Self-Correction giúp phục hồi khi sai. LangGraph điều phối toàn bộ quy trình.

**[T14-543]** Prompt rõ

**[T14-544]** → Model quyết định tốt

**[T14-545]** System Prompt rõ

**[T14-546]** → Agent hành xử nhất quán

**[T14-547]** Tool Schema rõ

**[T14-548]** → Agent hành động đúng

**[T14-549]** Control Flow rõ

**[T14-550]** → Hệ thống vận hành bền trong Production
