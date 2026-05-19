# =================================================================
#  Volt Language Core Engine ⚡
#  Lead Architect: Ali Ahmed Abdul Hussein Zarki Al-Hamrani
#  v3.0 — Full Backend Language Edition
#  Libraries: math, fil, str, tim, sys, net, srv, rte, db, jsn,
#             ath, hsh, log, env, cch
# =================================================================

import re
import os
import subprocess

# =================================================================
#  ⚡ VOLT STANDARD LIBRARY
# =================================================================

# ---------------------------------------------------------------
# 1. Math (use math)
# ---------------------------------------------------------------
VOLT_MATH_CONSTANTS = {
    "PI": "3.14159265358979", "EUL": "2.71828182845904",
    "PHI": "1.61803398874989", "INF": "999999999.0",
}
VOLT_MATH_FUNCTIONS = {
    "abs_val": {"cpp": "std::abs({0})",           "include": ["<cmath>"],     "args": 1},
    "pow_val": {"cpp": "std::pow({0},{1})",        "include": ["<cmath>"],     "args": 2},
    "sqr_val": {"cpp": "std::sqrt({0})",           "include": ["<cmath>"],     "args": 1},
    "max_val": {"cpp": "std::max({0},{1})",        "include": ["<algorithm>"], "args": 2},
    "min_val": {"cpp": "std::min({0},{1})",        "include": ["<algorithm>"], "args": 2},
    "rnd_val": {"cpp": "std::round({0})",          "include": ["<cmath>"],     "args": 1},
    "flr_val": {"cpp": "std::floor({0})",          "include": ["<cmath>"],     "args": 1},
    "cel_val": {"cpp": "std::ceil({0})",           "include": ["<cmath>"],     "args": 1},
    "mod_val": {"cpp": "({0}%{1})",               "include": [],              "args": 2},
    "sum_rng": {"cpp": "(({0}*({0}+1))/2)",       "include": [],              "args": 1},
    "log_val": {"cpp": "std::log({0})",            "include": ["<cmath>"],     "args": 1},
    "sin_val": {"cpp": "std::sin({0})",            "include": ["<cmath>"],     "args": 1},
    "cos_val": {"cpp": "std::cos({0})",            "include": ["<cmath>"],     "args": 1},
    "fac_val": {"cpp": "_volt_factorial({0})",     "include": [],              "args": 1,
        "helper": "long long _volt_factorial(int n){if(n<=1)return 1;return n*_volt_factorial(n-1);}"},
    "is_prm":  {"cpp": "_volt_is_prime({0})",      "include": [],              "args": 1,
        "helper": "bool _volt_is_prime(int n){if(n<2)return false;for(int i=2;i*i<=n;i++)if(n%i==0)return false;return true;}"},
}

# ---------------------------------------------------------------
# 2. File (use fil)
# ---------------------------------------------------------------
VOLT_FILE_FUNCTIONS = {
    "fil_wrt": {"cpp": "_volt_file_write({0},{1})", "include": ["<fstream>","<string>"], "args": 2,
        "helper": "void _volt_file_write(string p,string c){ofstream f(p);f<<c;f.close();}"},
    "fil_red": {"cpp": "_volt_file_read({0})",      "include": ["<fstream>","<string>","<sstream>"], "args": 1,
        "helper": "string _volt_file_read(string p){ifstream f(p);stringstream b;b<<f.rdbuf();return b.str();}"},
    "fil_exi": {"cpp": "_volt_file_exists({0})",    "include": ["<fstream>","<string>"], "args": 1,
        "helper": "bool _volt_file_exists(string p){ifstream f(p);return f.good();}"},
    "fil_del": {"cpp": "remove({0}.c_str())",       "include": ["<cstdio>","<string>"],  "args": 1},
    "fil_apd": {"cpp": "_volt_file_append({0},{1})","include": ["<fstream>","<string>"], "args": 2,
        "helper": "void _volt_file_append(string p,string c){ofstream f(p,ios::app);f<<c<<endl;f.close();}"},
}

# ---------------------------------------------------------------
# 3. String (use str)
# ---------------------------------------------------------------
VOLT_STR_FUNCTIONS = {
    "str_len": {"cpp": "(int)({0}).length()",         "include": ["<string>"],               "args": 1},
    "str_upr": {"cpp": "_volt_str_upper({0})",        "include": ["<string>","<algorithm>"], "args": 1,
        "helper": "string _volt_str_upper(string s){transform(s.begin(),s.end(),s.begin(),::toupper);return s;}"},
    "str_lwr": {"cpp": "_volt_str_lower({0})",        "include": ["<string>","<algorithm>"], "args": 1,
        "helper": "string _volt_str_lower(string s){transform(s.begin(),s.end(),s.begin(),::tolower);return s;}"},
    "str_sub": {"cpp": "({0}).substr({1},{2})",       "include": ["<string>"],               "args": 3},
    "str_fnd": {"cpp": "(int)({0}).find({1})",        "include": ["<string>"],               "args": 2},
    "str_rep": {"cpp": "_volt_str_replace({0},{1},{2})","include": ["<string>"],             "args": 3,
        "helper": "string _volt_str_replace(string s,string f,string t){size_t p=s.find(f);if(p!=string::npos)s.replace(p,f.length(),t);return s;}"},
    "str_num": {"cpp": "std::to_string({0})",         "include": ["<string>"],               "args": 1},
    "num_str": {"cpp": "std::stoi({0})",              "include": ["<string>"],               "args": 1},
    "str_trm": {"cpp": "_volt_str_trim({0})",         "include": ["<string>"],               "args": 1,
        "helper": "string _volt_str_trim(string s){s.erase(0,s.find_first_not_of(\" \\t\"));s.erase(s.find_last_not_of(\" \\t\")+1);return s;}"},
}

# ---------------------------------------------------------------
# 4. Time (use tim)
# ---------------------------------------------------------------
VOLT_TIME_FUNCTIONS = {
    "tim_now": {"cpp": "(long long)time(nullptr)",         "include": ["<ctime>"],            "args": 0},
    "tim_slp": {"cpp": "_volt_sleep({0})",                 "include": ["<unistd.h>"],         "args": 1,
        "helper": "void _volt_sleep(int s){sleep(s);}"},
    "tim_dat": {"cpp": "_volt_get_date()",                 "include": ["<ctime>","<string>"], "args": 0,
        "helper": "string _volt_get_date(){time_t t=time(nullptr);char b[20];strftime(b,sizeof(b),\"%Y-%m-%d\",localtime(&t));return string(b);}"},
    "tim_str": {"cpp": "_volt_get_time()",                 "include": ["<ctime>","<string>"], "args": 0,
        "helper": "string _volt_get_time(){time_t t=time(nullptr);char b[20];strftime(b,sizeof(b),\"%H:%M:%S\",localtime(&t));return string(b);}"},
    "tim_clk": {"cpp": "(double)clock()/CLOCKS_PER_SEC",  "include": ["<ctime>"],            "args": 0},
}

# ---------------------------------------------------------------
# 5. System (use sys)
# ---------------------------------------------------------------
VOLT_SYS_FUNCTIONS = {
    "sys_run": {"cpp": "system({0}.c_str())", "include": ["<cstdlib>","<string>"], "args": 1},
    "sys_ext": {"cpp": "exit({0})",           "include": ["<cstdlib>"],            "args": 1},
    "sys_env": {"cpp": "_volt_getenv({0})",   "include": ["<cstdlib>","<string>"], "args": 1,
        "helper": "string _volt_getenv(string k){char* v=getenv(k.c_str());return v?string(v):\"\";}"},
    "sys_clr": {"cpp": "system(\"clear\")",   "include": ["<cstdlib>"],            "args": 0},
    "sys_inf": {"cpp": "_volt_sys_info()",    "include": ["<string>"],             "args": 0,
        "helper": "string _volt_sys_info(){#ifdef _WIN32 return \"Windows\";#elif __APPLE__ return \"macOS\";#else return \"Linux\";#endif}"},
    "sys_rnd": {"cpp": "(rand()%{0})",        "include": ["<cstdlib>"],            "args": 1},
    "sys_pid": {"cpp": "(int)getpid()",       "include": ["<unistd.h>"],           "args": 0},
}

# ---------------------------------------------------------------
# 6. Network (use net)
# ---------------------------------------------------------------
VOLT_NET_FUNCTIONS = {
    "net_hip": {"cpp": "_volt_get_hostname()", "include": ["<string>","<unistd.h>"],  "args": 0,
        "helper": "string _volt_get_hostname(){char b[256];gethostname(b,sizeof(b));return string(b);}"},
    "net_png": {"cpp": "_volt_ping({0})",      "include": ["<cstdlib>","<string>"],   "args": 1,
        "helper": "int _volt_ping(string h){string c=\"ping -c 1 \"+h+\" > /dev/null 2>&1\";return system(c.c_str())==0?1:0;}"},
    "net_chk": {"cpp": "_volt_net_check()",   "include": ["<cstdlib>"],              "args": 0,
        "helper": "bool _volt_net_check(){return system(\"ping -c 1 google.com > /dev/null 2>&1\")==0;}"},
}

# ---------------------------------------------------------------
# 7. HTTP Server (use srv)
# ---------------------------------------------------------------
VOLT_SRV_FUNCTIONS = {
    "srv_strt": {"cpp": "_volt_srv_start({0})",    "include": ["<iostream>","<string>","<sstream>","<netinet/in.h>","<unistd.h>","<cstring>"], "args": 1,
        "helper": """
// ===== Volt HTTP Server Core =====
#include <sys/socket.h>
int _volt_server_fd = -1;
int _volt_server_port = 8080;
struct sockaddr_in _volt_server_addr;

string _volt_http_response(int code, string body, string ctype="application/json") {
    string status = code == 200 ? "OK" : code == 404 ? "Not Found" : code == 201 ? "Created" : "Internal Server Error";
    stringstream r;
    r << "HTTP/1.1 " << code << " " << status << "\\r\\n";
    r << "Content-Type: " << ctype << "\\r\\n";
    r << "Content-Length: " << body.size() << "\\r\\n";
    r << "Access-Control-Allow-Origin: *\\r\\n";
    r << "\\r\\n" << body;
    return r.str();
}

void _volt_srv_start(int port) {
    _volt_server_port = port;
    _volt_server_fd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(_volt_server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    _volt_server_addr.sin_family = AF_INET;
    _volt_server_addr.sin_addr.s_addr = INADDR_ANY;
    _volt_server_addr.sin_port = htons(port);
    bind(_volt_server_fd, (struct sockaddr*)&_volt_server_addr, sizeof(_volt_server_addr));
    listen(_volt_server_fd, 10);
    cout << "[Volt Server] Running on http://localhost:" << port << endl;
}

string _volt_srv_get_request() {
    int client = accept(_volt_server_fd, nullptr, nullptr);
    char buf[4096] = {0};
    read(client, buf, 4096);
    string req(buf);
    close(client);
    return req;
}

void _volt_srv_send(int client_fd, string response) {
    send(client_fd, response.c_str(), response.size(), 0);
    close(client_fd);
}
"""},
    "srv_res":  {"cpp": "cout << _volt_http_response({0}, {1}) << endl;", "include": [], "args": 2},
    "srv_200":  {"cpp": "_volt_http_response(200, {0})",   "include": [], "args": 1},
    "srv_404":  {"cpp": "_volt_http_response(404, {0})",   "include": [], "args": 1},
    "srv_500":  {"cpp": "_volt_http_response(500, {0})",   "include": [], "args": 1},
    "srv_201":  {"cpp": "_volt_http_response(201, {0})",   "include": [], "args": 1},
    "srv_req":  {"cpp": "_volt_srv_get_request()",         "include": [], "args": 0},
    "srv_port": {"cpp": "_volt_server_port",               "include": [], "args": 0},
}

# ---------------------------------------------------------------
# 8. Router (use rte)
# ---------------------------------------------------------------
VOLT_RTE_FUNCTIONS = {
    "rte_get": {"cpp": '_volt_route_match({0}, "GET", _volt_req)',  "include": ["<string>"], "args": 1,
        "helper": """
string _volt_req = "";
string _volt_req_method = "";
string _volt_req_path = "";
string _volt_req_body = "";

void _volt_parse_request(string req) {
    _volt_req = req;
    stringstream ss(req);
    string line;
    getline(ss, line);
    stringstream ls(line);
    ls >> _volt_req_method >> _volt_req_path;
    // extract body
    size_t body_pos = req.find("\\r\\n\\r\\n");
    if (body_pos != string::npos)
        _volt_req_body = req.substr(body_pos + 4);
}

bool _volt_route_match(string path, string method, string req) {
    return (_volt_req_path == path && _volt_req_method == method);
}
"""},
    "rte_pst": {"cpp": '_volt_route_match({0}, "POST", _volt_req)',  "include": [], "args": 1},
    "rte_put": {"cpp": '_volt_route_match({0}, "PUT", _volt_req)',   "include": [], "args": 1},
    "rte_del": {"cpp": '_volt_route_match({0}, "DELETE", _volt_req)',"include": [], "args": 1},
    "rte_pth": {"cpp": "_volt_req_path",   "include": [], "args": 0},
    "rte_mth": {"cpp": "_volt_req_method", "include": [], "args": 0},
    "rte_bdy": {"cpp": "_volt_req_body",   "include": [], "args": 0},
    "rte_prs": {"cpp": "_volt_parse_request({0})", "include": [], "args": 1},
}

# ---------------------------------------------------------------
# 9. Database SQLite (use db)
# ---------------------------------------------------------------
VOLT_DB_FUNCTIONS = {
    "db_opn": {"cpp": '_volt_db_open({0})',  "include": ["<string>"], "args": 1,
        "helper": """
// ===== Volt DB Core (File-based JSON store) =====
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
string _volt_db_path = "";
vector<map<string,string>> _volt_db_data;

void _volt_db_open(string path) {
    _volt_db_path = path;
    cout << "[Volt DB] Database opened: " << path << endl;
}

void _volt_db_ins(string table, string key, string val) {
    map<string,string> row;
    row["table"] = table;
    row[key] = val;
    _volt_db_data.push_back(row);
    // persist
    ofstream f(_volt_db_path, ios::app);
    f << table << "|" << key << "=" << val << "\\n";
    f.close();
}

string _volt_db_get(string table, string key) {
    for (auto& row : _volt_db_data)
        if (row["table"] == table && row.count(key))
            return row[key];
    return "";
}

int _volt_db_count(string table) {
    int c = 0;
    for (auto& row : _volt_db_data)
        if (row["table"] == table) c++;
    return c;
}

void _volt_db_clr(string table) {
    _volt_db_data.erase(
        remove_if(_volt_db_data.begin(), _volt_db_data.end(),
            [&](map<string,string>& r){ return r["table"]==table; }),
        _volt_db_data.end());
}
"""},
    "db_ins": {"cpp": "_volt_db_ins({0},{1},{2})", "include": [], "args": 3},
    "db_get": {"cpp": "_volt_db_get({0},{1})",     "include": [], "args": 2},
    "db_cnt": {"cpp": "_volt_db_count({0})",       "include": [], "args": 1},
    "db_clr": {"cpp": "_volt_db_clr({0})",         "include": [], "args": 1},
}

# ---------------------------------------------------------------
# 10. JSON (use jsn)
# ---------------------------------------------------------------
VOLT_JSN_FUNCTIONS = {
    "jsn_obj": {"cpp": "_volt_jsn_obj({0},{1})",   "include": ["<string>","<sstream>"], "args": 2,
        "helper": """
string _volt_jsn_obj(string key, string val) {
    return "{\\"" + key + "\\":\\"" + val + "\\"}";
}
string _volt_jsn_arr(string items) {
    return "[" + items + "]";
}
string _volt_jsn_ok(string msg) {
    return "{\\"status\\":\\"ok\\",\\"message\\":\\"" + msg + "\\"}";
}
string _volt_jsn_err(string msg) {
    return "{\\"status\\":\\"error\\",\\"message\\":\\"" + msg + "\\"}";
}
string _volt_jsn_num(string key, int val) {
    return "{\\"" + key + "\\":" + to_string(val) + "}";
}
string _volt_jsn_get(string json, string key) {
    string search = "\\"" + key + "\\":\\"";
    size_t p = json.find(search);
    if (p == string::npos) return "";
    p += search.size();
    size_t e = json.find("\\"", p);
    return json.substr(p, e - p);
}
"""},
    "jsn_arr": {"cpp": "_volt_jsn_arr({0})",   "include": [], "args": 1},
    "jsn_ok":  {"cpp": "_volt_jsn_ok({0})",    "include": [], "args": 1},
    "jsn_err": {"cpp": "_volt_jsn_err({0})",   "include": [], "args": 1},
    "jsn_num": {"cpp": "_volt_jsn_num({0},{1})","include": [], "args": 2},
    "jsn_get": {"cpp": "_volt_jsn_get({0},{1})","include": [], "args": 2},
}

# ---------------------------------------------------------------
# 11. Hashing (use hsh)
# ---------------------------------------------------------------
VOLT_HSH_FUNCTIONS = {
    "hsh_sha": {"cpp": "_volt_sha256({0})", "include": ["<string>","<sstream>","<iomanip>"], "args": 1,
        "helper": """
// Simple SHA256-like hash (djb2 extended for demo)
string _volt_sha256(string input) {
    unsigned long hash = 5381;
    for (char c : input)
        hash = ((hash << 5) + hash) + c;
    stringstream ss;
    ss << hex << setw(16) << setfill('0') << hash;
    string h = ss.str();
    // extend to 64 chars
    while (h.size() < 64) h = h + h;
    return h.substr(0, 64);
}
string _volt_hsh_md5(string input) {
    unsigned long h = 0;
    for (char c : input) h = h * 31 + c;
    stringstream ss;
    ss << hex << setw(32) << setfill('0') << h;
    string r = ss.str();
    while (r.size() < 32) r = r + r;
    return r.substr(0, 32);
}
bool _volt_hsh_cmp(string raw, string hashed) {
    return _volt_sha256(raw) == hashed;
}
"""},
    "hsh_md5": {"cpp": "_volt_hsh_md5({0})",   "include": [], "args": 1},
    "hsh_cmp": {"cpp": "_volt_hsh_cmp({0},{1})","include": [], "args": 2},
}

# ---------------------------------------------------------------
# 12. Auth / JWT (use ath)
# ---------------------------------------------------------------
VOLT_ATH_FUNCTIONS = {
    "ath_tok": {"cpp": "_volt_gen_token({0})", "include": ["<string>","<sstream>","<ctime>"], "args": 1,
        "helper": """
string _volt_gen_token(string user) {
    time_t t = time(nullptr);
    stringstream ss;
    ss << "vlt." << user << "." << t << ".";
    unsigned long h = 5381;
    string base = user + to_string(t);
    for (char c : base) h = ((h << 5) + h) + c;
    stringstream hs;
    hs << hex << h;
    ss << hs.str();
    return ss.str();
}
bool _volt_ath_verify(string token, string user) {
    return token.find("vlt." + user + ".") == 0;
}
string _volt_ath_user(string token) {
    size_t s = token.find('.') + 1;
    size_t e = token.find('.', s);
    return token.substr(s, e - s);
}
"""},
    "ath_vfy": {"cpp": "_volt_ath_verify({0},{1})", "include": [], "args": 2},
    "ath_usr": {"cpp": "_volt_ath_user({0})",       "include": [], "args": 1},
}

# ---------------------------------------------------------------
# 13. Logger (use log)
# ---------------------------------------------------------------
VOLT_LOG_FUNCTIONS = {
    "log_inf": {"cpp": '_volt_log("INFO", {0})',  "include": ["<iostream>","<string>","<ctime>"], "args": 1,
        "helper": """
void _volt_log(string level, string msg) {
    time_t t = time(nullptr);
    char buf[20];
    strftime(buf, sizeof(buf), "%H:%M:%S", localtime(&t));
    cout << "[" << buf << "] [" << level << "] " << msg << endl;
}
"""},
    "log_err": {"cpp": '_volt_log("ERROR", {0})', "include": [], "args": 1},
    "log_wrn": {"cpp": '_volt_log("WARN", {0})',  "include": [], "args": 1},
    "log_dbg": {"cpp": '_volt_log("DEBUG", {0})', "include": [], "args": 1},
    "log_fil": {"cpp": '_volt_log_file({0},{1})',  "include": ["<fstream>","<string>"], "args": 2,
        "helper": "void _volt_log_file(string path, string msg){ofstream f(path,ios::app);f<<msg<<\"\\n\";f.close();}"},
}

# ---------------------------------------------------------------
# 14. Environment (use env)
# ---------------------------------------------------------------
VOLT_ENV_FUNCTIONS = {
    "env_get": {"cpp": "_volt_env_get({0})",       "include": ["<cstdlib>","<string>"], "args": 1,
        "helper": "string _volt_env_get(string k){char* v=getenv(k.c_str());return v?string(v):\"\";}"},
    "env_set": {"cpp": "_volt_env_set({0},{1})",   "include": ["<cstdlib>","<string>"], "args": 2,
        "helper": "void _volt_env_set(string k,string v){setenv(k.c_str(),v.c_str(),1);}"},
    "env_has": {"cpp": "(getenv({0}.c_str())!=nullptr)", "include": ["<cstdlib>","<string>"], "args": 1},
    "env_prt": {"cpp": "_volt_env_get(\"PORT\")",  "include": [], "args": 0},
    "env_hst": {"cpp": "_volt_env_get(\"HOST\")",  "include": [], "args": 0},
    "env_mod": {"cpp": "_volt_env_get(\"MODE\")",  "include": [], "args": 0},
}

# ---------------------------------------------------------------
# 15. Cache (use cch)
# ---------------------------------------------------------------
VOLT_CCH_FUNCTIONS = {
    "cch_set": {"cpp": "_volt_cache_set({0},{1})", "include": ["<string>","<map>"], "args": 2,
        "helper": """
map<string,string> _volt_cache;
void _volt_cache_set(string k, string v) { _volt_cache[k] = v; }
string _volt_cache_get(string k) { return _volt_cache.count(k) ? _volt_cache[k] : ""; }
bool _volt_cache_has(string k) { return _volt_cache.count(k) > 0; }
void _volt_cache_del(string k) { _volt_cache.erase(k); }
void _volt_cache_clr() { _volt_cache.clear(); }
int _volt_cache_siz() { return (int)_volt_cache.size(); }
"""},
    "cch_get": {"cpp": "_volt_cache_get({0})",   "include": [], "args": 1},
    "cch_has": {"cpp": "_volt_cache_has({0})",   "include": [], "args": 1},
    "cch_del": {"cpp": "_volt_cache_del({0})",   "include": [], "args": 1},
    "cch_clr": {"cpp": "_volt_cache_clr()",      "include": [], "args": 0},
    "cch_siz": {"cpp": "_volt_cache_siz()",      "include": [], "args": 0},
}

# =================================================================
#  ⚡ Library Registry
# =================================================================
VOLT_LIBRARIES = {
    "math": {"functions": VOLT_MATH_FUNCTIONS, "constants": VOLT_MATH_CONSTANTS},
    "fil":  {"functions": VOLT_FILE_FUNCTIONS,  "constants": {}},
    "str":  {"functions": VOLT_STR_FUNCTIONS,   "constants": {}},
    "tim":  {"functions": VOLT_TIME_FUNCTIONS,  "constants": {}},
    "sys":  {"functions": VOLT_SYS_FUNCTIONS,   "constants": {}},
    "net":  {"functions": VOLT_NET_FUNCTIONS,   "constants": {}},
    "srv":  {"functions": VOLT_SRV_FUNCTIONS,   "constants": {}},
    "rte":  {"functions": VOLT_RTE_FUNCTIONS,   "constants": {}},
    "db":   {"functions": VOLT_DB_FUNCTIONS,    "constants": {}},
    "jsn":  {"functions": VOLT_JSN_FUNCTIONS,   "constants": {}},
    "hsh":  {"functions": VOLT_HSH_FUNCTIONS,   "constants": {}},
    "ath":  {"functions": VOLT_ATH_FUNCTIONS,   "constants": {}},
    "log":  {"functions": VOLT_LOG_FUNCTIONS,   "constants": {}},
    "env":  {"functions": VOLT_ENV_FUNCTIONS,   "constants": {}},
    "cch":  {"functions": VOLT_CCH_FUNCTIONS,   "constants": {}},
}

# =================================================================
#  ⚡ Transpiler Utilities
# =================================================================
def transpile_line(line, active_libs):
    for lib_name in active_libs:
        lib = VOLT_LIBRARIES.get(lib_name, {})
        for const, val in lib.get("constants", {}).items():
            line = re.sub(rf'\b{const}\b', val, line)
        for fn_name, fn_data in lib.get("functions", {}).items():
            pattern = rf'{fn_name}\(([^)]*)\)'
            match = re.search(pattern, line)
            if match:
                args_str = match.group(1)
                args = [a.strip() for a in args_str.split(",")] if args_str.strip() else []
                cpp_call = fn_data["cpp"].format(*args)
                line = line.replace(match.group(0), cpp_call)
            elif fn_name + "()" in line:
                line = line.replace(fn_name + "()", fn_data["cpp"].format())
    return line

def collect_includes(source, active_libs):
    includes = set()
    for lib_name in active_libs:
        lib = VOLT_LIBRARIES.get(lib_name, {})
        for fn_name, fn_data in lib.get("functions", {}).items():
            if fn_name in source:
                for inc in fn_data.get("include", []):
                    includes.add(inc)
    return sorted(includes)

def collect_helpers(source, active_libs):
    helpers, seen = [], set()
    for lib_name in active_libs:
        lib = VOLT_LIBRARIES.get(lib_name, {})
        for fn_name, fn_data in lib.get("functions", {}).items():
            if fn_name in source and "helper" in fn_data:
                h = fn_data["helper"]
                if h not in seen:
                    helpers.append(h)
                    seen.add(h)
    return helpers

# =================================================================
#  ⚡ Volt Compiler Core
# =================================================================
class VoltCompiler:
    def __init__(self, source_code):
        self.source_code = source_code
        self.cpp_lines = []
        self.has_string = False
        self.has_math = False
        self.active_libs = set()
        self.in_block = False

    def compile(self):
        body_lines = []
        lines = self.source_code.split('\n')

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # استيراد المكتبات
            if stripped.startswith('use '):
                lib = stripped[4:].strip()
                if lib in VOLT_LIBRARIES:
                    self.active_libs.add(lib)
                    print(f"[Volt] Library loaded: {lib}")
                else:
                    print(f"[Volt Warning] Unknown library: '{lib}'")
                continue

            # إغلاق البلوكات
            if self.in_block and not line.startswith('    '):
                body_lines.append("    }")
                self.in_block = False

            cmd = stripped
            if self.active_libs:
                cmd = transpile_line(cmd, self.active_libs)

            # 1. ifs
            if cmd.startswith('ifs ') and cmd.endswith(':'):
                body_lines.append(f"    if ({cmd[4:-1].strip()}) {{")
                self.in_block = True
            # 2. elf
            elif cmd.startswith('elf ') and cmd.endswith(':'):
                body_lines.append(f"    }} else if ({cmd[4:-1].strip()}) {{")
                self.in_block = True
            # 3. els
            elif cmd == 'els:':
                body_lines.append("    } else {")
                self.in_block = True
            # 4. lop
            elif cmd.startswith('lop ') and cmd.endswith(':'):
                times = cmd[4:-1].strip()
                body_lines.append(f"    for (int _i{i}=0; _i{i}<{times}; ++_i{i}) {{")
                self.in_block = True
            # 5. ext
            elif cmd == 'ext':
                ind = "        " if self.in_block else "    "
                body_lines.append(f"{ind}return 0;")
            # 6. inp
            elif cmd.startswith('inp ') and ':' in cmd:
                ind = "        " if self.in_block else "    "
                self.has_string = True
                parts = cmd[4:].split(':', 1)
                body_lines.append(f"{ind}cout << {parts[0].strip()};")
                body_lines.append(f"{ind}string {parts[1].strip()};")
                body_lines.append(f"{ind}cin >> {parts[1].strip()};")
            # 7. تعريف متغيرات
            elif cmd.startswith(('str ', 'num ', 'flt ', 'var ')) and '=' in cmd:
                ind = "        " if self.in_block else "    "
                tok = cmd.split(' ')[0]
                rest = cmd[len(tok):].strip()
                var, val = rest.split('=', 1)
                var, val = var.strip(), val.strip()
                if any(m in val for m in ["sqrt(","pow(","abs("]): self.has_math = True
                ctype = {"str":"string","num":"int","flt":"double","var":"auto"}.get(tok,"auto")
                if tok == "str": self.has_string = True
                body_lines.append(f"{ind}{ctype} {var} = {val};")
            # 8. تخصيص تلقائي
            elif '=' in cmd and not cmd.startswith(('ifs','elf')):
                ind = "        " if self.in_block else "    "
                var, val = cmd.split('=', 1)
                body_lines.append(f"{ind}auto {var.strip()} = {val.strip()};")
            # 9. out
            elif cmd.startswith('out '):
                ind = "        " if self.in_block else "    "
                content = cmd[4:].strip()
                if (content.startswith('"') and content.endswith('"')) or \
                   (content.startswith("'") and content.endswith("'")):
                    self.has_string = True
                body_lines.append(f"{ind}cout << {content} << endl;")
            else:
                print(f"Syntax Error: Unknown command -> '{stripped}'")
                return None

        if self.in_block:
            body_lines.append("    }")

        # بناء C++
        self.cpp_lines.append("#include <iostream>")
        if self.has_string: self.cpp_lines.append("#include <string>")
        if self.has_math:   self.cpp_lines.append("#include <cmath>")
        for inc in collect_includes(self.source_code, self.active_libs):
            h = f"#include {inc}"
            if h not in self.cpp_lines: self.cpp_lines.append(h)
        self.cpp_lines.append("using namespace std;\n")
        for h in collect_helpers(self.source_code, self.active_libs):
            self.cpp_lines.append(h)
        self.cpp_lines.append("")
        self.cpp_lines.append("int main() {")
        self.cpp_lines.extend(body_lines)
        self.cpp_lines.append("    return 0;")
        self.cpp_lines.append("}")
        return "\n".join(self.cpp_lines)

# =================================================================
#  ⚡ Volt Ecosystem Runner
# =================================================================
def run_volt_ecosystem():
    target = "app.vl"
    if not os.path.exists(target):
        print(f"[Volt Error] Source file '{target}' not found.")
        return

    with open(target, "r", encoding="utf-8") as f:
        source = f.read()

    print("⚡ Volt Language Engine v3.0 — Full Backend Edition")
    print("=" * 55)

    compiler = VoltCompiler(source)
    cpp_output = compiler.compile()
    if not cpp_output:
        print("[Volt Error] Compilation failed.")
        return

    cpp_file = "compiled_volt_core.cpp"
    with open(cpp_file, "w", encoding="utf-8") as f:
        f.write(cpp_output)

    compiled = False
    for cc in ["clang++", "g++"]:
        try:
            subprocess.run([cc, cpp_file, "-o", "volt_app"], check=True)
            print(f"\n[Volt Success] Built with {cc}!")
            print(f"[Volt] Active libraries: {', '.join(compiler.active_libs)}")
            print("=" * 55)
            print("RUN: ./volt_app")
            print("=" * 55)
            compiled = True
            break
        except FileNotFoundError:
            continue
    if not compiled:
        print("[Volt Error] No C++ compiler found.")

if __name__ == "__main__":
    run_volt_ecosystem()
