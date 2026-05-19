#!/bin/bash

echo "⚡ Initiating Volt Language Core Installation... ⚡"
echo "================================================="

# 1. تحديث الحزم وتثبيت المتطلبات تلقائياً دون تدخل المستخدم
echo "[1/3] Installing Prerequisites (Python & Clang)..."
pkg update -y && pkg install python clang git -y

# 2. إنشاء مجلد العمل والانتقال إليه
echo "[2/3] Setting up workspace..."
cd $HOME
if [ -d "Volt-Language" ]; then
    echo "Volt-Language directory already exists. Updating..."
    cd Volt-Language && git pull
else
    git clone https://github.com/AliAhmed-D/Volt-Language.git
    cd Volt-Language
fi

# 3. طباعة رسالة النجاح وتجهيز البيئة
echo "================================================="
echo "⚡ Volt Language Installed Successfully! ⚡"
echo "Architect: Ali Ahmed Abdul Hussein Zarki"
echo "To run your first code, type: python volt.py"
echo "================================================="
