## App to filter the Administrator View of the WPI 3d print lab 


#### Todo:
- Hide Admin Login :heavy_check_mark:
- Resize Chrome  Display :heavy_check_mark:
- Hide Passwords :heavy_check_mark:


- increase the close time

- prevent user page refresh

- optimize for speed
- Add a Flask UI
- Organize/Comment thoroughly
- make urls more flexible with contains or regex

#### Change Log

##### V2.5

- Updated userAuth function to find element by name because of page changes

- Updated userAuth function to make the label of admin or student work with the revised 3dprinteros page

- Changed Main method to pass admin email and password to be autofilled by the userAuth function

- Updated the url in the check for username to remove the <code>/#</code> in the url it looks for

- Updated the await logout function to include <code>#/</code> in the url it looks for

