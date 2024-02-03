#!/bin/bash

# 输入IP地址和子网掩码（例如：192.168.1.0/24）
read -p "Enter IP address (with subnet mask, e.g., 192.168.1.0/24): " target

# 使用ipcalc获取子网内的所有IP地址（假设ipcalc已安装）
# 注意：这里只是展示如何获取IP范围，实际脚本需要根据输出调整解析逻辑
ip_range=$(ipcalc -n $target | grep -oP 'HostMin: \K\S+')
ip_end=$(ipcalc -n $target | grep -oP 'HostMax: \K\S+')

# 转换开始和结束IP地址为整数（简化处理）
IFS='.' read -r -a start_ip_arr <<< "$ip_range"
IFS='.' read -r -a end_ip_arr <<< "$ip_end"

# 简化为四部分转换为整数的函数（可能需要调整以处理边界值）
start_ip=$((${start_ip_arr[0]} * 16777216 + ${start_ip_arr[1]} * 65536 + ${start_ip_arr[2]} * 256 + ${start_ip_arr[3]}))
end_ip=$((${end_ip_arr[0]} * 16777216 + ${end_ip_arr[1]} * 65536 + ${end_ip_arr[2]} * 256 + ${end_ip_arr[3]}))

# 扫描每个IP地址上的端口
for ((ip=start_ip; ip<=end_ip; ip++)); do
    # 转换整数回IP地址
    IFS='.' printf -v ip_str '%d.%d.%d.%d\n' $((ip>>24&255)) $((ip>>16&255)) $((ip>>8&255)) $((ip&255))

    # 扫描1到65535号端口
    for port in {1..65535}; do
        # 使用nc扫描端口，超时设置为1秒
        nc -zv $ip_str $port -w 1 &> /dev/null
        if [ $? -eq 0 ]; then
            echo "Port $port open on $ip_str"
        fi
    done
done
