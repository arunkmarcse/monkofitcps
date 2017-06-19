from __future__ import print_function

import json
import urllib
import boto3
from operator import attrgetter
import email
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

print('Loading function')

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')
arn_monk = 'arn:aws:sns:us-east-1:865013488897:monkofitcps-config'
client_sns = boto3.client('sns')
region = 'us-east-1'
ses_client = boto3.client(service_name = 'ses', region_name = region)

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    print("***EVENT***" +str(event))
    bucket = event['Records'][0]['s3']['bucket']['name']
    region_name = event['Records'][0]['awsRegion']
    account_id = '865013488897'
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        #response = s3.get_object(Bucket=bucket, Key=key)
        #response = s3.Object(bucket,key)
        response = s3.head_object(Bucket=bucket, Key=key)
        print("Response HEAD OBJECT: " +str(response))
        response_keys = response.keys()
        if 'ServerSideEncryption' not in response_keys:
            sub = 'S3 File Not Encrypted'
            string2 = "S3 File Not Encrypted"
            #publication = client_sns.publish(TopicArn=arn_monk,Subject=sub,Message=str(string2))
            me = 'arunkmarcse@gmail.com'
            iamuser = 'arunkumarpix@gmail.com'
            you = [iamuser,me]
            subject = 'S3 File Not Encrypted Alert'
            content_type = str(response['ContentType'])
            event_time = response['ResponseMetadata']['HTTPHeaders']['last-modified']
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
                <h3>Unencrypted File Uploaded to S3 Bucket</h3><br><div class="signup">"""
                bodyhtml = bodyhtml+'S3 Bucket Name: '+str(bucket)+'</div>'
                bodyhtml = bodyhtml+'<p  align="left">File Key: '+str(key)+'</p>'+'<p  align="left">Region Name: '+str(region_name)+'</p>'+'<p  align="left">EventTime: '+event_time+'</p>'+'<p  align="left">Account ID: '+account_id+'</p>'
                bodyhtml = bodyhtml+"""<p  align="left">Creating/Uploading Unencrypted file into the S3 Bucket is aginst Verizon's Security Policy. KIndly Delete this file from the S3 bucket and recreate by enabling encryption option. 
                To Know more about S3 Object Encryption, Please visit <a href="http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html">AWS S3 Encryption<a></p></div></div></body><html>""" 
                message = {'Subject' : {'Data' : subject},'Body': {'Html' : {'Data' : bodyhtml}}}
                result = ses_client.send_email(Source = me, Destination = destination, Message = message)
                print("****************S3 File Not Encrypted - Notification Sent**********")
        #print("CONTENT TYPE: " + response['ContentType'])
        return response
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
