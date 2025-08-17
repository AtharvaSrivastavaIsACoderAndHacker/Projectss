#include<iostream>
#include<string>
#include<fstream>
#include<sys/stat.h>
#include<vector>
#include<algorithm>
#include<cstdlib>
#include<windows.h>
#include<unistd.h>
#include<ctime>
#include"picosha2.h"
#include <windows.h>

using namespace std;

std::string getFolderName(const std::string& path) {
    size_t end = path.find_last_not_of("\\/"); // ignore trailing slash
    if (end == std::string::npos) return "";

    size_t pos = path.find_last_of("\\/", end);
    if (pos == std::string::npos) return path.substr(0, end + 1);

    return path.substr(pos + 1, end - pos);
}

bool isDirectory(const std::string& path) {
    DWORD attrs = GetFileAttributesA(path.c_str());
    return (attrs != INVALID_FILE_ATTRIBUTES) && (attrs & FILE_ATTRIBUTE_DIRECTORY);
}

std::string fileHash(const std::string& filepath) {
    std::ifstream file(filepath, std::ios::binary);
    if (!file) return "";

    std::vector<unsigned char> buffer(std::istreambuf_iterator<char>(file), {});
    std::vector<unsigned char> hash(picosha2::k_digest_size);
    picosha2::hash256(buffer.begin(), buffer.end(), hash.begin(), hash.end());
    return picosha2::bytes_to_hex_string(hash.begin(), hash.end());
}

void listFilesRecursively(const std::string& folder, std::vector<std::string>& files) {
    WIN32_FIND_DATAA findData;
    HANDLE hFind;

    std::string search = folder + "\\*";
    hFind = FindFirstFileA(search.c_str(), &findData);
    if (hFind == INVALID_HANDLE_VALUE) return;

    do {
        std::string name = findData.cFileName;
        if (name == "." || name == "..") continue;

        std::string fullPath = folder + "\\" + name;
        if (findData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
            listFilesRecursively(fullPath, files);
        } else {
            files.push_back(fullPath);
        }
    } while (FindNextFileA(hFind, &findData));
    FindClose(hFind);
}

std::string folderHash(const std::string& folderPath) {
    std::vector<std::string> files;
    listFilesRecursively(folderPath, files);
    std::sort(files.begin(), files.end());

    std::string combinedHashes;
    for (const auto& f : files) {
        combinedHashes += fileHash(f);
    }

    std::vector<unsigned char> hash(picosha2::k_digest_size);
    picosha2::hash256(combinedHashes.begin(), combinedHashes.end(), hash.begin(), hash.end());
    return picosha2::bytes_to_hex_string(hash.begin(), hash.end());
}

std::string getRoast() {
    static std::vector<std::string> roasts = {
        "read the damn readme u retard !",
        "ur brain is hollow as a lays packet :( .",
        "tum hi to ho agle linus torvalds. ",
        "aliases need 2 args, not your IQ score.",
        "error: user too dumb to use my program. solution: uninstall brain.",
        "sry bro, i shouldn't have expected brains from you. ", 
        "go search what's a damn readme on wiki. don't ask me abt what's wiki ! ",
        "bruh im damn sure you had a sieve when god handed out brains > ",
        "should i translate the readme into donkey-sound language ? you'll understand better that way. ",
        "this is ishi-certified dumbness."
    };

    static bool seeded = false;
    if (!seeded) {
        std::srand(std::time(nullptr));
        seeded = true;
    }

    int idx = std::rand() % roasts.size();
    return roasts[idx] + " u should be an apprentice of ISHI, she'll teach you how to be dumber !";
}

string getExeDir() {
    char path[MAX_PATH];
    GetModuleFileNameA(NULL, path, MAX_PATH);
    string exePath(path);
    size_t pos = exePath.find_last_of("\\/");
    return exePath.substr(0, pos);
}

bool pathExists(const string& path) {
    struct stat info;
    if (stat(path.c_str(), &info) != 0) {
        return false;
    }
    return (info.st_mode & (S_IFDIR | S_IFREG)) != 0;
}

string normalizePath(string path) {
    replace(path.begin(), path.end(), '\\', '/');
    while (path.size() > 3 && path.back() == '/') {
        path.pop_back();
    }
    return path;
}

bool fileExists(const string& filename) {
    ifstream file(filename);
    return file.good();
}

vector<pair<string, string>> getAliases(string path){
    std::ifstream file(path);
    std::vector<std::pair<std::string, std::string>> aliases;
    std::string str1, str2;

    while (file >> str1 >> str2) {
        if (!str1.empty() && !str2.empty()) {
            aliases.emplace_back(str1, str2);
        }
        file.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    return aliases;
}

void ensureFileExists(const std::string& path) {
    ofstream(path, std::ios::app).close();
}

std::string getFileName(const std::string& fullPath) {
    size_t pos = fullPath.find_last_of("\\/");
    if (pos == std::string::npos)
        return fullPath; // no directory separator found
    return fullPath.substr(pos + 1);
}

std::string expandEnvVars(const std::string& input) {
    std::string cmd = "cmd /C echo " + input;
    char buffer[512];
    std::string result;
    
    FILE* pipe = _popen(cmd.c_str(), "r");
    if (!pipe) return input; // fallback to original string
    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        result += buffer;
    }
    _pclose(pipe);
    
    // remove trailing newline
    if (!result.empty() && result.back() == '\n') result.pop_back();
    
    return result;
}

int main(int argc, char const *argv[]) {

    char cwd[512];
    getcwd(cwd, sizeof(cwd)); // getting cwd
    struct stat sb;
    strcat(cwd,"\\Dependencies"); // constructing path
    if (stat(cwd, &sb) != 0) CreateDirectoryA(cwd, NULL); // create dir if it doesn't exist !
    
    // random value so that it's not equal by default
    string srcHash = "69";
    string destHash = "96";
    bool transmissionCancelled = false;

    string finalSrc;
    string finalDest;

    if(argc == 1){
        return 0;
    }
    
    string rel = getExeDir() + "\\Dependencies\\goAliasesFile.txt";

    if(!fileExists(rel)){
        std::fstream file;
        file.open(rel, std::ios::out | std::ios::app);
        file.close();
    }
    
    vector<pair<string, string>> aliases = getAliases(rel);
    
    if (argc > 1 && string(argv[1]) == "alias"){
        if (argc < 4) {
            cerr << "2 args needed to create an alias !" << endl;
            cerr << "'alias' command needs an arg with an alias name, and another arg as the path to link with that alias name" << endl;
        }
        else{
            string path = normalizePath(string(argv[3]));

                auto it = find_if(aliases.begin(), aliases.end(),[&](const pair<string, string>& alias) {return alias.first == string(argv[2]);});
                if(it==aliases.end()){
                    std::fstream file(rel, std::ios::in | std::ios::out | std::ios::app);

                    file.seekg(0, std::ios::end);
                    bool hasContent = file.tellg() > 0;

                    if (hasContent) file << "\n";
                    file << argv[2] << " " << argv[3];
                    file.close();
                }
                else{
                    cerr << "alias exists ! duplicate alias names not allowed !" << endl;
                }
            }
    }    
    if (argc <= 2) {
        std::cerr<<getRoast()<<std::endl;
    }
    if (argc > 1) {
        auto it = find_if(aliases.begin(), aliases.end(),[&](const pair<string, string>& alias) {return alias.first == string(argv[1]);});
        if(it!=aliases.end()){
            string dest = it->second;
            replace(dest.begin(), dest.end(), '/', '\\');
            if (dest.back() != '\\') dest += "\\";


            char src[512];
            getcwd(src, sizeof(src));
            string relPath;
            if (argc >= 3) {
                relPath = argv[2];
            } else {
                transmissionCancelled = true;
                relPath = "rtfm u retard ! -- ncu54t5gho8vhyn958gh45iofh82ygu34fbiou52b28ncf34";
            }
            replace(relPath.begin(), relPath.end(), '/', '\\');
            string source = string(src)+"\\"+relPath;


            // string cmd = "xcopy \"" + source + "\" \"" + dest + "\" /E /H /K /-Y /I /F";

            string cmd;
            if(isDirectory(source)){
                if (dest.back() == '\\') dest.pop_back();
                string destFolder = dest + "\\" + getFolderName(source);
                CreateDirectoryA(destFolder.c_str(), NULL);
                cmd = "xcopy \"" + source + "\" \"" + destFolder + "\\\" /E /H /K /-Y /I /F";
            } else {
                cmd = "xcopy \"" + source + "\" \"" + dest + "\" /H /K /-Y /F";
            }

            system(cmd.c_str());
            
            if(transmissionCancelled == false){
                if(isDirectory(source)){
                    finalSrc = normalizePath(source);
                    finalDest = normalizePath(expandEnvVars(dest + "\\" + getFolderName(source)));
                    srcHash = folderHash(finalSrc);
                    destHash = folderHash(finalDest);
                } else {
                    finalSrc = normalizePath(source);
                    finalDest = normalizePath(expandEnvVars(dest + (dest.back() == '\\' ? "" : "\\") + getFileName(source)));
                    srcHash = fileHash(finalSrc);
                    destHash = fileHash(finalDest);
                }
            }

            // cout<<cmd<<endl;
            // cout<<srcHash<<" and "<<destHash<<endl;
            // cout<<finalSrc<<" and "<<finalDest<<endl;
        }
    }
    
    // cout<<srcHash<<" and "<<destHash<<endl;
    if(srcHash!="69" && destHash!="96"){ // trasmission ocurred
        if(srcHash==destHash){
            cout<<"Transmission Occurred ! Hashes Match !"<<endl;
        }
        else{
            cout<<"Fatal : Transmission Occurred but Hashes DON'T Match ! The file was modified during move !"<<endl;
        }
    }


    return 0;
}