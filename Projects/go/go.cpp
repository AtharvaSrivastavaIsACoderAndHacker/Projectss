#include<iostream>
#include<string>
#include<fstream>
#include<sys/stat.h>
#include<vector>
#include<algorithm>
#include <cstdlib>

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

std::vector<std::pair<std::string, std::string>> getAliases(std::string path){
    std::fstream file;
    file.open(path, std::ios::in);
    std::vector<std::pair<std::string, std::string>> aliases = {};
    std::string str1, str2;
    while(!file.eof()){
        file>>str1>>str2;
        if(std::string(str1) != "" && std::string(str2) != ""){
            std::pair<std::string, std::string> p = {str1,str2};
            aliases.push_back(p);
        }
        getline(file, str2);
    }
    file.close();
    
    return aliases;
}



int main(int argc, char const *argv[]) {

    
    if(!fileExists("Dependencies\\goAliasesFile.txt")){
        std::fstream file;
        file.open("Dependencies\\goAliasesFile.txt", std::ios::in | std::ios::out);
        file.close();
    }
    
    std::vector<std::pair<std::string, std::string>> aliases = getAliases("Dependencies\\goAliasesFile.txt");
    
    if (argc > 1 && std::string(argv[1]) == "alias") {
        if (argc < 4) {
            std::cerr << "2 args needed to create an alias !" << std::endl;
            std::cerr << "'alias' command needs an arg with an alias name, and another arg as the path to link with that alias name" << std::endl;
        }
        else{
            std::string path = normalizePath(std::string(argv[3]));
            if(pathExists(path)){
                auto it = std::find_if(aliases.begin(), aliases.end(),[&](const std::pair<std::string, std::string>& alias) {return alias.first == std::string(argv[2]);});
                if(it==aliases.end()){
                    std::fstream file;
                    file.open("Dependencies\\goAliasesFile.txt", std::ios::in | std::ios::out | std::ios::app);
                    file<<"\n"<<std::string(argv[2])<<" "<<std::string(argv[3]);
                    file.close();
                }
                else{
                    std::cerr << "alias exists ! duplicate alias names not allowed !" << std::endl;
                }
            }
            else{
                std::cerr << "provided path doesn't exist !" << std::endl;
            }
        }
    }
    
    if (argc > 1) {
        auto it = std::find_if(aliases.begin(), aliases.end(),[&](const std::pair<std::string, std::string>& alias) {return alias.first == std::string(argv[1]);});
        if(it!=aliases.end()){
            std::string cmd = "start powershell.exe /K \"cd /d " + it->second + "\"";
            system(cmd.c_str());
        }
    }

    return 0;
}
