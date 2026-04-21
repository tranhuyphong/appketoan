learning_path = [
    {
        "level": "🟢 Apprentice",
        "unlock_coins": 0,
        "modules": [

            # ================= MODULE 1 =================
            {
                "name": "Nguyên lý Kế toán",
                "lessons": [

                    {
                        "id": "asset",
                        "title": "Tài sản là gì?",
                        "xp": 20,
                        "content": """
Tài sản là tất cả những gì doanh nghiệp sở hữu và có thể tạo ra giá trị kinh tế.

Ví dụ:
- Tiền mặt
- Hàng tồn kho
- Máy móc
- Khoản phải thu

👉 Quy tắc: Tài sản LUÔN có số dư bên Nợ
                        """,
                        "quiz": [
                            {
                                "question": "Tài sản là gì?",
                                "options": [
                                    "Nguồn vốn của doanh nghiệp",
                                    "Những gì doanh nghiệp sở hữu",
                                    "Chi phí phát sinh"
                                ],
                                "answer": 1
                            },
                            {
                                "question": "Tài sản có số dư bên nào?",
                                "options": ["Nợ", "Có"],
                                "answer": 0
                            }
                        ]
                    },

                    {
                        "id": "liability_equity",
                        "title": "Nguồn vốn là gì?",
                        "xp": 20,
                        "content": """
Nguồn vốn là nơi hình thành nên tài sản.

Gồm 2 loại:
- Nợ phải trả (vay ngân hàng, phải trả NCC)
- Vốn chủ sở hữu

👉 Quy tắc: Nguồn vốn có số dư bên Có
                        """,
                        "quiz": [
                            {
                                "question": "Nguồn vốn gồm những gì?",
                                "options": [
                                    "Tài sản",
                                    "Nợ và vốn chủ",
                                    "Doanh thu"
                                ],
                                "answer": 1
                            },
                            {
                                "question": "Nguồn vốn có số dư bên nào?",
                                "options": ["Nợ", "Có"],
                                "answer": 1
                            }
                        ]
                    },

                    {
                        "id": "accounting_equation",
                        "title": "Phương trình kế toán",
                        "xp": 30,
                        "content": """
Phương trình kế toán:

Tài sản = Nợ phải trả + Vốn chủ sở hữu

👉 Đây là nền tảng của toàn bộ kế toán.

Mọi nghiệp vụ đều phải giữ cân bằng phương trình này.
                        """,
                        "quiz": [
                            {
                                "question": "Phương trình kế toán là gì?",
                                "options": [
                                    "Tài sản = Chi phí",
                                    "Tài sản = Nợ + Vốn",
                                    "Doanh thu = Lợi nhuận"
                                ],
                                "answer": 1
                            }
                        ]
                    },

                    {
                        "id": "double_entry",
                        "title": "Nguyên tắc ghi sổ kép",
                        "xp": 30,
                        "content": """
Mỗi nghiệp vụ kế toán luôn có 2 bút toán:

👉 Nợ = Có

Ví dụ:
Mua hàng bằng tiền:
- Nợ Hàng tồn kho
- Có Tiền

👉 Không bao giờ chỉ ghi 1 bên
                        """,
                        "quiz": [
                            {
                                "question": "Ghi sổ kép nghĩa là gì?",
                                "options": [
                                    "Ghi 1 bút toán",
                                    "Ghi 2 bút toán Nợ và Có",
                                    "Chỉ ghi Nợ"
                                ],
                                "answer": 1
                            }
                        ]
                    },

                    {
                        "id": "account_system",
                        "title": "Hệ thống tài khoản",
                        "xp": 25,
                        "content": """
Tài khoản kế toán dùng để phân loại nghiệp vụ.

Ví dụ:
- 111: Tiền mặt
- 112: Ngân hàng
- 131: Phải thu
- 331: Phải trả

👉 Mỗi tài khoản có quy tắc Nợ/Có riêng
                        """,
                        "quiz": [
                            {
                                "question": "TK 111 là gì?",
                                "options": [
                                    "Ngân hàng",
                                    "Tiền mặt",
                                    "Phải thu"
                                ],
                                "answer": 1
                            }
                        ]
                    }
                ]
            },

            # ================= MODULE 2 =================
            {
                "name": "Kế toán tài chính cơ bản",
                "lessons": [

                    {
                        "id": "cash",
                        "title": "Kế toán tiền",
                        "xp": 25,
                        "content": """
Tiền gồm:
- Tiền mặt (111)
- Tiền gửi ngân hàng (112)

Ví dụ:
Thu tiền bán hàng:
- Nợ 111
- Có 511

👉 Tiền tăng → ghi Nợ
                        """,
                        "quiz": [
                            {
                                "question": "Tiền tăng ghi gì?",
                                "options": ["Nợ", "Có"],
                                "answer": 0
                            }
                        ]
                    },

                    {
                        "id": "inventory",
                        "title": "Hàng tồn kho",
                        "xp": 25,
                        "content": """
Hàng tồn kho là hàng hóa doanh nghiệp mua để bán.

Ví dụ:
Mua hàng:
- Nợ 156
- Có 111/331

👉 Khi bán sẽ ghi nhận giá vốn
                        """,
                        "quiz": [
                            {
                                "question": "Mua hàng ghi gì?",
                                "options": [
                                    "Nợ 156",
                                    "Có 156"
                                ],
                                "answer": 0
                            }
                        ]
                    },

                    {
                        "id": "salary",
                        "title": "Kế toán tiền lương",
                        "xp": 30,
                        "content": """
Tiền lương là chi phí của doanh nghiệp.

Ví dụ:
- Nợ 642
- Có 334

👉 Khi trả lương:
- Nợ 334
- Có 111
                        """,
                        "quiz": [
                            {
                                "question": "Chi phí lương ghi vào đâu?",
                                "options": [
                                    "Tài sản",
                                    "Chi phí",
                                    "Doanh thu"
                                ],
                                "answer": 1
                            }
                        ]
                    },

                    {
                        "id": "fixed_asset",
                        "title": "Tài sản cố định",
                        "xp": 30,
                        "content": """
TSCĐ là tài sản có giá trị lớn và sử dụng lâu dài.

Ví dụ:
- Máy móc
- Nhà xưởng

👉 Phải trích khấu hao hàng tháng
                        """,
                        "quiz": [
                            {
                                "question": "TSCĐ là gì?",
                                "options": [
                                    "Tài sản ngắn hạn",
                                    "Tài sản dài hạn",
                                    "Chi phí"
                                ],
                                "answer": 1
                            }
                        ]
                    }
                ]
            }
        ]
    }
]
{
    "level2": "🔵 Professional",
    "unlock_coins": 200,
    "modules": [

        # ================= MODULE 3 =================
        {
            "name": "Kế toán chi phí & giá thành",
            "lessons": [

                {
                    "id": "cost_621",
                    "title": "Chi phí nguyên vật liệu (621)",
                    "xp": 30,
                    "content": """
TK 621 dùng để tập hợp chi phí nguyên vật liệu trực tiếp.

Ví dụ:
Xuất kho nguyên liệu sản xuất:
- Nợ 621
- Có 152

👉 Cuối kỳ kết chuyển vào 154
                    """,
                    "quiz": [
                        {
                            "question": "Xuất NVL sản xuất ghi gì?",
                            "options": [
                                "Nợ 621",
                                "Có 621"
                            ],
                            "answer": 0
                        }
                    ]
                },

                {
                    "id": "cost_622",
                    "title": "Chi phí nhân công (622)",
                    "xp": 30,
                    "content": """
TK 622 ghi nhận chi phí nhân công trực tiếp.

Ví dụ:
- Nợ 622
- Có 334

👉 Sau đó kết chuyển sang 154
                    """,
                    "quiz": [
                        {
                            "question": "Chi phí nhân công ghi vào đâu?",
                            "options": [
                                "622",
                                "642",
                                "111"
                            ],
                            "answer": 0
                        }
                    ]
                },

                {
                    "id": "cost_627",
                    "title": "Chi phí sản xuất chung (627)",
                    "xp": 35,
                    "content": """
TK 627 gồm:
- Điện, nước
- Khấu hao máy móc
- Lương quản lý xưởng

👉 Cuối kỳ phân bổ vào 154
                    """,
                    "quiz": [
                        {
                            "question": "Chi phí điện nhà xưởng vào đâu?",
                            "options": [
                                "627",
                                "621",
                                "642"
                            ],
                            "answer": 0
                        }
                    ]
                },

                {
                    "id": "costing_methods",
                    "title": "Phương pháp tính giá thành",
                    "xp": 40,
                    "content": """
Các phương pháp phổ biến:
- Giản đơn
- Hệ số
- Định mức

👉 Mục tiêu: tính giá thành sản phẩm chính xác
                    """,
                    "quiz": [
                        {
                            "question": "Mục tiêu của tính giá thành?",
                            "options": [
                                "Tính doanh thu",
                                "Tính giá sản phẩm",
                                "Tính lương"
                            ],
                            "answer": 1
                        }
                    ]
                }
            ]
        },

        # ================= MODULE 4 =================
        {
            "name": "Kế toán thuế",
            "lessons": [

                {
                    "id": "vat",
                    "title": "Thuế GTGT",
                    "xp": 35,
                    "content": """
Thuế GTGT gồm:
- Thuế đầu vào
- Thuế đầu ra

👉 Phải nộp = đầu ra - đầu vào
                    """,
                    "quiz": [
                        {
                            "question": "Thuế phải nộp tính thế nào?",
                            "options": [
                                "Đầu ra - đầu vào",
                                "Đầu vào - đầu ra"
                            ],
                            "answer": 0
                        }
                    ]
                },

                {
                    "id": "cit",
                    "title": "Thuế TNDN",
                    "xp": 35,
                    "content": """
Thuế TNDN đánh vào lợi nhuận doanh nghiệp.

Công thức:
Thuế = Lợi nhuận * thuế suất

👉 Thường là 20%
                    """,
                    "quiz": [
                        {
                            "question": "Thuế TNDN dựa trên gì?",
                            "options": [
                                "Doanh thu",
                                "Lợi nhuận",
                                "Chi phí"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "pit",
                    "title": "Thuế TNCN",
                    "xp": 30,
                    "content": """
Thuế TNCN áp dụng cho người lao động.

Doanh nghiệp:
👉 Khấu trừ trước khi trả lương
                    """,
                    "quiz": [
                        {
                            "question": "Thuế TNCN ai chịu?",
                            "options": [
                                "Doanh nghiệp",
                                "Người lao động"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "tax_review",
                    "title": "Rà soát thuế",
                    "xp": 40,
                    "content": """
Trước khi quyết toán:

👉 Kiểm tra:
- Hóa đơn hợp lệ
- Chi phí hợp lý
- Thuế kê khai đúng

👉 Tránh bị truy thu
                    """,
                    "quiz": [
                        {
                            "question": "Mục tiêu rà soát thuế?",
                            "options": [
                                "Tăng chi phí",
                                "Tránh sai sót",
                                "Tăng doanh thu"
                            ],
                            "answer": 1
                        }
                    ]
                }
            ]
        },

        # ================= MODULE 5 =================
        {
            "name": "Kế toán quản trị",
            "lessons": [

                {
                    "id": "breakeven",
                    "title": "Điểm hòa vốn",
                    "xp": 40,
                    "content": """
Điểm hòa vốn là mức doanh thu mà:

👉 Lợi nhuận = 0

Công thức:
Doanh thu = Chi phí

👉 Dùng để ra quyết định kinh doanh
                    """,
                    "quiz": [
                        {
                            "question": "Điểm hòa vốn là gì?",
                            "options": [
                                "Có lãi",
                                "Lỗ",
                                "Không lãi không lỗ"
                            ],
                            "answer": 2
                        }
                    ]
                },

                {
                    "id": "budgeting",
                    "title": "Lập ngân sách",
                    "xp": 35,
                    "content": """
Ngân sách là kế hoạch tài chính.

Bao gồm:
- Doanh thu dự kiến
- Chi phí dự kiến

👉 Giúp kiểm soát doanh nghiệp
                    """,
                    "quiz": [
                        {
                            "question": "Ngân sách dùng để làm gì?",
                            "options": [
                                "Tiêu tiền",
                                "Lập kế hoạch tài chính",
                                "Tăng lương"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "cashflow",
                    "title": "Dự báo dòng tiền",
                    "xp": 40,
                    "content": """
Dòng tiền rất quan trọng:

👉 Có lợi nhuận chưa chắc có tiền

Phải dự báo:
- Tiền vào
- Tiền ra

👉 Tránh thiếu tiền
                    """,
                    "quiz": [
                        {
                            "question": "Tại sao cần dự báo dòng tiền?",
                            "options": [
                                "Để đẹp báo cáo",
                                "Để tránh thiếu tiền",
                                "Để tăng thuế"
                            ],
                            "answer": 1
                        }
                    ]
                }
            ]
        }
    ]
}
{
    "level3": "🟠 Expert",
    "unlock_coins": 500,
    "modules": [

        # ================= MODULE 6 =================
        {
            "name": "IFRS & Báo cáo quốc tế",
            "lessons": [

                {
                    "id": "ifrs_intro",
                    "title": "IFRS là gì?",
                    "xp": 40,
                    "content": """
IFRS (International Financial Reporting Standards)
là chuẩn mực kế toán quốc tế.

👉 Giúp báo cáo tài chính minh bạch, so sánh toàn cầu

So với VAS:
- IFRS linh hoạt hơn
- IFRS dùng nhiều judgment hơn
                    """,
                    "quiz": [
                        {
                            "question": "IFRS là gì?",
                            "options": [
                                "Chuẩn kế toán Việt Nam",
                                "Chuẩn kế toán quốc tế",
                                "Luật thuế"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "vas_vs_ifrs",
                    "title": "Khác biệt VAS vs IFRS",
                    "xp": 45,
                    "content": """
VAS: theo quy định chặt
IFRS: theo bản chất kinh tế

Ví dụ:
- IFRS cho phép đánh giá lại tài sản
- VAS thường theo giá gốc

👉 IFRS phản ánh thực tế hơn
                    """,
                    "quiz": [
                        {
                            "question": "IFRS khác VAS ở điểm nào?",
                            "options": [
                                "Cứng nhắc hơn",
                                "Linh hoạt hơn",
                                "Không dùng kế toán"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "english_accounting",
                    "title": "Tiếng Anh kế toán",
                    "xp": 40,
                    "content": """
Một số từ quan trọng:

- Revenue: Doanh thu
- Expense: Chi phí
- Asset: Tài sản
- Liability: Nợ

👉 Bắt buộc nếu làm công ty nước ngoài
                    """,
                    "quiz": [
                        {
                            "question": "Revenue nghĩa là gì?",
                            "options": [
                                "Chi phí",
                                "Doanh thu",
                                "Tài sản"
                            ],
                            "answer": 1
                        }
                    ]
                }
            ]
        },

        # ================= MODULE 7 =================
        {
            "name": "Hợp nhất & M&A",
            "lessons": [

                {
                    "id": "consolidation",
                    "title": "Hợp nhất báo cáo tài chính",
                    "xp": 50,
                    "content": """
Khi công ty mẹ sở hữu công ty con:

👉 Phải hợp nhất báo cáo

Nguyên tắc:
- Cộng số liệu
- Loại trừ giao dịch nội bộ
                    """,
                    "quiz": [
                        {
                            "question": "Hợp nhất dùng khi nào?",
                            "options": [
                                "1 công ty",
                                "Công ty mẹ - con",
                                "Cá nhân"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "goodwill",
                    "title": "Lợi thế thương mại (Goodwill)",
                    "xp": 50,
                    "content": """
Goodwill phát sinh khi mua công ty:

👉 Giá mua > giá trị tài sản thuần

Ví dụ:
Mua công ty 10 tỷ
Tài sản chỉ 8 tỷ
→ Goodwill = 2 tỷ
                    """,
                    "quiz": [
                        {
                            "question": "Goodwill là gì?",
                            "options": [
                                "Lỗ",
                                "Chênh lệch khi mua công ty",
                                "Chi phí"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "intercompany",
                    "title": "Giao dịch nội bộ",
                    "xp": 45,
                    "content": """
Giao dịch nội bộ là giữa các công ty trong cùng tập đoàn.

👉 Khi hợp nhất phải loại bỏ

Ví dụ:
- Bán hàng nội bộ
- Cho vay nội bộ
                    """,
                    "quiz": [
                        {
                            "question": "Giao dịch nội bộ cần làm gì?",
                            "options": [
                                "Giữ nguyên",
                                "Loại bỏ",
                                "Tăng lên"
                            ],
                            "answer": 1
                        }
                    ]
                }
            ]
        },

        # ================= MODULE 8 =================
        {
            "name": "Kế toán ngành đặc thù",
            "lessons": [

                {
                    "id": "construction",
                    "title": "Kế toán xây dựng",
                    "xp": 50,
                    "content": """
Ngành xây dựng ghi nhận doanh thu theo tiến độ.

👉 Không ghi nhận 1 lần

Ví dụ:
Công trình 10 tỷ, hoàn thành 50%
→ Ghi nhận 5 tỷ
                    """,
                    "quiz": [
                        {
                            "question": "Doanh thu xây dựng ghi khi nào?",
                            "options": [
                                "Khi xong hết",
                                "Theo tiến độ",
                                "Khi thu tiền"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "banking",
                    "title": "Kế toán ngân hàng",
                    "xp": 50,
                    "content": """
Ngân hàng có nghiệp vụ đặc biệt:

- Cho vay
- Huy động vốn

👉 Thu nhập chính: lãi vay
                    """,
                    "quiz": [
                        {
                            "question": "Thu nhập chính của ngân hàng?",
                            "options": [
                                "Bán hàng",
                                "Lãi vay",
                                "Chi phí"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "industry_compare",
                    "title": "So sánh ngành",
                    "xp": 45,
                    "content": """
Mỗi ngành kế toán khác nhau:

- Xây dựng → theo tiến độ
- Thương mại → theo bán hàng
- Ngân hàng → theo lãi

👉 Không có 1 công thức chung
                    """,
                    "quiz": [
                        {
                            "question": "Kế toán có giống nhau giữa các ngành?",
                            "options": [
                                "Giống",
                                "Khác",
                                "Không dùng kế toán"
                            ],
                            "answer": 1
                        }
                    ]
                }
            ]
        }
    ]
}
{
    "level4": "🔴 Strategist",
    "unlock_coins": 1000,
    "modules": [

        # ================= MODULE 9 =================
        {
            "name": "Kế toán pháp y (Fraud Detection)",
            "lessons": [

                {
                    "id": "fraud_basic",
                    "title": "Gian lận tài chính là gì?",
                    "xp": 60,
                    "content": """
Gian lận tài chính là hành vi cố ý làm sai lệch số liệu.

Ví dụ:
- Khai khống doanh thu
- Giấu chi phí
- Lập hóa đơn giả

👉 Mục tiêu: làm đẹp báo cáo
                    """,
                    "quiz": [
                        {
                            "question": "Gian lận là gì?",
                            "options": [
                                "Sai sót vô ý",
                                "Cố ý làm sai số liệu",
                                "Chi phí hợp lệ"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "fraud_signals",
                    "title": "Dấu hiệu gian lận",
                    "xp": 65,
                    "content": """
Các dấu hiệu cảnh báo:

🚨 Doanh thu tăng bất thường
🚨 Lợi nhuận cao nhưng không có tiền
🚨 Giao dịch bất thường cuối kỳ

👉 Phải luôn nghi ngờ số liệu
                    """,
                    "quiz": [
                        {
                            "question": "Dấu hiệu gian lận?",
                            "options": [
                                "Doanh thu ổn định",
                                "Lợi nhuận cao bất thường",
                                "Chi phí hợp lý"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "fraud_analysis",
                    "title": "Phân tích gian lận",
                    "xp": 70,
                    "content": """
Cách phát hiện:

- So sánh kỳ trước
- Kiểm tra dòng tiền
- Đối chiếu chứng từ

👉 Không chỉ nhìn báo cáo
                    """,
                    "quiz": [
                        {
                            "question": "Phát hiện gian lận bằng cách nào?",
                            "options": [
                                "Chỉ đọc báo cáo",
                                "Phân tích & đối chiếu",
                                "Đoán"
                            ],
                            "answer": 1
                        }
                    ]
                }
            ]
        },

        # ================= MODULE 10 =================
        {
            "name": "ESG & Báo cáo bền vững",
            "lessons": [

                {
                    "id": "esg_intro",
                    "title": "ESG là gì?",
                    "xp": 60,
                    "content": """
ESG = Environmental, Social, Governance

👉 Đánh giá doanh nghiệp không chỉ bằng lợi nhuận

Bao gồm:
- Môi trường
- Xã hội
- Quản trị
                    """,
                    "quiz": [
                        {
                            "question": "ESG là gì?",
                            "options": [
                                "Báo cáo tài chính",
                                "Đánh giá bền vững",
                                "Thuế"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "carbon_accounting",
                    "title": "Kế toán carbon",
                    "xp": 65,
                    "content": """
Doanh nghiệp phải đo lượng khí thải CO2.

👉 Gọi là Carbon Accounting

Mục tiêu:
- Giảm phát thải
- Báo cáo minh bạch
                    """,
                    "quiz": [
                        {
                            "question": "Carbon accounting là gì?",
                            "options": [
                                "Kế toán tiền",
                                "Đo khí thải",
                                "Tính lương"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "sustainability_report",
                    "title": "Báo cáo bền vững",
                    "xp": 60,
                    "content": """
Ngoài báo cáo tài chính, DN còn phải báo cáo:

- Môi trường
- Nhân sự
- Trách nhiệm xã hội

👉 Xu hướng toàn cầu
                    """,
                    "quiz": [
                        {
                            "question": "Báo cáo bền vững gồm gì?",
                            "options": [
                                "Chỉ lợi nhuận",
                                "Môi trường & xã hội",
                                "Chi phí"
                            ],
                            "answer": 1
                        }
                    ]
                }
            ]
        },

        # ================= MODULE 11 =================
        {
            "name": "Tech-Accounting & AI",
            "lessons": [

                {
                    "id": "excel_advanced",
                    "title": "Excel nâng cao",
                    "xp": 70,
                    "content": """
Kế toán hiện đại cần Excel:

- Pivot Table
- VLOOKUP / XLOOKUP
- Dashboard

👉 Giúp xử lý dữ liệu nhanh
                    """,
                    "quiz": [
                        {
                            "question": "Excel dùng để làm gì?",
                            "options": [
                                "Chơi game",
                                "Phân tích dữ liệu",
                                "Ghi chép tay"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "powerbi",
                    "title": "Power BI",
                    "xp": 70,
                    "content": """
Power BI dùng để:

- Trực quan hóa dữ liệu
- Làm dashboard
- Phân tích tài chính

👉 Rất quan trọng cho kế toán quản trị
                    """,
                    "quiz": [
                        {
                            "question": "Power BI dùng để?",
                            "options": [
                                "Nhập liệu",
                                "Trực quan hóa dữ liệu",
                                "Tính thuế"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "ai_accounting",
                    "title": "AI trong kế toán",
                    "xp": 80,
                    "content": """
AI có thể:

- Tự động nhập liệu
- Phát hiện gian lận
- Dự báo tài chính

👉 Kế toán tương lai = AI + tư duy
                    """,
                    "quiz": [
                        {
                            "question": "AI giúp gì trong kế toán?",
                            "options": [
                                "Thay hoàn toàn con người",
                                "Hỗ trợ tự động hóa",
                                "Không liên quan"
                            ],
                            "answer": 1
                        }
                    ]
                },

                {
                    "id": "future_accountant",
                    "title": "Kế toán tương lai",
                    "xp": 100,
                    "content": """
Kế toán không còn là nhập liệu.

👉 Vai trò mới:
- Phân tích
- Ra quyết định
- Làm việc với AI

🔥 Bạn không phải kế toán
→ Bạn là Financial Strategist
                    """,
                    "quiz": [
                        {
                            "question": "Vai trò kế toán tương lai?",
                            "options": [
                                "Nhập liệu",
                                "Phân tích & chiến lược",
                                "Ghi sổ"
                            ],
                            "answer": 1
                        }
                    ]
                }
            ]
        }
    ]
}
