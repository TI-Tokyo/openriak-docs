---
title: 'Set the open-files limit'
description: 'Show performance engineers how to set the open-files limit using measurable before-and-after checks.'
weight: 4
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'performance-engineers'
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\performance\open-files-limit.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#setting-ulimit'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show performance engineers how to set the open-files limit using measurable before-and-after checks.

## Before you begin

A representative workload, a recorded performance baseline, current capacity measurements, and a safe environment in which to test one change at a time.

## Overview

### Open Files Limit

[plan backend]: {{< product-version-root >}}explanation/storage/choosing-backend/
[blog oracle]: http://blogs.oracle.com/elving/entry/too_many_open_files

OpenRiak KV can accumulate a large number of open file handles during operation. The creation of numerous data files is normal, and the [backend][plan backend] performs periodic merges of data file collections to avoid accumulating file handles.

To accomodate this you should increase the open files limit on your system. We recommend setting a soft limit of 65536 and a hard limit of 200000.

**Note:**
Superuser or root access may be required to perform these steps.

#### Changing Limit For Current Session

Most operating systems can change the open-files limit for the current shell session using the `ulimit -n` command:

```bash
ulimit -n 200000
```

#### Debian & Ubuntu

Start by checking the current open file limit values with:

```bash
ulimit -Hn # Hard limit
ulimit -Sn # Soft limit
```

If you installed OpenRiak KV from a binary package, you will need to the add the following settings to the /etc/security/limits.conf file for the `riak` user:

```/etc/security/limits.conf
riak soft nofile 65536
riak hard nofile 200000
```

If you use initialization scripts to start OpenRiak KV, you can create a /etc/default/riak file and add the following to specify a limit:

```/etc/default/riak
ulimit -n 200000
```

This file is automatically sourced from the initialization script, and the OpenRiak KV process will inherit this setting. Since initialization scripts are always run as the root user, there’s no need to set limits in /etc/security/limits.conf.

#### Enable PAM-Based Limits for Debian & Ubuntu

You can enable PAM-based user limits so that non-root users, such as the `riak` user, may specify a higher value for maximum open files.

For example, follow these steps to enable PAM-based limits for all users to allow a maximum of 200000 open files.

1\.  Edit /etc/pam.d/common-session and add the following line:

```/etc/pam.d/common-session
session    required   pam_limits.so
```

2\. Save and close the file. If /etc/pam.d/common-session-noninteractive exists, append the same line as above.

3\. Edit /etc/security/limits.conf and append the following lines to the file:

```/etc/security/limits.conf
* soft nofile 65536
* hard nofile 200000
```

4\. Save and close the file.

5\. (**Optional**) If you will be accessing the OpenRiak KV nodes via secure shell (SSH), you should also edit /etc/ssh/sshd_config and uncomment the following line:

```/etc/ssh/sshd_config
#UseLogin no
```

And set its value to `yes` as shown here:

```/etc/ssh/sshd_config
UseLogin yes
```

6\. Restart the machine so the limits take effect and verify that the new limits are set with the following command:

```bash
ulimit -a
```

**Note:**
In the above examples, the open files limit is raised for all users of the system. The limit can be specified for the `riak` user only by substituting the
two asterisks (`*`) in the examples with `riak`.

#### CentOS & Red Hat

#### Enable PAM-Based Limits for CentOS and Red Hat

1\. Edit /etc/pam.d/login and add the following line:

```/etc/pam.d/login
session    required   pam_limits.so
```

2\. Save and close /etc/pam.d/login

4\. Save and close the /etc/security/limits.conf file.

5\. Restart the machine so that the limits to take effect and verify that
the new limits are set with the following command:

#### Solaris

To increase the open file limit on Solaris, add the following line to the /etc/system file:

```/etc/system
set rlim_fd_max=200000
```

[Reference][blog oracle]

#### macOS Sierra and High Sierra

```bash
launchctl limit maxfiles
```

The response should look something like this:

```bash
maxfiles    65536          65536
```
The first column is the soft limit and the last column is the hard limit.

To change the open files limits on macOS Sierra or High Sierra, perform the following steps:

1\. Add the following line to your .bash\_profile or analogous file:

```bash
ulimit -n 65536 200000
```

2\. Save and close the file. Next create the file /Library/LaunchDaemons/limit.maxfiles.plist (owned by `root` in the group `wheel` with the mode `0644`). In it place the following XML:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
		"http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">
 <dict>
	<key>Label</key>
	<string>limit.maxfiles</string>
	<key>ProgramArguments</key>
	<array>
	  <string>launchctl</string>
	  <string>limit</string>
	  <string>maxfiles</string>
	  <string>65536</string>
	  <string>200000</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
	<key>ServiceIPC</key>
	<false/>
 </dict>
</plist>

```

3\. Save and close the file.

4\. Restart your computer and enter `ulimit -n` into your terminal. If your system is configured correctly, you should see that `maxfiles` has been set to 200000.

#### Mac OS X El Capitan

```bash
maxfiles    65536          65536
```

The first column is the soft limit and the last column is the hard limit.

To change the open files limits on Mac OS X El Capitan, perform the following steps:

1\. Add the following line to your .bash_profile or analogous file:

2\. Save and close the file. Next open /etc/sysctl.conf (or create it if it doesn't already exist) and add the following settings:

```/etc/sysctl.conf
kern.maxfiles=200000
kern.maxfilesperproc=200000
```

#### Mac OS X Yosemite

To change the open files limits on Mac OS X Yosemite, perform these steps:

2\. Save and close the file. Next edit the /etc/launchd.conf file and add:

```/etc/launchd.conf
limit maxfiles 200000
```

4\. After restarting, verify the new limits by running:

The response output should look something like this:

```bash
maxfiles    65536          200000
```

#### Mac OS X Older Versions

```bash
maxfiles    10240          10240
```

To adjust the maximum open file limits in OS X 10.7 (Lion) up to but not including OS X Yosemite, perform the following steps:

1\. Edit (or create) /etc/launchd.conf and increase the limits by adding:

```bash
limit maxfiles 65536 200000
```

2\. Save the file and restart the system for the new limits to take effect.

3\. After restarting, verify the new limits by running:

#### Setting ulimit

> Running Riak may require a much higher `ulimit` than the default set by the Operating System.

A `ulimit` of 100000 will be acceptable for small-scale non-production systems, but larger limits will be needed for full-scale production systems.  When Riak is installed as a package, then the default limit is increased using the `LimitNOFILE` file option within the systemd service definition.  For local deployments, the ulimit should be modified for the user starting the riak application.

## Verify the result

Repeat the baseline workload and compare latency, throughput, resource use, and error rates before deciding whether to retain the change.
