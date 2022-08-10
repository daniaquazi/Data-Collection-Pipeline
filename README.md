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
- S3 - My scraper will be running in headless mode so I will not be able to see exactly what is going on so in each of my methods, I send pictures to a bucket so I am able to see debug my code if anything goes wrong.
- RDS - After I have collected my comments, I added them into a dataframe because I wanted the data to be in the form of a table. After, I can send this data to an RDS.

- boto3 - In order to access the AWS services, S3 and RDS, I used a library called boto3 which allowed the management of AWS services.

Milestone 7
- I installed docker and containerized my scraper so that it can be run in an EC2 instance. 
- I made sure to run my scraper in headless mode (so that it runs in the background).
- After making sure my code works and containerizing my scraper, I created a new EC2 instance to run it. I decided to add a cronjob so that it is able to run everyday at a specific time.

Milestone 8
- In this milestone, I set up prometheus so that certain meteric could be collected e.g. which containers are running at the moment and which containers have stopped.
- I created a Grafana dashboard so that I could convert my metrics into different visualizations which made the metrics easier to read.

Milestone 9
- After committing my most recent code to Github, I set up a workflow in which my scraper could be built and pushed to Docker Hub.

<img width="640" alt="image" src="https://user-images.githubusercontent.com/46778501/184010681-0720b2ce-abca-4d1e-8cf0-09b025127539.png">

