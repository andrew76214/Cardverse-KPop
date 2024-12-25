#!/bin/bash

# 檢查是否以 root 權限運行
if [ "$(id -u)" != "0" ]; then
   echo "此腳本需要以 root 權限運行。" 1>&2
   exit 1
fi

# 更新系統並安裝必需軟件
echo "更新系統並安裝必要軟件..."
apt update
apt install -y certbot python3-certbot-nginx

# 輸入域名
read -p "請輸入你的域名（如 example.com）: " DOMAIN

# 檢查 Nginx 配置
echo "檢查 Nginx 配置..."
nginx -t
if [ $? -ne 0 ]; then
    echo "Nginx 配置測試失敗，請修正錯誤後重試。"
    exit 1
fi

# 為域名生成 SSL 證書
echo "生成 SSL 證書..."
certbot --nginx -d "$DOMAIN"

# 設置自動續期
echo "設置自動續期..."
if ! crontab -l | grep -q "certbot renew --quiet"; then
    (crontab -l 2>/dev/null; echo "0 0 * * * certbot renew --quiet") | crontab -
    echo "已設置自動續期任務。"
else
    echo "自動續期任務已存在。"
fi

# 重新加載 Nginx
echo "重新加載 Nginx..."
systemctl reload nginx

# 完成
echo "Let's Encrypt 安裝和配置完成！請訪問 https://$DOMAIN 測試。"
