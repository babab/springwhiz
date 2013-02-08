# springwhiz README

## What is springwhiz?

springwhiz is a collection of well-known web-tools such as a
notepad/pastebin and bookmarks app. It has a unique search box that allows
commands and quick navigation to bookmarks to be entered while passing 'normal'
searches to the duckduckgo.com search engine.

springwhiz is currectly in the initial stages of development, a demo version is
available at http://sprwz.babab.nl. Since this is a demo environment, accounts
and content will be reset periodically.

springwhiz proudly uses https://duckduckgo.com for searching the web and has
some support for it's tools. It must be made clear though, that springwhiz is
not endorsed by duckduckgo or affiliated with them.

springwhiz is free, open source software released under the GPL license. It is
written in Django, and can therefore easily be deployed and extended or altered
to suit your needs.

## Current features

These features are currently working and stable. Although small improvements
may still be done.


### Notepad / Pastebin

- Create private, secret or open notes
- Syntax higlighting for 236 (mixtures of) programming and markup languages
- Render markdown and/or reStructuredText to HTML
- Raw output in text/plain format

Create notes, which can be any content or textfile you like. You can keep your
notes private, share them via a secret url (much like Github gists) or create
'open' notes, which are listed and viewable for everybody.

View notes in raw format or with added linenumbers and optional syntax
highlighting. Syntax highlighting is added using Pygments which has great
support for a huge array of languages.

When the type is set to **markdown** or **reStructuredText** the note can be
rendered to HTML using Django's built-in support for these markup languages.


### Search / command box

Enhance your browsing experience with a simple command line. Prefix your query
with an `@` and springwhiz will run a command / navigate to a page.

    Basic commands

    command                      alias   description
    ---------------------------- ------- --------------------------------------
    @register                    @reg    Will bring you to the register dialog
    @login                       @li     Will bring you to the login dialog
    @logout                      @lo     Log out (from all your sessions)
    @notepad                     @np     Open notepad


Without these prefixes your query will be send directly to the duckduckgo.com
search engine. This means you can use the awesome !bang syntax duckduckgo
offers to search on hundreds of sites directly. Or use the `\` prefix to
navigate to the first page that duckduck has found.

    Duckduckgo.com bang syntax search

    bang                                 description
    ------------------------------------ --------------------------------------
    \<string>                            Browse to 1st result for string
    !yt <string>                         Search YouTube
    !g <string>                          Search Google
    !i <string>                          Search Google Images
    !m <string>                          Search Google Maps
    !synonyms <string>                   Search thesaurus.com

For more info on Duckduckgo's bang search abilities enter `!bang`


## Features to be added (most probably)

- Manage bookmarks and optionally share them
- TODO application


## License

Copyright (C) 2012-2013  Benjamin Althues

springwhiz is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

springwhiz is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with springwhiz.  If not, see <http://www.gnu.org/licenses/>.
