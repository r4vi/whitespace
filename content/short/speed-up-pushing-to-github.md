---
date: 2013-02-22 00:00:00
title: Speed Up Pushing to GitHub
---

```bash
    ssh -N git@github.com &
```
In your shell to keep a persistent connection to GitHub open in the background
so every time you push it doesn't need to go through they key exchange handshake

