pkg_name=vmware_reddit_bot
pkg_version="0.1.0"
pkg_maintainer="No one in particular"
pkg_license=("Apache-2.0")
pkg_deps=(core/python37)
pkg_lib_dirs=(lib)
pkg_bin_dirs=(bin)

do_unpack() {
  return 0
}

do_build() {
  return 0
}

do_setup_environment() {
  push_runtime_env PYTHONPATH ${pkg_prefix}/lib/python3.7/site-packages
}

do_install() {
  cp -R $PLAN_CONTEXT/../* $CACHE_PATH
  pushd $CACHE_PATH 2>/dev/null
  mkdir -p ${pkg_prefix}/lib/python3.7/site-packages
  python setup.py install --prefix ${pkg_prefix} --no-compile
  cp vmware_reddit_bot.py ${pkg_prefix}/bin
  cp comments_replied_to.txt ${pkg_prefix}/bin
}
