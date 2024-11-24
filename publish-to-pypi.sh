########## for uploading onto pypi
# for a project that uses pyproject.toml

# created in Oct 2024; mostly mimicks former Makefile.pypi
#
# to initialize twine credentials
# keyring set upload.pypi.org parmentelat
# keyring set test.pypi.org parmentelat

# NOTE: to upload on test.pypi.org, use
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# required to extract project metadata
type -p jq >& /dev/null || { echo ==== "jq is not installed; please install it and restart"; exit 1; }
pip show build >& /dev/null || { echo ==== installing build; pip install build; }
type -p hatch >& /dev/null || { echo ==== installing hatch; pip install hatch; }
type -p twine >& /dev/null || { echo ==== installing twine; pip install twine; }


PYPI_NAME=$(hatch project metadata | jq .name | tr -d '"')
VERSION=$(hatch project metadata | jq .version | tr -d '"')
VERSIONTAG="${PYPI_NAME}-${VERSION}"
GIT_TAG_ALREADY_SET=$(git tag | grep "^${VERSIONTAG}$")
# to check for uncommitted changes
GIT_CHANGES=$(echo $(git diff HEAD | wc -l))


function cleanpypi() {
	echo cleaning up build and dist
	rm -rf dist build
}

function raincheck() {
	if [ ${GIT_CHANGES} != 0 ]; then echo "You have uncommitted changes - cannot publish"; return 1; fi
	if [ -n "${GIT_TAG_ALREADY_SET}" ] ; then echo "tag ${VERSIONTAG} already set"; return 1; fi
	if ! grep -q " ${VERSION}" CHANGELOG.md ; then echo no mention of ${VERSION} in CHANGELOG.md; return 1; fi
}

function confirm() {
	echo "You are about to release ${VERSION} - OK (Ctrl-c if not) ? " ; read _
}

function settag() {
	echo "You are about to release ${VERSION} - OK (Ctrl-c if not) ? " ; read _
	git tag ${VERSIONTAG}
}

function build_and_publish() {
	python -m build && twine upload dist/*${VERSION}*
}

function git_push() {
	echo "Push to github (Ctrl-c if not) ? " ; read _
	git push --tags
}

all() {
	cleanpypi
	raincheck || return 1
	settag
	build_and_publish
	git_push
}

all
