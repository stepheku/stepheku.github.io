import glob
import os

post_dir = "./_posts/"
tag_dir = "./tag/"

file_names = glob.glob(f"{post_dir}*.md")

total_tags = []

for file_name in file_names:
    with open(file_name, "r") as f:
        crawl = False
        for line in f.readlines():
            if crawl:
                current_tags = line.strip().split()
                if current_tags[0] == "tags:":
                    total_tags.extend(current_tags[1:])
                    crawl = False
                    break
                else:
                    continue
                
            if line.strip() == "---":
                if not crawl:
                    crawl = True
                else:
                    crawl = False
                    break

total_tags = set(total_tags)

old_tags = glob.glob(f"{tag_dir}*.md")
for tag in old_tags:
    os.remove(tag)

if not os.path.exists(tag_dir):
    os.makedirs(tag_dir)

for tag in total_tags:
    tag_file_name = f"{tag_dir}{tag}.md"
    with open(tag_file_name, "a") as f:
        f.write(f"---\nlayout: tagpage\ntitle: \"Tag: {tag}\"\ntag: {tag}\nrobots: noindex\n---\n")

# Create index tag page
tag_index_page = f"{tag_dir}index.md"

with open(tag_index_page, "w") as f:
    f.write(f"---\nlayout: page\ntitle: \"Tags index\"\nrobots: noindex\n---\n")
    f.write(f"All tags available: <br>")
    for tag in sorted(total_tags):
        f.write(f" <a href=\"/tag/{tag}\"><code class=\"highligher-rouge\"><nobr>{tag}</nobr></code>&nbsp;</a><br>")


print(f"Tags generated, count: {len(total_tags)}")