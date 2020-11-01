import envoy


def is_package_installed(package: str) -> bool:
    package_res = envoy.run('pip list')
    packages = [p.split(' ')[0] for p in package_res.std_out.split('\n') if p]
    return package in packages
