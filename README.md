# Thought process:

First of all, I need to take a clean look of the data, and do some clicking on the URLs. The first thing I notice, is I
have to clean up the data set, as the domains are within double quotation marks.

Now that is out of the way, I want to make a simple script that checks for the response codes of the domains,
in other words, to see which ones give me a 200 response codes, and which domains need more tinkering, to see what web-scraping
technology I would use.

After some research using the requests framework, I noticed that some elements appear after interacting with the site. A couple of googles later
I found the playwright framework for scraping (I was previously familiar with BeautifulSoup, Selenium). After experimenting with it for a bit, and
learning how it works, I made the decision to stick with it.

I used Gemini to generate me most of the tech stacks so I could scrape for it.

# Challenges Encountered


The first issue I encountered is expired SSL/TLS certificates failures. I reconfigured the Playwright browser to ignore the handshakes and prioritize
data collection.

Another issue I encountered was https vs http protocol inconsistency. To tackle that, I implemented a fallback case as follows: the scraper first
tries a secure connection via https and if that fails, it falls back to http.


I think my implementation needs more work in bypassing scrapers, and I clearly need to gather more knowledge in that field.

# Scalability
I would scale this solution by making it asynchronous to run multiple chromium instances, and a proxy to avoid ip limiting.

# Final Thoughts

I don't know whether the description of the problem was to find 477 different technologies or how many technologies overall I can find. Half of the sites
I couldn't get them to work no matter what I tried. Anyways, this is my best solution I could've come up with without the use of AI (I only used it to generate me technologies)
and I am happy with my result. It's been a very good learning experience for Playwright and how technologies appear in a website. I will definetly come back to this once I get better at scraping.
Thank you again for the opportunity.


