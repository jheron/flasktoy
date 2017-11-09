
qwert:
	@for image in 'centos:6' 'centos:7' 'cern:sl6-base' 'cern:sl7-base' ; do \
		echo $$image ; \
	done

build:
	@for image in 'centos:6.9' 'centos:7.4' 'cern:sl6-base' 'cern:sl7-base' ; do \
		git clone https://github.com/jheron/flasktoy.git ; \
		VERSION=`git describe —tags —abbrev=0` ; \
		OS="${image/:/-/}"
		CURRENT=feflask-${OS}_${VERSION}
		sed  "s/docker_image/$$image/" Dockerfile-targz >Dockerfile-$$image ; \
		docker build -f Dockerfile$$image -t feflask-$$image . ; \
		docker run --name feflask-$$image ; \
		aws s3 cp s3://feflask/${CURRENT}.tar.gz ${CURRENT}.tar.gz ; \
		aws s3 cp s3://feflask/${CURRENT}.shasum ${CURRENT}.shasumgz ; \
	done

build-docker:
	@for image in 'centos:6' 'centos:7' 'cern:sl6-base' 'cern:sl7-base' ; do \
		git clone https://github.com/jheron/flasktoy.git ; \
		VERSION=`git describe —tags —abbrev=0` ; \
		OS="${image/:/-/}"
		CURRENT = di-feflask-${OS}_${VERSION}
		docker build -t feflask . ; \
		docker save -o ${CURRENT}.tar ; \
		shasum ${CURRENT}.tar >${CURRENT}.shasum ; \
		docker tag jheron/feflask:${VERSION} ; \
		docker push jheron/feflask:${VERSION} ; \
		aws s3 cp ${CURRENT}.tar  s3://feflask/${CURRENT}.tar ; \
		aws s3 cp ${CURRENT}.shasum  s3://feflask/${CURRENT}.shasum ; \
	done

test-docker:
	git clone https://github.com/jheron/flasktoy.git 
	VERSION=`git describe —tags —abbrev=0`
	docker pull jheron/feflask:${VERSION}
	docker run -d -p 80:80 —name feflask jheron/feflask:${VERSION}
	mkdir test_feflask
	cp test_feflask.py test
	cp test_requirements.txt test
	cd test
	virtualenv env
	source env/bin/activate
	pip install -r test_requirements.txt
	py.test --junitxml ../results/results.xml tests.py
	docker stop feflask
	cd ..
	deactivate
	rm -rf test_feflask

run:
	git clone https://github.com/jheron/flasktoy.git 
	VERSION=`git describe —tags —abbrev=0`
	@docker run -p 8080:8080 --name=feflask -d jheron/feflask:${VERSION}

start:
		@docker start feflask
stop:
		@docker stop feflask
clean:	stop
		@docker rm -v feflask
