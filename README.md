## Transcoding

音视频转码服务 (Video/Audio Transcoding Service)

- [uv](https://docs.astral.sh/uv/) Python package and project manager
- [FFmpeg](https://ffmpeg.org/download.html) FFmpeg is the leading multimedia framework
- [MinIO](https://min.io/download) MinIO is an object storage solution
- [FastAPI](https://fastapi.tiangolo.com/) FastAPI is a modern, fast (high-performance), web framework

### 项目结构

```
transcoding/
├── app/                        # 服务代码
|   ├── routers/
|   |   └── os.py               # 文件上传 API
|   ├── utils/
|   |   ├── ffmpeg_client.py    # 视频转码工具
|   |   └── minio_client.py     # MinIO 客户端
|   └── ...
├── ffmpeg-7.1/                 # FFmpeg 执行文件
├── player/                     # Web 播放器
├── temp/                       # 上传、转码临时文件夹
└── ...
```

### FFmpeg 配置

1. 下载并解压 FFmpeg 到项目根目录，确保目录结构如下：
```
transcoding/
├── ffmpeg-7.1/
│   └── bin/
│       ├── ffmpeg.exe
│       └── ffprobe.exe
```

2. 如需自定义 FFmpeg 路径，请修改 `app/utils/video_transcoding.py` 中的配置：
```python
ffprobe_path = os.path.join("ffmpeg-7.1", "bin", "ffprobe.exe")
ffmpeg_path = os.path.join("ffmpeg-7.1", "bin", "ffmpeg.exe")
```

### MinIO 配置

在 `app/utils/minio_utils.py` 中配置 MinIO 连接信息：
```python
minio_client = Minio(
    endpoint="127.0.0.1:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)
```

### 同步环境

```bash
uv sync
```


### 启动服务
```bash
uv run fastapi dev
```
