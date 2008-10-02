#!/bin/bash
#
# buildsys-build-list-kernels.sh - Helper script for building kernel module RPMs for Fedora
#
# Copyright (c) 2007 Thorsten Leemhuis <fedora@leemhuis.info>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

shopt -s extglob

myver="0.0.7"
repo=rpmfusion
myprog="buildsys-build-${repo}-kerneldevpkgs"
supported_targetarchs="i586 i686 x86_64 ppc ppc64"
if [[ -e ./buildsys-build-${repo}-kerneldevpkgs-current ]]; then
	prefix=./buildsys-build-${repo}-
else
	prefix=/usr/share/buildsys-build-${repo}/
fi

requires=
filterfile=
target=$(uname -m)
show_kernels="current"

print_kernels ()
{
	local this_target=${1}
	local this_grepoptions=
	local this_command=
	local this_kernellistfiles=

	# which files to use
	if [[ "${show_kernels}" == "newest" ]]; then
		this_kernellistfiles="${prefix}kerneldevpkgs-newest"
	elif [[ "${show_kernels}" == "current" ]]; then
		this_kernellistfiles="${prefix}kerneldevpkgs-current"
	fi

	# error out if not defined
	if (( $(stat -c%s "${this_kernellistfiles}") <= 1 )); then
		echo "(no kernels defined)"
		return 1
	fi

	# if there are no newest kernels use current ones for newest 
	# can happen in rawhide 
	if [[ "${show_kernels}" == "newest" ]] && [[ -e "${prefix}kerneldevpkgs-newest" ]] && (( $(stat -c%s "${prefix}kerneldevpkgs-newest") <= 1 )) ; then
		this_kernellistfiles="${prefix}kerneldevpkgs-current"
	fi

	# target
	if [[ "${this_target}" ]] ; then
		this_grepoptions="${this_grepoptions} --file ${prefix}filterfile_${this_target}"	
	fi

	# custom filterfile
	if [[ "${filterfile}" ]]; then
		this_grepoptions="${this_grepoptions} --file ${filterfile}"	
	fi

	# do we need grep at all?
	if [[ "${this_grepoptions}" ]]; then 
		this_command="grep --invert-match --no-filename"
	else
		this_command="cat"
	fi

	# go
	${this_command} ${this_grepoptions} ${this_kernellistfiles} | while read this_kernel; do 
		this_kernel_verrel=${this_kernel%%$kernels_known_variants}
		this_kernel_variant=${this_kernel##$this_kernel_verrel}

		if [[ "${requires}" ]]  || [[ "${buildrequires}" ]]; then
			if echo ${this_kernel} | grep -- 'default' &> /dev/null; then		
				if [[ "${requires}" ]]; then
					echo "Requires: kernel${this_kernel_variant:+-${this_kernel_variant}}-devel-${this_target}"
				fi
	
				if [[ "${buildrequires}" ]]; then 
					echo "BuildRequires: kernel${this_kernel_variant:+-${this_kernel_variant}}-devel-${this_target}"
				fi
			else
				if [[ "${requires}" ]]; then
					echo "Requires: kernel-devel-uname-r = ${this_kernel}"
				fi
	
				if [[ "${buildrequires}" ]]; then 
					echo "BuildRequires: kernel-devel-uname-r = ${this_kernel}"
				fi
			fi
		else
			echo ${this_kernel_verrel}.${this_target}${this_kernel_variant:+.${this_kernel_variant}}
		fi
	done
}

print_requires ()
{
	local this_kernel_verrel
	local this_kernel_variant

	for this_arch in ${supported_targetarchs}; do
		echo $'\n'"%ifarch ${this_arch}"	
		print_kernels ${this_arch}
		echo "%endif"	
	done
}

myprog_help ()
{
	echo "Usage: $(basename ${0}) [OPTIONS]"
	echo $'\n'"Prints a list of all avilable kernel-devel packages in the buildsys, as"$'\n'"defined by the buildsys-buildkmods-all package."
	echo $'\n'"Available options:"
	echo " --filterfile <file> -- filter the results with grep --file <file>"
	echo " --current           -- only list current up2date kernels"
#	echo " --newest            -- only list newly released kernels"
	echo " --requires          -- print list as requires with ifarch section for"$'\n'"                        further use in a RPM spec file package header"
	echo " --prefix <dir>      -- look for the data files in <prefix>"
	echo " --target <arch>     -- target-arch (ignored if --requires is used)"
	echo $'\n'"Supported target archs: ${supported_targetarchs}"
}

while [ "${1}" ] ; do
	case "${1}" in
		--prefix)
			shift
			if [[ ! "${1}" ]] ; then
				echo "Error: Please provide a prefix where to find data-files together with --prefix" >&2
				exit 2
			fi
			prefix="${1}"
			shift
			;;
		--filterfile)
			shift
			if [[ ! "${1}" ]] ; then
				echo "Error: Please provide path to a filter-file together with --filterfile" >&2
				exit 2
			elif [[ ! -e "${1}" ]]; then	
				echo "Error: Filterfile ${1} not found" >&2
				exit 2
			fi
			filterfile="${1}"
			shift
			;;
		--target)
			shift
			if [[ ! "${1}" ]] ; then
				echo "Error: Please provide one of the supported targets together with --target" >&2
				exit 2
			fi

			for this_arch in ${supported_targetarchs}; do
				if [[ "${this_arch}" = "${1}" ]]; then
					target="${1}"
					shift
					break
				fi
			done

			if [[ ! "${target}" ]]; then
				echo "Error: ${1} is not a supported target" >&2
				exit 2
			fi
			;;
		--requires)
			shift
			requires="true"
			;;
		--buildrequires)
			shift
			buildrequires="true"
			;;
		--current)
			shift
			show_kernels="current"
			;;
		--newest)
			shift
			show_kernels="newest"
			;;
		--help)
			myprog_help
			exit 0
			;;
		--version)
			echo "${myprog} ${myver}"
			exit 0
			;;
		*)
			echo "Error: Unknown option '${1}'."$'\n' >&2
			myprog_help >&2
			exit 2
			;;
	esac
done

# more init after parsing command line parameters
if [[ -e ./kmodtool-kernel-variants ]] ; then
	kernels_known_variants="$(cat ./kmodtool-kernel-variants)"
elif [[ -e /usr/share/kmodtool/kernel-variants ]] ; then
	kernels_known_variants="$(cat /usr/share/kmodtool/kernel-variants)"
else
	echo "Could not find /usr/share/kmodtool/kernel-variants (required)" >&2
	exit 2
fi

# sanity checks
if [[ ! "${kernels_known_variants}" ]] ; then
	echo "could not determine known kenrel variants"
	exit 2
fi

# go
if [[ "${requires}" ]] || [[ "${buildrequires}" ]] ; then
	print_requires
else
	print_kernels ${target}
fi
