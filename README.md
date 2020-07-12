# WikipediaSpeedRunDiscordBot
This is a wikipedia speed run discord bot

Usage: 
`.wiki [mode] [degrees of separation]`

e.g: 
`.wiki dynamic 20`

or 

`.wiki random 0`

The `[mode]` specifies how generating is conducted. Either `[dynamic]` - a crawl of wikipedia from a random start, which may take up to 2 minutes - or random. For dynamic mode, you then need to specify degrees of separation with a number (max 25). Random generation picks two articles at random. However, you still need to specify a second argument, but can do as 0 or None.
