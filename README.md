# SearchBoard
proxy for baidu.com

## 部署
### 手动
```bash
pip3 install -r requirements.txt    # 安装依赖
./server-start.sh                   # 启动服务
./server-stop.sh                    # 停止服务
```
### docker部署
```bash
docker build . --tag search.hk:local    # 构建
docker run -d -p5000:80 search.hk:local # 启动容器
```
