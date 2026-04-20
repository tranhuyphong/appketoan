# ==========================================
# FILE DATA: GIÁO TRÌNH KẾ TOÁN THỰC CHIẾN (FINAL MASTER)
# ==========================================

SYSTEM_PROMPT = """
Bạn là Cô giáo Gen Z dạy Kế toán cực kỳ 'slay', thông minh và tâm lý. 
- Phong cách: Dùng từ lóng Gen Z (vô tri, xà lơ, keo lỳ...) và emoji 💅✨🤌.
- Chuyên môn: Chuẩn Thông tư 200, tập trung giải thích BẢN CHẤT, không lôi lý thuyết suông.
"""

LESSONS = {
    1: {
        "title": "📖 Chặng 1: Bản chất Nợ - Có",
        "theory": "Tài sản tăng ghi Nợ, giảm ghi Có. Nguồn vốn tăng ghi Có, giảm ghi Nợ. Đừng học thuộc, hãy nhớ: Cái gì vào túi là Nợ, cái gì ra khỏi túi là Có (đối với tài sản).",
        "quizzes": [
            {
                "question": "Rút tiền ngân hàng về nhập quỹ tiền mặt 50tr. Hạch toán sao?",
                "options": ["Nợ 111 / Có 112", "Nợ 112 / Có 111", "Nợ 111 / Có 131"],
                "correct_answer": "Nợ 111 / Có 112",
                "success_msg": "Chuẩn! Tiền mặt tăng (Nợ), Tiền bank giảm (Có). ✨",
                "error_msg": "Sai rồi má ơi! Tiền mặt tăng mà ghi Có là mất tiền đó! 🥲"
            }
        ]
    },
    2: {
        "title": "📖 Chặng 2: Hóa Đơn & Quy Tắc 20 Triệu",
        "theory": "Mọi hóa đơn từ 20 triệu trở lên (đã bao gồm VAT) BẮT BUỘC phải chuyển khoản. Dùng tiền mặt là Thuế gạch tên chi phí đó ngay!",
        "quizzes": [
            {
                "question": "Hóa đơn 19tr, VAT 1.9tr. Tổng 20.9tr. Trả tiền mặt được không?",
                "options": ["Được vì gốc dưới 20tr", "Không, vì tổng thanh toán trên 20tr"],
                "correct_answer": "Không, vì tổng thanh toán trên 20tr",
                "success_msg": "Rất tỉnh táo! Thuế tính trên tổng số tiền ghi trên hóa đơn nha. 💅",
                "error_msg": "Toang! Dính bẫy rồi. Tổng tiền có VAT mới là mốc để tính nha. 🤌"
            }
        ]
    },
    # ... (Các chặng 3-10 bạn có thể thêm nội dung tương tự dựa trên chuyên môn)
    11: {
        "title": "📖 Chặng 11: Công Nghệ & Phần Mềm (MISA/HTKK)",
        "theory": "Kế toán không chỉ là hạch toán, mà phải biết dùng HTKK để nộp tờ khai thuế .xml và dùng MISA để quản lý sổ sách tự động.",
        "quizzes": [
            {
                "question": "Để nộp tờ khai thuế qua mạng, em cần kết xuất file định dạng nào từ HTKK?",
                "options": [".pdf", ".xlsx", ".xml"],
                "correct_answer": ".xml",
                "success_msg": "Đúng rồi! File .xml mới là 'tiếng nói' chung với cơ quan thuế. 💻",
                "error_msg": "Sai nha, file Excel thuế không đọc được đâu em! ❌"
            }
        ]
    },
    12: {
        "title": "🏆 Chặng 12: Kỹ Năng Sinh Tồn & Chốt Sổ",
        "theory": "Khi Sếp yêu cầu làm sai, hãy dùng rủi ro pháp lý để thuyết phục. Khi Thuế kiểm tra, hãy bình tĩnh giải trình dựa trên chứng từ thực tế.",
        "quizzes": [
            {
                "question": "Sếp muốn trốn thuế bằng cách giấu doanh thu. Em xử lý sao?",
                "options": ["Làm theo sếp", "Phân tích rủi ro bị phạt gấp 3 lần và truy cứu hình sự cho sếp hiểu", "Nghỉ việc ngay lập tức"],
                "correct_answer": "Phân tích rủi ro bị phạt gấp 3 lần và truy cứu hình sự cho sếp hiểu",
                "success_msg": "Kế toán trưởng tương lai đây rồi! Phải biết bảo vệ sếp và chính mình. 🛡️",
                "error_msg": "Cẩn thận! Làm theo là đi tù, còn nghỉ việc ngay là bỏ cuộc sớm quá! 🤌"
            }
        ]
    }
}
