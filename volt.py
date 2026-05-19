# =================================================================
#  Volt Language Core Engine - Strict 3-Letter Syntax Edition ⚡
#  Lead Architect: Ali Ahmed Abdul Hussein Zarki Al-Hamrani
# =================================================================

import re
import os
import subprocess

class VoltCompiler:
    def __init__(self, source_code):
        self.source_code = source_code
        self.cpp_lines = []
        self.has_string = False
        self.has_math = False  
        self.in_block = False  

    def compile(self):
        body_lines = []
        lines = self.source_code.split('\n')
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            if not stripped_line or stripped_line.startswith('#'):
                continue
            
            # إغلاق البلوكات تلقائياً حسب المحاذاة
            if self.in_block and not line.startswith('    '):
                body_lines.append("    }")
                self.in_block = False

            current_command = stripped_line

            # 1. 🔥 الشرط الصارم ثلاثي الحروف (ifs)
            if current_command.startswith('ifs ') and current_command.endswith(':'):
                condition = current_command[4:-1].strip()
                body_lines.append(f"    if ({condition}) {{")
                self.in_block = True
                continue
            
            # 2. 🔥 الشرط المتعدد الصارم ثلاثي الحروف (elf)
            elif current_command.startswith('elf ') and current_command.endswith(':'):
                condition = current_command[4:-1].strip()
                body_lines.append(f"    }} else if ({condition}) {{")
                self.in_block = True
                continue
            
            # 3. 🔥 الشرط البديل الصارم ثلاثي الحروف (els)
            elif current_command == 'els:':
                body_lines.append("    } else {")
                self.in_block = True
                continue

            # 4. 🔥 الحلقة التكرارية الصارمة ثلاثية الحروف (lop)
            elif current_command.startswith('lop ') and current_command.endswith(':'):
                times = current_command[4:-1].strip()
                body_lines.append(f"    for (int _i{i} = 0; _i{i} < {times}; ++_i{i}) {{")
                self.in_block = True
                continue

            # 5. 🔥 أمر إنهاء البرنامج الصارم ثلاثي الحروف (ext)
            elif current_command == 'ext':
                indent = "        " if self.in_block else "    "
                body_lines.append(f"{indent}return 0;")

            # 6. 🔥 أمر الإدخال الذكي ثلاثي الحروف (inp "Msg": var)
            elif current_command.startswith('inp ') and ':' in current_command:
                indent = "        " if self.in_block else "    "
                self.has_string = True
                parts = current_command[4:].split(':', 1)
                msg_content = parts[0].strip()
                var_name = parts[1].strip()
                
                body_lines.append(f"{indent}cout << {msg_content};")
                body_lines.append(f"{indent}string {var_name};")
                body_lines.append(f"{indent}cin >> {var_name};")

            # 7. تعريف المتغيرات الصريح بـ 3 أحرف (str, num, flt, var)
            elif current_command.startswith(('str ', 'num ', 'flt ', 'var ')) and '=' in current_command:
                indent = "        " if self.in_block else "    "
                token_type = current_command.split(' ')[0].strip()
                rest = current_command[len(token_type):].strip()
                parts = rest.split('=', 1)
                var_name = parts[0].strip()
                var_value = parts[1].strip()
                
                if any(m in var_value for m in ["sqrt(", "pow(", "abs("]):
                    self.has_math = True

                cpp_type = "auto"
                if token_type == "str":
                    cpp_type = "string"
                    self.has_string = True
                elif token_type == "num":
                    cpp_type = "int"
                elif token_type == "flt":
                    cpp_type = "double"
                elif token_type == "var":
                    cpp_type = "auto"

                body_lines.append(f"{indent}{cpp_type} {var_name} = {var_value};")

            # 8. التخصيص التلقائي للمتغيرات (بدون تحديد نوع)
            elif '=' in current_command:
                parts = current_command.split('=', 1)
                var_name = parts[0].strip()
                var_value = parts[1].strip()
                indent = "        " if self.in_block else "    "
                
                if any(m in var_value for m in ["sqrt(", "pow(", "abs("]):
                    self.has_math = True
                body_lines.append(f"{indent}auto {var_name} = {var_value};")

            # 9. أمر الطباعة الصارم ثلاثي الحروف (out)
            elif current_command.startswith('out '):
                content = current_command[4:].strip()
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
        if self.has_math:
            self.cpp_lines.append("#include <cmath>")
        
        self.cpp_lines.append("using namespace std;\n")
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

    with open(target_file, "r", encoding="utf-8") as f:
        source_code = f.read()
    
    compiler = VoltCompiler(source_code)
    cpp_output = compiler.compile()
    
    if not cpp_output:
        print("[Volt Error] Compilation level syntax failure.")
        return

    cpp_filename = "compiled_volt_core.cpp"
    with open(cpp_filename, "w", encoding='utf-8') as f:
        f.write(cpp_output)

    try:
        subprocess.run(["clang++", cpp_filename, "-o", "volt_app"], check=True)
        print(f"\n[Volt Success] Strict 3-Letter Architecture built successfully!")
        print("-" * 50)
        print("RUN YOUR APP VIA: ./volt_app")
        print("-" * 50)
    except FileNotFoundError:
        print("\n[Volt Error] Compiler 'clang++' not accessible.")

if __name__ == "__main__":
    run_volt_ecosystem()
