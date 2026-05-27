cd ~
sudo apt-get update
sudo apt upgrade -y
sudo apt install -y dialog
sudo apt install -y software-properties-common build-essential wget curl nano ssh git
sudo apt-add-repository -y ppa:deadsnakes/ppa
sudo apt-add-repository -y universe
sudo apt-get update
sudo apt install -y python3.12 python3.12-dev python3.12-venv

git config --global user.email "spottedalbinojumpingfrog@gmail.com"
git config --global user.name "Matthew Gunther"

mkdir -p repos
cd repos
git clone git@github.com:quabbermackle/dndtools.git
git clone git@github.com:quabbermackle/shardspace.git
git clone --recursive git@github.com:quabbermackle/relativity.git

cd relativity
python3.12 -m venv venv
source venv/bin/activate
chmod +x update_reqs.sh
chmod +x pip_upgrade.sh
chmod +x setup_env.sh
pip install -r requirements.txt
