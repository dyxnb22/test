# csv-cleaner-cli 运行命令（Docker）

> `environment/Dockerfile` 的默认 `CMD` 是 `python --version`，所以直接 `docker run` 会打印版本后退出，这是预期行为。

```bash
REPO_ROOT="/path/to/your/repo"   # 必须替换为你本机实际仓库绝对路径，例如：/home/user/projects/test
PROJECT_ROOT="$REPO_ROOT/answer/csv-cleaner-cli"
```

## 1) 构建镜像

```bash
docker build -t csv-cleaner-cli:latest -f "$PROJECT_ROOT/environment/Dockerfile" "$PROJECT_ROOT"
```

## 2) 运行容器（普通执行 / 交互调试）

```bash
# 普通执行：直接进入 shell 并执行命令
docker run --rm -it -v "$PROJECT_ROOT:/workspace" csv-cleaner-cli:latest sh
```

```bash
# 交互调试：查看目录与关键文件
docker run --rm -it -v "$PROJECT_ROOT:/workspace" csv-cleaner-cli:latest sh -c "pwd && ls -la && find /workspace -maxdepth 3 -type f"
```

## 3) 执行 CSV 清洗并产出输出文件

```bash
docker run --rm -v "$PROJECT_ROOT:/workspace" csv-cleaner-cli:latest python /workspace/solution/cleaner.py --input /workspace/environment/dirty_data.csv --output /workspace/solution/cleaned_data.csv
```

```bash
# 查看输出
cat "$PROJECT_ROOT/solution/cleaned_data.csv"
```

## 4) 运行测试

```bash
docker run --rm -v "$PROJECT_ROOT:/workspace" csv-cleaner-cli:latest sh -c "python /workspace/solution/cleaner.py --input /workspace/environment/dirty_data.csv --output /workspace/solution/cleaned_data.csv && python /workspace/tests/test_logic.py"
```

## 5) 如需拷贝产物到宿主机

> 上面命令使用了目录挂载，`cleaned_data.csv` 已直接写到宿主机目录，通常不需要 `docker cp`。  
> 若你改用不挂载的容器，可先用 `docker ps -a` 找到容器 ID，再执行：

```bash
docker cp <container_id>:/workspace/solution/cleaned_data.csv "$PROJECT_ROOT/solution/cleaned_data.csv"
```
