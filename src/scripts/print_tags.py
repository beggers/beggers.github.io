import os

# !!!!!!
# Don't run this script from the scripts/ directory. If you do, it won't
# be able to find _posts/. Instead, run it from .. (src/) via the softlink.
# Or, better yet, don't use this directly and instead use ../new_post.
#
# This is also gross and brittle, but it meets my requirements exactly and
# nobody else will use it.
# !!!!!!

POSTS_DIR='./_posts/'

def main():
    tags = set()
    for fname in os.listdir(POSTS_DIR):
        f = open(POSTS_DIR + fname)
        for line in f.readlines():
            if 'tags:' in line:
                # Horrible, horrible stuff here.
                tags.update(line[6:-1].replace(",", "").replace("[", "").replace("]", "").split(" "))
                break
    print(list(tags))

main()
