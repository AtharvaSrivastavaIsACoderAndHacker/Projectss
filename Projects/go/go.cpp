#include<iostream>
#include<string>
#include<fstream>
#include<sys/stat.h>
#include<vector>
#include<algorithm>
#include<cstdlib>
#include<windows.h>
#include<unistd.h>
#include <limits>


std::string getExeDir() {
    char path[MAX_PATH];
    GetModuleFileNameA(NULL, path, MAX_PATH);
    std::string exePath(path);
    size_t pos = exePath.find_last_of("\\/");
    return exePath.substr(0, pos);
}

bool pathExists(const std::string& path) {
    struct stat info;
    if (stat(path.c_str(), &info) != 0) {
        return false;
    }
    return (info.st_mode & (S_IFDIR | S_IFREG)) != 0;
}

std::string normalizePath(std::string path) {
    std::replace(path.begin(), path.end(), '\\', '/');
    while (path.size() > 3 && path.back() == '/') {
        path.pop_back();
    }
    return path;
}

bool fileExists(const std::string& filename) {
    std::ifstream file(filename);
    return file.good();
}

std::vector<std::pair<std::string, std::string>> getAliases(const std::string& path) {
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

int main(int argc, char const *argv[]) {

    
    char executablePath[512];
    strcpy(executablePath, getExeDir().c_str());
    strcat(executablePath,"\\Dependencies"); // constructing path
    struct stat sb;
    if (stat(executablePath, &sb) != 0) CreateDirectoryA(executablePath, NULL); // create dir if it doesn't exist !
    

    
    if(argc == 1){
        return 0;
    }

    std::string rel = getExeDir() + "\\Dependencies\\goAliasesFile.txt";

    if(!fileExists(rel)){
        std::fstream file;
        file.open(rel, std::ios::out | std::ios::app);
        file.close();
    }
    
    std::vector<std::pair<std::string, std::string>> aliases = getAliases(rel);
    
    if (argc > 1 && std::string(argv[1]) == "alias") {
        if (argc < 4) {
            std::cerr << "2 args needed to create an alias !" << std::endl;
            std::cerr << "'alias' command needs an arg with an alias name, and another arg as the path to link with that alias name" << std::endl;
        }
        else{
            std::string path = normalizePath(std::string(argv[3]));

                auto it = std::find_if(aliases.begin(), aliases.end(),[&](const std::pair<std::string, std::string>& alias) {return alias.first == std::string(argv[2]);});
                if(it==aliases.end()){
                    std::fstream file(rel, std::ios::in | std::ios::out | std::ios::app);

                    file.seekg(0, std::ios::end);
                    bool hasContent = file.tellg() > 0;

                    if (hasContent) file << "\n";
                    file << argv[2] << " " << argv[3];
                    file.close();
                }
                else{
                    std::cerr << "alias exists ! duplicate alias names not allowed !" << std::endl;
                }
        }
    }
    
    if (argc > 1) {
        auto it = std::find_if(aliases.begin(), aliases.end(),[&](const std::pair<std::string, std::string>& alias) {return alias.first == std::string(argv[1]);});
        if(it!=aliases.end()){
            std::string path = it->second;
            std::replace(path.begin(), path.end(), '/', '\\');
            std::string cmd = "start \"\" powershell -NoExit -Command \"cd \\\"" + path + "\\\"\"";


            system(cmd.c_str());
            // std::cout<<cmd;
        }
    }

    return 0;
}
