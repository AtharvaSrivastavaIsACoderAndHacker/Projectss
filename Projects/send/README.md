# **📦 Send**

A tool I developed out of laziness to drag things over or type long paths ! my goNav utility had path aliasing feature, so the idea of sending files to aliased paths struck me !

yk 1 thing ? commands like xcopy and other ones suck, they require full paths and a long list of flags for easy things, this solves it

get the `send.exe` and a `Dependencies` folder in a location that's added to PATH, (like system32(not recommended))

how convinient it is to really type `send des tumhiho.mp3`, and the audio file gets copied to des (i've aliased des for desktop path) from the current dir --------------- if u want to send a file that's in the parent dir, just say `send des ..\tumhiho.mp3`\

Safety ui feature --> if one acidentally types `send aliasName`, it could be interpreted as `send aliasName ""`, meaning send the pwd to the aliasName path --------- to prevent this noobness and accidental file corruption, if third arg is absent, we set the source path to gibberish in order to not accidentally corrupt ur pwd and roast you !


---------------------------------------------------------------------


# **📦 Send.exe -- Reliable File/Folder Transmission Tool**

A small but mastt utility for copying files or folders on Windows.
instead of typing whole file paths, this tool gives you the freedom to create aliases and store them as a substitute to typing long paths
Fast, deterministic, and with safety rails so you don't nuke your stuff by mistake. 🚀


------------------------------------------------------------------------


## ✨ **Features**

-   📁 **File/Folder Auto-Detection** \
    - Pass a path -- if it's a file, it copies as a file; if it's a
    folder, it handles recursion.
    - --> send aliasedName /myfold/ -------------------------------  this is read as, --> send to aliasedName , the folder myfold
    - --> send down text.txt                           --> send to down (downloads for me), text.txt

-   **Add it to PATH and enjoy**\
    `send.exe` and it's `Dependencies` folder must be in a location that's added to PATH, only then it can be accessed like a command from anywhere !

-   🔒 **Hash Verification**\
    After transfer, source & destination hashes are compared.\
    If something's off → you'll know immediately.

-   📜 **Verbose Copying**\
    Uses `xcopy /F` , so you see what's goin on.

-   🛡️ **Safety Nets**
    -   Prompts before overwriting (`/-Y`).\
    -   Keeps file attributes like hidden/system (`/H`, `/K`).\
    -   Clean recursion in folder mode.
    -   if one acidentally types `send aliasName`, it could be interpreted as `send aliasName ""`, meaning send the pwd to the aliasName path --------- to prevent this noobness and accidental file corruption, if third arg is absent, we set the source path to gibberish in order to not accidentally corrupt ur pwd and roast you !
    - if u wanna move the pwd, just type `send aliasName .\` or `send alias \`

-   🧪 **Developer Friendly**\
    Designed with hash mismatch detection to catch transmission authenticity and check if Precesses were tryna race each other (ie race conditions).

-   **Copies Metadata too**\
    eg -- if u sent a file/ folder using it, which was created a year ago, at the new location, the copied folder will have the metadata ( ir the year old date) preserved !

-   **Built-in Roast generator**\
    - try it urself, just enter only 1 arg with send 
    - `send alias` or `send des`


------------------------------------------------------------------------


## **🚀 Usage**

``` powershell
# Create alias, if using env variables, use it in cmd style, %VARNAME%
.\send.exe alias down %USERPROFILE%\Downloads

# Send a folder
.\send.exe down .\myfolder\

# Send a single file
.\send.exe down .\hello.txt
```

------------------------------------------------------------------------


## **⚠️ Important Notes (Read Before Rage)**

This tool uses **cmd.exe expansion**, *not* PowerShell.\
this utility will work in PowerShell too, just remember to use cmd-style env var referencing (%VAR%) while creating an alias
this doesn't mean that it works only from cmd.exe

✅ Correct way (cmd-style):

    %USERNAME%

❌ Wrong way (PowerShell-style, will break as my code relies on cmd-style variable referencing):

    $Env:USERNAME

btw if u want to store $Env:USERNAME and not let PowerShellresolve it before it gets aliased, just use `$Env:USERNAME -- ` to escape the $ sign (backtick prevents PowerShell from expanding it during alias creation).


------------------------------------------------------------------------


## **💡 TL;DR**

Think of this as a **safer, easier and shorter to type xcopy** that refuses to silently
screw you over.\
If you break it, you probably ignored the `%USERNAME%` vs
`$Env:USERNAME` thing. 😉


------------------------------------------------------------------------