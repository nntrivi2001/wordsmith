# Step 1.5 - Contract (Hợp Đồng Chương)

## Mục Tiêu (Goal)

Converge `extract_chapter_context.py` context and guidance into an "executable contract," directly driving Step 2A.

## Cấu Trúc Đầu Ra Tối Thiểu (Scene-Sequel Minimum Closed Loop)

### Các Trường Bắt Buộc

- **Goal** (Mục tiêu - trong vòng 20 ký tự): Hành động chính của chương. Ví dụ: "Giành lại kiếm", "Tìm thấy Pandora"
- **Resistance** (Cản trở - trong vòng 20 ký tự): Lực cản chính. Ví dụ: "Đối thủ mạnh hơn", "Thiếu manh mối"
- **Cost** (Chi phí - trong vòng 20 ký tự): Cái phải trả. Ví dụ: "Mất máu", "Lộ bí mật"
- **This chapter's change** (Thay đổi chương này - trong vòng 30 ký tự): Ưu tiên định lượng được. Ví dụ: "+1 relationship", "+50 mana", "rank up"
- **Unclosed issue** (Vấn đề chưa đóng - trong vòng 30 ký tự): Để cho chương sau hoặc cuối chương giải quyết. Ví dụ: "Ai đứng sau?"
- **Core conflict in one sentence** (Xung đột cốt lõi trong một câu): Một câu, rõ ràng, không mơ hồ
- **Opening type** (Kiểu mở đầu): `conflict` / `suspense` / `action` / `dialogue` / `atmosphere` / `status-card`
- **Emotional rhythm** (Nhịp cảm xúc): `low→high` / `high→low` / `low→high→low` / `stable`
- **Information density** (Mật độ thông tin): `low` / `medium` / `high`
- **Is transition chapter** (Có phải chương chuyển tiếp): `true` / `false`, bắt buộc xác định bằng outline, không phải theo số từ
- **Continuation power design** (Thiết kế sức mạnh kết nối): Hook type/intensity, micro-delivery list, cool point pattern

### Quy tắc xác định chương chuyển tiếp (bắt buộc)
- Dựa trên chapter outline/volume outline's chapter function tags và goals (setup/transition/continuation/recovery, etc.).
- Nếu outline không đánh dấu rõ ràng, xác định bằng "liệu mục tiêu cốt lõi của chương này có chủ yếu là thúc đẩy xung đột chính không".
- Nghiêm cấm sử dụng ngưỡng số từ để xác định chương chuyển tiếp.

### Pattern Mở Đầu Vietnamese (Ưu Tiên)

| Loại | Mẫu | Nguồn |
|------|-----|-------|
| Mở bằng hành động | "Dội nắm đấm xuống sàn, Rosa lập tức rời khỏi bàn tròn." | BNsr Chương 4 |
| Mở bằng cảnh quan | "Chiều lăn tròn qua đám mây quện loang lổ..." | BNsr Chương 1 |
| Mở bằng đối thoại | '"Hẳn các vị ở đây vẫn còn khá ngỡ ngàng..."' | UH Chương 1 |
| Mở bằng suy nghĩ | "Rốt cuộc là chuyện quái gì đang diễn ra?" | UH Chương 1 |
| Mở bằng sự kiện | "Bão. Tuyết. Cái lạnh cắt da cắt thịt." | BNsr Chương 2, 3 |
| Mở bằng thẻ trạng thái | "Thẻ trạng thái!" | UH Chương 1 |

### Pattern Cliffhanger Kết Chương

| Kỹ thuật | Ví dụ | Nguồn |
|----------|-------|-------|
| Câu bỏ dở | "Bảy ngày…C" | BNsr Chương 1 |
| Twist bất ngờ | "Là nó. Thanatos." | BNsr Chương 1 |
| Hành động dở dang | "Nhưng khi Tanaka ngồi dậy..." | UH Chương 5 |
| Lời hứa hẹn | "—0o0—" rồi hết chương | UH |

## Kiểm Tra Phân Biệt (Differentiation Check)

- Hook type ưu tiên tránh lặp lại với 3 chương trước.
- Opening type ưu tiên tránh lặp lại với 3 chương trước.
- Cool point pattern ưu tiên tránh lặp lại với 5 chương trước.

Nếu cần lặp lại, bắt buộc ghi lại Override reason, và thay đổi ít nhất một trong:
- **Object** (Đối tượng)
- **Cost** (Chi phí)
- **Result** (Kết quả)

## Genre Quick Call (Gọi Nhanh Theo Thể Loại - chỉ khi khớp)

Matched genre: `esports` / `livestream` / `cosmic-horror`

Thực hiện:
1. Chọn 1 expectation anchor từ `writing/genre-hook-payoff-library.md` (ưu tiên cuối chương, cũng có thể là đoạn sau).
2. Chọn 1-2 micro-deliveries, ưu tiên cùng hướng với xung đột cốt lõi của chương này.

## Reading Priority (Ưu Tiên Đọc)

1. **Bắt buộc:** `writing_guidance.guidance_items`
2. **Có điều kiện:** `rag_assist` (`invoked=true` and `hits` not empty)
3. **Tùy chọn:** `reader_signal`, `genre_profile.reference_hints`
