#! /bin/bash
print_kernellist()
{
	echo ${1}
	echo ${1}smp
	echo ${1}PAE
}

if [[ ! "${1}" ]] ; then
	echo "Please call with verrel of latest standard kernel version" >&2
	exit 1
fi

if [[ x"$(rpmdev-packager)" == x""  ]] ; then
	echo "Please set RPM_PACKAGER for rpmdev-bumpspec" >&2
	exit 1
fi

# update spec file
rpmdev-bumpspec -c "- rebuild for kernel ${1}" *.spec
# update buildsys-build-rpmfusion-kerneldevpkgs-current
print_kernellist ${1} > buildsys-build-rpmfusion-kerneldevpkgs-current

cvs diff -u
read
make clog; cvs commit -F clog 
rm clog
make tag build
