from __future__ import print_function

import json
import boto3

print('Loading function')
arn_monk = 'arn:aws:sns:us-east-1:865013488897:monkofitcps-config'
client_sns = boto3.client('sns')
def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print ("From Event:" + str(event))
    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + str(message))
    message_json = json.loads(message)
    message_type = str(message_json['messageType'])
    if message_type == "ConfigurationItemChangeNotification":
        resource_type = message_json["configurationItem"]["resourceType"]
        event_type = message_json["configurationItemDiff"]["changeType"]
        if resource_type == "AWS::EC2::Volume" and event_type == "CREATE":
            event_type = message_json["configurationItemDiff"]["changeType"]
            encrypted = str(message_json["configurationItem"]["configuration"]["encrypted"])
            volumeid = message_json["configurationItem"]["configuration"]["volumeId"]
            volume_size = message_json["configurationItem"]["configuration"]["size"]
            creation_time = message_json["configurationItem"]["resourceCreationTime"]
            aws_account_id = message_json["configurationItem"]["awsAccountId"]
            aws_region = message_json["configurationItem"]["awsRegion"]
            availabilityZone = message_json["configurationItem"]["availabilityZone"]
            print("Type of Operation:" + str(event_type))
            print("Encrypted:" + str(encrypted))
            print("volumeid:" + str(volumeid))
            print("volume_size:" + str(volume_size))
            print("creation_time:" + str(creation_time))
            sub = 'EBS Not Encrypted'
            string2 = "EBS Not Encrypted" + '\n'
            string2 = string2 +"Volume ID: "+str(volumeid) +'\n'
            string2 = string2 +"Volume Size: "+str(volume_size)+ '\n'
            string2 = string2 +"Creation Time: "+str(creation_time)+ '\n'
            string2 = string2 +"AWS Account ID: "+str(aws_account_id)+ '\n'
            string2 = string2 +"AWS Region: "+str(aws_region)+ '\n'
            string2 = string2 +"Availability Zone: "+str(availabilityZone)+ '\n'
            if encrypted == "False" or "false":
                publication = client_sns.publish(TopicArn=arn_monk,Subject=sub,Message=str(string2))
                print("****************EBS Not Encrypted - Notification Sent**********")
        if resource_type == "AWS::RDS::DBInstance" and event_type == "CREATE":
            event_type = message_json["configurationItemDiff"]["changeType"]
            aws_account_id = message_json["configurationItem"]["awsAccountId"]
            aws_region = message_json["configurationItem"]["awsRegion"]
            availabilityZone = message_json["configurationItem"]["availabilityZone"]
            creation_time = message_json["configurationItem"]["resourceCreationTime"]
            db_instance_id = message_json["configurationItem"]["configuration"]["dBInstanceIdentifier"]
            db_instance_type = message_json["configurationItem"]["configuration"]["dBInstanceClass"]
            db_encrypted = str(message_json["configurationItem"]["configuration"]["storageEncrypted"])
            sub = "RDS Not Encrypted"
            string2 = "RDS Not Encrypted"
            if db_encrypted == "False" or "false":
                publication = client_sns.publish(TopicArn=arn_monk,Subject=sub,Message=str(string2))
                print("****************RDS Not Encrypted - Notification Sent**********")
        if resource_type == "AWS::S3::Bucket" and event_type == "CREATE":
            event_type = message_json["configurationItemDiff"]["changeType"]
            aws_account_id = message_json["configurationItem"]["awsAccountId"]
            aws_region = message_json["configurationItem"]["awsRegion"]
            availabilityZone = message_json["configurationItem"]["availabilityZone"]
            creation_time = message_json["configurationItem"]["resourceCreationTime"]
            bucket_name = message_json["configurationItem"]["configuration"]["name"]
            acl = message_json["configurationItem"]["supplementaryConfiguration"]["AccessControlList"]
            acl_json = json.loads(acl)
            grant_list = acl_json['grantList']
            grant_val = 'true'
            for i in grant_list:
                if i.get('grantee') == 'AllUsers' and i.get('permission') == 'Read':
                    grant_val = 'false'
                if i.get('grantee') == 'AllUsers' and i.get('permission') == 'Write':
                    grant_val = 'false'
            print("S3 ACCESS Control List:" +str(acl)) 
            print("Type of ACL:" +str(type(acl)))
            sub = 'Globally opened S3 bucket'
            string2 = 'Globally opened S3 bucket'
            if grant_val == 'false':
                publication = client_sns.publish(TopicArn=arn_monk,Subject=sub,Message=str(string2))
                print("*************Globally Opened S3 bucket - Notification Sent**********")
        if resource_type == "AWS::EC2::SecurityGroup" and event_type == "CREATE":
            event_type = message_json["configurationItemDiff"]["changeType"]
            aws_account_id = message_json["configurationItem"]["awsAccountId"]
            aws_region = message_json["configurationItem"]["awsRegion"]
            availabilityZone = message_json["configurationItem"]["availabilityZone"]
            creation_time = message_json["configurationItem"]["resourceCreationTime"]
            sec_group_name = message_json["configurationItem"]["configuration"]["groupName"]
            sec_group_id = message_json["configurationItem"]["configuration"]["groupId"]
            sec_group_description = message_json["configurationItem"]["configuration"]["description"]
            ippermissions = message_json["configurationItem"]["configuration"]["ipPermissions"]
            #ippermissions_json = json.loads(ippermissions)
            for ip in ippermissions:
                ipprotocol = str(ip.get('ipProtocol'))
                ip_fromport = str(ip.get('fromPort'))
                ip_toport = str(ip.get('toPort'))
                ipRanges_list = ip.get('ipRanges')
                print("ip_fromport:" +ip_fromport)
                print("ip_toport:" +ip_toport)
                print("ipRanges_list:" +str(ipRanges_list))
                if ip_fromport != '80' and ip_toport != '80':
                    for ipranges in ipRanges_list:
                        if ipranges == '0.0.0.0/0':
                            sub = 'Globally opened Security Group identified other than port 80'
                            string2 = 'Globally opened Security Group identified other than port 80'
                            publication = client_sns.publish(TopicArn=arn_monk,Subject=sub,Message=str(string2))
                            print("*************Globally Security Group Identified - Notification Sent**********")
        if resource_type == "AWS::EC2::SecurityGroup" and event_type == "UPDATE":
            event_type = message_json["configurationItemDiff"]["changeType"]
            aws_account_id = message_json["configurationItem"]["awsAccountId"]
            aws_region = message_json["configurationItem"]["awsRegion"]
            availabilityZone = message_json["configurationItem"]["availabilityZone"]
            creation_time = message_json["configurationItem"]["resourceCreationTime"]
            sec_group_name = message_json["configurationItem"]["configuration"]["groupName"]
            sec_group_id = message_json["configurationItem"]["configuration"]["groupId"]
            sec_group_description = message_json["configurationItem"]["configuration"]["description"]
            updated_value = message_json["configurationItemDiff"]["changedProperties"]
            for changekey, changevalue in updated_value.iteritems():
                print("Change Value Type " +str(type(changevalue) ))
                print("Change Key " +str(changekey))
                print("Change Value " +str(changevalue))
                change_type = changevalue.get('changeType')
                change_updated_val = changevalue.get('updatedValue')
                if change_type != 'DELETE':
                    ipprotocol = str(change_updated_val.get('ipProtocol'))
                    ip_fromport = str(change_updated_val.get('fromPort'))
                    ip_toport = str(change_updated_val.get('toPort'))
                    ipRanges_list = change_updated_val.get('ipRanges')
                    ipv4Ranges_list = change_updated_val.get('ipv4Ranges')
                    globally_open = 'false'
                    if ip_fromport != '80' or ip_toport != '80':
                        for ipranges in ipRanges_list:
                            if ipranges == '0.0.0.0/0':
                                globally_open = 'true'
                                print("Globally Opened1" +str(globally_open))
                        for ipv4ranges in ipv4Ranges_list:
                            if str(ipv4ranges.get('cidrIp')) == '0.0.0.0/0':
                                globally_open = 'true'
                                print("Globally Opened2" +str(globally_open))
                    if 	globally_open == 'true':
                        sub = 'Globally opened Security Group Updated other than port 80'
                        string2 = 'Globally opened Security Group Updated other than port 80'
                        publication = client_sns.publish(TopicArn=arn_monk,Subject=sub,Message=str(string2))
                        print("*************Globally Security Group Identified - Notification Sent**********")
        
        
    return message
