# =================================================================
#  Volt Language Core Engine - Ultimate Loop Edition ⚡
#  Lead Architect: Ali Ahmed Abdul Hussein Zarki (ialidev)
# =================================================================

import re
import os
import subprocess

class VoltCompiler:
    def __init__(self, source_code):
        self.source_code = source_code
        self.cpp_lines = []
        self.has_string = False
        self.has_server = False 
        self.in_block = False  # تتبع إن كنا داخل بلوك (شرط أو تكرار)

    def detect_type(self, value):
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            self.has_string = True
            return "string"
        elif re.match(r"^\d+$", value):
            return "int"
        elif re.match(r"^\d+\.\d+$", value):
            return "float"
        return "auto"

    def compile(self):
        body_lines = []
        
        server_cpp_function = """
void start_server(int port) {
    std::cout << "\\n[Volt Server] Initializing Local Microservice on Port " << port << "..." << std::endl;
    std::cout << "[Volt Server] Server successfully running! Ready for data packets.\\n" << std::endl;
}
"""

        lines = self.source_code.split('\n')
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            if not stripped_line or stripped_line.startswith('#'):
                continue
            
            # إغلاق البلوكات المفتوحة إذا قل التوجيه (المرور لسطر غير محاذى)
            if self.in_block and not line.startswith('    '):
                body_lines.append("    }")
                self.in_block = False

            current_command = stripped_line

            # 1. تحليل الشروط if
            if current_command.startswith('if ') and current_command.endswith(':'):
                condition = current_command[3:-1].strip()
                body_lines.append(f"    if ({condition}) {{")
                self.in_block = True
                continue
            
            # 2. تحليل الشروط else
            elif current_command == 'else:':
                body_lines.append("    else {")
                self.in_block = True
                continue

            # 3. تحليل ميزة الحلقات التكرارية الجديدة loop
            elif current_command.startswith('loop ') and current_command.endswith(':'):
                times = current_command[5:-1].strip()
                # توليد حلقة C++ باستخدام متغير فريد بناءً على رقم السطر لمنع التداخل
                body_lines.append(f"    for (int _i{i} = 0; _i{i} < {times}; ++_i{i}) {{")
                self.in_block = True
                continue

            # 4. دالة السيرفر
            elif current_command.startswith('start_server '):
                port = current_command[13:].strip()
                self.has_server = True
                indent = "        " if self.in_block else "    "
                body_lines.append(f"{indent}start_server({port});")

            # 5. تحليل المتغيرات والمدخلات
            elif '=' in current_command:
                parts = current_command.split('=', 1)
                var_name = parts[0].strip()
                var_value = parts[1].strip()
                
                if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", var_name):
                    indent = "        " if self.in_block else "    "
                    
                    if var_value == "input":
                        self.has_string = True
                        body_lines.append(f"{indent}string {var_name};")
                        body_lines.append(f"{indent}cin >> {var_name};")
                    else:
                        var_type = self.detect_type(var_value)
                        body_lines.append(f"{indent}{var_type} {var_name} = {var_value};")
                else:
                    print(f"Error: Invalid variable name '{var_name}'")
                    return None

            # 6. تحليل أمر الطباعة
            elif current_command.startswith('print '):
                content = current_command[6:].strip()
                indent = "        " if self.in_block else "    "
                if (content.startswith('"') and content.endswith('"')) or (content.startswith("'") and content.endswith("'")):
                    self.has_string = True
                body_lines.append(f"{indent}cout << {content} << endl;")
            
            else:
                print(f"Syntax Error in Volt: Unknown command -> '{stripped_line}'")
                return None

        if self.in_block:
            body_lines.append("    }")

        self.cpp_lines.append("#include <iostream>")
        if self.has_string:
            self.cpp_lines.append("#include <string>")
        
        self.cpp_lines.append("using namespace std;\n")
        
        if self.has_server:
            self.cpp_lines.append(server_cpp_function)

        self.cpp_lines.append("int main() {")
        self.cpp_lines.extend(body_lines)
        self.cpp_lines.append("    return 0;")
        self.cpp_lines.append("}")
        
        return "\n".join(self.cpp_lines)


def run_volt_ecosystem():
    target_file = "app.vl"
    
    if not os.path.exists(target_file):
        print(f"[Volt Error] Source file '{target_file}' not found.")
        return

    print(f"[Volt Core] Reading and parsing '{target_file}'...")
    with open(target_file, "r", encoding="utf-8") as f:
        source_code = f.read()
    
    compiler = VoltCompiler(source_code)
    cpp_output = compiler.compile()
    
    if not cpp_output:
        print("[Volt Error] Compilation failed.")
        return

    cpp_filename = "compiled_volt_core.cpp"
    with open(cpp_filename, "w", encoding='utf-8') as f:
        f.write(cpp_output)

    try:
        subprocess.run(["clang++", cpp_filename, "-o", "volt_app"], check=True)
        print(f"\n[Volt Success] Hardwired binary with Loop support built successfully!")
        print("-" * 50)
        print("RUN YOUR APP VIA: ./volt_app")
        print("-" * 50)
    except FileNotFoundError:
        print("\n[Volt Error] Compiler 'clang++' not accessible.")

if __name__ == "__main__":
    run_volt_ecosystem()
