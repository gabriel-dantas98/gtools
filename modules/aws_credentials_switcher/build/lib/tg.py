# -*- coding: utf-8 -*-
import pprint
import yaml
import os
import click
import inquirer 
import string
import subprocess
import sys

def console(string, color):
    click.echo(click.style(string, fg=color))
    
def load_vpn_configs():

    with open("vpn_configs.yaml", "r") as file:
        dict_yaml = yaml.load(file)

    return dict_yaml

def load_credentials():

    ROOT_DIR = "/home/gabrield/lab/lab/piton/team-ghost-cli"

    with open(ROOT_DIR + "/aws_credentials.yaml", "r") as file:
        aws_credentials = yaml.load(file)

    return aws_credentials

@click.group()
def cli():
    pass

@cli.command(help="Comando para adicionar cliente [conta] [access_key] [secret_access_key]")
@click.option('--client', help="Nome da conta da AWS")
@click.option('--access_key', help="access_key cadastrada no IAM")
@click.option('--secret_access_key', help="secret_access_key cadastrada no IAM")
def add_client(client, access_key, secret_access_key):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))   
    console("client: {} | access-key {} | secret_access_key: {}".format(client, access_key, secret_access_key), "yellow")

    new_credential = {client: {'access_key': access_key, 'secret_access_key': secret_access_key}}

    dict_credentials = load_credentials()
    
    #Se nao for verdadeiro, a funcao ja interrompe a execucao
    if not (verify_credentials(new_credential, dict_credentials)):
       return
    
    dict_credentials["keys"].update(new_credential)
    
    with open(ROOT_DIR + "/aws_credentials.yaml", "w") as yaml_file:
        yaml.dump(dict_credentials, yaml_file, default_flow_style=False)
        console("aws_credentials.yaml atualizado", "green")

@cli.command(help="Comando para exibir todas as chaves")
def list_all():
    dict_credentials = load_credentials()

    for client, access_keys in dict_credentials['keys'].items():
        console(client, "blue")
        for key_type, key_value in access_keys.items():
            print("  {}: {}".format(key_type, key_value))

def verify_credentials(new_credential, dict_credentials):
    #Verifica se ja existe registros e para o fluxo se ja existir algo
    for new_client, new_access_keys in new_credential.items():

        if new_client in dict_credentials['keys']:
            console("Ja existe uma credencial com o nome {}".format(new_client) , "red")
            return False

        for key, credential_value in dict_credentials["keys"].items():

            if new_access_keys["access_key"] in credential_value["access_key"]:
                console("O {} ja possui uma access_key com o valor {}".format(key,credential_value["access_key"]), "red")
                return False

            elif new_access_keys["secret_access_key"] in credential_value["secret_access_key"]:
                console("O {} ja possui uma secret_access_key com o valor {}".format(key,credential_value["secret_access_key"]), "red")
                return False
    return True  

def switch_credential(aws_account_key):
    # print("Mudando para:")
    # console("access_key: {} \nsecret_access_key: {} \n".format(aws_account_key["access_key"], aws_account_key["secret_access_key"]), "cyan") 

    configure_key_id = "aws configure set aws_access_key_id " + aws_account_key["access_key"]
    configure_secret = "aws configure set aws_secret_access_key " + aws_account_key["secret_access_key"]
    
    switch_access_key = subprocess.run(configure_key_id, shell=True)
    if(switch_access_key.returncode == 0):
        console("access_key: OK", "green")
    else:
        console("access_key: ERROR", "red")

    switch_secret_access_key = subprocess.run(configure_secret, shell=True)
    if(switch_secret_access_key.returncode == 0):
        console("secret_access_key: OK", "green")
    else:
        console("secret_access_key: ERROR", "red")
    
def get_crendential_by_name(name):

    dict_credentials = load_credentials()

    for client, access_keys in dict_credentials["keys"].items():
        if name in client:
            return access_keys

@cli.command(help="Comando para mudar a chave usada")
def swap():
    
    dict_credentials = load_credentials()

    list_name = list(dict_credentials["keys"].keys())

    questions = [
                inquirer.List('account',
                    message="Qual credencial você quer mudar?",
                    choices=list_name,
                            ),
                ]

    answers = inquirer.prompt(questions)["account"]

    aws_account_key = get_crendential_by_name(answers)

    switch_credential(aws_account_key)

@cli.command(help="Comando para fazer conexão de vpn")
def vpn():

#sudo openvpn --remote  52.67.133.159   1194 udp --comp-lzo yes --nobind --dev tun --cipher AES-128-CBC --auth-nocache --persist-key --persist-tun --client --auth-user-pass --ca Dropbox/Rivendel-Projetos/Ekko/ekko-vpn/OpenVPN/ca.crt --user gdantas

#command = "sudo openvpn --remote {} 1194 udp --comp-lzo yes --nobind --dev tun --cipher AES-128-CBC --auth-nocache --persist-key --persist-tun --client --auth-user-pass --ca {} --user {}".format(remote_add, crt_file, user)
    config = load_vpn_configs()
    pprint.pprint(config['clients'])
    # for key, value in config.items():
    #     print("key {}, value {}".format(key,value))

cli.add_command(add_client)
cli.add_command(list_all)
cli.add_command(swap)
cli.add_command(vpn)

if __name__ == '__main__':
    cli()
