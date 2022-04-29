---
layout: post
title:  "Ubuntu Startup Disk Creator not displaying iso files"
date:   2022-04-28 20:04:52 -0500
tags:   ubuntu
---
This post is just a reminder to myself so I don't forget this again later, because this was the 3rd time I had to look this up

There are multiple ways to create a bootable USB. Although there are plenty of Windows apps (Pen Drive Linux, etc), I try personally favour anything that I could apt install on Ubuntu. Startup Disk Creator seems like the no-brainer way with a GUI to create a bootable USB. However, most of the times I'm using this for something other than Ubuntu (proxmox, truenas, etc) and the iso files never show up

Solution: Change the iso file into an img file using `mv my_file.iso my_file.img` and it should do the trick
