# data.py - Cơ sở dữ liệu toàn bộ lộ trình học Kế toán Slay

ACADEMY_DATA = {
    "PHASE_1": {
        "name": "📍 CHẶNG 1: KIẾN THỨC CỐT LÕI (CORE)",
        "modules": {
            "M1": {
                "name": "Module 1: Nguyên lý Kế toán (Luật chơi)",
                "is_premium": False,
                "lessons": [
                    {
                        "id": "L1.1",
                        "title": "Ngôn ngữ kinh doanh & Đối tượng kế toán",
                        "theory": """Kế toán là ngôn ngữ dùng để mô tả sức khỏe tài chính. Đối tượng của nó bao gồm:
                        - **Tài sản (Assets):** Những gì công ty sở hữu (Tiền, hàng, máy móc).
                        - **Nguồn vốn (Liabilities & Equity):** Nguồn hình thành tài sản (Vốn tự có hoặc đi vay).""",
                        "visuals": [""],
                        "deep_dive": "💡 **Góc nhìn chuyên gia:** Tài sản luôn bằng Nguồn vốn vì mọi thứ bạn 'có' đều phải được lấy từ một 'nguồn' nào đó.",
                        "exercises": [
                            {"q": "Doanh nghiệp dùng tiền mặt mua máy tính. Máy tính thuộc nhóm nào?", "options": ["Tài sản", "Nguồn vốn"], "correct": "Tài sản"}
                        ]
                    },
                    {
                        "id": "L1.2",
                        "title": "Nguyên tắc ghi sổ kép (Nợ - Có)",
                        "theory": "Kế toán sử dụng ghi sổ kép: Một nghiệp vụ tác động vào ít nhất 2 tài khoản. Tổng Nợ luôn bằng Tổng Có.",
                        "visuals": [""],
                        "deep_dive": "💡 **Mẹo Gen Z:** Hãy nhớ 'Nợ vào - Có ra' đối với tài sản. Tiền vào túi là Nợ, tiền ra khỏi túi là Có.",
                        "exercises": [
                            {"q": "Ghi Nợ tài khoản 111 (Tiền mặt) có nghĩa là gì?", "options": ["Tiền mặt tăng", "Tiền mặt giảm"], "correct": "Tiền mặt tăng"}
                        ]
                    }
                ]
            },
            "M2": {
                "name": "Module 2: Kế toán Tài chính thực chiến",
                "is_premium": False,
                "lessons": [
                    {
                        "id": "L2.1",
                        "title": "Kế toán Hàng tồn kho & Giá vốn",
                        "theory": "Hàng tồn kho được tính giá theo nhiều cách như FIFO (Nhập trước xuất trước). Cách tính này ảnh hưởng trực tiếp đến lợi nhuận.",
                        "visuals": [""],
                        "deep_dive": "💡 **Mở rộng:** Trong thời kỳ bão giá, phương pháp FIFO sẽ làm lợi nhuận trông cao hơn thực tế do dùng giá cũ thấp hơn.",
                        "exercises": [
                            {"q": "Phương pháp FIFO ưu tiên xuất kho lô hàng nào trước?", "options": ["Lô hàng mới nhất", "Lô hàng cũ nhất"], "correct": "Lô hàng cũ nhất"}
                        ]
                    }
                ]
            },
            "M4": {
                "name": "Module 4: Kế toán Thuế (Sống sót)",
                "is_premium": False,
                "lessons": [
                    {
                        "id": "L4.1",
                        "title": "Cơ chế Thuế GTGT Khấu trừ",
                        "theory": "Thuế GTGT là thuế gián thu. Doanh nghiệp đóng vai trò thu hộ nhà nước phần chênh lệch giữa đầu ra và đầu vào.",
                        "visuals": [""],
                        "deep_dive": "💡 **Lưu ý:** Hóa đơn trên 20 triệu bắt buộc phải chuyển khoản mới được khấu trừ thuế đầu vào.",
                        "exercises": [
                            {"q": "Hóa đơn mua vào 10tr, thuế GTGT 1tr. 1tr này gọi là gì?", "options": ["Thuế GTGT đầu vào", "Thuế GTGT đầu ra"], "correct": "Thuế GTGT đầu vào"}
                        ]
                    }
                ]
            }
        }
    },
    "PHASE_2": {
        "name": "📍 CHẶNG 2: NÂNG CẤP (PREMIUM)",
        "modules": {
            "M5": {
                "name": "Module 5: Kế toán Tập đoàn & Hợp nhất",
                "is_premium": True,
                "lessons": [
                    {
                        "id": "L5.1",
                        "title": "Hợp nhất Báo cáo tài chính",
                        "theory": "Kỹ thuật cộng hợp các báo cáo của công ty mẹ và con, loại trừ giao dịch nội bộ.",
                        "visuals": [""],
                        "deep_dive": "💡 **Mở rộng:** Đây là kỹ năng khó nhất và lương cao nhất trong nghề kế toán.",
                        "exercises": [
                            {"q": "Giao dịch bán hàng giữa mẹ và con có được tính vào doanh thu tập đoàn không?", "options": ["Có", "Không, phải loại trừ"], "correct": "Không, phải loại trừ"}
                        ]
                    }
                ]
            }
        }
    },
    "PHASE_3": {
        "name": "📍 CHẶNG 3: CÔNG NGHỆ & SỰ NGHIỆP",
        "modules": {
            "M8": {
                "name": "Module 8: AI & Phân tích dữ liệu",
                "is_premium": False,
                "lessons": [
                    {
                        "id": "L8.1",
                        "title": "Ứng dụng AI trong soát lỗi",
                        "theory": "Dùng AI để đọc hiểu hàng nghìn hóa đơn và phát hiện sai sót định khoản tự động.",
                        "visuals": [""],
                        "deep_dive": "💡 **Tương lai:** Kế toán không bị AI thay thế, nhưng kế toán không biết dùng AI sẽ bị đào thải.",
                        "exercises": [
                            {"q": "AI giúp ích gì nhất cho kế toán?", "options": ["Nhập liệu tay", "Phân tích và soát lỗi tự động"], "correct": "Phân tích và soát lỗi tự động"}
                        ]
                    }
                ]
            }
        }
    }
}
