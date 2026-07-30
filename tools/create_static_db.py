import json
from pathlib import Path

db = {
  "T10": {
    "transcript_id": "T10",
    "transcript_title": "Paper - AI & LLM Foundation",
    "key_points": [
      {
        "content": "Xu hướng công nghệ AI năm 2025 đánh dấu bước chuyển dịch quan trọng từ Generative AI sang Agentic AI, tự động hóa lập kế hoạch và thực thi độc lập.",
        "citations": ["T10-004"]
      },
      {
        "content": "AI Taxonomy bao gồm các tầng từ ngoài vào trong: AI, Machine Learning (ML), Deep Learning (DL), Foundation Models, và Large Language Models (LLM).",
        "citations": ["T10-010", "T10-015"]
      },
      {
        "content": "Kiến trúc Decoder-only Transformer đọc từ trái sang phải là kiến trúc thắng thế trong các LLM hiện đại nhờ khả năng mở rộng (scaling) vượt trội.",
        "citations": ["T10-033"]
      },
      {
        "content": "Tiếng Việt tốn nhiều token hơn tiếng Anh (1 token ~ 0.5 từ tiếng Việt so với 0.75 từ tiếng Anh) do đặc thù dấu thanh và mã hóa Unicode.",
        "citations": ["T10-043"]
      },
      {
        "content": "Quy trình huấn luyện LLM trải qua ba giai đoạn chính: Pre-training (học sơ khởi), Supervised Fine-Tuning (SFT - tinh chỉnh), và RLHF/DPO (căn chỉnh hành vi).",
        "citations": ["T10-044", "T10-047"]
      }
    ],
    "keywords": ["Agentic AI", "Decoder-only", "Transformer", "Tokenization", "SFT", "RLHF", "Hallucination", "ROI"],
    "questions": [
      {
        "question": "Theo xu hướng công nghệ AI năm 2025, sự chuyển dịch quan trọng nhất là từ đâu đến đâu?",
        "options": [
          "A. Từ Machine Learning sang Deep Learning",
          "B. Từ Generative AI sang Agentic AI",
          "C. Từ Foundation Models sang Large Language Models",
          "D. Từ Discriminative AI sang Generative AI"
        ],
        "correct_option": "B",
        "explanation": "Xu hướng công nghệ AI năm 2025 đánh dấu bước chuyển mình quan trọng từ việc tối ưu hóa khả năng phản hồi ngôn ngữ thông thường (Generative AI) sang các hệ thống tự động hóa lập kế hoạch và thực thi hành động độc lập (Agentic AI).",
        "citations": ["T10-004"]
      },
      {
        "question": "Chỉ số hiệu quả đầu tư (ROI) trung bình của ứng dụng AI trong doanh nghiệp đạt bao nhiêu lần trên mỗi 1 USD chi phí đầu tư ban đầu?",
        "options": [
          "A. 1.5 lần",
          "B. 2.5 lần",
          "C. 3.7 lần",
          "D. 5.0 lần"
        ],
        "correct_option": "C",
        "explanation": "Hiệu quả đầu tư (ROI) đạt trung bình 3.7 lần (3.7x) trên mỗi 1 USD chi phí đầu tư ban đầu.",
        "citations": ["T10-008"]
      },
      {
        "question": "Trong phân loại AI, mô hình nền tảng được huấn luyện trên khối lượng dữ liệu khổng lồ nhằm phục vụ cho đa tác vụ hạ nguồn được gọi là gì?",
        "options": [
          "A. Deep Learning",
          "B. Foundation Models",
          "C. Large Language Models",
          "D. Agentic AI"
        ],
        "correct_option": "B",
        "explanation": "Foundation Models là mô hình nền tảng được huấn luyện trên khối lượng dữ liệu khổng lồ nhằm phục vụ cho đa tác vụ hạ nguồn.",
        "citations": ["T10-014"]
      },
      {
        "question": "Công thức chức năng cốt lõi của Discriminative AI là gì?",
        "options": [
          "A. Input → Label",
          "B. Prompt → Content",
          "C. Goal → Plan → Action",
          "D. Dataset → Training"
        ],
        "correct_option": "A",
        "explanation": "Discriminative AI có công thức cốt lõi là Input → Label, dùng để phân loại dữ liệu, nhận diện mẫu và đưa ra dự đoán.",
        "citations": ["T10-023"]
      },
      {
        "question": "Kiến trúc nào của Transformer là kiến trúc thắng thế hiện nay trong LLM nhờ khả năng mở rộng (scaling) vượt trội?",
        "options": [
          "A. Encoder-Decoder Transformer",
          "B. Encoder-only Transformer",
          "C. Decoder-only Transformer",
          "D. Bidirectional LSTM"
        ],
        "correct_option": "C",
        "explanation": "Kiến trúc Decoder-only Transformer đọc văn bản từ trái sang phải để dự đoán token tiếp theo một cách tuần tự (Autoregressive), là kiến trúc thắng thế nhờ khả năng mở rộng vượt trội.",
        "citations": ["T10-033"]
      },
      {
        "question": "Trung bình, 1 token tiếng Việt tương đương khoảng bao nhiêu từ tiếng Việt?",
        "options": [
          "A. 0.75 từ",
          "B. 0.5 từ",
          "C. 1.0 từ",
          "D. 1.5 từ"
        ],
        "correct_option": "B",
        "explanation": "Một token tương đương khoảng 0.75 từ tiếng Anh, nhưng chỉ tương đương khoảng 0.5 từ đối với tiếng Việt.",
        "citations": ["T10-043"]
      },
      {
        "question": "Tại sao tiếng Việt lại tốn nhiều token hơn tiếng Anh khi xử lý trong LLM?",
        "options": [
          "A. Do tiếng Việt là ngôn ngữ đa nghĩa",
          "B. Do đặc thù sử dụng dấu thanh và hệ thống mã hóa Unicode đa ký tự",
          "C. Do tiếng Việt có nhiều từ ghép phức tạp",
          "D. Do từ điển tiếng Việt của các model quá lớn"
        ],
        "correct_option": "B",
        "explanation": "Tiếng Việt tốn nhiều token hơn do đặc thù sử dụng dấu thanh và hệ thống mã hóa ký tự Unicode đa ký tự.",
        "citations": ["T10-043"]
      },
      {
        "question": "Giai đoạn huấn luyện SFT (Supervised Fine-Tuning) có vai trò gì trong quá trình phát triển LLM?",
        "options": [
          "A. Mô hình đọc lượng lớn văn bản thô từ Internet để xây dựng vốn ngôn ngữ",
          "B. Mô hình được căn chỉnh bằng phản hồi con người để uốn nắn hành vi an toàn",
          "C. Mô hình được huấn luyện dựa trên các bộ dữ liệu dạng cặp câu hỏi - trả lời mẫu để phản hồi theo cấu trúc",
          "D. Mô hình được kết nối công cụ tìm kiếm ngoại vi"
        ],
        "correct_option": "C",
        "explanation": "SFT là giai đoạn tinh chỉnh có giám sát, mô hình được huấn luyện dựa trên các bộ dữ liệu dạng cặp câu hỏi - câu trả lời mẫu chất lượng cao để hiểu cách phản hồi theo đúng cấu trúc yêu cầu.",
        "citations": ["T10-046"]
      },
      {
        "question": "Hiện tượng mô hình tối ưu hóa dựa trên xác suất chuỗi token tiếp theo chứ không tối ưu hóa dựa trên tính đúng đắn logic của sự thật, dẫn đến việc đưa ra các tuyên bố sai lệch một cách tự tin được gọi là gì?",
        "options": [
          "A. Knowledge Cutoff",
          "B. Lost in the Middle",
          "C. Context Window Limits",
          "D. Hallucination"
        ],
        "correct_option": "D",
        "explanation": "Hallucination (sự ảo tưởng) là hiện tượng mô hình tối ưu hóa dựa trên xác suất chuỗi token tiếp theo chứ không tối ưu hóa dựa trên tính đúng đắn logic của sự thật, dẫn đến đưa ra tuyên bố sai lệch một cách tự tin.",
        "citations": ["T10-050"]
      },
      {
        "question": "Nguyên tắc cốt lõi (Rule of Thumb) của việc chọn mô hình LLM là gì?",
        "options": [
          "A. Luôn luôn chọn mô hình mạnh nhất và mới nhất",
          "B. Bắt đầu với mô hình ĐỦ TỐT và ĐỦ RẺ, chỉ nâng cấp khi mô hình nhỏ hơn là nút thắt cổ chai",
          "C. Luôn tự host các mô hình mã nguồn mở để tối ưu bảo mật",
          "D. Chọn mô hình dựa trên số lượng tham số lớn nhất có thể"
        ],
        "correct_option": "B",
        "explanation": "Nguyên tắc cốt lõi: Hãy luôn bắt đầu với mô hình ĐỦ TỐT và ĐỦ RẺ. Chỉ nâng cấp lên mô hình cao cấp hơn khi chất lượng của mô hình nhỏ hơn thực sự trở thành nút thắt cổ chai cho bài toán nghiệp vụ.",
        "citations": ["T10-098"]
      }
    ]
  },
  "T11": {
    "transcript_id": "T11",
    "transcript_title": "Day 01 - AI & LLM Foundation",
    "key_points": [
      {
        "content": "Xu hướng công nghệ AI năm 2025 đánh dấu bước chuyển dịch quan trọng từ Generative AI sang Agentic AI, tự động hóa lập kế hoạch và thực thi độc lập.",
        "citations": ["T11-004"]
      },
      {
        "content": "AI Taxonomy bao gồm các tầng từ ngoài vào trong: AI, Machine Learning (ML), Deep Learning (DL), Foundation Models, và Large Language Models (LLM).",
        "citations": ["T11-010", "T11-015"]
      },
      {
        "content": "Kiến trúc Decoder-only Transformer đọc từ trái sang phải là kiến trúc thắng thế trong các LLM hiện đại nhờ khả năng mở rộng (scaling) vượt trội.",
        "citations": ["T11-033"]
      },
      {
        "content": "Tiếng Việt tốn nhiều token hơn tiếng Anh (1 token ~ 0.5 từ tiếng Việt so với 0.75 từ tiếng Anh) do đặc thù dấu thanh và mã hóa Unicode.",
        "citations": ["T11-043"]
      },
      {
        "content": "Quy trình huấn luyện LLM trải qua ba giai đoạn chính: Pre-training (học sơ khởi), Supervised Fine-Tuning (SFT - tinh chỉnh), và RLHF/DPO (căn chỉnh hành vi).",
        "citations": ["T11-044", "T11-047"]
      }
    ],
    "keywords": ["Agentic AI", "Decoder-only", "Transformer", "Tokenization", "SFT", "RLHF", "Hallucination", "ROI"],
    "questions": [
      {
        "question": "Theo xu hướng công nghệ AI năm 2025, sự chuyển dịch quan trọng nhất là từ đâu đến đâu?",
        "options": [
          "A. Từ Machine Learning sang Deep Learning",
          "B. Từ Generative AI sang Agentic AI",
          "C. Từ Foundation Models sang Large Language Models",
          "D. Từ Discriminative AI sang Generative AI"
        ],
        "correct_option": "B",
        "explanation": "Xu hướng công nghệ AI năm 2025 đánh dấu bước chuyển mình quan trọng từ việc tối ưu hóa khả năng phản hồi ngôn ngữ thông thường (Generative AI) sang các hệ thống tự động hóa lập kế hoạch và thực thi hành động độc lập (Agentic AI).",
        "citations": ["T11-004"]
      },
      {
        "question": "Chỉ số hiệu quả đầu tư (ROI) trung bình của ứng dụng AI trong doanh nghiệp đạt bao nhiêu lần trên mỗi 1 USD chi phí đầu tư ban đầu?",
        "options": [
          "A. 1.5 lần",
          "B. 2.5 lần",
          "C. 3.7 lần",
          "D. 5.0 lần"
        ],
        "correct_option": "C",
        "explanation": "Hiệu quả đầu tư (ROI) đạt trung bình 3.7 lần (3.7x) trên mỗi 1 USD chi phí đầu tư ban đầu.",
        "citations": ["T11-008"]
      },
      {
        "question": "Trong phân loại AI, mô hình nền tảng được huấn luyện trên khối lượng dữ liệu khổng lồ nhằm phục vụ cho đa tác vụ hạ nguồn được gọi là gì?",
        "options": [
          "A. Deep Learning",
          "B. Foundation Models",
          "C. Large Language Models",
          "D. Agentic AI"
        ],
        "correct_option": "B",
        "explanation": "Foundation Models là mô hình nền tảng được huấn luyện trên khối lượng dữ liệu khổng lồ nhằm phục vụ cho đa tác vụ hạ nguồn.",
        "citations": ["T11-014"]
      },
      {
        "question": "Công thức chức năng cốt lõi của Discriminative AI là gì?",
        "options": [
          "A. Input → Label",
          "B. Prompt → Content",
          "C. Goal → Plan → Action",
          "D. Dataset → Training"
        ],
        "correct_option": "A",
        "explanation": "Discriminative AI có công thức cốt lõi là Input → Label, dùng để phân loại dữ liệu, nhận diện mẫu và đưa ra dự đoán.",
        "citations": ["T11-023"]
      },
      {
        "question": "Kiến trúc nào của Transformer là kiến trúc thắng thế hiện nay trong LLM nhờ khả năng mở rộng (scaling) vượt trội?",
        "options": [
          "A. Encoder-Decoder Transformer",
          "B. Encoder-only Transformer",
          "C. Decoder-only Transformer",
          "D. Bidirectional LSTM"
        ],
        "correct_option": "C",
        "explanation": "Kiến trúc Decoder-only Transformer đọc văn bản từ trái sang phải để dự đoán token tiếp theo một cách tuần tự (Autoregressive), là kiến trúc thắng thế nhờ khả năng mở rộng vượt trội.",
        "citations": ["T11-033"]
      },
      {
        "question": "Trung bình, 1 token tiếng Việt tương đương khoảng bao nhiêu từ tiếng Việt?",
        "options": [
          "A. 0.75 từ",
          "B. 0.5 từ",
          "C. 1.0 từ",
          "D. 1.5 từ"
        ],
        "correct_option": "B",
        "explanation": "Một token tương đương khoảng 0.75 từ tiếng Anh, nhưng chỉ tương đương khoảng 0.5 từ đối với tiếng Việt.",
        "citations": ["T11-043"]
      },
      {
        "question": "Tại sao tiếng Việt lại tốn nhiều token hơn tiếng Anh khi xử lý trong LLM?",
        "options": [
          "A. Do tiếng Việt là ngôn ngữ đa nghĩa",
          "B. Do đặc thù sử dụng dấu thanh và hệ thống mã hóa Unicode đa ký tự",
          "C. Do tiếng Việt có nhiều từ ghép phức tạp",
          "D. Do từ điển tiếng Việt của các model quá lớn"
        ],
        "correct_option": "B",
        "explanation": "Tiếng Việt tốn nhiều token hơn do đặc thù sử dụng dấu thanh và hệ thống mã hóa ký tự Unicode đa ký tự.",
        "citations": ["T11-043"]
      },
      {
        "question": "Giai đoạn huấn luyện SFT (Supervised Fine-Tuning) có vai trò gì trong quá trình phát triển LLM?",
        "options": [
          "A. Mô hình đọc lượng lớn văn bản thô từ Internet để xây dựng vốn ngôn ngữ",
          "B. Mô hình được căn chỉnh bằng phản hồi con người để uốn nắn hành vi an toàn",
          "C. Mô hình được huấn luyện dựa trên các bộ dữ liệu dạng cặp câu hỏi - trả lời mẫu để phản hồi theo đúng cấu trúc",
          "D. Mô hình được kết nối công cụ tìm kiếm ngoại vi"
        ],
        "correct_option": "C",
        "explanation": "SFT là giai đoạn tinh chỉnh có giám sát, mô hình được huấn luyện dựa trên các bộ dữ liệu dạng cặp câu hỏi - câu trả lời mẫu chất lượng cao để hiểu cách phản hồi theo đúng cấu trúc yêu cầu.",
        "citations": ["T11-046"]
      },
      {
        "question": "Hiện tượng mô hình tối ưu hóa dựa trên xác suất chuỗi token tiếp theo chứ không tối ưu hóa dựa trên tính đúng đắn logic của sự thật, dẫn đến việc đưa ra các tuyên bố sai lệch một cách tự tin được gọi là gì?",
        "options": [
          "A. Knowledge Cutoff",
          "B. Lost in the Middle",
          "C. Context Window Limits",
          "D. Hallucination"
        ],
        "correct_option": "D",
        "explanation": "Hallucination (sự ảo tưởng) là hiện tượng mô hình tối ưu hóa dựa trên xác suất chuỗi token tiếp theo chứ không tối ưu hóa dựa trên tính đúng đắn logic của sự thật, dẫn đến đưa ra tuyên bố sai lệch một cách tự tin.",
        "citations": ["T11-050"]
      },
      {
        "question": "Nguyên tắc cốt lõi (Rule of Thumb) của việc chọn mô hình LLM là gì?",
        "options": [
          "A. Luôn luôn chọn mô hình mạnh nhất và mới nhất",
          "B. Bắt đầu với mô hình ĐỦ TỐT và ĐỦ RẺ, chỉ nâng cấp khi mô hình nhỏ hơn là nút thắt cổ chai",
          "C. Luôn tự host các mô hình mã nguồn mở để tối ưu bảo mật",
          "D. Chọn mô hình dựa trên số lượng tham số lớn nhất có thể"
        ],
        "correct_option": "B",
        "explanation": "Nguyên tắc cốt lõi: Hãy luôn bắt đầu với mô hình ĐỦ TỐT và ĐỦ RẺ. Chỉ nâng cấp lên mô hình cao cấp hơn khi chất lượng của mô hình nhỏ hơn thực sự trở thành nút thắt cổ chai cho bài toán nghiệp vụ.",
        "citations": ["T11-098"]
      }
    ]
  },
  "T12": {
    "transcript_id": "T12",
    "transcript_title": "Day 02 - Từ yêu cầu mơ hồ đến Problem Statement",
    "key_points": [
      {
        "content": "Một sản phẩm AI (AI Product) là sự giao thoa chặt chẽ của ba trụ cột cốt lõi: AI Engineering, Product Thinking và Design Thinking.",
        "citations": ["T12-003"]
      },
      {
        "content": "Don Norman nhấn mạnh triết lý: 'Do not solve the problem I am asked to solve' nhằm khuyến khích đi sâu tìm ra vấn đề thực sự ẩn sau yêu cầu ban đầu.",
        "citations": ["T12-021"]
      },
      {
        "content": "Mô hình Double Diamond chia quá trình thiết kế thành hai giai đoạn lớn với các vòng lặp phân kỳ và hội tụ: Tìm đúng vấn đề và Tìm đúng giải pháp.",
        "citations": ["T12-023"]
      },
      {
        "content": "Khung Problem Statement gồm 9 trường thông tin, chia thành 6 yếu tố bài toán cốt lõi và 3 yếu tố quyết định AI.",
        "citations": ["T12-036"]
      },
      {
        "content": "Theo Google PAIR, quyết định có nên ứng dụng AI được thực hiện qua 3 bước, trong đó cần xác định rõ vai trò Automate hay Augment và thiết lập đánh đổi Precision vs. Recall.",
        "citations": ["T12-068", "T12-086"]
      }
    ],
    "keywords": ["AI Product", "Double Diamond", "Problem Statement", "Google PAIR", "Precision vs Recall", "Automate vs Augment", "Workflow Patterns", "UX Fallback"],
    "questions": [
      {
        "question": "Trụ cột nào tập trung vào Retrieval-Augmented Generation (RAG), AI Agent, Guardrails và Evaluation?",
        "options": [
          "A. AI Engineering",
          "B. Product Thinking",
          "C. Design Thinking",
          "D. Software Architecture"
        ],
        "correct_option": "A",
        "explanation": "AI Engineering triển khai các kỹ thuật hệ thống thực tế như Retrieval-Augmented Generation (RAG), AI Agent, Guardrails (hệ thống rào chắn), Evaluation (đánh giá hiệu năng) và vận hành hệ thống AI trong môi trường production.",
        "citations": ["T12-004"]
      },
      {
        "question": "Triết lý của Don Norman khuyên chúng ta điều gì khi bắt đầu giải quyết một vấn đề?",
        "options": [
          "A. Giải quyết ngay yêu cầu được đưa ra",
          "B. Không giải quyết vấn đề mà mình được yêu cầu giải quyết mà tìm vấn đề thực sự",
          "C. Bỏ qua ý kiến của khách hàng",
          "D. Tập trung viết code ngay lập tức"
        ],
        "correct_option": "B",
        "explanation": "Triết lý thiết kế lấy con con người làm trung tâm (HCD) của Don Norman nhấn mạnh: 'Do not solve the problem I am asked to solve.' - cần đi sâu tìm ra vấn đề thực sự ẩn sau yêu cầu ban đầu.",
        "citations": ["T12-021"]
      },
      {
        "question": "Hai giai đoạn lớn của mô hình Double Diamond là gì?",
        "options": [
          "A. Tìm đúng vấn đề và Tìm đúng giải pháp",
          "B. Thu thập dữ liệu và Huấn luyện mô hình",
          "C. Lập kế hoạch và Triển khai hệ thống",
          "D. Thiết kế giao diện và Viết code"
        ],
        "correct_option": "A",
        "explanation": "Mô hình Double Diamond chia quá trình thiết kế thành hai giai đoạn lớn với hai vòng lặp phân kỳ (mở rộng góc nhìn) và hội tụ (định nghĩa chính xác): Diamond 1 là Tìm đúng vấn đề, Diamond 2 là Tìm đúng giải pháp.",
        "citations": ["T12-023"]
      },
      {
        "question": "Trong Double Diamond, các phương pháp như Observation, User Interview, Survey nằm ở khâu nào?",
        "options": [
          "A. Discover",
          "B. Define",
          "C. Develop",
          "D. Deliver"
        ],
        "correct_option": "A",
        "explanation": "Diamond 1 - Tìm đúng vấn đề (Discover): Khám phá các vấn đề căn bản bằng cách quan sát thực tế (Observation), phỏng vấn người dùng (User Interview), khảo sát (Survey), nhật ký hành vi (Diary Study)...",
        "citations": ["T12-024"]
      },
      {
        "question": "Khung Problem Statement hoàn chỉnh trong chương trình đào tạo gồm bao nhiêu trường thông tin?",
        "options": [
          "A. 5 trường",
          "B. 7 trường",
          "C. 9 trường",
          "D. 12 trường"
        ],
        "correct_option": "C",
        "explanation": "Để chuyển đổi một điểm đau (pain point) mơ hồ thành một bài toán rõ ràng sẵn sàng cho triển khai kỹ thuật, chương trình thiết lập khung Problem Statement hoàn chỉnh gồm 9 trường thông tin (chia làm 6 yếu tố bài toán cốt lõi và 3 yếu tố quyết định AI).",
        "citations": ["T12-036"]
      },
      {
        "question": "Theo Google PAIR, trường hợp nào sau đây AI có ưu thế hơn so với rule/heuristic tĩnh?",
        "options": [
          "A. Khi cần duy trì tính nhất quán và dự đoán được",
          "B. Khi lỗi sai của hệ thống quá tốn kém",
          "C. Khi cần hiểu ngôn ngữ tự nhiên viết tự do của người dùng",
          "D. Khi yêu cầu tính minh bạch tuyệt đối"
        ],
        "correct_option": "C",
        "explanation": "AI có lợi thế vượt trội so với các quy tắc luật tĩnh khi cần hiểu ngôn ngữ tự nhiên viết tự do của người dùng (Natural Language Understanding).",
        "citations": ["T12-074"]
      },
      {
        "question": "Quyết định Automate (Tự động hóa) nên chọn khi nào?",
        "options": [
          "A. Khi người dùng thích tự làm",
          "B. Khi tác vụ nhàm chán, lặp lại và có một đáp án đúng thống nhất",
          "C. Khi tác vụ có rủi ro pháp lý cao",
          "D. Khi kết quả cần trách nhiệm cá nhân sâu sắc"
        ],
        "correct_option": "B",
        "explanation": "Automate (AI làm thay): Chọn khi tác vụ nhàm chán, nguy hiểm, cần mở rộng quy mô lớn, hoặc có một đáp án đúng thống nhất.",
        "citations": ["T12-087"]
      },
      {
        "question": "Độ chính xác (Precision) trong thiết kế hệ thống AI ưu tiên điều gì?",
        "options": [
          "A. Ít gợi ý nhưng gợi ý nào cũng chắc chắn đúng",
          "B. Gợi ý thật nhiều để không bỏ sót trường hợp nào",
          "C. Chi phí vận hành thấp nhất",
          "D. Tốc độ phản hồi nhanh nhất"
        ],
        "correct_option": "A",
        "explanation": "Ưu tiên Precision cao: Hệ thống ít đưa ra gợi ý, nhưng gợi ý nào cũng chắc chắn đúng (giảm thiểu tối đa lỗi False Positive).",
        "citations": ["T12-091"]
      },
      {
        "question": "Cấp độ giải pháp Workflow là gì?",
        "options": [
          "A. Dùng logic phân nhánh rành mạch If/Else cố định",
          "B. AI tự điều phối, tự lập kế hoạch giữa các bước lặp động",
          "C. Các bước quy trình cố định, có AI xử lý ngôn ngữ và con người kiểm duyệt trước khi gửi",
          "D. Máy học tự động 100% không cần con người"
        ],
        "correct_option": "C",
        "explanation": "Cấp độ 2 - Workflow (Quy trình): Áp dụng khi đầu vào đa dạng không thể viết hết luật tĩnh, nhưng các bước quy trình đã định hình rõ. Từng công đoạn cần AI hỗ trợ xử lý ngôn ngữ hoặc đánh giá, có con người kiểm tra trước khi gửi.",
        "citations": ["T12-096"]
      },
      {
        "question": "Theo Google PAIR, thiết kế trải nghiệm UX Fallback khi AI có độ tin cậy thấp (low confidence) nên làm gì?",
        "options": [
          "A. Tự động thực thi hành động",
          "B. Yêu cầu người dùng xác nhận rõ ràng trước khi thực hiện",
          "C. Không thông báo gì cho người dùng",
          "D. Tắt hoàn toàn hệ thống"
        ],
        "correct_option": "B",
        "explanation": "UX Fallback cho Trạng thái không chắc chắn (Low confidence): Yêu cầu người dùng xác nhận rõ ràng trước khi thực hiện hành động.",
        "citations": ["T12-141"]
      }
    ]
  },
  "T13": {
    "transcript_id": "T13",
    "transcript_title": "Day 03 - Agentic AI và ReAct",
    "key_points": [
      {
        "content": "Sự tiến hóa của các hệ thống AI theo phổ phát triển (AI Spectrum) diễn ra như sau: Rule-based Bot -> LLM Chatbot -> Reactive Agent -> Autonomous Agent.",
        "citations": ["T13-007"]
      },
      {
        "content": "Định nghĩa cốt lõi của một Agent thực sự là: Có khả năng tự đưa ra quyết định, thực thi hành động, quan sát kết quả phản hồi từ môi trường, và lặp lại vòng lặp để đạt mục tiêu.",
        "citations": ["T13-012"]
      },
      {
        "content": "Bộ nhớ ngắn hạn (Short-term memory) nằm trong context window tối ưu cho tác vụ hiện tại nhưng dễ bị đầy khi chuỗi hội thoại kéo dài.",
        "citations": ["T13-109"]
      },
      {
        "content": "Ba trạng thái cốt lõi của chu trình vòng lặp ReAct là Thought (Suy nghĩ), Action (Hành động), và Observation (Quan sát).",
        "citations": ["T13-125", "T13-126"]
      },
      {
        "content": "Để tránh lặp vô hạn và lãng phí tài nguyên, hệ thống Agent trong production bắt buộc phải có Max Iterations Safeguard, Timeout, và Loop Detection.",
        "citations": ["T13-154", "T13-158"]
      }
    ],
    "keywords": ["AI Spectrum", "Agent", "ReAct", "Thought-Action-Observation", "Short-term Memory", "Long-term Memory", "Agentic Fit", "Hybrid Pattern", "LangGraph"],
    "questions": [
      {
        "question": "Sự tiến hóa của các hệ thống AI theo phổ phát triển (AI Spectrum) diễn ra như thế nào?",
        "options": [
          "A. Rule-based Bot → LLM Chatbot → Reactive Agent → Autonomous Agent",
          "B. Deep Learning → LLM → RAG → Agentic AI",
          "C. Chatbot → Knowledge Base → Tool Calling → Agent",
          "D. Prompt Engineering → RAG → LangGraph → Agentic AI"
        ],
        "correct_option": "A",
        "explanation": "Mô hình phổ phát triển AI (AI Spectrum) biểu diễn qua phổ: Rule-based Bot → LLM Chatbot → Reactive Agent → Autonomous Agent. Khả năng thích nghi, sử dụng công cụ, bộ nhớ và mức độ rủi ro tăng dần.",
        "citations": ["T13-007"]
      },
      {
        "question": "Định nghĩa cốt lõi của một Agent thực sự là gì?",
        "options": [
          "A. Bất kỳ hệ thống nào sử dụng Large Language Model (LLM)",
          "B. Hệ thống có khả năng tự đưa ra quyết định, thực thi hành động, quan sát phản hồi từ môi trường và lặp lại để đạt mục tiêu",
          "C. Chatbot có thể trả lời câu hỏi dài trôi chảy và tự nhiên",
          "D. Hệ thống chạy trên nền tảng LangGraph"
        ],
        "correct_option": "B",
        "explanation": "Nguyên tắc phân định Agent: Agent thực sự chỉ xuất hiện khi hệ thống có khả năng tự đưa ra quyết định, thực thi hành động, quan sát kết quả phản hồi từ môi trường, và lặp lại vòng lặp này để đạt mục tiêu.",
        "citations": ["T13-012"]
      },
      {
        "question": "Điểm khác biệt lớn nhất về bộ nhớ của Agent so với LLM Chatbot thông thường là gì?",
        "options": [
          "A. Agent không sử dụng bộ nhớ ngắn hạn",
          "B. Agent chỉ lưu trữ thông tin tĩnh",
          "C. Agent có sự kết hợp giữa bộ nhớ ngắn hạn trong context và bộ nhớ dài hạn ngoài context window",
          "D. Agent lưu toàn bộ lịch sử trong database SQL"
        ],
        "correct_option": "C",
        "explanation": "Bảng so sánh chi tiết chỉ ra: LLM Chatbot chỉ có bộ nhớ ngắn hạn (trong context window), còn Agent có cả bộ nhớ ngắn hạn và bộ nhớ dài hạn (Long-term memory).",
        "citations": ["T13-029"]
      },
      {
        "question": "Theo khung Agentic Fit, tổng điểm bao nhiêu thì nên đầu tư vào kiến trúc Agent?",
        "options": [
          "A. Dưới 5 điểm",
          "B. Từ 6 đến 10 điểm",
          "C. Từ 11 điểm trở lên",
          "D. Trên 20 điểm"
        ],
        "correct_option": "C",
        "explanation": "Định hướng kiến trúc dựa trên tổng điểm Agentic Fit: Từ 11 điểm trở lên thì kiến trúc hệ thống Agent là giải pháp rất đáng để đầu tư và thử nghiệm.",
        "citations": ["T13-093"]
      },
      {
        "question": "Trường hợp nào sau đây là phản mẫu (anti-pattern) cần tránh khi thiết kế Agent?",
        "options": [
          "A. Bài toán một bước (Single-step) hoặc giới hạn nghiêm ngặt về thời gian phản hồi (latency constraint)",
          "B. Tác vụ cần suy luận nhiều bước",
          "C. Hệ thống cần kết nối API bên thứ ba",
          "D. Ứng dụng yêu cầu độ trễ cao"
        ],
        "correct_option": "A",
        "explanation": "Cảnh báo thiết kế: Triển khai kiến trúc Agent sẽ trở nên phản tác dụng và gây lãng phí lớn nếu rơi vào các trường hợp: Bài toán một bước (Single-step), Thiếu công cụ, Yêu cầu chính xác 100%, hoặc Giới hạn nghiêm ngặt về thời gian phản hồi.",
        "citations": ["T13-096", "T13-099"]
      },
      {
        "question": "Bốn khối thành phần cốt lõi của một Agent hoàn chỉnh là gì?",
        "options": [
          "A. Input, Processing, Output, Storage",
          "B. Prompt, Model, Tool, Log",
          "C. Perception, Reasoning, Action, Memory",
          "D. Chatbot, RAG, ReAct, LangGraph"
        ],
        "correct_option": "C",
        "explanation": "Một hệ thống Agent hoàn chỉnh được xây dựng dựa trên sự liên kết chặt chẽ của bốn khối kiến trúc cơ bản: Nhận thức (Perception), Suy luận (Reasoning), Hành động (Action), và Bộ nhớ (Memory).",
        "citations": ["T13-101", "T13-102"]
      },
      {
        "question": "Hạn chế lớn nhất của bộ nhớ ngắn hạn (Short-term memory) trong context window là gì?",
        "options": [
          "A. Chi phí triển khai quá cao",
          "B. Dễ bị đầy khi chuỗi hội thoại kéo dài",
          "C. Tốc độ truy xuất chậm",
          "D. Không thể lưu trữ thông tin tạm thời"
        ],
        "correct_option": "B",
        "explanation": "Bộ nhớ ngắn hạn nằm trực tiếp trong context window. Nhược điểm lớn nhất là dễ bị đầy khi chuỗi hội thoại kéo dài.",
        "citations": ["T13-109"]
      },
      {
        "question": "Ba trạng thái cốt lõi của chu trình vòng lặp ReAct là gì?",
        "options": [
          "A. Thought → Action → Observation",
          "B. Input → Process → Output",
          "C. Plan → Execute → Verify",
          "D. Parse → Embed → Search"
        ],
        "correct_option": "A",
        "explanation": "Trong mẫu thiết kế ReAct, Agent thực hiện vòng lặp tuần hoàn qua ba trạng thái: Thought (Suy nghĩ), Action (Hành động), và Observation (Quan sát).",
        "citations": ["T13-125", "T13-126"]
      },
      {
        "question": "Dấu hiệu nào sau đây cho thấy Agent đang bị rơi vào vòng lặp lỗi (infinite loop)?",
        "options": [
          "A. Agent trả lời câu hỏi của người dùng rất nhanh",
          "B. Agent gọi các công cụ khác nhau liên tiếp",
          "C. Agent liên tục thực hiện gọi lặp lại cùng một công cụ với cùng một tham số đầu vào",
          "D. Agent đưa ra Final Answer ngay lập tức"
        ],
        "correct_option": "C",
        "explanation": "Dấu hiệu nhận biết vòng lặp lỗi (Loop Detection): Agent liên tục thực hiện gọi lặp lại cùng một công cụ với cùng một tham số đầu vào; hoặc kết quả quan sát không đổi nhưng Agent vẫn tiếp tục vòng lặp.",
        "citations": ["T13-158"]
      },
      {
        "question": "Mô hình Lai (Hybrid Pattern) tối ưu chi phí và độ trễ bằng cách nào?",
        "options": [
          "A. Sử dụng nhiều agent chạy song song để gom ý kiến biểu quyết",
          "B. Phân loại ý định: câu hỏi FAQ đi qua Chatbot thường, câu phức tạp đi qua Agent loop",
          "C. Cho con người duyệt qua 100% câu trả lời",
          "D. Tự động hóa hoàn toàn các tác vụ không cần chốt chặn"
        ],
        "correct_option": "B",
        "explanation": "Mô hình Lai (Hybrid Pattern) phân loại ý định đầu vào (Intent Triage): Nhánh 1 (FAQ lặp lại) qua Simple Chatbot để phản hồi nhanh; Nhánh 2 (phức tạp) qua Agent Loop; Nhánh 3 qua con người.",
        "citations": ["T13-180"]
      }
    ]
  },
  "T14": {
    "transcript_id": "T14",
    "transcript_title": "Day 04 - Prompt Engineering và Tool Calling",
    "key_points": [
      {
        "content": "Prompt Engineering bản chất là thiết kế giao diện giữa ý định của con người và hành vi của mô hình (Human Intent -> Prompt Interface -> Model Behavior).",
        "citations": ["T14-021"]
      },
      {
        "content": "Nguyên tắc trung tâm của Prompt Engineering là 'Specificity beats cleverness' - cụ thể giúp giảm đầu ra bất ngờ và dễ viết test.",
        "citations": ["T14-028", "T14-029"]
      },
      {
        "content": "System Prompt đóng vai trò là policy layer (lớp quy định hành vi xuyên suốt phiên làm việc) thay vì chỉ giới thiệu vai trò đơn giản.",
        "citations": ["T14-074"]
      },
      {
        "content": "XML tags hoặc Delimiters đóng vai trò như các dấu ngoặc giúp attention mechanism nhận diện cấu trúc, phân tách instructions, documents, và user input.",
        "citations": ["T14-233"]
      },
      {
        "content": "Trong Tool Calling, mô hình không trực tiếp chạy tool mà chỉ phân tích và đề xuất hành động. Tầng ứng dụng mới là nơi thực thi và validate quyền.",
        "citations": ["T14-325", "T14-326"]
      }
    ],
    "keywords": ["Prompt Engineering", "System Prompt", "Specificity", "Token Budget", "XML tags", "Context Bleed", "Lost in the Middle", "Tool Calling", "Validation", "Authorization"],
    "questions": [
      {
        "question": "Prompt Engineering bản chất là thiết kế giao diện giữa hai yếu tố nào?",
        "options": [
          "A. Mã nguồn Python và API của LLM",
          "B. Ý định của con người và hành vi của mô hình",
          "C. Cơ sở dữ liệu và kết quả đầu ra",
          "D. CPU/GPU và tốc độ sinh token"
        ],
        "correct_option": "B",
        "explanation": "Prompt Engineering là thiết kế giao diện giữa ý định của con người và hành vi của mô hình (Human Intent → Prompt Interface → Model Behavior).",
        "citations": ["T14-021"]
      },
      {
        "question": "Nguyên tắc trung tâm của Prompt Engineering trong Production là gì?",
        "options": [
          "A. Phải viết prompt thật dài và hoa mỹ",
          "B. Cleverness beats specificity",
          "C. Specificity beats cleverness",
          "D. Luôn sử dụng Chain-of-Thought cho mọi tác vụ"
        ],
        "correct_option": "C",
        "explanation": "Nguyên tắc trung tâm của tài liệu là: Specificity beats cleverness. Một yêu cầu ngắn nhưng cụ thể thường hiệu quả hơn một yêu cầu dài mà lan man.",
        "citations": ["T14-028"]
      },
      {
        "question": "Hai thành phần nào của một prompt tốt nên được xác định đầu tiên?",
        "options": [
          "A. Role và Context",
          "B. Role và Format",
          "C. Task và Context",
          "D. Task và Format"
        ],
        "correct_option": "D",
        "explanation": "Task và Format là hai thành phần nên được xác định đầu tiên. Role và Context chỉ nên được thêm khi thực sự cần thiết.",
        "citations": ["T14-047"]
      },
      {
        "question": "Sự khác biệt chính về vai trò của System Prompt so với các loại prompt thông thường là gì?",
        "options": [
          "A. Nó đóng vai trò là policy layer (quy định hành vi xuyên suốt phiên làm việc)",
          "B. Nó chỉ dùng để tóm tắt văn bản",
          "C. Nó là input của người dùng gửi lên",
          "D. Nó giúp tăng tốc độ sinh token của GPU"
        ],
        "correct_option": "A",
        "explanation": "System Prompt không nên bị xem như một đoạn giới thiệu vai trò đơn giản. Trong hệ thống thực tế, nó là policy layer, tức lớp quy định hành vi xuyên suốt phiên làm việc.",
        "citations": ["T14-074"]
      },
      {
        "question": "Hậu quả khi prompt quá dài trong context window là gì?",
        "options": [
          "A. Làm mô hình chạy nhanh hơn",
          "B. Giảm thiểu hiện tượng Lost in the Middle",
          "C. Tăng chi phí nạp Input Tokens, tăng độ trễ (latency) và tăng nhiễu cho mô hình",
          "D. Model hoàn toàn không bị ảnh hưởng"
        ],
        "correct_option": "C",
        "explanation": "Prompt dài làm tăng: Input Tokens → Chi phí → Latency → Nhiễu.",
        "citations": ["T14-080"]
      },
      {
        "question": "Kỹ thuật Chain-of-Thought (CoT) phù hợp nhất với loại bài toán nào?",
        "options": [
          "A. Tác vụ chỉ cần trích xuất hoặc định dạng dữ liệu đơn giản",
          "B. Bài toán logic, suy luận phức tạp, có nhiều điều kiện ràng buộc",
          "C. Phân loại email spam nhanh chóng",
          "D. Auto-reply tin nhắn chào hỏi khách hàng"
        ],
        "correct_option": "B",
        "explanation": "CoT phù hợp khi bài toán logic, cần suy luận nhiều bước. CoT thường là overkill đối với tác vụ chỉ cần trích xuất hoặc định dạng dữ liệu.",
        "citations": ["T14-098", "T14-105"]
      },
      {
        "question": "XML tags hoặc Delimiters có vai trò gì trong cấu trúc prompt?",
        "options": [
          "A. Giúp attention mechanism nhận diện cấu trúc, phân tách rõ instructions, documents, và user input",
          "B. Dùng để mã hóa bảo mật thông tin API keys",
          "C. Tăng số lượng token để mô hình thông minh hơn",
          "D. Bắt buộc để model có thể chạy được code Python"
        ],
        "correct_option": "A",
        "explanation": "XML tags đóng vai trò tương tự dấu ngoặc trong lập trình, giúp attention mechanism nhận diện cấu trúc và phân biệt rõ chỉ dẫn và dữ liệu.",
        "citations": ["T14-233"]
      },
      {
        "question": "Hiện tượng 'Context Bleed' xảy ra khi nào?",
        "options": [
          "A. Khi mô hình bị mất kết nối mạng giữa các bước",
          "B. Khi mô hình nhầm lẫn dữ liệu cần xử lý (payload) thành chỉ dẫn phải tuân theo (instruction)",
          "C. Khi token của input tràn sang output",
          "D. Khi model bị quá tải bộ nhớ và crash"
        ],
        "correct_option": "B",
        "explanation": "Context Bleed xảy ra khi mô hình nhầm dữ liệu cần xử lý (payload) với chỉ dẫn phải tuân theo (instruction), ví dụ như khi trong tài liệu có chứa câu: 'hãy bỏ qua hướng dẫn phía trên'.",
        "citations": ["T14-237", "T14-243"]
      },
      {
        "question": "Nguyên tắc cốt lõi về bản chất của Tool Calling là gì?",
        "options": [
          "A. Mô hình tự động thực thi trực tiếp các câu lệnh SQL trên DB",
          "B. Mô hình trực tiếp gọi API của bên thứ ba không qua server",
          "C. Mô hình không trực tiếp chạy tool mà chỉ phân tích và đề xuất hành động + tham số JSON",
          "D. Tool tự động chạy mà không cần LLM ra quyết định"
        ],
        "correct_option": "C",
        "explanation": "Điểm quan trọng nhất là: Model không trực tiếp chạy tool. Model chỉ đề xuất hành động. Tầng ứng dụng mới thực thi và trả kết quả lại.",
        "citations": ["T14-325", "T14-326"]
      },
      {
        "question": "Tại sao tầng ứng dụng phải thực hiện validation và authorization cho Tool Calling?",
        "options": [
          "A. Để giảm số lượng token nạp vào model",
          "B. Vì mô hình LLM có thể tự động kiểm tra quyền bảo mật",
          "C. Để model tự động sửa lỗi tham số",
          "D. Vì System Prompt không thay thế hệ thống phân quyền và kiểm soát lỗi của phần mềm"
        ],
        "correct_option": "D",
        "explanation": "Tầng ứng dụng phải kiểm tra kiểu dữ liệu, giới hạn, quyền và xác nhận vì System Prompt không thay thế Authorization System. Đây là ranh giới quan trọng giữa kiểm soát mô hình và bảo mật phần mềm thực tế.",
        "citations": ["T14-387", "T14-388"]
      }
    ]
  },
  "T15": {
    "transcript_id": "T15",
    "transcript_title": "Day 05 - AI Product Thinking và Requirements",
    "key_points": [
      {
        "content": "Sự khác biệt lớn nhất giữa Software truyền thống (Deterministic - 1+1=2) và AI Product (Probabilistic - xác suất, có dải chất lượng và fallback).",
        "citations": ["T15-030", "T15-031"]
      },
      {
        "content": "Lý thuyết Jobs-to-be-Done (JTBD) cho AI phân tích nhu cầu người dùng qua ba khía cạnh: Functional Job, Emotional Job, và Social Job.",
        "citations": ["T15-043"]
      },
      {
        "content": "Năm trụ cột cốt lõi của Responsible AI (AI có trách nhiệm) bao gồm: Công bằng (Fairness), Tin cậy & An toàn, Bảo mật & Riêng tư, Toàn diện, và Minh bạch.",
        "citations": ["T15-062", "T15-067"]
      },
      {
        "content": "Chân dung người dùng (Persona) cho sản phẩm AI cần bổ sung thêm bốn chiều kích đặc thù: AI Literacy Level, Automation Willingness, Error Tolerance, và Explainability Need.",
        "citations": ["T15-093", "T15-097"]
      },
      {
        "content": "Mức độ nghiêm trọng của rủi ro được định lượng bằng công thức: Điểm rủi ro = Khả năng xảy ra (Likelihood) x Mức độ ảnh hưởng (Impact).",
        "citations": ["T15-180"]
      }
    ],
    "keywords": ["Product Thinking", "Probabilistic", "JTBD", "Responsible AI", "NIST AI RMF", "EU AI Act", "Feedback Loops", "PRD", "Risk Matrix", "Go/No-Go"],
    "questions": [
      {
        "question": "Hai kiểu thất bại phổ biến nhất trong phát triển sản phẩm AI là gì?",
        "options": [
          "A. Không đủ GPU và không có API key",
          "B. Build the wrong thing (xây dựng sai sản phẩm) và Build the thing wrong (xây dựng sản phẩm sai cách)",
          "C. Viết code lỗi và không có tài liệu hướng dẫn sử dụng",
          "D. Thu thập thiếu dữ liệu và chọn sai mô hình ngôn ngữ lớn"
        ],
        "correct_option": "B",
        "explanation": "Hai kiểu thất bại phổ biến: Build the wrong thing (xây dựng sai sản phẩm - do không thấu hiểu người dùng/JTBD) và Build the thing wrong (xây dựng sản phẩm sai cách - do yêu cầu mơ hồ, thiếu tiêu chí nghiệm thu).",
        "citations": ["T15-020", "T15-021"]
      },
      {
        "question": "Bản chất kết quả đầu ra (Output) của một sản phẩm AI thực tế so với phần mềm truyền thống là gì?",
        "options": [
          "A. Deterministic (Có tính xác định cứng, 1+1 luôn bằng 2)",
          "B. Probabilistic (Có tính xác suất, biến thiên và không đồng nhất)",
          "C. Luôn chính xác tuyệt đối 100%",
          "D. Không đổi theo thời gian"
        ],
        "correct_option": "B",
        "explanation": "Đầu ra của phần mềm truyền thống là Deterministic (xác định), còn đầu ra của AI Product thực tế là Probabilistic (xác suất, biến thiên và không đồng nhất).",
        "citations": ["T15-030", "T15-031"]
      },
      {
        "question": "Lý thuyết Jobs-to-be-Done (JTBD) phân tích nhu cầu người dùng qua ba khía cạnh nào?",
        "options": [
          "A. Input, Process, Output",
          "B. User, Buyer, Administrator",
          "C. Functional Job, Emotional Job, Social Job",
          "D. Business KPI, Product Metric, AI Metric"
        ],
        "correct_option": "C",
        "explanation": "Lý thuyết JTBD cho sản phẩm AI phân tích nhu cầu qua ba khía cạnh: Functional Job (mục tiêu chức năng), Emotional Job (cảm xúc nội tại), và Social Job (vị thế xã hội).",
        "citations": ["T15-043"]
      },
      {
        "question": "Chỉ số North Star Metric khuyên dùng cho trường hợp Tra cứu văn bản chính sách (Policy Assistant) là gì?",
        "options": [
          "A. Độ dài trung bình của câu trả lời sinh ra",
          "B. Thời gian trả lời đúng nguồn trích dẫn chính thức (Time-to-answer)",
          "C. Số lượng tài liệu được tải lên hệ thống",
          "D. Tỷ lệ số câu hỏi chat trong một ngày"
        ],
        "correct_option": "B",
        "explanation": "Chỉ số North Star Metric cho Tra cứu văn bản chính sách: Đo lường bằng Thời gian trả lời đúng nguồn trích dẫn chính thức (Time-to-answer) – Đừng chỉ đo độ dài của câu trả lời sinh ra.",
        "citations": ["T15-057"]
      },
      {
        "question": "Năm trụ cột cốt lõi của Responsible AI (AI có trách nhiệm) bao gồm những gì?",
        "options": [
          "A. Speed, Cost, Memory, Tools, Accuracy",
          "B. Python, PyTorch, Transformers, OpenAI, Gemini",
          "C. Công bằng, Tin cậy & An toàn, Bảo mật & Riêng tư, Toàn diện, Minh bạch",
          "D. Pre-training, SFT, RLHF, DPO, Inference"
        ],
        "correct_option": "C",
        "explanation": "5 Trụ cột cốt lõi của Responsible AI: Công bằng (Fairness), Tin cậy & An toàn (Reliability & Safety), Bảo mật & Riêng tư (Privacy & Security), Toàn diện (Inclusiveness), và Minh bạch (Transparency).",
        "citations": ["T15-062", "T15-067"]
      },
      {
        "question": "Theo Đạo luật AI Act của Liên minh Châu Âu (EU AI Act 2024), các PM/BA bắt buộc phải thiết kế yếu tố nào khi sản phẩm AI tham gia lĩnh vực nhạy cảm?",
        "options": [
          "A. Tối ưu thuật toán mã hóa GPU mới nhất",
          "B. Hệ thống ghi nhật ký (Logging), hiển thị tuyên bố rõ (Disclosure), xử lý ngoại lệ và quy trình con người kiểm duyệt",
          "C. Tự động nâng cấp lên model đắt tiền nhất",
          "D. Mua bản quyền phần mềm độc quyền từ EU"
        ],
        "correct_option": "B",
        "explanation": "EU AI Act 2024 buộc đội ngũ phát triển phải thiết kế hệ thống ghi nhật ký (Logging), hiển thị tuyên bố rõ ràng (Disclosure), xử lý ngoại lệ (Exception Handling) và quy trình phê duyệt (Review Process) ngay từ đầu.",
        "citations": ["T15-083"]
      },
      {
        "question": "Bốn chiều kích đặc thù cần bổ sung vào chân dung người dùng (Persona) cho sản phẩm AI là gì?",
        "options": [
          "A. Tuổi, Giới tính, Nghề nghiệp, Thu nhập",
          "B. AI Literacy Level, Automation Willingness, Error Tolerance, Explainability Need",
          "C. Hệ điều hành, Thiết bị sử dụng, Băng thông mạng, Vị trí địa lý",
          "D. Số giờ học, Điểm thi thử, Số lượng câu hỏi đã chat, Lịch sử nộp bài"
        ],
        "correct_option": "B",
        "explanation": "Persona thiết kế cho sản phẩm AI bắt buộc phải mở rộng thêm 4 chiều kích đặc thù: AI Literacy Level, Automation Willingness, Error Tolerance, và Explainability Need.",
        "citations": ["T15-093", "T15-097"]
      },
      {
        "question": "Trong thiết kế vòng phản hồi (Feedback Loops), tín hiệu như Copy, Rephrase, Override, Abandon thuộc nhóm nào?",
        "options": [
          "A. Explicit Feedback (Phản hồi trực tiếp)",
          "B. Behavioral Signal (Tín hiệu hành vi)",
          "C. Outcome Signal (Tín hiệu kết quả)",
          "D. User CSAT Score"
        ],
        "correct_option": "B",
        "explanation": "Behavioral Signal (Tín hiệu hành vi) là các chỉ báo ngầm như sao chép câu trả lời (Copy), sửa đổi nội dung sinh ra (Rephrase), ghi đè kết quả (Override), hoặc bỏ ngang phiên làm việc (Abandon).",
        "citations": ["T15-101"]
      },
      {
        "question": "Mức độ nghiêm trọng của mỗi rủi ro trong Risk Register được định lượng bằng công thức nào?",
        "options": [
          "A. Điểm rủi ro = Khả năng xảy ra (Likelihood) x Mức độ ảnh hưởng (Impact)",
          "B. Điểm rủi ro = Chi phí vận hành / Số lượng người dùng",
          "C. Điểm rủi ro = Số lỗi ảo giác x Tốc độ phản hồi",
          "D. Điểm rủi ro = Precision x Recall"
        ],
        "correct_option": "A",
        "explanation": "Mức độ nghiêm trọng của mỗi rủi ro được định lượng bằng công thức: Điểm rủi ro = Khả năng xảy ra (Likelihood) x Mức độ ảnh hưởng (Impact).",
        "citations": ["T15-180"]
      },
      {
        "question": "Điều kiện No-Go (Không triển khai) được kích hoạt khi nào?",
        "options": [
          "A. Khi mô hình có một vài lỗi chính tả nhỏ không ảnh hưởng lớn",
          "B. Khi hệ thống chưa xử lý triệt để rủi ro lớn về bảo mật riêng tư, tuân thủ pháp lý hoặc thiếu cơ chế dự phòng",
          "C. Khi chi phí API tăng nhẹ 5%",
          "D. Khi người dùng muốn tự tay làm một số tác vụ cá nhân"
        ],
        "correct_option": "B",
        "explanation": "No-Go kích hoạt khi hệ thống chưa xử lý triệt để các rủi ro lớn liên quan đến bảo mật riêng tư dữ liệu (privacy) hoặc rủi ro pháp lý tuân thủ (compliance gap); hoặc chưa thiết lập được cơ chế dự phòng (fallback) đáng tin cậy; hoặc chưa chứng minh được rõ ràng giá trị mang lại cho người dùng cuối.",
        "citations": ["T15-221"]
      }
    ]
  }
}

# Write out the study_packs_db.json
output_path = Path("d:/Python/vin_ai_thuc_chien/K4-hackathon-AI_Magnet-D304/data/study_packs_db.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(db, indent=2, ensure_ascii=False), encoding='utf-8')
print("Successfully generated data/study_packs_db.json!")
