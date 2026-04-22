# Step 5 - Debt Switch (Chuyển Nợ)

## Chiến Lược Mặc Định

- Tính lãi nợ mặc định **tắt**.
- Chỉ hai tình huống cho phép bật:
  1. Người dùng yêu cầu bật một cách **rõ ràng**;
  2. Dự án đã bật tính năng theo dõi nợ rõ ràng.

## Lệnh Thực Thi

```bash
python "${SCRIPTS_DIR}/wordsmith.py" --project-root "${PROJECT_ROOT}" index accrue-interest --current-chapter {chapter_num}
```

## Yêu Cầu Sau Thực Thi

Trong đầu ra của Step 5, đánh dấu liệu tính lãi có được thực thi lần này hay không:

| Trường hợp | Ghi chú | Ví dụ |
|------------|---------|-------|
| **Thực thi** | Xuất tóm tắt: số nợ đã xử lý, lãi tích lũy, có xảy ra quá hạn không | "Xử lý: 3 nợ, lãi: +150, quá hạn: 0" |
| **Không thực thi** | Đánh dấu `debt_interest: skipped (default off)` | debt_interest: skipped |

## Pattern Vietnamese cho Scene Nợ

### Khi hiển thị nợ:
- Dùng **ngắn gọn**, câu dồn dập: "Nợ. 1000 mana. Hắn nợ ta."
- Tránh mô tả dài dòng khi đối thoại căng thẳng

### Khi tình huống căng thẳng:
- Câu ngắn, dồn dập: "Chết tiệt! Lãi kép à?"
- Dấu chấm than khi phẫn nộ: "Mẹ nó! Bao nhiêu lần rồi?"

### Khi kết thúc scene nợ:
- Cliffhanger pattern: Câu bỏ dở "... và rồi hắn ta xuất hiện."
- Không resolution hoàn toàn - tạo tension cho chương tiếp theo
