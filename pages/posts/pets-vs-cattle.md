---
title: Pets vs Cattle
subtitle: 
date: 2023-11-20
tags: ['frameworks', 'software']
---

One of the most useful questions I ask myself about a software project is: "Is this a pet or is it cattle?" I've been surprised how often asking this question helps clarify my thinking.

- _Pets_ are special and unique. When they are ill you spend the time to nurse them back to health. Examples of pets include my personal laptop, my phone, and the (currently) one binary serving [Chroma](www.trychroma.com)'s customer dashboard data.
- _Cattle_ are replaceable, identifiable only by numbers or UUIDs. The usual reaction to a cattle struggling is to kill it and replace it with another -- you only care if there's a pattern of problematic behavior (cattle disease, even) which is harming your customers. If you've worked on a large distributed system you're very familiar with cattle: the load-balancers in front of your service, database replicas, and compute nodes are all probably cattle. Customer requests to query a database or kick off a job are definitely cattle; that's why we have retries!

The product maturity lifecycle for SaaS applications tends naturally to start with pets which graduate to cattle. In development you may only have one instance of each of your critical components. When they break you spend the time to debug and diagnose. This is a productive exercise since it helps you harden the binaries against faults and also learn how to operationalize your system.

But as time goes on and the system matures individual requests, then even jobs and machines, become cattle. The first customer requests flowing through the system are magical; the 10-millionth is just another blip on the dashboard. When I worked at Google the old-hat SREs were incredibly principled about _not_ investigating issues-apparent unless they fired an alert. "You could spend all your time trying to figure out why something in the dashboard looks weird. If it isn't hurting customers enough to fire an alert, choose not to care."  -- A wise SRE.

This isn't an epistle against deep debugging in distributed systems. It's incredibly important to understand exactly how and why things go wrong, especially when they go wrong all at once. But if one job out of 200 goes sideways...eh.

*(Credit for introducing me to this concept goes to John Truscott Reese.)*