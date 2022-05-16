BUCKET := taxi-service-gljun2021-04
TIMESTAMP := $(shell date +%s )

init:
	@echo "initializing workspace"
	@echo "copying files to s3 bucket"
	mkdir build
	aws s3api create-bucket --bucket $(BUCKET) --region us-east-1 --acl public-read --object-ownership BucketOwnerPreferred
build: check-env
	@echo "running build"
	@echo "copying files to build directory"
	aws s3 sync src/ s3://$(BUCKET)/build/$(GLNAME)/ --acl public-read

deploy: build
	@echo "deploying application"
	aws cloudformation validate-template --template-url https://$(BUCKET).s3.amazonaws.com/build/$(GLNAME)/stack/main.yml > /dev/null
	aws cloudformation deploy --template-file src/stack/main.yml --stack-name $(GLNAME)-taxi-service \
		--parameter-overrides Bucket=$(BUCKET) Namespace=$(GLNAME) \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

undeploy: check-env
	@echo "running undeploy"
	aws cloudformation delete-stack --stack-name $(GLNAME)-taxi-service

cleanup: check-env
	@echo "running cleanup"
	aws s3 rm s3://$(BUCKET)/build/$(GLNAME)/ --recursive
	rm -rf build/*

check-env:
ifndef GLNAME
	$(error GLNAME is undefined)
endif