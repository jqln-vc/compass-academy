"""Sprint 5: AWS Lab
hospedagem.py: Script para criação de bucket e hospedagem de website estático.
Autoria: Jaqueline V. Costa
Data: Dez/2024_
"""

import boto3

nome_balde = 'sprint5-lab-aws'
regiao = 'us-east-1'  # US East: North Virginia
index = 'index.html'
erro = '404.html'
politica_acesso = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::{nome_balde}/*"
            ]
        }
    ]
}