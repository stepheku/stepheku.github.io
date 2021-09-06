---
layout: post
title:  "Ansible vault for storing credentials in a playbook"
date: 2021-01-31 19:01:52 -0500
tags: ansible
---
## Why this?
I've been slowly learning how to use ansible for the last few months as a way to automate managing some of my raspberry pi's as well as VMs that are sitting off of my proxmox server. One of the main things I've had trouble with is running commands via playbooks that require some sort of sudo password. Hard-coded credentials are bad news, as well as leaving credentials in the .bash_history. I figured I would take a look at ansible-vault since it's one recommended way to store credentials

After banging my head against the wall for an afternoon and not understanding the documentation on https://docs.ansible.com/ansible/latest/user_guide/vault.html, I'd gotten at least one method of storing credentials to work. This post will be about that method 

## Method 1: Having an encrypted string in a playbook
For this method I:
1. Created a password file to be used as the `vault-password-file`
2. Set the `chown` to 600 on the password file
3. Used `ansible-vault encrypt_string` to get the encrypted output
4. Copied the encrypted output as a variable into my playbook

### Background
My ansible setup is fairly simple
    - 1 Ubuntu 20.04 host at IP 192.168.10.10 with the alias host1
    - 1 playbook that updates/upgrades all apt packages and restarts the host

Playbook contents:
```yml
---
- name: Update and upgrade packages
  hosts: host1
  become: true
  tasks:
    - name: Upgrade all packages to the latest version
      apt:
        name: "*"
        state: latest
    - name: Update all packages to the latest version
      apt:
        upgrade: dist
    - name: Run "apt update"
      apt:
        update_cache: yes
    - name: Remove useless packages from the cache
      apt:
        autoclean: yes
    - name: Remove dependencies that are no longer needed
      apt:
        autoremove: yes
    - name: Reboot
      reboot:
        reboot_timeout: 300
```

My SSH keys have a passphrase and the public key has already been copied to the host. To run the playbook, I would first run:
- `ssh-agent bash`
- `ssh-add` and type in the passphrase

Afterwards, I can run the playbook this with `ansible-playbook -u ubuntu update.yml`

However user that I would use (`ubuntu`) to run this playbook currently does not have any `sudo` commands that can be run without the password (as it should be). This also means that commands that require `sudo` and the playbook will fail.

The main issue is that we have the `become` directive, but we don't have a password. We would need to define the `ansible_become_password` variable, but I'd rather not have my password hard-coded into the playbook like:

```yml
---
- name: Update and upgrade packages
  hosts: host1
  become: true
  vars:
    ansible_become_password: my_secure_password_in_plain_text
  tasks:
    - name: Upgrade all packages to the latest version
...
```

### Create password file
I created a password file that contains the password that would be used for encryption/decryption

```bash
vim vault_password_file

# or:

echo "my_vault_password" > vault_password_file
```

So now `vault_password_file` contains a single line, which is the vault password (`my_vault_password`)

### Set permissions on the password file
Now that we have the password file, we want to restrict permissions so that only the user can read/write and no one in the same group or other can take any action (chmod 600)

```
chmod 600 vault_password_file
```

### ansible-vault encrypt_string and pasting into the playbook
Next, we can now use the password (in the password file) to encrypt strings, such as our user password

We can use `ansible-vault encrypt_string` to encrypt a string and give us the output of the encrypted string

```
ansible-vault encrypt_string \
--vault-password-file vault_password_file \
'my_secure_password_in_plain_text' \
--name 'sudo'
```

- `vault-password-file` will designate the password file that contains the password, in this case it's the file we created before `vault_password_file`
- `'my_secure_password_in_plain_text'` is the password that we need in our playbook for privilege escalation
- `--name` will mark the encrypted string with a string name. Here, we arbitrarily decided to name it `sudo`

The output would look something like:
```
sudo: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          61373031613665383065616532633665316463366636623830393135376139613330303133316261
          3965633738643430393538643334633534303766626665650a306538666132653661326262383937
          32623331346235623839666161363861323762623763386139666334366265376365313838633532
          3830363361353930360a323835363264393735373233363230393364613361626264393235633038
          37306439373636666439326461336533363837653134646361613564633733353635663266656163
          3865316563343635633338646432363462326337353532393738
```

The output after `sudo: ` is what we can paste into our playbook to have the password in our playbook, but encrypted

So our new playbook will look like:

```yml
---
- name: Update and upgrade packages
  hosts: host1
  become: true
  vars:
    ansible_become_password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      61373031613665383065616532633665316463366636623830393135376139613330303133316261
      3965633738643430393538643334633534303766626665650a306538666132653661326262383937
      32623331346235623839666161363861323762623763386139666334366265376365313838633532
      3830363361353930360a323835363264393735373233363230393364613361626264393235633038
      37306439373636666439326461336533363837653134646361613564633733353635663266656163
      3865316563343635633338646432363462326337353532393738

  tasks:
    - name: Upgrade all packages to the latest version
...
```

Now, we can run our playbook again, but denote the password-file that we use to decrypt the encrypted password in our playbook
```
ansible-playbook -u ubuntu --vault-password-file vault_password_file update.yml
```
