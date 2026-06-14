cd ~
mkdir -p repos
cd repos

ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub
sv-enable ssh-agent
sv-enable sshd

git clone --recursive git@github.com:quabbermackle/relativity.git
git clone git@github.com:quabbermackle/shardspace.git
git clone git@github.com:quabbermackle/dndtools.git

git clone git@github.com:01101010110/proot-distro-scripts.git
git clone git@github.com:ra3xdh/qucs_s.git

cd relativity
python3.11 -m venv venv
source venv/bin/activate
