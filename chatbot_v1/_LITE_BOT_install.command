#!/bin/bash
SCRIPT_DIR=$(dirname $0)
cd $SCRIPT_DIR
COLOR="3[4;34;37m"
NONE="3[0m"

NO_FORMAT="\033[0m"
F_BOLD="\033[1m"
C_CHARTREUSE2="\033[38;5;82m"
# echo -e "${C_CHARTREUSE2}Color me, surprised${NO_FORMAT}"

echo -e "${C_CHARTREUSE2}Creating Virtual Environment${NO_FORMAT}"
virtualenv venv

echo -e "${C_CHARTREUSE2}Activating Virtual Environment${NO_FORMAT}"
source venv/bin/activate

echo -e "${C_CHARTREUSE2}Installing Default Chatterbot${NO_FORMAT}"
pip3 install chatterbot

echo -e "${C_CHARTREUSE2}Installing spaCy 2.3.5${NO_FORMAT}"
pip3 install spacy==2.3.5

echo -e "${C_CHARTREUSE2}Downloading spaCy Model EN${NO_FORMAT}"
python -m spacy download en_core_web_sm

echo -e "${C_CHARTREUSE2}Downloading spaCy Model FR${NO_FORMAT}"
python -m spacy download fr

echo -e "${C_CHARTREUSE2}Unzipping custom chatterbot${NO_FORMAT}"
unzip ./chatterbot.zip
rm -rf ./__MACOSX
rm -rf ./venv/lib/python*/site-packages/chatterbot

echo -e "${C_CHARTREUSE2}Moving chatterbot${NO_FORMAT}"
mv ./chatterbot ./venv/lib/python*/site-packages/

echo -e "${C_CHARTREUSE2}Installation complete${NO_FORMAT}"
# echo -e "${C_CHARTREUSE2}Starting Chatbot${NO_FORMAT}"
# python3 ./lite_bot.py
