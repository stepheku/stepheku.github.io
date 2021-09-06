---
layout: post
title:  "Wiring up my home network (Part 1)"
date:   2020-12-23 19:01:52 -0500
tags: networking
---
This blog and post (like most others of this same nature) were mostly inspired by [Troy Hunt's Wiring a home network from the ground-up with Ubiquiti](https://www.troyhunt.com/wiring-a-home-network-from-the-ground-up-with-ubiquiti/). When we bought our home, creating a home network and having multiple ethernet runs in all rooms was at the top of my to-do list. This would be a step up from a basic apartment setup of a modem, consumer-grade router and a switch if I felt a little edgy.

My equipment has been collected over several years and are across multiple vendors. Some were purchased through recommendations from other people doing their home networks (Ubiquiti Access Points) and others were purchased blindly through recommendations from Amazon (like my Mikrotik router - I am not proud of how I made that decision, but am glad I made it).

Also to preface that when starting this project/series of projects, I had little to no networking knowledge. At the time, I could vaguely explain with some frantic hand-waving how DNS worked and what an IP address was. Looking back now, I would say I learned a thing or two, and can hold a basic conversation about network segmentation with VLANs and subnets.

## Equipment list
1. Tripp Lite 6U Wall Mount Rack Enclosure
2. Cable Matters 24-Port RJ45 Patch Panel
3. Mikrotik Router RB2011UiAS-2HnD-IN
4. Netgear GS724TPv2 24-Port Switch
5. Ubiquiti Unifi Cloud Key Gen 2 Plus
6. Ubiquiti Unifi AP-AC Long Range Wireless access point
7. Tripp Lite 1200VA Smart UPS Battery Back Up
8. TP-Link 8 Port PoE Switch (TL-SG108PE)
9. Ubiquiti Unifi 8-Port PoE 150W Switch

### Tripp Lite 6U Wall Mount Rack Enclosure
I ended up with this rack enclosure because it was the cheapest rack at the time. Instead of mounting it on the wall, it just sits on the floor, which isn't the best place for it.

### Cable Matters 24-Port RJ45 Patch Panel
This is just a basic patch panel. On the back, you use the punch-down tool to connect a cable that comes from its terminal port (or wherever). On the front, you can use a patch cable to connect the cable on the back to another device (on my case, usually a switch). One of my biggest issues with this patch panel is how it's not as modular as say a coupler patch panel (for example: [kenable 24 Port RJ45 CAT6 Gigabit Through Coupler Patch Panel with Back Bar](https://www.amazon.com/gp/product/B07951MLD4)). Although there are limitations to the modularity of the coupler patch panel, giving a change to correct your mistakes when you accidentally across another cable inappropriately is well appreciated

### Mikrotik Router RB2011UiAS-2HnD-IN
A pretty solid consumer router. Does VLANs, subnetting, more advanced firewall rules, etc

### Netgear GS724TPv2 24-Port Switch
Super reliable switch that also offers power over ethernet (PoE, using 802.3at). The only time I need to reboot my switch is if I'm doing firmware updates or I've just completely messed up and need to do a factory reset

### Ubiquiti Unifi Cloud Key Gen 2 Plus
The Cloud Key from Ubiquiti offers a place to access the Unifi Controller and Unifi Protect apps. Prior to using this, I had installed the Unifi Controller on to a VM instead

### Ubiquiti Unifi AP-AC Long Range Wireless access point
Super solid wireless access points. Because there are so many different Unifi access points out there, I had just purchased these because I saw a review about them somewhere. It took some time to get used to the fact that all of them were controlled by the Unifi Controller and not using individual web-interfaces

### Tripp Lite 1200VA Smart UPS Battery Back Up
Solid UPS. Has saved me plenty of times during power surges or times when I had lost power

### TP-Link 8 Port PoE Switch (TL-SG108PE)
An older switch I was using before I started to use the Netgear switch. This one is just an ancillary switch in the loft area

### Ubiquiti Unifi 8-Port PoE 150W Switch
A newer purchase that is also an ancillary switch in the garage. This switch acts similarly to the wireless access points where it's controlled from the Unifi Controller rather than a web interface

## Rack setup
The main rack is located underneath the stairs
1. 1U Cable Matters 24-Port RJ45 Patch Panel
2. 1U Netgear GS724TPv2 24-Port Switch
3. Blank
4. 1U rack to hold the Mikrotik Router RB2011UiAS-2HnD-IN and a Unifi AP
5. 2U Tripp Lite 1200VA Smart UPS Battery Back Up
The modem connects to the Mikrotik router, which then connects to the Netgear switch. Primary workstations are connected to the Netgear switch as well as the Unifi AP

## Running the ethernet cables
The house did not have any ethernet ports already set up. There were RJ-11 and coax ports installed, but were fished through areas that didn't have attic access or easy crawlspace access. That meant either taking down the walls or putting down cable runners. Since I had no experience doing anything with drywall, cable runners were the go to option. A trip to Home Depot later, I was a few hundred dollars lighter, spent on cable runners, data boxes and a ton of Cat6 cabling, keystone jacks and plugs.  

After laying down the cable runners along baseboards and corners, and setting up the data boxes and cabling, I had finally started the fun process of crimping, testing and hoping I didn't mess up all of the Cat6 cabling. A few days of frustration later, the living room now has 3 data boxes with 2 to 5 ports each, the loft area has a databox with 2 ports and the guest room has a databox with 4 ports

## Ancillary switches and APs
With more ports to plug stuff in, I started thinking of attaching ancillary switches and APs. My reasoning for the ancillary switches was more for PoE reasons so I would make sure not to overload the main switch by plugging in too many PoE devices, and I suppose my reasoning for the APs is obvious. 

Because the ports in the living room had the largest coverage area, I decided to set up the additional AP there. 

## Lessons learned
I had made some lucky choices through all of this, but there are some major things I would change if I had to do it all again. This comes from both screwing up and learning from the posts and comments on r/homelab

Purchase patch cables instead of making your own. They are cheap, they save you time and they're likely more durable than the ones you crimp yourself (especially if you just started to learn how to crimp ethernet cables for the sole purpose of your home network)

Modular patch panels can be helpful down the road. If you realize you have to move some equipment around, or did a terrible job at estimating cable length, the ability to quickly swap in-and-out jacks without having to do a punch-down again

Purchase the right rack for the right setting. I purchased a wall mount because I thought I could save some money by purchasing it and placing it on the ground, and now it attracts dust like crazy because of the giant opening in the back that should have been attached to a wall
