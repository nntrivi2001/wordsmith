# Checker Unified Output Schema

All review Agents should follow this unified output format for automated aggregation and trend analysis.

Notes:
- Single-chapter writing scenarios use the `chapter` field by default.
- For range statistics compatibility, `start_chapter/end_chapter` can be added at the aggregation layer; individual checkers are not required to include them.
- Extension fields are allowed, but the required fields defined in this document must not be deleted or replaced.

## Standard JSON Schema

```json
{
  "agent": "checker-name",
  "chapter": 100,
  "overall_score": 85,
  "pass": true,
  "issues": [
    {
      "id": "ISSUE_001",
      "type": "issue type",
      "severity": "critical|high|medium|low",
      "location": "location description",
      "description": "issue description",
      "suggestion": "fix suggestion",
      "can_override": false
    }
  ],
  "metrics": {},
  "summary": "brief summary"
}
```

## Field Descriptions

| Field | Type | Required | Description |
|------|------|------|------|
| `agent` | string | ✅ | Agent name |
| `chapter` | int | ✅ | Chapter number |
| `overall_score` | int | ✅ | Total score (0-100) |
| `pass` | bool | ✅ | Whether it passes |
| `issues` | array | ✅ | List of issues |
| `metrics` | object | ✅ | Agent-specific metrics |
| `summary` | string | ✅ | Brief summary |

Extension field conventions (optional):
- Checker-private fields (e.g., `hard_violations`, `soft_suggestions`, `override_eligible`) may be appended.
- Private fields are for enhanced interpretation; they do not replace `issues`.

## Issue Severity Definitions

| severity | Meaning | Handling |
|----------|------|------|
| `critical` | Critical issue, must be fixed | Must be fixed in the polish step |
| `high` | High-priority issue | Fix with priority |
| `medium` | Moderate issue | Recommended to fix |
| `low` | Minor issue | Optional to fix |

## Checker-Specific Metrics

### reader-pull-checker
```json
{
  "metrics": {
    "hook_present": true,
    "hook_type": "crisis hook",
    "hook_strength": "strong",
    "prev_hook_fulfilled": true,
    "micropayoff_count": 2,
    "micropayoffs": ["ability payoff", "recognition payoff"],
    "is_transition": false,
    "debt_balance": 0.0
  }
}
```

### high-point-checker
```json
{
  "metrics": {
    "cool_point_count": 2,
    "cool_point_types": ["flex counter", "overlevel counter-kill"],
    "density_score": 8,
    "type_diversity": 0.8,
    "milestone_present": false
  }
}
```

### consistency-checker
```json
{
  "metrics": {
    "power_violations": 0,
    "location_errors": 1,
    "timeline_issues": 0,
    "entity_conflicts": 0
  }
}
```

### ooc-checker
```json
{
  "metrics": {
    "severe_ooc": 0,
    "moderate_ooc": 1,
    "minor_ooc": 2,
    "speech_violations": 0,
    "character_development_valid": true
  }
}
```

### continuity-checker
```json
{
  "metrics": {
    "transition_grade": "B",
    "active_threads": 3,
    "dormant_threads": 1,
    "forgotten_foreshadowing": 0,
    "logic_holes": 0,
    "outline_deviations": 0
  }
}
```

### pacing-checker
```json
{
  "metrics": {
    "dominant_strand": "quest",
    "quest_ratio": 0.6,
    "fire_ratio": 0.25,
    "constellation_ratio": 0.15,
    "consecutive_quest": 3,
    "fire_gap": 4,
    "constellation_gap": 8,
    "fatigue_risk": "low"
  }
}
```

## Summary Format

After Step 3 completes, output the summary JSON:

```json
{
  "chapter": 100,
  "checkers": {
    "reader-pull-checker": {"score": 85, "pass": true, "critical": 0, "high": 1},
    "high-point-checker": {"score": 80, "pass": true, "critical": 0, "high": 0},
    "consistency-checker": {"score": 90, "pass": true, "critical": 0, "high": 0},
    "ooc-checker": {"score": 75, "pass": true, "critical": 0, "high": 1},
    "continuity-checker": {"score": 85, "pass": true, "critical": 0, "high": 0},
    "pacing-checker": {"score": 80, "pass": true, "critical": 0, "high": 0}
  },
  "overall": {
    "score": 82.5,
    "pass": true,
    "critical_total": 0,
    "high_total": 2,
    "can_proceed": true
  }
}
```

## Vietnamese Webnovel Style Supplement

Based on STYLE_GUIDE_VN.md patterns for consistency checking:

### Vietnamese Pronoun Consistency

| Emotion Level | Pronouns Used | Example |
|---------------|---------------|---------|
| Calm/Friendly | mày, tao, tụi mày | *"Tao cá là mày chưa từng..."* |
| Angry/Hostile | thằng khốn, con nhóc, chết mẹ mày | *"Thằng chó đó mà dám..."* |
| Formal | ngài, tôi, ông, bà | *"Ngài có thể giúp tôi..."* |

**OOC Violation Pattern:** Character suddenly shifts formality without emotional trigger.

### Sentence Structure Patterns

| Scene Type | Pattern | Example |
|-----------|---------|---------|
| Action | Short punchy, minimal commas | *"Jack xông ra!"* |
| Emotional | Long descriptive, multiple clauses | *"Lâu đài Chyrse một buổi chiều lặng tuyết buồn tẻ..."* |
| Combat (UH style) | Status check → decision → action | See UH Chương 4 |

### Show-Don't-Tell Emotion Markers

**Consistency check:** Verify emotion expressions match Vietnamese patterns:

| Emotion | Correct (Show) | Incorrect (Tell) |
|---------|----------------|------------------|
| Giận | nghiến răng, nổ gân, mắt đỏ | *"Cô ấy rất giận."* |
| Sợ | run bần bật, mặt tái mét | *"Cô ấy rất sợ."* |
| Buồn | nước mắt lã chã, cười méo | *"Cô ấy buồn."* |
| Bất ngờ | tròn mắt, há hốc | *"Cô ấy ngạc nhiên."* |

### Transition Consistency

| Transition Type | Vietnamese Pattern | Example |
|-----------------|-------------------|---------|
| Scene change | *** or dòng trắng | *"***" giữa các phân cảnh lớn |
| Time jump | "Sáu năm trước..." | Flashback marker |
| Small transition | —0o0— | UH style inner transition |
| Location change | "Ở trong khu rừng..." | Explicit location shift |

**OOC check:** Verify transitions follow consistent pattern per genre - BNsr uses ***, UH uses —0o0—.

### Formality Level Checklist

For OOC consistency checking:

```
[ ] Character pronouns match relationship context
[ ] Pronoun shifts justified by emotion/state change
[ ] Formal characters (ngài, tôi) maintain register
[ ] Close characters (tao, mày) use casual register
[ ] Angry state triggers formality drop (thằng chó, con khốn)
```

### Slang và Vernacular Patterns

| Slang | Ý nghĩa | Ví dụ |
|-------|---------|-------|
| thằng chó | Chửi thề mạnh | *"Thằng chó đó mà dám..."* (UH Chương 3) |
| khốn | Khinh bỉ | *"Đồ khốn nạn!"* |
| chó đẻ | Mắng thô bạo | *"Chết mẹ mày đi!"* (UH Chương 4) |
| hớt hải | Vội vàng | *"Tanaka hớt hải hỏi"* (UH Chương 2) |
| lèm nhèm | Yếu đuối | *"Đứa nhèm nhèm"* |

### Colloquial vs Literary Register

| Đời thường | Văn chương | Ghi chú |
|------------|------------|----------|
| đi đường | đường đi | Cùng nghĩa, khác trật tự |
| làm gì | làm chi | Hỏi mục đích |
| đâu | ở đâu | Nơi chốn |
| vậy | như vậy / thế | Cách nói |

### Inverted Syntax Patterns

**Mẫu phổ biến:**
```
Bình thường: Rosa đứng dậy.
Đảo ngược: Đứng dậy Rosa. (Sách vở)

Bình thường: Hắn ta đi ra ngoài.
Đảo ngược: Ra ngoài hắn ta đi. (Cổ xưa)
```

### Subordinate Clause Patterns

| Loại | Cấu trúc | Ví dụ |
|------|----------|-------|
| Nguyên nhân | vì... nên... | *"Vì mệnh lệnh từ Jack bất ngờ..."* (BNsr Chương 5) |
| Kết quả | ...nên... | *"Nên cô tạm thời được giải phóng..."* |
| Điều kiện | nếu... thì... | *"Nếu một ngày kia rồng chúa quay trở lại..."* |
| Nhượng bộ | tuy... nhưng... | *"Tuy nhiên, dù bản thân có thể..."* |
| Thời gian | khi... thì... | *"Khi còn nhỏ tôi đã nhìn..."* (BNsr Chương 1) |

### Logic Linking Words

| Từ nối | Chức năng | Ví dụ |
|--------|-----------|-------|
| vì | Nguyên nhân | "Vì những lý do không ai biết..." |
| nhưng | Đối lập | "Tuy nhiên, nhưng mà" |
| mà | Liên kết | "Đó là cách... mà cũng là..." |
| tuy nhiên | Đối lập nhẹ | "Tuy nhiên, với những gì..." |
| thế là | Kết quả | "Thế là chấm hết." |
| nên | Kết quả trực tiếp | "Nên cô tạm thời được giải phóng..." |
| đằng | Mặc dù | "Đằng ấy thì sao?" |
| thậm chí | Nhấn mạnh | "Thậm chí ngay cả..."

