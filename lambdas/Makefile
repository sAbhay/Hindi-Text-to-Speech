LAMBDA_NAME:=hinditoipa
# TODO: add ability to change this in method

.PHONY: copy_dependencies_to_output_folder
copy_dependencies_to_output_folder:
	rd /s /q output
	mkdir output
	echo "${LAMBDA_NAME}"
	xcopy /E ${LAMBDA_NAME} output

.PHONY: ci_build
ci_build:
	cd output && sam build
	cd output/.aws-sam/build/${LAMBDA_NAME} && zip -r ${LAMBDA_NAME}.zip . && chmod u=rwx,go=r ${LAMBDA_NAME}.zip
	copy output\.aws-sam\build\${LAMBDA_NAME}\${LAMBDA_NAME}.zip .

.PHONY: ci_build_hinditoipa
ci_build_hinditoipa:
	set LAMBDA_NAME:=hinditoipa
	make copy_dependencies_to_output_folder
	make ci_build

.PHONY: run-hinditoipa
run-hinditoipa:
	set LAMBDA_NAME:=hinditoipa
	make ci_build_hinditoipa
	cd ${LAMBDA_NAME} && sam local invoke -e event.json