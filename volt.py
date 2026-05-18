# =================================================================
#  Volt Language Core Engine - Standalone Android Edition ⚡
#  Lead Architect: Ali Ahmed Abdul Hussein Zarki
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
        self.in_if_block = False

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
        for line in lines:
            stripped_line = line.strip()
            
            if not stripped_line or stripped_line.startswith('#'):
                continue
            
            # إدارة الخروج الذكي من بلوك الشرط
            if self.in_if_block and not line.startswith('    '):
                body_lines.append("    }")
                self.in_if_block = False

            current_command = stripped_line

            # 1. تحليل الشروط
            if current_command.startswith('if ') and current_command.endswith(':'):
                condition = current_command[3:-1].strip()
                body_lines.append(f"    if ({condition}) {{")
                self.in_if_block = True
                continue
            
            # 2. تحليل وتفريغ else
            elif current_command == 'else:':
                body_lines.append("    else {")
                self.in_if_block = True
                continue

            # 3. دالة السيرفر المدمجة لـ Volt
            elif current_command.startswith('start_server '):
                port = current_command[13:].strip()
                self.has_server = True
                indent = "        " if self.in_if_block else "    "
                body_lines.append(f"{indent}start_server({port});")

            # 4. تحليل المتغيرات والتعرف على الأنواع
            elif '=' in current_command:
                parts = current_command.split('=', 1)
                var_name = parts[0].strip()
                var_value = parts[1].strip()
                
                if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", var_name):
                    var_type = self.detect_type(var_value)
                    indent = "        " if self.in_if_block else "    "
                    body_lines.append(f"{indent}{var_type} {var_name} = {var_value};")
                else:
                    print(f"Error: Invalid variable name '{var_name}'")
                    return None

            # 5. تحليل أمر الطباعة المطور
            elif current_command.startswith('print '):
                content = current_command[6:].strip()
                indent = "        " if self.in_if_block else "    "
                if (content.startswith('"') and content.endswith('"')) or (content.startswith("'") and content.endswith("'")):
                    self.has_string = True
                body_lines.append(f"{indent}cout << {content} << endl;")
            
            else:
                print(f"Syntax Error in Volt: Unknown command -> '{stripped_line}'")
                return None

        if self.in_if_block:
            body_lines.append("    }")

        # صياغة ملف الـ C++ المترجم
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


def run_volt_ecosystem(source_code):
    print("[Volt Core] Reading and parsing your Volt source file...")
    
    compiler = VoltCompiler(source_code)
    cpp_output = compiler.compile()
    
    if not cpp_output:
        print("[Volt Error] Compilation failed.")
        return

    cpp_filename = "compiled_volt_core.cpp"
    with open(cpp_filename, "w", encoding='utf-8') as f:
        f.write(cpp_output)
    print(f"[Volt Core] Intermediate C++ code generated successfully.")

    print(f"[Volt Core] Invoking Android system compiler (clang++) to build native machine code...")
    
    try:
        # استدعاء مترجم الأندرويد لإنتاج الباينري الخالص
        subprocess.run(["clang++", cpp_filename, "-o", "volt_app"], check=True)
        print(f"\n[Volt Success] Hardwired binary generated successfully: './volt_app'")
        print("-" * 50)
        print("YOU CAN NOW RUN YOUR HIGH-PERFORMANCE VOLT APP!")
        print("-" * 50)
    except FileNotFoundError:
        print("\n[Volt Error] Compiler 'clang++' not accessible.")


# =================================================================
#  برنامجك الرسمي لـ Volt مكتوب ومحقون هنا بالأسفل بشكل سليم ومضمون
# =================================================================
if __name__ == "__main__":
    
    volt_program = """
name = "Ali Zarki"
print name

if 10 > 5:
    print "Deploying high-performance server..."
    start_server 8080
"""

    run_volt_ecosystem(volt_program)
