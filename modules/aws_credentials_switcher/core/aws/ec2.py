import boto3

class Ec2:

    def __init__(self, instance):
        instance = instance['Instances'][0]
        
        self.monitoring = self.get_att(instance,'Monitoring')
        self.publicDnsName = self.get_att(instance,'PublicDnsName')
        self.stateReason = self.get_att(instance,'StateReason')
        self.state = self.get_att(instance,'State')
        self.ebsOptimized = self.get_att(instance,'EbsOptimized')
        self.launchTime = self.get_att(instance,'LaunchTime')
        self.publicIpAddress = self.get_att(instance,'PublicIpAddress')
        self.privateIpAddress = self.get_att(instance,'PrivateIpAddress')
        self.productCodes = self.get_att(instance,'ProductCodes')
        self.vpcId = self.get_att(instance,'VpcId')
        self.cpuOptions = self.get_att(instance,'CpuOptions')
        self.stateTransitionReason = self.get_att(instance,'StateTransitionReason')
        self.instanceId = self.get_att(instance,'InstanceId')
        self.imageId = self.get_att(instance,'ImageId')
        self.privateDnsName = self.get_att(instance,'PrivateDnsName')
        self.keyPair = self.get_att(instance,'KeyName')
        self.securityGroups = self.get_att(instance,'SecurityGroups')
        self.clientToken = self.get_att(instance,'ClientToken')
        self.subnetId = self.get_att(instance,'SubnetId')
        self.instanceType = self.get_att(instance,'InstanceType')
        self.networkInterfaces = self.get_att(instance,'NetworkInterfaces')
        self.sourceDestCheck = self.get_att(instance,'SourceDestCheck')
        self.placement = self.get_att(instance,'Placement')
        self.hypervisor = self.get_att(instance,'Hypervisor')
        self.blockDeviceMappings = self.get_att(instance,'BlockDeviceMappings')
        self.architecture = self.get_att(instance,'Architecture')
        self.rootDeviceType = self.get_att(instance,'RootDeviceType')
        self.rootDeviceName = self.get_att(instance,'RootDeviceName')
        self.virtualizationType = self.get_att(instance,'VirtualizationType')
        self.tags = self.get_att(instance,'Tags')
        self.instanceName = self.get_tag_value('Name')
        self.instanceEnvironment = self.get_tag_value('Environment')
        self.instanceApplicationType = self.get_tag_value('Type')
        self.amiLaunchIndex = self.get_att(instance,'AmiLaunchIndex')
        
    def get_att(self, obj, prop):
        
        if obj == None:
            return ''
        # Como pode acontecer do boto nao retornar nenhum valor, 
        # retornamos nada para que o atributo exista, porem vazio
        
        if prop in obj:
            return obj[prop]
        else:
            return ''
    
    def get_all(self):

        ec2 = boto3.client('ec2')
        instances = ec2.describe_instances()['Reservations']
        ec2_list = []

        for instace in instances:
            try:
                ec2_list.append(Ec2(instace))
            except:
                "Erro ao inserir objeto Ec2 na lista"

        return ec2_list 
    
    def get_attributes(self):
        """ 
            Metodo com que somente printa todos os atributos da classe 
            para saber como montar o seu header 
        """
        # 
        my_self = self.__dict__
        
        for key in my_self.keys():
            print(key)

    def get_tag_value(self, key):
        """ 
            Metodo que recebe uma a key de uma TAG
            e retorna o seu valor
        """


        tag_value = ''
        # Valor default para caso a busca nao retorne nada 
        for tag in self.tags:
            if tag['Key'] == key:
                tag_value = tag['Value']
        return tag_value            