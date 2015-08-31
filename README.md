# Line-Pls
<h3>Rap Genius meets LinkedIn for aspiring Actors.</h3>

<h5> Overview </h5>
So you want to be an actor!...Success in the entertainment industry hinges on a delicate balance of talent, good audition material and who you know. Line Pls is designed to address all of those needs by providing a platform for actors to showcase their talent, collaborate, and easily find compelling new audition material by combining social networking with a large database of crowdsourced annotations on dramatic literature. Additionally, Actors can tag youtube videos of their performances to various monologues, and showcase their work on personal profile pages... and who knows, maybe even get discovered! 

<h5> Technical Stack </h5>
Python, Javascript, Flask, Jinja, jQuery, SQLalchemy, D3.js, HTML/CSS, Bootstrap, Scrapy, BeautifulSoup, JSON, s3 buckets, boto, Python unittests, Youtube Data API, Youtube iFrame Player, OAuth 2.0, Google Login

<h5> Feature List </h5>
- PostgreSQL Database
  - Seeded a db of the complete works of Shakespeare
  - Used Scrapy and Beautiful Soup to scrape monologue contents 
  - Tables for Users, Monologues, Characters, Plays, Youtube Videos, Comments
- Crowdsourced Annotations on Monologues 
  - Implemented search
  - Created modal windows for pop up comments
  - Integrated a comment feed to display previous user comments
- Youtube API 
  - Figured out how to upload/display videos on individual monologues
  - Figured out how to store user theater reels
  - Created db to store youtube keys 
- User Accounts
  - Users can signup, login, logout 
  - Users can create profiles
  - Users can upload pictures
  - Users can follow eachother; profile pages display followers
- Created Actor Reel Feed
  - Displays acting reels of users that link back to user profiles
- D3js
  - wrote algorithm to flatten a complex data structure and generate node/links for a d3 force graph. 
      - Actual graph removed from current version to enhance user experience, but code remains in d3 directory
- Boostrap/HTML/CSS
  - Integrated front-end styling with bootstrap
- Tests
  - Working on implementing unittests

<h5> Favorite Challenges </h5>
- Learning about web scrapping with Scrapy & Beautiful Soup
- Wrestling with D3
- Designing database architecture 
- YouTube API 






