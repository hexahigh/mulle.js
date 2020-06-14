openssl aes-256-cbc -K $encrypted_db2095f63ba3_key -iv $encrypted_db2095f63ba3_iv -in deployment/deploy_rsa.enc -out /tmp/deploy_rsa -d
eval "$(ssh-agent -s)"
chmod 600 /tmp/deploy_rsa
ssh-add /tmp/deploy_rsa