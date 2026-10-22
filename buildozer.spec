
[app]

title = Missao Oceano
package.name = missaooceano
package.domain = org.missaooceano
source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,txt
source.exclude_dirs = testes,.git,.buildozer,bin,__pycache__

version = 1.0.0
requirements = python3,pygame
orientation = landscape
fullscreen = 1

android.api = 35
android.minapi = 23
android.ndk = 27c
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = False

[buildozer]

log_level = 2
warn_on_root = 1
