# csv-cleaner-cli 题目说明（中文）

## 1) 题目目标（Plain Chinese）
- 这是一个 **CSV 清洗 CLI** 题目：读取脏数据 `environment/dirty_data.csv`，按规则清洗后输出到 `solution/cleaned_data.csv`。
- 本质考察点：**数据清洗规则实现能力 + 命令行工具能力 + 可测试性/可复现性（Docker）**。

## 2) 现有答案如何实现（实现 walkthrough）
### 文件职责
- `instruction.md`：题目英文要求与清洗规则。
- `solution/cleaner.py`：核心实现（解析参数、清洗、写回）。
- `solution/solve.sh`：标准运行入口，固定输入输出路径。
- `tests/test_logic.py`：断言输出是否与期望完全一致。
- `tests/test.sh`：测试入口（先运行答案，再跑断言）。
- `environment/Dockerfile`：本地统一环境（Python 3.11.9）。

### 核心流程（`cleaner.py`）
1. `main()` 解析 `--input` 和 `--output`。
2. `clean_rows()`：
   - 用 `csv.DictReader` 读入并清理 header/字段空白。
   - 跳过全空行。
   - 校验 `id`：必须是正整数；重复 `id` 只保留首个有效行。
   - 规范化字段：
     - `name`：压缩多空格并转 Title Case（`normalize_name`）。
     - `email`：转小写并做基础合法性检查（`email_valid`）。
     - `age`：仅保留 `[0,120]` 整数，否则置空（`parse_age`）。
     - `score`：仅保留 `[0,100]` 数值，格式化为两位小数，否则置空（`parse_score`）。
   - 按 `id` 升序排序后返回。
3. `write_rows()`：按固定列头 `id,name,email,age,score` 写出结果文件。

## 3) 如何运行/测试（优先 Docker 本地流程）
> 以下命令在仓库根目录执行：`<repo-root>`（占位符，表示你的仓库根目录实际路径）。
> 例如先执行：`cd /path/to/your-repo`，再继续下面命令。

### A. Docker 本地测试（录屏必须包含）
```bash
cd <repo-root>/answer/csv-cleaner-cli

# 1) 构建镜像（锁定 Python 3.11.9）
docker build -t csv-cleaner-cli-local -f environment/Dockerfile .

# 2) 容器内跑测试（标准方式）
docker run --rm \
  -v "$(pwd)":/workspace \
  -w /workspace \
  csv-cleaner-cli-local \
  bash -lc "python --version && bash tests/test.sh"
```

成功标志：看到 `Python 3.11.9` 且最后输出 `PASS`。

### B. 非 Docker（本机快速验证）
```bash
cd <repo-root>/answer/csv-cleaner-cli
bash tests/test.sh
```

## 4) 录屏脚本（两部分都不遗漏）
按下面顺序讲，基本不会漏：

1. **开场（10~20 秒）**
   - 说明任务：做一个 CSV 清洗 CLI，输出需可被测试脚本验证。

2. **第一部分：Docker 本地测试（必须）**
   - 展示目录：`answer/csv-cleaner-cli`。
   - 执行 `docker build ...`。
   - 执行 `docker run ... bash -lc "python --version && bash tests/test.sh"`。
   - 展示关键结果：`Python 3.11.9`、`PASS`。

3. **第二部分：完整解题思路讲解（必须）**
   - 打开 `instruction.md`，快速过一遍规则（id、email、age、score、去重、排序、输出列头）。
   - 打开 `solution/cleaner.py`，按函数讲：
     - `normalize_name / email_valid / parse_age / parse_score`
     - `clean_rows` 主流程（清理空白、过滤非法、去重、规范化、排序）
     - `write_rows` 固定表头输出
   - 打开 `tests/test_logic.py`，说明如何通过“期望值对比”防止伪通过。

4. **收尾（10 秒）**
   - 再强调：已在 Docker 内完成测试并 PASS；思路讲解完成。

## 5) 常见坑 + 最终提交检查清单
### 常见坑
- 漏录其中一部分（只录测试或只录思路）→ 不合格。
- 在宿主机跑过但没在 Docker 里跑 → 不满足录屏要求。
- `id` 去重逻辑写错（没保留首个有效行）。
- `score` 没按两位小数输出。
- 输出列顺序/列名与要求不完全一致。

### 提交前 checklist
- [ ] 录屏包含 **Docker 本地测试** 全流程且看到 `PASS`
- [ ] 录屏包含 **完整解题思路讲解**
- [ ] 讲解覆盖核心规则与关键函数/流程
- [ ] 命令、路径、输出展示清楚，可复现
