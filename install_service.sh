#:/bin/bash
echo Copie du fichier galibat.service
sudo cp galidpe.service /etc/systemd/system/galidpe.service


sudo systemctl daemon-reload

sudo systemctl enable galidpe
sudo systemctl restart galidpe
sudo systemctl status galidpe

