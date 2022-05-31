def append_to_txt(link, filename):

  print(f'Appending link to {filename}')
  with open(filename, 'a') as f:
    f.write(link)
    f.write('\n')

def join_all_scrape_results(scrape_results):

    lst = []

    for i in scrape_results:
        lst.append(i)

    out = []
    for sublist in lst:
        out.extend(sublist)

    return out
