# Data-Collection-Pipeline

![image](https://user-images.githubusercontent.com/46778501/182449479-5f89fd2d-b23b-4212-93eb-be95890effc0.png)


Milestone 1
- I decided to scrape the Instagram website. I want to create a scraper bot that is able to get the links of the most recent posts and using this, retrieve the comments.

Milestone 2
- I have written code using selenium in order to perform certain actions automatically.
    - Accepting cookies: When loading the instagram website, a pop up appears saying to accept cookies. So, I have written code in order to automatically accept cookies.
    - Saving information: Another popup which asks the user to save login information appears so if accepted, the user does not have to login with their user name and password next time. So I have written code in order to bypass this.
    - Login: In order to navigate through the instagram website, a user has to login. I have hard coded my username and password in the code that I have written, so it will automatically enter in a username and password and click on the "login" button.
    - Getting the URLS: This function can navigate to an instagram page and retrieve the URLS of recent instagram posts. 
        - In the HTML, there are around 30 posts that are visible, so instagram will retrieve the URLS of all 30. When these are retrieved, the URLS are listed in a random order, so in order to only analyse the three most recent posts, I scrape the dates of when the posts were uploaded, sort values by descending order, and finally slice the dataframe so only the top 3 exist.

- Technologies used: Pandas in order to convert a list into a dataframe to sort URLS in descending order.

Milestone 3
- Scraping comments
    - I have created a function that scrapes the public comments of a post.
        - This function will use the returned result of the "Get URLS" function. (The returned result is the three recent URLS.) The code that I have written will navigate to the URLS and retrieve all the comments of a post (even ones that are hidden and can only be accessed if a "Load more" button is clicked). These comments are then appended to a list which is then converted into a dataframe.
- Unique UUIDs
    - I have written a function that gives each unique URL a UUID so these can be distinguished just in case there 2 or more URLS are similar. To do this, I used the UUID library which randomly generates a UUID.
    - In the "Get URLS" function, to make sure URLs are unique, I have converted the list into a set in order to remove duplicates.

Milestone 4
- I have created unit tests i order to show that my code works.
- 1st unit test- test login: testing wrong log in details to check if it fails.
- 2nd unit test- dump products: test if a file directory exists.
- 3rd unit test- scrape comments: testing to see if comments can be scraped.
- 4th unit test- get urls: testing to see if a URL exists.

Milestone 5
- Talk about the cloud services you have used and how you interact with them in your code using boto3.
Milestone 7
- Talk about docker and how it works, your code refactorisation and the techniques you used to avoid rescraping data.
Milestone 8
- talk about prometheus and grafana
Milestone 9
- Talk about CI/CD pipelines and the process you have developed.
