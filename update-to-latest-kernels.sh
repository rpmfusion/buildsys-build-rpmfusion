#! /bin/bash
print_kernellist()
{
	echo ${1}
	echo ${1}smp
	echo ${1}PAE
}

if [[ ! "${1}" ]] || [[ ! "${2}" ]] ; then
	echo "Please call with list of latest standard and xen kernel versions" >&2
	exit 1
fi

if [[ ! "${RPM_PACKAGER}" ]] ; then
	echo "Please set RPM_PACKAGER for rpmdev-bumpspec" >&2
	exit 1
fi

# update spec file
rpmdev-bumpspec -c "- rebuild for kernels ${1} ${2}" *.spec

listofnewkernels=
listofcurrentkernels="$(cat buildsys-build-rpmfusion-kerneldevpkgs-current)"
new=0
while [[ "${1}" ]] ; do
	if [[ "${1}" != "${1%%xen}" ]]; then
		# this is a xen kernel
		if ! echo "${listofcurrentkernels}" |  grep "${1}" &> /dev/null
		then
			# xen kernel is new! remove the old one and put and the new one in
			listofcurrentkernels="$(echo "${listofcurrentkernels}" |  grep -v -e "xen$")"$'\n'"${1}"
			listofnewkernels="${listofnewkernels}${1}"
			let new++
		fi
	else
		# this is a standard kernel
		if ! echo "${listofcurrentkernels}" |  grep "${1}" &> /dev/null
		then
			# standard kernel is new! put the old ones put and the new ones in
			listofcurrentkernels="$(echo "${listofcurrentkernels}" |  grep "xen")"$'\n'"${1}"$'\n'"${1}PAE"$'\n'"${1}smp"
			listofnewkernels="${listofnewkernels}${1}"$'\n'"${1}PAE"$'\n'"${1}smp"
			let new++
		fi
	fi
	
	shift
done
	
echo "${listofcurrentkernels}" > buildsys-build-rpmfusion-kerneldevpkgs-current
if (( ${new} < 2 )); then
	echo "${listofnewkernels}" > buildsys-build-rpmfusion-kerneldevpkgs-newest
else
	: > buildsys-build-rpmfusion-kerneldevpkgs-newest
fi	

cvs diff -u | less
echo hit enter to continue 
read
make clog; cvs commit -F clog 
rm clog
make tag build
