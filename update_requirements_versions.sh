#!/bin/bash

# 检查当前是否在 conda 虚拟环境中
if [[ -z "$CONDA_DEFAULT_ENV" ]]; then
    echo "Error: You are not in a conda environment."
    exit 1
fi

# 检查 requirements.txt 是否存在
if [[ ! -f "requirements.txt" ]]; then
    echo "Error: requirements.txt not found in the current directory."
    exit 1
fi

# 创建一个临时文件来存储更新的版本信息
temp_file=$(mktemp)

# 遍历 requirements.txt 中的每个包
while IFS= read -r package; do
    # 获取包名（去除可能存在的版本号）
    package_name=$(echo "$package" | sed 's/[>=<].*//')
    
    # 获取当前 conda 环境中该包的版本号
    version=$(pip show "$package_name" 2>/dev/null | grep Version | awk '{print $2}')
    
    if [[ -n "$version" ]]; then
        # 将包名和版本号写入临时文件
        echo "$package_name==$version" >> "$temp_file"
        echo "Updated $package_name to version $version"
    else
        # 如果包在当前环境中不存在，保持原样
        echo "$package" >> "$temp_file"
        echo "Warning: $package_name not found in the current environment, keeping the original entry."
    fi
done < requirements.txt

# 用更新后的内容替换 requirements.txt
mv "$temp_file" requirements.txt

# 提示更新完成
echo "requirements.txt has been updated successfully!"
