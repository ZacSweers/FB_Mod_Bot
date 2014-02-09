Facebook Mod Bot
================

<p align="center">
  <img src="http://i.imgur.com/xqpBTlg.png" alt="Sublet Bot" height="250" width="250"/>
</p>

This is a facebook bot that I wrote to moderate a group I admin, essentially keeping some order and upholding some requirements per the group rules. The main purpose is to crack down on vague/uninformative posts.

**[Changelog](https://github.com/pandanomic/FB_Mod_Bot/blob/master/CHANGELOG.md)**

Anyone is welcome to use this code and/or repurpose it for their own use. All I ask is that you give me credit somewhere :)

The bot is written in Python, using the [facebook-sdk](https://github.com/pythonforfacebook/facebook-sdk) API wrapper for Facebook's graph API. To make the bot functional and separate from my personal account, I created a dedicated Facebook account for my bot (literally called "Sublets Bot"), registered it as a developer, created an app, granted that same app full permissions to the account, and finally use that access token in the bot itself to authenticate with Facebook's Graph API.

  * *Why make a dedicated app instead of just creating an access token? Because only an app (with an app ID and secret key) can programatically request an extended access token. If I don't do that, I'd have to manually generate a new one every two hours.* 

The group is a sublets/roommate finding group for students at my university, where people can post sublet offerings, say they're looking for one, and also seek out other potential roommates.

### The bot has three major validation checks:
* Pricing reference
  * There must be some sort of pricing referenced, either with `$` signs or by saying `____/month` or `____ per month`
* Minimum length or craigslist link
  * If their post is under 200 characters, doesn't have a link to a craiglist ad, and isn't a parking offering, then they need to edit and include more details.
* Proper tag
  * For easy searching, we require them to prepend their post with `[LOOKING]`, `[OFFERING]`, `[ROOMING]`, or `[PARKING]`.
  * The bot is purposefully a little fuzzy on this due to the large number of people that can't find the bracket keys on their keyboards ಠ_ಠ

If any of those checks fail, it comments on the user notifying them of the problem(s) and specifies what it(they) are. Upon warning, it caches the post ID and time, giving them 24 hours to fix their post. On later runs, if a previously warned post is now valid, it removes the warning comment and the post ID from the cache. ~~I'd send a message thanking them too, but Facebook's API doesn't allow apps to send messages.~~ Yay XMPP

### TODO
* ~~Prepare for Heroku hosting~~ Done!
* Improve documentation

### Caveats
* Facebook's API doesn't allow you to delete anything that the app itself didn't create. 
  * Therefore, you'll have to delete any other posts manually. Locally I have it set to just open the post-to-be-deleted in a new browser tab. On Heroku, I'll set up some form of sending those links back to me.
* Depending on how many posts you request at once (the `LIMIT` option in FQL queries), Facebook's API periodically just crashes and returns an internal server error. Fortunately this doesn't seem to happen unless you ask for extremely high numbers.


## License

     The MIT License (MIT)

     Copyright (c) 2014 Henri Sweers

     Permission is hereby granted, free of charge, to any person obtaining a copy of
     this software and associated documentation files (the "Software"), to deal in
     the Software without restriction, including without limitation the rights to
     use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
     the Software, and to permit persons to whom the Software is furnished to do so,
     subject to the following conditions:

     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
     FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
     COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
     IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
     CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
