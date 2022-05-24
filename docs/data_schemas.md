# Data Schemas

This markdown file gathers thoughts about how to model data.

## Entities:
* User
* Post
* Like
* Comment

## Actions:
* Create User with email, username, password (send email to verify) 
* Alter User information (change email, change password, change username)
* Query user with all its posts by username
* post new "tweet" (maximum of 140 chars)
* like tweet / unlike tweet
* comment tweet
* delete comment
* show post with number of comments and likes
* show "all" tweets (no personal feed)

### Secondary Actions:
* find out who liked post
* show comment section
* personal feed:
  * subscribe to person
  * unsubscribe to person
  * personal feed

## User Entity:
* email
* hashed password
* username (is userid)

## Post
* postId
* content (length restriction)
* timestamp (for feed)
* likes (list of userIds) (you can get number of likes from there)
* number of comments

## Comments
* commentId
* postId
* userId
* timestamp
* content (length restriction)fro