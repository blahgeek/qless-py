# Encoding: utf-8
# -*- mode: ruby -*-
# vi: set ft=ruby :

# http://docs.vagrantup.com/v2/
Vagrant.configure('2') do |config|
  config.vm.box = 'ubuntu/trusty64'
  config.vm.hostname = 'qless-py'
  config.ssh.forward_agent = true

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
    vb.customize ["modifyvm", :id, "--cpus", "2"]
  end

  config.vm.provision :shell, path: 'provision.sh', privileged: false
end
