# gust_ebm - Ebm file processor for Gust (Koei/Tecmo) PC games
# Copyright © 2019 VitaSmith (for the orignal C version)
# Copyright © 2020 Xzonn

import json
import os
import struct
import sys

KEYS = ["type", "voice_id", "unknown1", "name_id", "extra_id", "expr_id", "msg_id", "unknown2", "msg_length"];
VERSION = "0.1";

def ebmToJson(path):
    assert os.path.exists(path);
    with open(path, "rb") as f:
        data = f.read();
    name = path;
    nb_messages, = struct.unpack("<L", data[0:4]);
    pos = 4;
    messages = [];
    for i in range(nb_messages):
        d = struct.unpack("<9L", data[pos: pos + 36]);
        msg_string = data[pos + 36: pos + 36 + d[8] - 1].decode("utf-8");
        pos += 36 + d[8];
        m = dict(zip(KEYS, d));
        m.update({
            "msg_string": msg_string
        });
        messages.append(m);
    jdata = dict(zip(["name", "nb_messages", "messages"], [name, nb_messages, messages]));
    with open(os.path.splitext(path)[0] + ".json", "w", encoding = "utf-8") as f:
        json.dump(jdata, f, ensure_ascii = False, indent = 4);

def jsonToEbm(path):
    assert os.path.exists(path);
    with open(path, encoding = "utf-8") as f:
        data = json.load(f);
    nb_messages = data["nb_messages"];
    messages = data["messages"];
    byteData = list(struct.pack("<L", nb_messages));
    for i in messages:
        m = [i[k] for k in KEYS];
        s = i["msg_string"].encode("utf-8");
        m[8] = len(s) + 1
        byteData += list(struct.pack("<9L", *m));
        byteData += list(s) + [0];
    with open(os.path.splitext(path)[0] + ".ebm", "wb") as f:
        f.write(bytes(byteData));

if __name__ == "__main__":
    argv = sys.argv[1:];
    if len(argv):
        for i in argv:
            if i.lower().endswith(".ebm"):
                ebmToJson(i);
            elif i.lower().endswith(".json"):
                jsonToEbm(i);
    else:
        name = os.path.basename(sys.argv[0]);
        print(("%s %s (c) 2019 VitaSmith / (c) 2020 Xzonn\n\n" + 
               "Usage: %s <file>\n\n" +
               "Convert a .ebm file to or from an editable JSON file.") % (name, VERSION, name));
