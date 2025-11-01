<<<<<<< HEAD
def get_user_input():
    """Get citation information from the user."""
    author = input("Enter the author's name (Last, First): ")
    title = input("Enter the title of the work: ")
    date = input("Enter the publication date (YYYY-MM-DD): ")
    link = input("Enter the URL (press Enter if none): ")
    publisher = input("Enter the publisher (press Enter if none): ")
    
    return {
        "author": author,
        "title": title,
        "date": date,
        "link": link,
        "publisher": publisher
    }

def format_apa(citation_info):
    """Format citation in APA style."""
    author = citation_info["author"]
    year = citation_info["date"].split("-")[0]
    title = citation_info["title"]
    publisher = citation_info["publisher"]
    link = citation_info["link"]
    
    citation = f"{author} ({year}). {title}."
    if publisher:
        citation += f" {publisher}."
    if link:
        citation += f" Retrieved from {link}"
    
    return citation

def format_mla(citation_info):
    """Format citation in MLA style."""
    author = citation_info["author"]
    title = citation_info["title"]
    publisher = citation_info["publisher"]
    date = citation_info["date"]
    link = citation_info["link"]
    
    citation = f"{author}. \"{title}.\""
    if publisher:
        citation += f" {publisher},"
    citation += f" {date}"
    if link:
        citation += f". {link}"
    citation += "."
    
    return citation

def format_asa(citation_info):
    """Format citation in ASA style."""
    author = citation_info["author"]
    year = citation_info["date"].split("-")[0]
    title = citation_info["title"]
    publisher = citation_info["publisher"]
    link = citation_info["link"]
    
    citation = f"{author}. {year}. \"{title}.\""
    if publisher:
        citation += f" {publisher}."
    if link:
        citation += f" Retrieved {citation_info['date']} ({link})."
    
    return citation

def main():
    print("Welcome to the Citation Formatter!")
    print("\nPlease enter the source information:")
    
    citation_info = get_user_input()
    
    while True:
        print("\nChoose the citation format:")
        print("1. APA")
        print("2. MLA")
        print("3. ASA")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            print("\nAPA Format:")
            print(format_apa(citation_info))
        elif choice == "2":
            print("\nMLA Format:")
            print(format_mla(citation_info))
        elif choice == "3":
            print("\nASA Format:")
            print(format_asa(citation_info))
        elif choice == "4":
            print("\nThank you for using Citation Formatter!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
=======
print("Hello World")
>>>>>>> 637225f6574357aa39e262e854834b4c9cd4dfb5
