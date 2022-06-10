BUCKET := taxi-service-gljun2021-04-1
BUILD_STAMP := $(shell date +%s )
SECURITY_GROUP := sg-08b055a5ae2d14602 #sg-0c75e8c54d14a7923 #
SUBNET_ID := subnet-05576b7ac00da1a6a #subnet-057d907ff8e06168e #
VPC_ID := vpc-097d844410c7d0517 #vpc-0f92c984154228ba8 #
MongoURL := mongodb+srv://root:root@capstone.ctccm.mongodb.net/?retryWrites=true&w=majority

init: check-env prepare-build
	@echo "initializing workspace"
	aws s3api create-bucket --bucket $(BUCKET) --region us-east-1 --acl public-read

	aws cloudformation deploy --template-file stack/base.yml --stack-name base-stack \
		--parameter-overrides SubnetId=$(SUBNET_ID) SecurityGroup=$(SECURITY_GROUP) VpcId=$(VPC_ID) \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

build: check-env prepare-build
	@echo "running build"
	@echo "copying files to build directory"
	# upload layer zip
	mkdir /tmp/gl-build/$(BUILD_STAMP)/python
	pip3 install -r src/requirements.txt --target /tmp/gl-build/$(BUILD_STAMP)/python/
	cd /tmp/gl-build/$(BUILD_STAMP)/python/; rm -r *dist-info __pycache__
	cd /tmp/gl-build/$(BUILD_STAMP)/; zip -r /tmp/gl-build/layer.zip python;
	aws s3 cp /tmp/gl-build/layer.zip s3://$(BUCKET)/build/$(GLNAME)-$(BUILD_STAMP)-layer.zip
	# upload lambda zip
	rm -rf /tmp/gl-build/$(BUILD_STAMP)/*; cp -r src/* /tmp/gl-build/$(BUILD_STAMP)/
	cd /tmp/gl-build/$(BUILD_STAMP)/; zip -r /tmp/gl-build/lambda.zip *; rm -rf /tmp/gl-build/$(BUILD_STAMP);
	aws s3 sync src/ s3://$(BUCKET)/build/$(GLNAME)/$(BUILD_STAMP)/ --acl public-read
	aws s3 sync stack/ s3://$(BUCKET)/build/$(GLNAME)/$(BUILD_STAMP)/stack/ --acl public-read
	aws s3 cp /tmp/gl-build/lambda.zip s3://$(BUCKET)/build/$(GLNAME)/$(BUILD_STAMP)/

deploy: build
	@echo "deploying application"
	aws cloudformation validate-template --template-url https://$(BUCKET).s3.amazonaws.com/build/$(GLNAME)/$(BUILD_STAMP)/stack/main.yml > /dev/null
	aws cloudformation deploy --template-file stack/main.yml --stack-name $(GLNAME)-taxi-service \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --parameter-overrides Bucket=$(BUCKET) Namespace=$(GLNAME) BuildStamp=$(BUILD_STAMP)\
		SubnetId=$(SUBNET_ID) SecurityGroup=$(SECURITY_GROUP) MongoUri=$(MongoURL)\



undeploy: check-env
	@echo "running undeploy"
	aws cloudformation delete-stack --stack-name $(GLNAME)-taxi-service

client: check-env
	@echo "running clients"
	API=$(shell aws cloudformation describe-stacks --stack-name $(GLNAME)-taxi-service --query 'Stacks[0].Outputs[0].OutputValue'); \
	python3 ./src/taxi_app.py --uri $$API --count $(COUNT) --latitude-min 12.87 --latitude-max 13.21 --longitude-min 77.34 \
	  --longitude-max 77.87

cleanup: check-env
	@echo "running cleanup"
	aws s3 rm s3://$(BUCKET)/build/$(GLNAME)/ --recursive
	rm -rf build/*

prepare-build:
	rm -rf /tmp/gl-build/*
	rm -f /tmp/gl-build/lambda.zip
	mkdir -p /tmp/gl-build/$(BUILD_STAMP)

check-env:
ifndef GLNAME
	$(error GLNAME is undefined)
endif