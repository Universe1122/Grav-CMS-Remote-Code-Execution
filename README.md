# Grav-CMS-Remote-Code-Execution

해당 래포는 [Grav CMS](https://github.com/getgrav/grav)의 post auth RCE 취약점을 설명한 것입니다.

취약점을 트리거 하기 위해서는 writer 권한을 가진 계정이 필요하며, `<= 1.7.42.3` 까지 동작하는 것을 확인 했으며 환경에 따라 그 이상의 버전에서도 동작할 수 있습니다.