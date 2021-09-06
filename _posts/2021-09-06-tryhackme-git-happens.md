---
layout: post
title:  "TryHackMe: Git Happens"
date: 2021-09-06 09:01:00 -0500
tags: tryhackme security
---
Since I have not really been doing TryHackMe rooms, I figured I should try doing them again and do some of my own write-ups. Write-ups have been super helpful in that I can review things that I forget in the future

## Background
- Link: https://tryhackme.com/room/githappens
- Target IP: 10.10.122.39

## nmap scan
Starting off, we can do a quick `nmap` scan to see what ports are available and if anything is also helpful:
```
nmap -A 10.10.122.39 -vv
```

Open ports:
- 80

Helpful output:
```
PORT   STATE SERVICE REASON         VERSION
80/tcp open  http    syn-ack ttl 61 nginx 1.14.0 (Ubuntu)
| http-git: 
|   10.10.122.39:80/.git/
|     Git repository found!
|_    Repository description: Unnamed repository; edit this file 'description' to name the...
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: Super Awesome Site!

```

Okay great, it looks like there is a git respository available

## investigate port 80
- When we navigate to `http://10.10.122.39/`, looking at the source, there's a large chunk of javascript that is very obfuscated
- Because there is a `.git` item available, that means there is a bare repository that's available. We can use the following wget flags and recursively download everything into our current directory
```bash
wget --recursive --no-parent http://10.10.122.39/.git
```
- Then because we have the git folder, we can use git clone to get the original source code into a test directory
```bash
git clone 10.10.122.39/ test
```

## investigate git repository
- Since we're using git, let's look at all of the previous commits
- Double-check the `index.html` file, 
<pre>
git log

commit 395e087334d613d5e423cdf8f7be27196a360459
Author: Hydragyrum <hydragyrum@gmail.com>
Date:   Thu Jul 23 23:17:43 2020 +0200

    Made the login page, boss!

commit 2f423697bf81fe5956684f66fb6fc6596a1903cc
Author: Adam Bertrand <hydragyrum@gmail.com>
Date:   Mon Jul 20 20:46:28 2020 +0000

    Initial commit
</pre>

We can take a look at the original `index.html` by using the git command:
```bash
git show 395e08733:index.html
```

This will show us the password in the javascript:
```html
    <script>
      function login() {
        let form = document.getElementById("login-form");
        console.log(form.elements);
        let username = form.elements["username"].value;
        let password = form.elements["password"].value;
        if (
          username === "admin" &&
          password === "<flag_here!>"
        ) {
          document.cookie = "login=1";
          window.location.href = "/dashboard.html";
```