def get_article_count(total_articles):
    try:
        count = int(input("How many articles would you like to summarize? "))

        if count <= 0:
            print("Please enter a number greater than 0.")
            return None

        if count > total_articles:
            print(f"\nOnly {total_articles} articles are available.")
            print(f"Summarizing all {total_articles} articles.\n")
            return total_articles

        return count

    except ValueError:
        print("Please enter a valid number.")
        return None