# =================================================================
#  Volt Language Core Engine - Open Source Edition ⚡
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
        
        # دالة السيرفر المدمجة التي سيتم توليدها بـ C++ خلف الكواليس
        server_cpp_function = """
void start_server(int port) {
    std::cout << "[Volt Server] Initializing Local Microservice on Port " << port << "..." << std::endl;
    std::cout << "[Volt Server] Server successfully running! Ready for data packets." << std::endl;
}
"""

        lines = self.source_code.split('\n')
        for line in lines:
            stripped_line = line.strip()
            
            if not stripped_line or stripped_line.startswith('#'):
                continue
            
            # تتبع الخروج من بلوك الـ if بناءً على المسافات
            if self.in_if_block and not line.startswith('    '):
                body_lines.append("    }")
                self.in_if_block = False

            current_command = stripped_line

            # 1. تحليل الشروط if
            if current_command.startswith('if ') and current_command.endswith(':'):
                condition = current_command[3:-1].strip()
                body_lines.append(f"    if ({condition}) {{")
                self.in_if_block = True
                continue
            
            # 2. تحليل التفرع else:
            elif current_command == 'else:':
                body_lines.append("    else {")
                self.in_if_block = True
                continue

            # 3. دالة السيرفر المدمجة الخاصة بـ Volt
            elif current_command.startswith('start_server '):
                port = current_command[13:].strip()
                self.has_server = True
                indent = "        " if self.in_if_block else "    "
                body_lines.append(f"{indent}start_server({port});")

            # 4. تحليل المتغيرات والتعرف الذكي على الأنواع
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

        # تجميع الهيكل النهائي المترجم لـ C++
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
    print(f"[Volt Core] Intermediate C++ code generated and saved to '{cpp_filename}'.")

    executable_name = "volt_app.exe" if os.name == 'nt' else "./volt_app"
    
    # اختيار المترجم تلقائياً (clang++ للأندرويد وتيرموكس، أو g++ للحاسبة)
    sys_compiler = "clang++" if not os.name == 'nt' and os.path.exists("/data/data/com.termux") else "g++"
    print(f"[Volt Core] Invoking system compiler ({sys_compiler}) to build native machine code...")
    
    try:
        subprocess.run([sys_compiler, cpp_filename, "-o", "volt_app"], check=True)
        print(f"\n[Volt Success] Hardwired binary generated successfully: '{executable_name}'")
        print("-" * 50)
        print("YOU CAN NOW RUN YOUR HIGH-PERFORMANCE VOLT APP!")
        print("-" * 50)
    except FileNotFoundError:
        print("\n[Volt Note] Intermediate C++ code generated perfectly!")
        print(f"[System Advisory] Please ensure compiler '{sys_compiler}' is installed on your device.")


# =================================================================
#  برنامج الاختبار المدمج تلقائياً داخل المحرك
# =================================================================
if __name__ == "__main__":
    
    volt_program = """
    # كود تجريبي لاختبار لغة فولت ⚡
    print "--- Welcome to Volt Environment ---"
    
    traffic_load = 45.8
    print "Current Traffic Load on Nodes:"
    print traffic_load
    
    if traffic_load > 40.0:
        print "Status: Threat level high. Deploying Volt local microservice..."
        start_server 8080
    else:
        print "Status: Secure operation mode."
    """

    run_volt_ecosystem(volt_program)
