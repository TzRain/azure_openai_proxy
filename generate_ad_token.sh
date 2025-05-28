#!/bin/bash

# 找到脚本所在目录，支持任何目录执行
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 调用 Python 脚本，输出 export 语句并执行
eval "$(python3 $SCRIPT_DIR/generate_ad_token.py)"