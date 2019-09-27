/*
  Common code for Gust (Koei/Tecmo) PC games tools
  Copyright © 2019 VitaSmith

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "util.h"

bool create_path(char* path)
{
    bool result = true;
    struct stat st;
    if (stat(path, &st) != 0) {
        // Directory doesn't exist, create it
        size_t pos = 0;
        for (size_t n = strlen(path); n > 0; n--) {
            if (path[n] == PATH_SEP) {
                pos = n;
                break;
            }
        }
        if (pos > 0) {
            // Create parent dirs
            path[pos] = 0;
            char* new_path = malloc(strlen(path) + 1);
            if (new_path == NULL) {
                fprintf(stderr, "ERROR: Can't allocate path\n");
                return false;
            }
            strcpy(new_path, path);
            result = create_path(new_path);
            free(new_path);
            path[pos] = PATH_SEP;
        }
        // Create node
        if (result)
            result = CREATE_DIR(path);
    } else if (!S_ISDIR(st.st_mode)) {
        fprintf(stderr, "ERROR: '%s' exists but isn't a directory\n", path);
        return false;
    }

    return result;
}
