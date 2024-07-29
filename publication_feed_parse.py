# clean env
all_variables = locals()

# Iterate over all variable names and delete them
for var_name in list(all_variables.keys()):
    # Exclude special variables starting with '__' (e.g., '__name__', '__doc__')
    if not var_name.startswith('__'):
        del all_variables[var_name]
        
import feedparser
import os
import pickle

# Parse the RSS feed
NewsFeed = feedparser.parse("https://pubmed.ncbi.nlm.nih.gov/rss/search/1jue2dFuI_LFj_phV9s9PjTEhPInBPr1NTb858Yzvn1De2GMXv/?limit=5000&utm_campaign=pubmed-2&fc=20230630074326")

# Load old entries from a .pkl file
old_entries = []
if os.path.exists('old_entries.pkl'):
    with open('old_entries.pkl', 'rb') as f:
        old_entries = pickle.load(f)

# Collect existing URLs from the existing content
existing_titles = set(entry['title'] for entry in old_entries)

# Collect new entries that do not already exist
new_entries = []
for entry in NewsFeed.entries:
    title = entry["title"]
    
    # Check if the URL already exists
    if title not in existing_titles:
        author_list = [i["name"] for i in entry.get("authors", [])]
        author_string = ", ".join(author_list) if author_list else "No authors listed"
        title = entry["title"]
        link = entry["link"]
        publish_time = entry["published"].split(" ")
        time_string = publish_time[1] + " " + publish_time[2] + " " + publish_time[3]
        paper_string = entry["dc_source"] + ", "  + time_string + ", " + "[" + entry["dc_identifier"]+ "]" +"("+entry["link"]+")" 
        
        out_string = f"  \n{author_string}  \n**{title}**  \n{paper_string} \n"
        new_entries.append(out_string)
        existing_titles.add(title)  # Update existing URLs

# Write new entries to the QMD file
with open("publications.qmd", "a", encoding='utf-8') as qmd_file:
    for entry in new_entries:
        qmd_file.write(entry)

# Update the .pkl file with the combined entries
combined_entries = NewsFeed.entries
with open('old_entries.pkl', 'wb') as f:
    pickle.dump(combined_entries, f)


