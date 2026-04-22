# Vietnamese Writing Patterns - Outline Structure

> Sử dụng các pattern từ STYLE_GUIDE_VN.md để định hướng cấu trúc dàn Ý phù hợp với webnovel tiếng Việt.

## Vietnamese Pattern Considerations

### Cấu Trúc Câu Trong Dàn Ý
- **Hành động chiến đấu**: Câu ngắn, dồn dập → phù hợp cho điểm cool cao trào
- **Mô tả nội tâm**: Câu dài, nhiều mệnh đề → phù hợp cho dàn Ý tập phát triển cảm xúc
- **Đối thoại căng thẳng**: Câu ngắn, cắt ngang nhau → phù hợp cho móc kết chương

### Đại Từ Xưng Hô Trong Thiết Kế Nhân Vật
| Tình huống | Sử dụng | Ví dụ |
|------------|---------|-------|
| Bạn bè thân | tao/mày | *"Tao cá là mày chưa từng..."* |
| Kẻ thù/đối thủ | thằng khốn, con nhóc | *"Hắn ta dám..."* |
| Quý tộc/cổ đại | ta, ngài | *"Ta là Vincent..."* |
| Nhân vật chính vs phản diện | Đối lập rõ ràng | Dùng ngôn ngữ đời thường cho protagonist |

### Nhịp Điệu Cho Dàn Ý Từng Tầng
- **Dàn Ý xương sống**: 30% nội dung → thiết lập worldview, main conflict
- **Dàn Ý tập**: 50% nội dung → xen kẽ cao trào (cấp B-A) và chuyển tiếp (cấp C)
- **Dàn Ý chương**: 20% nội dung → mỗi chương có ít nhất 1 điểm cool nhỏ

### Pattern Đặc Biệt Cho Dàn Ý Webnovel VN
- **Mở bằng hành động**: "Jack xông ra!" thay vì mô tả dài
- **Kết thúc bằng cliffhanger**: "Bảy ngày…" để tạo hứng thú đọc tiếp
- **Chuyển cảnh bằng *** hoặc —0o0—**: Phân tách các phân cảnh lớn
- **Show don't tell**: Thiết kế dàn Ý thể hiện qua hành động, không chỉ kể

---

# Cấu Trúc Dàn Ý - Hướng Dẫn Thiết Kế Dàn Ý

> **Ghi chú lưu trữ**: File này là tài liệu tham khảo phương pháp lịch sử và không được tự động nạp trong workflow chính `/webnovel-plan`.
> Để tích hợp, trước tiên cần thêm điều kiện kích hoạt bước rõ ràng và hướng dẫn đọc trong `SKILL.md`.

> **Nguyên tắc cốt lõi**: Dàn Ý là bản đồ, không phải xiềng xích. Một dàn Ý tốt có thể chỉ hướng, nhưng cũng để lại không gian cho cảm hứng.

---

## 1. Kiến Trúc Ba Tầng Của Dàn Ý

### Tầng Thứ Nhất: Dàn Ý Xương Sống (Bắt Buộc, 30%)
**Mục đích**: Đảm bảo câu chuyện có khởi đầu, phát triển, cao trào và kết thúc rõ ràng.

```markdown
## Dàn Ý Xương Sống Ví Dụ
**Mở đầu (Chương 1-50)**: Thanh niên trash Lin Tian bị bỏ rơi, có được hệ thống nuốt tươi qua cơ duyên
**Đầu (Chương 51-200)**: Vươn lên trong môn phái, vả mặt kẻ cười nhạo, phát hiện em gái bị bắt cóc
**Giữa (Chương 201-500)**: Phiêu lưu qua thế giới tu luyện để cứu em, điều hướng các thế lực, sức mạnh tăng nhanh
**Cuối (Chương 501-800)**: Khám phá bí ẩn thân phận, phát hiện thực ra là đại nhân vật cổ đại tái sinh, đối đầu cuối cùng với Chưởng môn Tà Thần Giáo
**Kết thúc (Chương 801-850)**: Đánh bại Tà Thần, cứu em gái, thăng cấp tiên giới (mở giao diện sequel)
```

**Tiêu chuẩn kiểm tra Dàn Ý Xương Sống**:
- [ ] **Điểm khởi đầu rõ ràng**: Trạng thái ban đầu và mâu thuẫn cốt lõi của nhân vật chính là gì?
- [ ] **Điểm ngoặt**: ít nhất 3 cao trào cốt truyện lớn (ví dụ: có được năng lực cheat, gia nhập môn phái, sư phụ chết)
- [ ] **Điểm kết thúc rõ ràng**: Mục tiêu cuối cùng của câu chuyện (đánh bại quỷ vương/thăng cấp/trở thành bá chủ)

---

### Tầng Thứ Hai: Dàn Ý Tập (Khuyến khích, 50%)
**Mục đích**: Chia nhỏ truyện dài thành nhiều cao trào nhỏ để tránh reader mệt mỏi.

#### Nguyên tắc Tập
- **Mỗi tập có một mục tiêu nhỏ**: Ví dụ, Tập 1 "phát triển ở làng新手", Tập 2 "thử thách môn phái"
- **Kết tập phải có cao trào**: Đánh bại BOSS nhỏ, có được vũ khí thần, đột phá cảnh giới
- **Chuyển tiếp giữa các tập**: Không thể đột ngột chuyển bản đồ, phải có dấu hiệu trước

#### Mẫu Dàn Ý Tập
```markdown
## Tập Một: Con Đường Vươn Lên (Chương 1-150)
**Mục tiêu cốt lõi**: Từ trash đến đảo ngược thiên tài
**Xung đột chính**: Xung đột nội bộ gia đình, hủy hợp đồng, chọn môn phái
**Cao trào**: Vô địch cuộc thi môn phái, vả mặt Ye Liangchen
**Dấu hiệu**: Nhắc nhở nhân vật chính có xuất thân bất thường, trồng manh mối cho "huyết thống cổ đại" sau này

## Tập Hai: Môn Phái Đại Loạn (Chương 151-300)
**Mục tiêu cốt lõi**: Chiếm chỗ đứng trong Thiên Kiếm Môn
**Xung đột chính**: Ngoại trừ đệ tử nội môn, đấu tranh phe phái của các trưởng lão, bảo vật bí cảnh
**Cao trào**: Có được di sản kiếm phần trong bí cảnh, sức mạnh tăng vọt
**Dấu hiệu**: Phát hiện manh mối em gái bị Tà Thần Giáo bắt cóc

## Tập Ba: Hành Trình Cứu Em Gái (Chương 301-500)
**Mục tiêu cốt lõi**: Truy đuổi Tà Thần Giáo, cứu em gái
**Xung đột chính**: Nhiều lần đối đầu Tà Thần Giáo, hiểu lầm giữa chính đạo và tà đạo, lo lắng về sức mạnh chưa đủ
**Cao trào**: Một mình xông vào đại bản doanh Tà Thần Giáo, lần đầu đối đầu chưởng môn (thua nhưng sống sót)
**Dấu hiệu**: Biết em gái có thể chất đặc biệt, là chìa khóa cho sự hồi sinh của Tà Thần
```

---

### Tầng Thứ Ba: Dàn Ý Chương (Tùy chọn, 20%)
**Mục đích**: Chi tiết đến nội dung cụ thể từng chương, phù hợp cho người mới bắt đầu hoặc khi bí.

#### Mẫu Dàn Ý Chương
```markdown
## Chương 1: Nhục Nhã Hủy Hợp Đồng
**Số từ**: 3000
**Cốt truyện chính**:
  - Tiểu gia chủ Ye Liangchen đến hủy hợp đồng
  - Lin Tian nhục nhã, cả gia đình mang tiếng
  - Lin Tian tức giận nhưng bất lực (thể hiện trạng thái trash)
**Cốt truyện phụ**:
  - Cha thở dài, em gái an ủi
  - Dấu hiệu: Ngọc bích của Lin Tian hơi phát sáng
**Điểm cool**: Không có (chương kìm nén, tạo đà cho vả mặt sau)
**Móc kết chương**: "Ngay lúc đó, một giọng nói máy móc đột nhiên vang lên trong tâm trí Lin Tian: 'Hệ Thống Nuốt Tươi Đang Kích Hoạt...'"
```

**Tính linh hoạt của dàn ý chương**:
- Chỉ cần viết nội dung cốt lõi, đối thoại cụ thể và chi tiết được triển khai trong quá trình viết
- Nếu cảm hứng đến, có thể deviated khỏi dàn ý (nhưng nhớ quay lại sửa dàn ý)

---

## 2. Lựa Chọn Mức Độ Chi Tiết Dàn Ý

### Dàn Ý Sơ Lược (Phù Hợp Với Người Có Kinh Nghiệm)
- **Nội dung**: Chỉ dàn Ý xương sống + dàn Ý tập
- **Ưu điểm**: Tự do viết cao, có thể điều chỉnh bất kỳ lúc nào
- **Nhược điểm**: Dễ deviated hoặc bí

### Dàn Ý Chi Tiết (Phù Hợp Với Người Mới)
- **Nội dung**: Dàn Ý xương sống + tập + chương (ít nhất 50 chương đầu)
- **Ưu điểm**: Không bị bí khi viết, biết cần viết gì mỗi ngày
- **Nhược điểm**: Thời gian chuẩn bị dài

### Dàn Ý Kết Hợp (Khuyến khích)
- **Nội dung**: Dàn Ý xương sống (toàn bộ sách) + dàn Ý tập (toàn bộ sách) + dàn Ý chương (10-20 chương tiếp theo)
- **Ưu điểm**: Vừa có định hướng vừa linh hoạt
- **Phương pháp**: Sau khi hoàn thành một tập, bổ sung dàn Ý chương của tập tiếp theo

---

## 3. Điều Chỉnh Dàn Ý Động

### Khi Nào Điều Chỉnh Dàn Ý?
1. **Phản hồi từ độc giả**: Nếu một nhân vật/cốt truyện đặc biệt phổ biến, có thể tăng thời gian lên sàn của họ
2. **Cảm hứng đến**: Đột nhiên nghĩ ra hướng cốt truyện tốt hơn
3. **Dữ liệu bất thường**: Lượt đăng ký/tổng hợp giảm mạnh ở một chương, cho thấy vấn đề cốt truyện

### Cách Điều Chỉnh Dàn Ý
```markdown
## Nhật Ký Thay Đổi Dàn Ý
**Ngày**: 2025-01-03
**Nội dung thay đổi**: Ban đầu dự định cho em gái chết ở Tập 2 (dao), nhưng phản hồi độc giả nói em gái quá phổ biến
**Kế hoạch mới**: Đổi thành "bị mang đi", hoãn đến Tập 3 để tiết lộ sống chết (kéo dài suspense)
**Phạm vi ảnh hưởng**: Cao trào Tập 2 cần thiết kế lại, đổi thành "Có Được Di Sản Kiếm Phần"
```

### Vạch Đỏ Cho Điều Chỉnh Dàn Ý (Không Thể Vượt Qua)
- **Nhân vật chính**: Không thể đột ngột thay đổi từ tốt sang xấu (hoặc ngược lại) trừ khi đã có dấu hiệu đầy đủ
- **Hệ thống sức mạnh**: Không thể ngẫu nhiên sửa đổi cài đặt cảnh giới, nếu không tất cả các so sánh sức mạnh chiến đấu trước đó sụp đổ
- **Cốt truyện chính cốt lõi**: Có thể điều chỉnh cốt truyện phụ, nhưng mục tiêu cốt lõi như "cứu em gái" không thể dễ dàng từ bỏ

---

## 4. Công Cụ Dàn Ý Được Khuyến Khích

### Công Cụ A: Markdown + Git
```
Dàn Ý/
├── Dàn Ý Xương Sống.md
├── Dàn Ý Các Tập/
│   ├── Tập Một.md
│   ├── Tập Hai.md
│   └── Tập Ba.md
├── Dàn Ý Chương/
│   ├── Chương 001-050.md
│   └── Chương 051-100.md
└── Nhật Ký Thay Đổi Dàn Ý.md
```
**Ưu điểm**: Văn bản thuần túy, dễ kiểm soát phiên bản và tìm kiếm

### Công Cụ B: Bản Đồ Tư Duy (XMind/MindNode)
```
Đường chính: Cứu em gái
├── Tập 1: Làng新手 phát triển
│   ├── Chương 1-10: Sự cố hủy hợp đồng
│   ├── Chương 11-30: Có được hệ thống
│   └── Chương 31-50: Chọn môn phái
├── Tập 2: Môn phái đại loạn
│   └── ...
```
**Ưu điểm**: Trực quan mạnh, quan hệ phân cấp rõ ràng

### Công Cụ C: Bảng tính (Excel/Notion)
| Chương | Cốt Truyện Chính | Cốt Truyện Phụ | Điểm Cool | Dấu hiệu | Số Từ |
|--------|------------------|----------------|-----------|----------|--------|
| 1 | Hủy hợp đồng | Em gái an ủi | Không có | Ngọc bích phát sáng | 3000 |
| 2 | Kích hoạt hệ thống | Test năng lực | Nuốt thú | Hệ thống có chức năng ẩn | 3000 |
**Ưu điểm**: Phù hợp cho quản lý dữ liệu, thuận tiện cho thống kê mật độ điểm cool

---

## 5. Liên Kết Dàn Ý và Cài Đặt

Dàn Ý không cô lập; phải kết hợp với cài đặt:

### Tiêu Chí Kiểm Tra
- [ ] **Thẻ nhân vật**: Trước khi mỗi nhân vật quan trọng xuất hiện, thẻ nhân vật của họ đã được thiết lập trong cài đặt chưa?
- [ ] **Quan hệ phe phái**: Khi xung đột phe phái liên quan, chúng có tuân thủ mạng lưới quan hệ phe phái trong cài đặt không?
- [ ] **Hệ thống sức mạnh**: Tiến trình cảnh giới của nhân vật chính có theo nhịp đã đặt trong cài đặt hệ thống sức mạnh không?
- [ ] **Dòng thời gian**: Khoảng thời gian của mỗi tập có hợp lý không? (Không đột ngột nhảy mười năm)

### Ví Dụ: Xung Đột Dàn Ý và Cài Đặt
```markdown
## Vấn Đề
Dàn Ý: Nhân vật chính đột phá đến Kim Đan ở Chương 50
Cài đặt: Nhân vật chính 16 tuổi, tốc độ tu luyện bình thường là 20 năm đến Kim Đan
Xung đột: Dòng thời gian không hợp lý

## Giải Pháp
Phương án A: Điều chỉnh dàn Ý, đổi thành Trúc Cơ
Phương án B: Thêm vào cài đặt "Hệ Thống Nuốt Tươi có thể tăng tốc tu luyện 100x"
Phương án C: Thêm cốt truyện cơ duyên (ăn quả tinh thể ngàn năm)
```

---

## 🛠️ Tiêu Chí Kiểm Tra Dàn Ý

Trước khi bắt đầu viết, sử dụng tiêu chí này để xác minh dàn Ý đạt chuẩn:
- [ ] **Tính đầy đủ**: Có điểm khởi đầu, giữa và kết thúc không?
- [ ] **Nhịp điệu**: Có sự xen kẽ rõ ràng của cao trào và điểm thấp không? (Không thể toàn cao trào hoặc toàn bằng phẳng)
- [ ] **Tính logic**: Tiến trình cốt truyện có hợp lý không? (Không thể dựa vào nhân vật đột ngột trở nên ngu)
- [ ] **Điểm cool**: Có ít nhất 1 điểm cool mỗi 10-20 chương không?
- [ ] **Dấu hiệu**: Những lỗ hổng đào sẽ có kế hoạch lấp đầy không? (Đánh dấu ở chương nào để lấp)
- [ ] **Số từ**: Ước tính tổng số từ có phù hợp với nền tảng không? (Qidian ít nhất 1 triệu từ)

---

## Phụ Lục: Phân Tích Trường Hợp Dàn Ý Cổ Điển

### Trường Hợp 1: Đặc Điểm Dàn Ý《Lữ Bị Cầu Tiên》 
- **Xương sống**: Thanh niên phàm tu luyện → Trở thành đại nhân vật tiên giới (đường rất dài, 8 triệu từ)
- **Tập**: Chia theo "bản đồ" (phàm giới → tinh giới → tiên giới), mỗi bản đồ reset sức mạnh về zero
- **Nhịp điệu**: Mỗi cảnh giới nhỏ có cao trào nhỏ độc lập riêng (có được bảo vật/đánh bại kẻ thù)

### Trường Hợp 2: Đặc Điểm Dàn Ý《Đấu Phá Thương Khung》
- **Xương sống**: Thiên tài tu yếu → Vươn lên trả thù → Trở thành Đấu Hoàng
- **Tập**: Chia theo "cấp độ sức mạnh" (Tu Sĩ → Đấu Vương → Đấu Thánh), mỗi cảnh giới lớn một tập
- **Nhịp điệu**: "Ba năm ước hẹn" này loại nút thời gian rõ ràng, tạo cảm giác cấp bách

---

## Ghi Chú Bổ Sung

### Về Việc Viết Dàn Ý Linh Hoạt
- Dàn Ý phục vụ câu chuyện, không phải ngược lại
- Để dành không gian cho đột phá sáng tạo trong quá trình viết thực tế
- Cập nhật dàn Ý khi cảm hứng đến, nhưng ghi lại các thay đổi

### Về Việc Duy Trì Tính Nhất Quán
- Đối chiếu chéo với tài liệu Cài Đặt thường xuyên
- Theo dõi cập nhật dòng thời gian
- Ghi lại mọi retcons cần thiết

---

## Vietnamese Writing Patterns Section

### Rhythms and Pacing (Nhịp Điệu)

**Fast-paced (Hành động chiến đấu):**
```
Câu ngắn, dồn dập, động từ mạnh
Không có nhiều mệnh đề phụ
Xen kẽ sound effects
```

**Slow-paced (Cảm xúc, nội tâm):**
```
Câu dài, descriptive hơn
Sử dụng ẩn dụ, so sánh
Nhiều chi tiết giác quan
```

**Pattern:**
- Mở đầu chương: Câu dài, descriptive để dựng cảnh
- Chiến đấu: Câu cực ngắn, động từ mạnh
- Căng thẳng cao trào: Xen kẽ ngắn-dài-ngắn
- Kết chương cliffhanger: Thường 1-2 câu ngắn, bỏ dở

---

### Punctuation (Dấu Câu)

**Dấu ba chấm (...):**
- Suy nghĩ kéo dài: "Cô ấy đang nghĩ... về những ký ức..."
- Chần chừ: "Ờ... để tớ nghĩ lại..."
- Cliffhanger: "Bảy ngày…"
- Ngắt quãng: "Không... không phải tôi..."

**Dấu gạch ngang (—):**
- Đối thoại: "—Cô ấy đi rồi."
- Inner thoughts: "—Mình sẽ không chết đâu."
- Giải thích bổ sung: "Anh ta — kẻ phản bội — đã chết."

**Dấu chấm than (!):**
- Shouting: "JACKKKK!!!!"
- Cảm xúc mạnh: "Cái mẹ gì thế này!?"

---

### Show-Don't-Tell Patterns

**Thay vì nói:** "Cô ấy rất giận."

**Hãy viết:** "Rosa nghiến răng, nắm chặt tay lại đến trắng bóc. Mắt cô nổ đom đóm."

**Trigger words cho emotion:**

| Cảm xúc | Biểu hiện |
|---------|-----------|
| Giận | nghiến răng, nổ gân, mặt đỏ, hét lên |
| Sợ | run bần bật, mặt tái mét, đứng không vững |
| Buồn | nước mắt, cười méo, thở dài |
| Vui | cười phá lên, mỉm cười, nhảy lên |
| Bất ngờ | tròn mắt, há hốc, giật mình |

---

### Vocabulary & Pronouns (Từ Vựng & Đại Từ Xưng Hô)

| Từ | Giới | Ngữ cảnh sử dụng |
|----|------|------------------|
| **hắn** | Thứ ba nam | Hành động/khích đối thủ |
| **tao** | Ngang hàng/bạn bè | Tính cách mạnh mẽ, tự tin |
| **mày** | Ngang hàng/bạn bè | Đối đáp thân thiết |
| **tụi mày** | Đám đông | Gọi nhiều người |
| **ta** | Cổ đại/nghi thức | Nhân vật quý tộc, phép lịch sự |
| **ngài** | Kính ngữ | Xưng hô với người có quyền |
| **tôi** | Lịch sự | Ngữ cảnh nghiêm túc, xã giao |

**Pattern quan trọng:**
- Đại từ xưng hô thay đổi theo cảm xúc: Bình thường dùng "mày/mày", khi giận dữ chuyển sang "thằng khốn", "con nhóc"
- Đối thủ/hậu nhân thường bị gọi là "thằng nào", "con khốn" khi căng thẳng

---

### Scene Transitions (Chuyển Cảnh)

| Phương pháp | Mô tả |
|-------------|-------|
| `***` | Giữa các phân cảnh lớn |
| —0o0— | Phân cách cảnh nhỏ |
| Thay đổi thời gian | "Sáu năm trước..." |
| Thay đổi địa điểm | "Ở trong khu rừng..." |

**Pattern:**
- Chuyển cảnh quan trọng: "***" hoặc dòng trắng
- Chuyển thời gian: Ghi rõ "Sáu năm trước", "Buổi sáng hôm đó"
- Chuyển视角: Thường kèm "***" và tên nhân vật mới

---

### Chapter Cliffhanger Patterns

| Kỹ thuật | Mô tả |
|----------|-------|
| Câu bỏ dở | "Bảy ngày…" |
| Twist bất ngờ | "Là nó. Thanatos." |
| Hành động dở dang | "Nhưng khi Tanaka ngồi dậy..." |
| Lời hứa hẹn | "—0o0—" rồi hết chương |

**Pattern quan trọng:**
- Kết chương thường là điểm cao trào hoặc ngay trước cao trào
- Không có full resolution - tạo tension
- Để lại câu hỏi trong đầu người đọc

---

*Nguồn: STYLE_GUIDE_VN.md - Hướng dẫn Phong cách Viết Webnovel Tiếng Việt*
