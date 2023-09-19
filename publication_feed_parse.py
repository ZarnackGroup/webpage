import feedparser
NewsFeed = feedparser.parse("https://pubmed.ncbi.nlm.nih.gov/rss/search"
                            "/1jue2dFuI_LFj_phV9s9PjTEhPInBPr1NTb858Yzvn1De2GMXv/?limit=5000&utm_campaign=pubmed-2&fc"
                            "=20230630074326")

with open("publications.qmd", "w", encoding='utf-8') as quarto_out:
    quarto_out.write('---\ntitle: "Publications"\n---\n')
    for entry in NewsFeed.entries:
        author_list = []
        title = entry["title"]
        link = entry["link"]
        publish_time = entry["published"].split(" ")
        time_string = publish_time[1] + " " + publish_time[2] + " " + publish_time[3]
        paper_string = entry["dc_source"] + ", " + entry["dc_identifier"] + ", " + time_string
        for i in entry["authors"]:
            author_list.append(i["name"])

        author_string = ", ".join(author_list)
        out_string = "  \n" + author_string + "  \n" + title + "  \n" + paper_string + "  \n" + link + "  \n"
        quarto_out.write(str(out_string))




