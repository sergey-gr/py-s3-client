# S3 Browser

- Python package [MinIO](https://github.com/minio/minio-py).
- Python Client [API Reference](https://min.io/docs/minio/linux/developers/python/API.html).

## Setup

Required: `Python 3`

### Virtual environment

Install python virtual environment package

```shell
pip3 install virtualenv
```

Initialize virtual environment

Linux:

```shell
python -m venv .venv
```

Windows:

```shell
py -m venv .venv
```

### Script setup

Activate virtual environment

Linux:

```shell
source .venv/bin/activate
```

Windows:

```shell
# Git Bash
source .venv/Scripts/activate

# PowerShell
.venv\Scripts\activate
```

Install dependencies

```shell
pip3 install -r requirements.txt
```

Create configuration file from sample:

```shell
cp config/config.yml.sample config/config.yml
```

Edit configuration file by setting s3 credentials:

```yml
s3:
  address: s3.example.com
  bucket: my_bucket_name
  accessKey: my_access_key
  secretKey: my_secret_key
```

<br>

## Usage

```shell
python main.py
```

Log files are stored in `logs` directory if `logging.output: file`.

Log file name example:

```text
./logs/YYY-MM-DD.log
```
