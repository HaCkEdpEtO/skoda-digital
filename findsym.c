#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>
#include <string.h>
#include <sys/stat.h>
#include <limits.h>

void find_symbolic_links(const char *path, const char *target_file) {
    DIR *dir = opendir(path);
    if (dir == NULL) {
        perror("opendir");
        return;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }

        char entry_path[PATH_MAX];
        snprintf(entry_path, sizeof(entry_path), "%s/%s", path, entry->d_name);

        struct stat entry_stat;
        if (lstat(entry_path, &entry_stat) == -1) {
            perror("lstat");
            continue;
        }

        if (S_ISLNK(entry_stat.st_mode)) {
            char link_target[PATH_MAX];
            ssize_t len = readlink(entry_path, link_target, sizeof(link_target) - 1);
            if (len == -1) {
                perror("readlink");
                continue;
            }
            link_target[len] = '\0';

            if (strcmp(link_target, target_file) == 0) {
                printf("%s -> %s\n", entry_path, link_target);
            }
        } else if (S_ISDIR(entry_stat.st_mode)) {
            find_symbolic_links(entry_path, target_file);
        }
    }

    closedir(dir);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <directory> <target_file>\n", argv[0]);
        return 1;
    }

    find_symbolic_links(argv[1], argv[2]);

    return 0;
}
