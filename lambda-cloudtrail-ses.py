import json
import urllib
import boto3
import gzip
import uuid
from datetime import date
import json
from operator import attrgetter
import email
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

print('Loading function')
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
client = boto3.client('sns')
arn_monk = 'arn:aws:sns:us-east-1:865013488897:monkofitcps-cloudtrail'
random=str(uuid.uuid4())
temp_file='/tmp/temp_' + random + '.gz'
def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    region = 'us-east-1'
    ses_client = boto3.client(service_name = 'ses', region_name = region)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    string=''
    sub=''
    try:
        response=s3.meta.client.download_file(bucket,key,temp_file)
        with gzip.open(temp_file, 'rb') as f:
            file_content = f.read()
        file_json=json.loads(file_content)
        if file_json is not None:
            for i in file_json.get('Records'):
                if 'AuthorizeSecurityGroup' in i.get('eventName'):
                    sub = 'Security group Rule with 0.0.0.0/0'
                    request = i.get('requestParameters')
                    string1='Globally Opened Security group Rule Alert' + '\n'
                    if '0.0.0.0/0' in str(request):
                        string1=string1 + "EventTime  : " + str(i.get('eventTime')) + '\n'
                        string1=string1 + "Security Group : " + str(i.get('requestParameters').get('groupId')) + '\n'
                        string1=string1 + "Region : " + str(i.get('awsRegion')) + '\n'
                        string1=string1 + "User : " + str(i.get('userIdentity').get('userName')) + '\n'
                        string1=string1 + "Account : " + str(i.get('userIdentity').get('accountId')) + '\n'
                        for rule in i.get('requestParameters').get('ipPermissions').get('items'):
                            if '0.0.0.0/0' in str(rule):
                                fromport=rule.get('fromPort')
                                toport=rule.get('toPort')
                                ipRange=rule.get('ipRanges').get('items')[0]
                                ipProtocol=rule.get('ipProtocol')
                                security_group = str(i.get('requestParameters').get('groupId'))
                                iamuser = str(i.get('userIdentity').get('userName'))
                                region_name = str(i.get('awsRegion'))
                                event_time = str(i.get('eventTime'))
                                account_id = str(i.get('userIdentity').get('accountId'))
                                if fromport!=80 or toport!=80:
                                    string1=string1 + "FromPort : " + str(fromport) + '\n'
                                    string1=string1 + "ToPort : " + str(toport) + '\n'
                                    string1=string1 + "ipProtocol : " + str(ipProtocol) + '\n'
                                    string1=string1 + "IpRange : " + str(ipRange) + '\n'
                                    string1=string1 + "--------------------------" + '\n'
                                    #publication = client.publish(TopicArn=arn_monk,Subject=sub,Message=str(string1))
                                    me = 'arunkmarcse@gmail.com'
                                    you = [iamuser, me]
                                    subject = 'Globally Opened Security Group Rule'
                                    #COMMASPACE = ', '
                                    #you = COMMASPACE.join(you)
                                    for tomails in you:
                                        destination = { 'ToAddresses' : [tomails],'CcAddresses' : [],'BccAddresses' : []}
                                        bodyhtml = """<html><head><style>body{background: ornage;}#pricing-table {margin: 150px auto;text-align: center;width: 892px; 
                                        /* total computed width = 222 x 3 + 226 */}#pricing-table .plan {font: 12px "Lucida Sans", "trebuchet MS", Arial, Helvetica;text-shadow: 0 1px rgba(255,255,255,.8);
                                        background: #fff;      border: 1px solid #ddd;color: #333;padding: 20px;width: 670px; /* (old 180) plan width = 180 + 20 + 20 + 1 + 1 = 222px */      
                                        float: left;position: relative;}#pricing-table #most-popular {z-index: 2;top: -140px;border-width: 3px;
                                        padding: 30px 20px;-moz-border-radius: 5px;-webkit-border-radius: 5px;border-radius: 5px;
                                        -moz-box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);
                                        -webkit-box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);
                                        box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);    }
                                        #pricing-table .plan:nth-child(1) {-moz-border-radius: 5px 0 0 5px;-webkit-border-radius: 5px 0 0 5px;
                                        border-radius: 5px 0 0 5px;        }#pricing-table .plan:nth-child(4) {-moz-border-radius: 0 5px 5px 0;
                                        -webkit-border-radius: 0 5px 5px 0;border-radius: 0 5px 5px 0;        }/* --------------- */            
                                        #pricing-table h3 {font-size: 20px;font-weight: normal;padding: 20px;margin: -20px -20px -10px -20px;
                                        background-color: #eee;background-image: -moz-linear-gradient(#fff,#eee);background-image: 
                                        -webkit-gradient(linear, left top, left bottom, from(#fff), to(#eee));    background-image: 
                                        -webkit-linear-gradient(#fff, #eee);background-image: -o-linear-gradient(#fff, #eee);background-image: 
                                        -ms-linear-gradient(#fff, #eee);background-image: linear-gradient(#fff, #eee);}
                                        #pricing-table #most-popular h3 {background-color: #ddd;background-image: -moz-linear-gradient(#eee,#ddd);
                                        background-image: -webkit-gradient(linear, left top, left bottom, from(#eee), to(#ddd));    background-image: 
                                        -webkit-linear-gradient(#eee, #ddd);background-image: -o-linear-gradient(#eee, #ddd);background-image: 
                                        -ms-linear-gradient(#eee, #ddd);background-image: linear-gradient(#eee, #ddd);margin-top: -30px;padding-top: 
                                        30px;-moz-border-radius: 5px 5px 0 0;-webkit-border-radius: 5px 5px 0 0;border-radius: 5px 5px 0 0; }
                                        #pricing-table .plan:nth-child(1) h3 {-moz-border-radius: 5px 0 0 0;-webkit-border-radius: 5px 0 0 0;
                                        border-radius: 5px 0 0 0;       }#pricing-table .plan:nth-child(4) h3 {-moz-border-radius: 0 5px 0 0;
                                        -webkit-border-radius: 0 5px 0 0;border-radius: 0 5px 0 0;       }              #pricing-table h3 span {display: block;
                                        font: bold 25px/100px Georgia, Serif;color: #777;background: #fff;border: 0px solid #fff;height: 98px;width: 476px;
                                        margin: 10px auto -65px;-moz-border-radius: 100px;-webkit-border-radius: 100px;border-radius: 100px;
                                        -moz-box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;-webkit-box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;}
                                        /* --------------- */#pricing-table ul {margin: 20px 0 0 0;padding: 0;list-style: none;}#pricing-table li {border-top: 1px solid #ddd;padding: 10px 0;}
                                        /* --------------- */#pricing-table .signup {position: relative;padding: 8px 20px;margin: 20px 0 0 0;  
                                        color: #fff;font: bold 14px Arial, Helvetica;/*    text-transform: uppercase; */text-decoration: none;display: inline-block;       
                                        background-color: #e82817;background-image: -moz-linear-gradient(#e82817, #db1c0a);background-image: 
                                        -webkit-gradient(linear, left top, left bottom, from(#e82817), to(#db1c0a));    background-image: 
                                        -webkit-linear-gradient(#e82817, #db1c0a);background-image: -o-linear-gradient(#e82817, #db1c0a);
                                        background-image: -ms-linear-gradient(#e82817, #db1c0a);background-image: linear-gradient(#e82817, #db1c0a);
                                        -moz-border-radius: 3px;-webkit-border-radius: 3px;border-radius: 3px;     text-shadow: 0 1px 0 rgba(0,0,0,.3);        
                                        -moz-box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);
                                        -webkit-box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);}#pricing-table .signup:hover {background-color: #db1c0a;background-image: 
                                        -moz-linear-gradient(#db1c0a, #e82817);background-image: 
                                        -webkit-gradient(linear, left top, left bottom, from(#db1c0a), to(#e82817));      background-image: 
                                        -webkit-linear-gradient(#db1c0a, #e82817);background-image: -o-linear-gradient(#db1c0a, #e82817);
                                        background-image: -ms-linear-gradient(#db1c0a, #e82817);background-image: linear-gradient(#db1c0a, #e82817); }
                                        #pricing-table .signup:active, #pricing-table .signup:focus {background: #db1c0a;       top: 2px;
                                        -moz-box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset;-webkit-box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset;
                                        box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset; }.right {align: right;}    
                                        /* --------------- */.clear:before, .clear:after {content:"";display:table}.clear:after {clear:both}.clear {zoom:1}
                                        </style></head><body><div id="pricing-table" class="clear"><div class="plan" id="most-popular" style=width="500px">
                                        <img src="https://s3.amazonaws.com/cftemplate-hackathon/verizon-logo-2.png" alt="Verizon Logo" align="left" height="50" width="60" style="padding-top: 50px;">
                                        <img src="https://s3.amazonaws.com/cftemplate-hackathon/security-alert-logo.gif" alt="Security Logo" align="right" height="50" width="60" style="padding-top: 50px;">
                                        <h3>Globally Opened Security Group Rule</h3><br><div class="signup">"""
                                        bodyhtml = bodyhtml+'0.0.0.0/0 Global Rule-Created</div>'
                                        bodyhtml = bodyhtml+'<b><p align="left">Security Group ID: '+security_group+'</p>'+'<p align="left">From Port: '+str(fromport)+'</p>'+'<p align="left">To Port: '+str(toport)+'</p>'+'<p align="left">IP Protocol: '+str(ipProtocol)+'</p>'+'<p align="left">IP Range: '+str(ipRange)+'</p>'
                                        bodyhtml = bodyhtml+'<p align="left">IAM User Name: '+iamuser+'</p>'+'<p align="left">Region: '+region_name+'</p>'+'<p align="left">EventTime: '+event_time+'</p>'+'<p align="left">Account ID: '+account_id+'</p></b>'
                                        bodyhtml = bodyhtml+"""<p align="left">Note: Creating Globally Opened Security group for ports other 80 is against Verizon's Security Policy. KIndly Delete this security group rule and recreate by providing IPs specific to inter verizon IP. 
                                        To Know more about Security Group, Please visit <a href="https://aws.amazon.com/whitepapers/aws-security-best-practices/">AWS Security Best Practices<a></p></div></div></body><html>""" 
                                        message = {'Subject' : {'Data' : subject},'Body': {'Html' : {'Data' : bodyhtml}}}
                                        result = ses_client.send_email(Source = me, Destination = destination, Message = message)
                if 'CreateVolume' in i.get('eventName'):
                    string2='Unencryption EBS Volume Created' + '\n'
                    sub = 'Unencryption EBS Volume Created'
                    request = i.get('requestParameters')
                    response_elements = i.get('responseElements')
                    print("EBS Volume Response Elements" +str(response_elements))
                    volume_id = response_elements.get('volumeId')
                    encrypted = str(response_elements.get('encrypted'))
                    iamuser = str(i.get('userIdentity').get('userName'))
                    region_name = str(i.get('awsRegion'))
                    event_time = str(i.get('eventTime'))
                    account_id = str(i.get('userIdentity').get('accountId'))
                    if encrypted == 'false' or 'False':
                        string2 = string2 + str(volume_id) + "created is not Encrypted"
                        event_time = str(i.get('eventTime'))
                        iam_user_name = str(i.get('userIdentity').get('userName'))
                        string2=string2+"IAM User Name "+str(iamuser)
                        string2=string2+"VolumeID "+str(volume_id)
                        #publication = client.publish(TopicArn=arn_monk,Subject=sub,Message=str(string2))
                        me = 'arunkmarcse@gmail.com'
                        you = [iamuser,me]
                        subject = 'UnEncrypted EBS Volume Creation Alert'
                        #COMMASPACE = ', '
                        #you = COMMASPACE.join(you)
                        for tomails in you:
                            destination = { 'ToAddresses' : [tomails],'CcAddresses' : [],'BccAddresses' : []}
                            bodyhtml = """<html><head><style>body{background: ornage;}#pricing-table {margin: 150px auto;text-align: center;width: 892px; 
                            /* total computed width = 222 x 3 + 226 */}#pricing-table .plan {font: 12px "Lucida Sans", "trebuchet MS", Arial, Helvetica;text-shadow: 0 1px rgba(255,255,255,.8);
                            background: #fff;      border: 1px solid #ddd;color: #333;padding: 20px;width: 670px; /* (old 180) plan width = 180 + 20 + 20 + 1 + 1 = 222px */      
                            float: left;position: relative;}#pricing-table #most-popular {z-index: 2;top: -140px;border-width: 3px;
                            padding: 30px 20px;-moz-border-radius: 5px;-webkit-border-radius: 5px;border-radius: 5px;
                            -moz-box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);
                            -webkit-box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);
                            box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);    }
                            #pricing-table .plan:nth-child(1) {-moz-border-radius: 5px 0 0 5px;-webkit-border-radius: 5px 0 0 5px;
                            border-radius: 5px 0 0 5px;        }#pricing-table .plan:nth-child(4) {-moz-border-radius: 0 5px 5px 0;
                            -webkit-border-radius: 0 5px 5px 0;border-radius: 0 5px 5px 0;        }/* --------------- */            
                            #pricing-table h3 {font-size: 20px;font-weight: normal;padding: 20px;margin: -20px -20px -10px -20px;
                            background-color: #eee;background-image: -moz-linear-gradient(#fff,#eee);background-image: 
                            -webkit-gradient(linear, left top, left bottom, from(#fff), to(#eee));    background-image: 
                            -webkit-linear-gradient(#fff, #eee);background-image: -o-linear-gradient(#fff, #eee);background-image: 
                            -ms-linear-gradient(#fff, #eee);background-image: linear-gradient(#fff, #eee);}
                            #pricing-table #most-popular h3 {background-color: #ddd;background-image: -moz-linear-gradient(#eee,#ddd);
                            background-image: -webkit-gradient(linear, left top, left bottom, from(#eee), to(#ddd));    background-image: 
                            -webkit-linear-gradient(#eee, #ddd);background-image: -o-linear-gradient(#eee, #ddd);background-image: 
                            -ms-linear-gradient(#eee, #ddd);background-image: linear-gradient(#eee, #ddd);margin-top: -30px;padding-top: 
                            30px;-moz-border-radius: 5px 5px 0 0;-webkit-border-radius: 5px 5px 0 0;border-radius: 5px 5px 0 0; }
                            #pricing-table .plan:nth-child(1) h3 {-moz-border-radius: 5px 0 0 0;-webkit-border-radius: 5px 0 0 0;
                            border-radius: 5px 0 0 0;       }#pricing-table .plan:nth-child(4) h3 {-moz-border-radius: 0 5px 0 0;
                            -webkit-border-radius: 0 5px 0 0;border-radius: 0 5px 0 0;       }              #pricing-table h3 span {display: block;
                            font: bold 25px/100px Georgia, Serif;color: #777;background: #fff;border: 0px solid #fff;height: 98px;width: 476px;
                            margin: 10px auto -65px;-moz-border-radius: 100px;-webkit-border-radius: 100px;border-radius: 100px;
                            -moz-box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;-webkit-box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;}
                            /* --------------- */#pricing-table ul {margin: 20px 0 0 0;padding: 0;list-style: none;}#pricing-table li {border-top: 1px solid #ddd;padding: 10px 0;}
                            /* --------------- */#pricing-table .signup {position: relative;padding: 8px 20px;margin: 20px 0 0 0;  
                            color: #fff;font: bold 14px Arial, Helvetica;/*    text-transform: uppercase; */text-decoration: none;display: inline-block;       
                            background-color: #e82817;background-image: -moz-linear-gradient(#e82817, #db1c0a);background-image: 
                            -webkit-gradient(linear, left top, left bottom, from(#e82817), to(#db1c0a));    background-image: 
                            -webkit-linear-gradient(#e82817, #db1c0a);background-image: -o-linear-gradient(#e82817, #db1c0a);
                            background-image: -ms-linear-gradient(#e82817, #db1c0a);background-image: linear-gradient(#e82817, #db1c0a);
                            -moz-border-radius: 3px;-webkit-border-radius: 3px;border-radius: 3px;     text-shadow: 0 1px 0 rgba(0,0,0,.3);        
                            -moz-box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);
                            -webkit-box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);}#pricing-table .signup:hover {background-color: #db1c0a;background-image: 
                            -moz-linear-gradient(#db1c0a, #e82817);background-image: 
                            -webkit-gradient(linear, left top, left bottom, from(#db1c0a), to(#e82817));      background-image: 
                            -webkit-linear-gradient(#db1c0a, #e82817);background-image: -o-linear-gradient(#db1c0a, #e82817);
                            background-image: -ms-linear-gradient(#db1c0a, #e82817);background-image: linear-gradient(#db1c0a, #e82817); }
                            #pricing-table .signup:active, #pricing-table .signup:focus {background: #db1c0a;       top: 2px;
                            -moz-box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset;-webkit-box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset;
                            box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset; }.right {align: right;}    
                            /* --------------- */.clear:before, .clear:after {content:"";display:table}.clear:after {clear:both}.clear {zoom:1}
                            </style></head><body><div id="pricing-table" class="clear"><div class="plan" id="most-popular" style=width="500px">
                            <img src="https://s3.amazonaws.com/cftemplate-hackathon/verizon-logo-2.png" alt="Verizon Logo" align="left" height="50" width="60" style="padding-top: 50px;">
                            <img src="https://s3.amazonaws.com/cftemplate-hackathon/security-alert-logo.gif" alt="Security Logo" align="right" height="50" width="60" style="padding-top: 50px;">
                            <h3>Unencrypted EBS Volume Created</h3><br><div class="signup">"""
                            bodyhtml = bodyhtml+'Volume ID: '+str(volume_id)+'</div>'
                            bodyhtml = bodyhtml+'<p align="left">Encrypted: '+encrypted+'</p>'+'<p align="left">IAM User Name: '+iamuser+'</p>'+'<p align="left">Region: '+region_name+'</p>'+'<p align="left">EventTime: '+event_time+'</p>'+'<p align="left">Account ID: '+account_id+'</p></b>'
                            bodyhtml = bodyhtml+"""<p align="left">Creating Unenrypted EBS Volume is aginst Verizon's Security Policy. KIndly Delete this EBS Volume and recreate by enabling the encryption option. 
                            To Know more about EBS Encryption, Please visit <a href="http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html">AWS EBS Encryption<a></p></div></div></body><html>""" 
                            message = {'Subject' : {'Data' : subject},'Body': {'Html' : {'Data' : bodyhtml}}}
                            result = ses_client.send_email(Source = me, Destination = destination, Message = message)
                if 'CreateDBInstance' in i.get('eventName'):
                    string2='Unencryption RDS Instance Created' + '\n'
                    sub = 'Unencryption RDS Instance Created'
                    request_parameters = i.get('requestParameters')
                    response_elements = i.get('responseElements')
                    event_time = i.get('eventTime')
                    event_region = i.get('awsRegion')
                    rds_instance_identifier = response_elements.get('dBInstanceIdentifier')
                    storage_encrypted = str(response_elements.get('storageEncrypted'))
                    iamuser = str(i.get('userIdentity').get('userName'))
                    region_name = str(i.get('awsRegion'))
                    event_time = str(i.get('eventTime'))
                    account_id = str(i.get('userIdentity').get('accountId'))
                    print("RDS Instance Response Elements" +str(response_elements))
                    if encrypted == 'false' or 'False':
                        string2 = string2 + str(rds_instance_identifier) + "created is not Encrypted is created by" +str(iamuser)
                        event_time = str(i.get('eventTime'))
                        #publication = client.publish(TopicArn=arn_monk,Subject=sub,Message=str(string2))
                        me = 'arunkmarcse@gmail.com'
                        you = [iamuser,me]
                        subject = 'UnEncrypted RDS Instance Creation Alert'
                        #COMMASPACE = ', '
                        #you = COMMASPACE.join(you)
                        for tomails in you:
                            destination = { 'ToAddresses' : [tomails],'CcAddresses' : [],'BccAddresses' : []}
                            bodyhtml = """<html><head><style>body{background: ornage;}#pricing-table {margin: 150px auto;text-align: center;width: 892px; 
                            /* total computed width = 222 x 3 + 226 */}#pricing-table .plan {font: 12px "Lucida Sans", "trebuchet MS", Arial, Helvetica;text-shadow: 0 1px rgba(255,255,255,.8);
                            background: #fff;      border: 1px solid #ddd;color: #333;padding: 20px;width: 670px; /* (old 180) plan width = 180 + 20 + 20 + 1 + 1 = 222px */      
                            float: left;position: relative;}#pricing-table #most-popular {z-index: 2;top: -140px;border-width: 3px;
                            padding: 30px 20px;-moz-border-radius: 5px;-webkit-border-radius: 5px;border-radius: 5px;
                            -moz-box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);
                            -webkit-box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);
                            box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);    }
                            #pricing-table .plan:nth-child(1) {-moz-border-radius: 5px 0 0 5px;-webkit-border-radius: 5px 0 0 5px;
                            border-radius: 5px 0 0 5px;        }#pricing-table .plan:nth-child(4) {-moz-border-radius: 0 5px 5px 0;
                            -webkit-border-radius: 0 5px 5px 0;border-radius: 0 5px 5px 0;        }/* --------------- */            
                            #pricing-table h3 {font-size: 20px;font-weight: normal;padding: 20px;margin: -20px -20px -10px -20px;
                            background-color: #eee;background-image: -moz-linear-gradient(#fff,#eee);background-image: 
                            -webkit-gradient(linear, left top, left bottom, from(#fff), to(#eee));    background-image: 
                            -webkit-linear-gradient(#fff, #eee);background-image: -o-linear-gradient(#fff, #eee);background-image: 
                            -ms-linear-gradient(#fff, #eee);background-image: linear-gradient(#fff, #eee);}
                            #pricing-table #most-popular h3 {background-color: #ddd;background-image: -moz-linear-gradient(#eee,#ddd);
                            background-image: -webkit-gradient(linear, left top, left bottom, from(#eee), to(#ddd));    background-image: 
                            -webkit-linear-gradient(#eee, #ddd);background-image: -o-linear-gradient(#eee, #ddd);background-image: 
                            -ms-linear-gradient(#eee, #ddd);background-image: linear-gradient(#eee, #ddd);margin-top: -30px;padding-top: 
                            30px;-moz-border-radius: 5px 5px 0 0;-webkit-border-radius: 5px 5px 0 0;border-radius: 5px 5px 0 0; }
                            #pricing-table .plan:nth-child(1) h3 {-moz-border-radius: 5px 0 0 0;-webkit-border-radius: 5px 0 0 0;
                            border-radius: 5px 0 0 0;       }#pricing-table .plan:nth-child(4) h3 {-moz-border-radius: 0 5px 0 0;
                            -webkit-border-radius: 0 5px 0 0;border-radius: 0 5px 0 0;       }              #pricing-table h3 span {display: block;
                            font: bold 25px/100px Georgia, Serif;color: #777;background: #fff;border: 0px solid #fff;height: 98px;width: 476px;
                            margin: 10px auto -65px;-moz-border-radius: 100px;-webkit-border-radius: 100px;border-radius: 100px;
                            -moz-box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;-webkit-box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;}
                            /* --------------- */#pricing-table ul {margin: 20px 0 0 0;padding: 0;list-style: none;}#pricing-table li {border-top: 1px solid #ddd;padding: 10px 0;}
                            /* --------------- */#pricing-table .signup {position: relative;padding: 8px 20px;margin: 20px 0 0 0;  
                            color: #fff;font: bold 14px Arial, Helvetica;/*    text-transform: uppercase; */text-decoration: none;display: inline-block;       
                            background-color: #e82817;background-image: -moz-linear-gradient(#e82817, #db1c0a);background-image: 
                            -webkit-gradient(linear, left top, left bottom, from(#e82817), to(#db1c0a));    background-image: 
                            -webkit-linear-gradient(#e82817, #db1c0a);background-image: -o-linear-gradient(#e82817, #db1c0a);
                            background-image: -ms-linear-gradient(#e82817, #db1c0a);background-image: linear-gradient(#e82817, #db1c0a);
                            -moz-border-radius: 3px;-webkit-border-radius: 3px;border-radius: 3px;     text-shadow: 0 1px 0 rgba(0,0,0,.3);        
                            -moz-box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);
                            -webkit-box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);}#pricing-table .signup:hover {background-color: #db1c0a;background-image: 
                            -moz-linear-gradient(#db1c0a, #e82817);background-image: 
                            -webkit-gradient(linear, left top, left bottom, from(#db1c0a), to(#e82817));      background-image: 
                            -webkit-linear-gradient(#db1c0a, #e82817);background-image: -o-linear-gradient(#db1c0a, #e82817);
                            background-image: -ms-linear-gradient(#db1c0a, #e82817);background-image: linear-gradient(#db1c0a, #e82817); }
                            #pricing-table .signup:active, #pricing-table .signup:focus {background: #db1c0a;       top: 2px;
                            -moz-box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset;-webkit-box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset;
                            box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset; }.right {align: right;}    
                            /* --------------- */.clear:before, .clear:after {content:"";display:table}.clear:after {clear:both}.clear {zoom:1}
                            </style></head><body><div id="pricing-table" class="clear"><div class="plan" id="most-popular" style=width="500px">
                            <img src="https://s3.amazonaws.com/cftemplate-hackathon/verizon-logo-2.png" alt="Verizon Logo" align="left" height="50" width="60" style="padding-top: 50px;">
                            <img src="https://s3.amazonaws.com/cftemplate-hackathon/security-alert-logo.gif" alt="Security Logo" align="right" height="50" width="60" style="padding-top: 50px;">
                            <h3>Unencrypted RDS Instance Created</h3><br><div class="signup">"""
                            bodyhtml = bodyhtml+'RDS Instance ID: '+str(rds_instance_identifier)+'</div>'
                            bodyhtml = bodyhtml+'<p  align="left">Storage Encrypted: '+storage_encrypted+'</p>'+'<p  align="left">IAM User Name: '+iamuser+'</p>'+'<p  align="left">Region: '+region_name+'</p>'+'<p  align="left">EventTime: '+event_time+'</p>'+'<p  align="left">Account ID: '+account_id+'</p>'
                            bodyhtml = bodyhtml+"""<p  align="left">Creating Unencrypted RDS Instance is aginst Verizon's Security Policy. KIndly Delete this RDS Instance and recreate by enabling the storage encryption option. 
                            To Know more about RDS Encryption, Please visit <a href="http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html">AWS RDS Encryption<a></p></div></div></body><html>""" 
                            message = {'Subject' : {'Data' : subject},'Body': {'Html' : {'Data' : bodyhtml}}}
                            result = ses_client.send_email(Source = me, Destination = destination, Message = message)
                if 'CreateBucket' in i.get('eventName'):
                    event_request = i.get('eventName')
                    request_parameters = i.get('requestParameters')
                    bucket_name = request_parameters.get('bucketName')
                    print("S3 Bucket Event" +str(event_request))
                    print("S3 Bucket Request_Parameters:" +str(request_parameters))
                    response = s3_client.get_bucket_acl(Bucket=bucket_name)
                    grant = response.get('Grants')
                    for grantitem in grant:
                        grant_flag = 'false'
                        if grantitem['Permission'] != 'FULL_CONTROL':
                            grant_type = grantitem['Permission']
                            groups = grantitem['Grantee']['URI']
                            group_val = groups.split('/')[-1]
                            if grant_type == 'READ' and group_val == 'AllUsers':
                                grant_flag = 'true'
                                print("READ is globally opened")
                            if grant_type == 'WRITE' and group_val == 'AllUsers':
                                grant_flag = 'true'
                                print("WRITE is globally opened")
                            if grant_flag == 'true' or 'True':
                                iam_user_name = str(i.get('userIdentity').get('userName'))
                                string2 = 'Globally Opened S3 Bucket'        
                                string2 = string2 + str(bucket_name) + "created is globally Opened created by" +str(iam_user_name)
                                event_time = str(i.get('eventTime'))
                                #publication = client.publish(TopicArn=arn_monk,Subject=sub,Message=str(string2))
                                #print("*******Globally Opened S3 Bucket**** Notification Sent")
                            iamuser = str(i.get('userIdentity').get('userName'))
                            region_name = str(i.get('awsRegion'))
                            event_time = str(i.get('eventTime'))
                            account_id = str(i.get('userIdentity').get('accountId'))
                            me = 'arunkmarcse@gmail.com'
                            you = [iamuser,me]
                            subject = 'S3 Bucket with Publicly opened ACL'
                            #COMMASPACE = ', '
                            #you = COMMASPACE.join(you)
                            for tomails in you:
                                destination = { 'ToAddresses' : [tomails],'CcAddresses' : [],'BccAddresses' : []}
                                bodyhtml = """<html><head><style>body{background: ornage;}#pricing-table {margin: 150px auto;text-align: center;width: 892px; 
                                /* total computed width = 222 x 3 + 226 */}#pricing-table .plan {font: 12px "Lucida Sans", "trebuchet MS", Arial, Helvetica;text-shadow: 0 1px rgba(255,255,255,.8);
                                background: #fff;      border: 1px solid #ddd;color: #333;padding: 20px;width: 670px; /* (old 180) plan width = 180 + 20 + 20 + 1 + 1 = 222px */      
                                float: left;position: relative;}#pricing-table #most-popular {z-index: 2;top: -140px;border-width: 3px;
                                padding: 30px 20px;-moz-border-radius: 5px;-webkit-border-radius: 5px;border-radius: 5px;
                                -moz-box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);
                                -webkit-box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);
                                box-shadow: 20px 0 10px -10px rgba(0, 0, 0, .15), -20px 0 10px -10px rgba(0, 0, 0, .15);    }
                                #pricing-table .plan:nth-child(1) {-moz-border-radius: 5px 0 0 5px;-webkit-border-radius: 5px 0 0 5px;
                                border-radius: 5px 0 0 5px;        }#pricing-table .plan:nth-child(4) {-moz-border-radius: 0 5px 5px 0;
                                -webkit-border-radius: 0 5px 5px 0;border-radius: 0 5px 5px 0;        }/* --------------- */            
                                #pricing-table h3 {font-size: 20px;font-weight: normal;padding: 20px;margin: -20px -20px -10px -20px;
                                background-color: #eee;background-image: -moz-linear-gradient(#fff,#eee);background-image: 
                                -webkit-gradient(linear, left top, left bottom, from(#fff), to(#eee));    background-image: 
                                -webkit-linear-gradient(#fff, #eee);background-image: -o-linear-gradient(#fff, #eee);background-image: 
                                -ms-linear-gradient(#fff, #eee);background-image: linear-gradient(#fff, #eee);}
                                #pricing-table #most-popular h3 {background-color: #ddd;background-image: -moz-linear-gradient(#eee,#ddd);
                                background-image: -webkit-gradient(linear, left top, left bottom, from(#eee), to(#ddd));    background-image: 
                                -webkit-linear-gradient(#eee, #ddd);background-image: -o-linear-gradient(#eee, #ddd);background-image: 
                                -ms-linear-gradient(#eee, #ddd);background-image: linear-gradient(#eee, #ddd);margin-top: -30px;padding-top: 
                                30px;-moz-border-radius: 5px 5px 0 0;-webkit-border-radius: 5px 5px 0 0;border-radius: 5px 5px 0 0; }
                                #pricing-table .plan:nth-child(1) h3 {-moz-border-radius: 5px 0 0 0;-webkit-border-radius: 5px 0 0 0;
                                border-radius: 5px 0 0 0;       }#pricing-table .plan:nth-child(4) h3 {-moz-border-radius: 0 5px 0 0;
                                -webkit-border-radius: 0 5px 0 0;border-radius: 0 5px 0 0;       }              #pricing-table h3 span {display: block;
                                font: bold 25px/100px Georgia, Serif;color: #777;background: #fff;border: 0px solid #fff;height: 98px;width: 476px;
                                margin: 10px auto -65px;-moz-border-radius: 100px;-webkit-border-radius: 100px;border-radius: 100px;
                                -moz-box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;-webkit-box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;box-shadow: 0 5px 20px #ddd inset, 0 3px 0 #999 inset;}
                                /* --------------- */#pricing-table ul {margin: 20px 0 0 0;padding: 0;list-style: none;}#pricing-table li {border-top: 1px solid #ddd;padding: 10px 0;}
                                /* --------------- */#pricing-table .signup {position: relative;padding: 8px 20px;margin: 20px 0 0 0;  
                                color: #fff;font: bold 14px Arial, Helvetica;/*    text-transform: uppercase; */text-decoration: none;display: inline-block;       
                                background-color: #e82817;background-image: -moz-linear-gradient(#e82817, #db1c0a);background-image: 
                                -webkit-gradient(linear, left top, left bottom, from(#e82817), to(#db1c0a));    background-image: 
                                -webkit-linear-gradient(#e82817, #db1c0a);background-image: -o-linear-gradient(#e82817, #db1c0a);
                                background-image: -ms-linear-gradient(#e82817, #db1c0a);background-image: linear-gradient(#e82817, #db1c0a);
                                -moz-border-radius: 3px;-webkit-border-radius: 3px;border-radius: 3px;     text-shadow: 0 1px 0 rgba(0,0,0,.3);        
                                -moz-box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);
                                -webkit-box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);box-shadow: 0 1px 0 rgba(255, 255, 255, .5), 0 2px 0 rgba(0, 0, 0, .7);}#pricing-table .signup:hover {background-color: #db1c0a;background-image: 
                                -moz-linear-gradient(#db1c0a, #e82817);background-image: 
                                -webkit-gradient(linear, left top, left bottom, from(#db1c0a), to(#e82817));      background-image: 
                                -webkit-linear-gradient(#db1c0a, #e82817);background-image: -o-linear-gradient(#db1c0a, #e82817);
                                background-image: -ms-linear-gradient(#db1c0a, #e82817);background-image: linear-gradient(#db1c0a, #e82817); }
                                #pricing-table .signup:active, #pricing-table .signup:focus {background: #db1c0a;       top: 2px;
                                -moz-box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset;-webkit-box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset;
                                box-shadow: 0 0 3px rgba(0, 0, 0, .7) inset; }.right {align: right;}    
                                /* --------------- */.clear:before, .clear:after {content:"";display:table}.clear:after {clear:both}.clear {zoom:1}
                                </style></head><body><div id="pricing-table" class="clear"><div class="plan" id="most-popular" style=width="500px">
                                <img src="https://s3.amazonaws.com/cftemplate-hackathon/verizon-logo-2.png" alt="Verizon Logo" align="left" height="50" width="60" style="padding-top: 50px;">
                                <img src="https://s3.amazonaws.com/cftemplate-hackathon/security-alert-logo.gif" alt="Security Logo" align="right" height="50" width="60" style="padding-top: 50px;">
                                <h3>S3 Bucket with Public ACL Opened</h3><br><div class="signup">"""
                                bodyhtml = bodyhtml+'S3 Bucket Name: '+str(bucket_name)+'</div>'
                                bodyhtml = bodyhtml+'<p align="left">IAM User Name: '+iamuser+'</p>'+'<p align="left">Region: '+region_name+'</p>'+'<p align="left">EventTime: '+event_time+'</p>'+'<p align="left">Account ID: '+account_id+'</p>'
                                bodyhtml = bodyhtml+"""<p align="left">Creating S3 Bucket with globally accessible policy at ACL rule is aginst Verizon's Security Policy. KIndly Delete this RDS Instance and recreate by enabling the storage encryption option. 
                                To Know more about S3 Bucket ACL, Please visit <a href="http://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html">AWS S3 Bucket ACL<a></p></div></div></body><html>""" 
                                message = {'Subject' : {'Data' : subject},'Body': {'Html' : {'Data' : bodyhtml}}}
                                result = ses_client.send_email(Source = me, Destination = destination, Message = message)
                        
                         
    except Exception as e:
        print(e)
