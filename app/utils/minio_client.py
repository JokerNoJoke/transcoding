from pathlib import Path

from minio import Minio

_client = Minio(
    endpoint="127.0.0.1:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,  # Disable SSL for local development
)

_bucket_name = "transcoding"


def fput_object(object_name: str, file_path: str) -> None:
    """Upload a file or directory to MinIO.

    Args:
        object_name (str): Object name in MinIO
        file_path (str): Path to file or directory to upload

    Raises:
        FileNotFoundError: If the file_path doesn't exist
        ValueError: If the file_path is neither a file nor a directory
        Exception: If upload to MinIO fails
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Path does not exist: {file_path}")

    try:
        if file_path.is_file():
            # Upload single file directly
            _client.fput_object(_bucket_name, object_name, str(file_path))
        elif file_path.is_dir():
            # Upload all files in directory recursively
            for item in file_path.rglob("*"):
                if item.is_file():
                    # Calculate relative path from base directory
                    relative_path = item.relative_to(file_path)
                    # Construct MinIO object name with forward slashes
                    object_name_full = f"{object_name}/{relative_path}".replace(
                        "\\", "/"
                    )
                    _client.fput_object(_bucket_name, object_name_full, str(item))
        else:
            raise ValueError(f"Path is neither a file nor a directory: {file_path}")
    except Exception as e:
        # Wrap MinIO errors with more context
        raise Exception(
            f"Failed to upload {file_path} to MinIO bucket {_bucket_name}: {str(e)}"
        )
