# Step 3 - Review Gate (Cổng Đánh Giá)

## Call Constraints (Hard Rules) - Ràng Buộc Gọi (Quy Tắc Cứng)

- Phải sử dụng `Task` để gọi review subagent, nghiêm cấm main flow trực tiếp inlining "self-review conclusions."
- Review tasks có thể được khởi chạy song song, phải tổng hợp sau khi tất cả trả về.
- `overall_score` phải từ kết quả tổng hợp, không thể chấm điểm chủ quan.
- Trong kịch bản viết một chương duy nhất, truyền đồng nhất: `{chapter, chapter_file, project_root}`.

## Review Routing Mode

| Mode | Mô tả | Khi nào dùng |
|------|-------|--------------|
| `standard` / `--fast` | `auto` routing (core 3 + conditional hits) | Default |
| `--minimal` | Core 3 cố định (không có conditional reviewers) | Review nhanh, không cần full check |

### Core Reviewers (Luôn thực thi)

- `consistency-checker` - Kiểm tra logic nhất quán
- `continuity-checker` - Kiểm tra liên tục chuỗi sự kiện
- `ooc-checker` - Kiểm tra giọng văn nhất quán

### Conditional Reviewers (Chỉ thực thi khi `auto` hit)

- `reader-pull-checker` - Kiểm tra sức hút đọc tiếp
- `high-point-checker` - Kiểm tra điểm cao trào
- `pacing-checker` - Kiểm tra nhịp điệu

## Auto Routing Decision Signals - Tín Hiệu Quyết Định Auto Routing

Nguồn tín hiệu đầu vào:
1. Step 1.5 contract (có phải chương chuyển tiếp, continuation power design, core conflict).
2. Body của chương này (battle/reversal/highlight/chapter end unclosed issue, etc. signals).
3. Outline tags (key chapter/climax chapter/volume end chapter/transition chapter).
4. Recent chapter rhythm (consecutive main line, emotional line break, worldview line break).

Routing rules:
- `reader-pull-checker`: Bật khi có bất kỳ điều kiện nào
  - Non-transition chapter;
  - Có unclosed issue/expectation anchor rõ ràng;
  - Người dùng yêu cầu rõ ràng "continuation power review."
- `high-point-checker`: Bật khi có bất kỳ điều kiện nào
  - Key chapter/climax chapter/volume end chapter;
  - Body có battle, counterkill, face-slap, identity reveal, big reversal, etc. highlight signals.
- `pacing-checker`: Bật khi có bất kỳ điều kiện nào
  - Chapter number >= 10;
  - Recent chapters có obvious rhythm imbalance risk;
  - Người dùng yêu cầu rõ ràng "rhythm review."

## Task Call Template (Example) - Template Gọi Task (Ví Dụ)

```text
selected = ["consistency-checker", "continuity-checker", "ooc-checker"]

if mode != "minimal":
  if trigger_reader_pull: selected.append("reader-pull-checker")
  if trigger_high_point: selected.append("high-point-checker")
  if trigger_pacing: selected.append("pacing-checker")

parallel Task(agent, {chapter, chapter_file, project_root}) for agent in selected
```

## Output Contract (Unified) - Hợp Đồng Đầu Ra (Thống Nhất)

Mỗi giá trị trả về của checker phải tuân theo `${CLAUDE_PLUGIN_ROOT}/references/checker-output-schema.md`:
- **Bắt buộc:** `agent`, `chapter`, `overall_score`, `pass`, `issues`, `metrics`, `summary`
- **Cho phép mở rộng:** (ví dụ: `hard_violations`, `soft_suggestions`), nhưng không thể thay thế các trường bắt buộc

Đầu ra tổng hợp tối thiểu:
- `chapter` (single chapter)
- `start_chapter`, `end_chapter` (bằng nhau khi single chapter)
- `selected_checkers`
- `overall_score`
- `severity_counts`
- `critical_issues`
- `issues` (flattened aggregation)
- `dimension_scores` (tính bằng enabled checkers)

## Aggregated Output Template - Template Đầu Ra Tổng Hợp

```text
Review Summary - Chapter {chapter_num}
- Enabled reviewers: {list}
- Critical issues: {N}
- High priority issues: {N}
- Overall score: {score}
- Can enter polishing: {Yes/No}
```

## Review Metrics Storage (Required) - Lưu Review Metrics (Bắt Buộc)

```bash
python -X utf8 "${SCRIPTS_DIR}/wordsmith.py" --project-root "${PROJECT_ROOT}" index save-review-metrics --data "@${PROJECT_ROOT}/.wordsmith/tmp/review_metrics.json"
```

review_metrics file field constraints (current workflow convention only passes following fields):
- `start_chapter` (int), `end_chapter` (int): bằng nhau khi single chapter
- `overall_score` (float): bắt buộc
- `dimension_scores` (Dict[str, float]): tính bằng enabled checkers
- `severity_counts` (Dict[str, int]): keys là critical / high / medium / low
- `critical_issues` (List[str])
- `report_file` (str)
- `notes` (str): trong contract thực thi hiện tại phải là single string; thông tin mở rộng như `selected_checkers`, `timeline_gate`, `anti_ai_force_check` etc. nén đồng nhất thành single-line text vào trường này, không thể truyền như top-level keys độc lập
- Workflow hiện tại không truyền top-level fields khác; script side không làm hard validation mới ở đây

## Pre-Step 4 Gateway - Cổng Trước Step 4

- `overall_score` đã được tạo.
- `save-review-metrics` đã thành công.
- `issues`, `severity_counts` từ review report có thể được sử dụng trực tiếp bởi Step 4.
- **Timeline gate (mới):** Nếu `TIMELINE_ISSUE` tồn tại với `severity >= high`, nghiêm cấm vào Step 4/5, phải sửa trước.

### Timeline Gate Rules - Quy Tắc Timeline Gate

**Hard Block (phải sửa để tiếp tục):**
- `TIMELINE_ISSUE` + `severity = critical` (countdown arithmetic error)
- `TIMELINE_ISSUE` + `severity = high` (event sequence contradiction/age conflict/time rollback/large span without transition)

**Soft Warning (nên sửa nhưng có thể tiếp tục):**
- `TIMELINE_ISSUE` + `severity = medium` (missing time anchor)
- `TIMELINE_ISSUE` + `severity = low` (slight time ambiguity)

**Gate decision logic:**
```text
timeline_issues = filter(issues, type="TIMELINE_ISSUE")
critical_timeline = filter(timeline_issues, severity in ["critical", "high"])

if len(critical_timeline) > 0:
    BLOCK: "Có {len(critical_timeline)} vấn đề timeline nghiêm trọng, phải sửa trước khi vào polishing step"
    for issue in critical_timeline:
        print(f"- Chapter {issue.chapter}: {issue.description}")
    return BLOCKED
else:
    Pass: "Timeline check passed"
```

**Fix guide - Hướng dẫn sửa:**
- Countdown error → sửa countdown progression, đảm bảo D-N → D-(N-1) continuity
- Time rollback → thêm flashback marker, hoặc điều chỉnh time anchor
- Large span without transition → thêm time transition sentence/paragraph, hoặc chèn transition chapter
- Event sequence contradiction → điều chỉnh event sequence hoặc thêm time jump explanation
