def retrieveText(filename = "pyramus_monologue.txt"):
  """
  Retrieves the paragraph from a text file.
  """
  
  try:
    with open(filename, "r") as f:
      paragraph = f.read()
      print(f'successfully retrieved file: '+filename)
      return paragraph
  except OSError as e:
    print(f"Error retrieving paragraph from file: {e}")
    return "File not found"


def splitTextIntoList(text, char_limit=160):
  """
  Splits a paragraph into a list of sentences, so e-reader screen doesn't go over
  """

  words = text.split() #holds a list of words 
  list_of_text = []
  current_page = ''
  page_count = 1
    
  for word in words:
    if len(current_page) >= char_limit: #the current page will cap when the char limit is hit, and a new page will be added
      list_of_text.append(current_page)
      current_page = ''
      page_count = page_count + 1
    current_page += word + ' '

  # Add any remaining words to the last sentence
  if current_page:
    list_of_text.append(current_page)

  return list_of_text, page_count


def retrieveTextAsList(filename="pyramus_monologue.txt"):
    #grabs text from .txt file, then splits it into lists of a certain amount of characters
    text = retrieveText(filename)
    list, page_count = splitTextIntoList(text) #returns the list needed, and the number of pages
    return list, page_count
    


if __name__=="__main__":
    list, page_count = retrieveTextAsList()
    print(list)
    print(page_count)