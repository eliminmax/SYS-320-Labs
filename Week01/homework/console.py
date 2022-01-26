#!/usr/bin/env python
# coding: utf-8

# # Syslog Reviewer

# ## 1. Kerebos Failed Login hosts
# 
# Parses the log for failed klogind logins, and prints each source IP address, and the number of occurences of said address.

# In[ ]:


import klogind_syslog

klogind_syslog.get_klogind_auth_failures()


# ## 2. SSH User login parser
# 
# Parses the log for every time a user logs in with SSH, and prints the number of times each of the detected users logged in

# In[ ]:


import ssh_syslog

ssh_syslog.get_sshd_login_counts()


# ## 3. Analysis of SSH Log
# 
# *Question: What is your interpretation of the users that authenticated to SSH based on the usernames?  The context is that you are a security analyst and checking your log files for anomalies.*
# 
# There is not much to go on without making assumptions - the conclusion is that there is a user called test, and someone logged in as test 36 times.
# 
# If we assume that this is in a production environment, then a user called test is itself concerning, as is the number of times said user has logged in - a test user should not be involved in any way, shape, or form, in a production environment. It might be an attempt by attackers to use an account that should have been disabled to access the network, or, more concerningly, it could mean that attackers are in a position to create accounts on the system and test their access, which means that they would have full root access to the system, which is bad.
# 
# ## 4. My Thoughts on this lab
# 
# *Question: What did you like the most and least about the lab?*
# 
# I don't have much to say about this lab - Jupyter Notebooks are new to me, and I don't know how I feel about them yet. That said, I would much rather figure out a way to use my plugin-ridden Neovim installation instead of an Electron-based frontend to Jupyter, but I have not found the time to set up the existing solutions.
# 
# To answer the question, I liked getting to work with regular expressions - they're fun. I did not like working with JupterLab Desktop, but I did not hate it.
# 
# ## 5. Questions I have
# 
# *Question: What additional questions do you have?*
# 
# Could I set up [jupytext.vim](https://github.com/goerz/jupytext.vim) instead of JupyterLab Desktop?
# 
# ### Credits
# * *Unix username regex adapted from [brent saner's Unix StackExchange answer](https://unix.stackexchange.com/a/435120)*
# * *Non-capturing regex groups from [Facing Security](https://medium.com/@yeukhon/non-capturing-group-in-pythons-regular-expression-75c4a828a9eb)*
