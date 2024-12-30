# Cardverse-KPop

---
## 自動生成資料夾架構
```bash
sudo apt-get install tree
```

```bash
.
├── app
│   ├── extensions.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── __pycache__
│   │   ├── api.cpython-39.pyc
│   │   ├── extensions.cpython-39.pyc
│   │   ├── __init__.cpython-39.pyc
│   │   ├── models.cpython-39.pyc
│   │   └── routes.cpython-39.pyc
│   ├── routes.py
│   ├── static
│   │   ├── css
│   │   │   ├── card.css
│   │   │   ├── fontawesome-all.min.css
│   │   │   ├── main.css
│   │   │   ├── noscript.css
│   │   │   ├── style_login.css
│   │   │   └── style_register.css
│   │   ├── images
│   │   │   ├── background.png
│   │   │   ├── background_register.png
│   │   │   ├── banner.jpg
│   │   │   ├── card_after_training.png
│   │   │   ├── pic01.jpg
│   │   │   ├── pic02.jpg
│   │   │   ├── pic03.jpg
│   │   │   ├── pic04.jpg
│   │   │   ├── pic05.jpg
│   │   │   ├── pic06.jpg
│   │   │   ├── pic07.jpg
│   │   │   ├── pic08.jpg
│   │   │   ├── pic09.jpg
│   │   │   ├── pic10.jpg
│   │   │   └── pic11.jpg
│   │   ├── js
│   │   │   ├── breakpoints.min.js
│   │   │   ├── browser.min.js
│   │   │   ├── jquery.min.js
│   │   │   ├── jquery.scrollex.min.js
│   │   │   ├── jquery.scrolly.min.js
│   │   │   ├── main.js
│   │   │   └── util.js
│   │   ├── sass
│   │   │   ├── base
│   │   │   │   ├── _page.scss
│   │   │   │   ├── _reset.scss
│   │   │   │   └── _typography.scss
│   │   │   ├── components
│   │   │   │   ├── _actions.scss
│   │   │   │   ├── _box.scss
│   │   │   │   ├── _button.scss
│   │   │   │   ├── _contact-method.scss
│   │   │   │   ├── _form.scss
│   │   │   │   ├── _icon.scss
│   │   │   │   ├── _icons.scss
│   │   │   │   ├── _image.scss
│   │   │   │   ├── _list.scss
│   │   │   │   ├── _pagination.scss
│   │   │   │   ├── _row.scss
│   │   │   │   ├── _section.scss
│   │   │   │   ├── _spotlights.scss
│   │   │   │   ├── _table.scss
│   │   │   │   └── _tiles.scss
│   │   │   ├── layout
│   │   │   │   ├── _banner.scss
│   │   │   │   ├── _contact.scss
│   │   │   │   ├── _footer.scss
│   │   │   │   ├── _header.scss
│   │   │   │   ├── _main.scss
│   │   │   │   ├── _menu.scss
│   │   │   │   └── _wrapper.scss
│   │   │   ├── libs
│   │   │   │   ├── _breakpoints.scss
│   │   │   │   ├── _functions.scss
│   │   │   │   ├── _html-grid.scss
│   │   │   │   ├── _mixins.scss
│   │   │   │   ├── _vars.scss
│   │   │   │   └── _vendor.scss
│   │   │   ├── main.scss
│   │   │   └── noscript.scss
│   │   └── webfonts
│   │       ├── fa-brands-400.eot
│   │       ├── fa-brands-400.svg
│   │       ├── fa-brands-400.ttf
│   │       ├── fa-brands-400.woff
│   │       ├── fa-brands-400.woff2
│   │       ├── fa-regular-400.eot
│   │       ├── fa-regular-400.svg
│   │       ├── fa-regular-400.ttf
│   │       ├── fa-regular-400.woff
│   │       ├── fa-regular-400.woff2
│   │       ├── fa-solid-900.eot
│   │       ├── fa-solid-900.svg
│   │       ├── fa-solid-900.ttf
│   │       ├── fa-solid-900.woff
│   │       └── fa-solid-900.woff2
│   └── templates
│       ├── card.html
│       ├── dashboard.html
│       ├── elements.html
│       ├── generic.html
│       ├── index.html
│       ├── landing.html
│       ├── login1.html
│       ├── login.html
│       ├── login_ori.html
│       ├── register.html
│       └── test.html
├── config.py
├── docker-compose.yaml
├── Dockerfile
├── html5up-forty
│   ├── assets
│   │   ├── css
│   │   │   ├── fontawesome-all.min.css
│   │   │   ├── main.css
│   │   │   └── noscript.css
│   │   ├── js
│   │   │   ├── breakpoints.min.js
│   │   │   ├── browser.min.js
│   │   │   ├── jquery.min.js
│   │   │   ├── jquery.scrollex.min.js
│   │   │   ├── jquery.scrolly.min.js
│   │   │   ├── main.js
│   │   │   └── util.js
│   │   ├── sass
│   │   │   ├── base
│   │   │   │   ├── _page.scss
│   │   │   │   ├── _reset.scss
│   │   │   │   └── _typography.scss
│   │   │   ├── components
│   │   │   │   ├── _actions.scss
│   │   │   │   ├── _box.scss
│   │   │   │   ├── _button.scss
│   │   │   │   ├── _contact-method.scss
│   │   │   │   ├── _form.scss
│   │   │   │   ├── _icon.scss
│   │   │   │   ├── _icons.scss
│   │   │   │   ├── _image.scss
│   │   │   │   ├── _list.scss
│   │   │   │   ├── _pagination.scss
│   │   │   │   ├── _row.scss
│   │   │   │   ├── _section.scss
│   │   │   │   ├── _spotlights.scss
│   │   │   │   ├── _table.scss
│   │   │   │   └── _tiles.scss
│   │   │   ├── layout
│   │   │   │   ├── _banner.scss
│   │   │   │   ├── _contact.scss
│   │   │   │   ├── _footer.scss
│   │   │   │   ├── _header.scss
│   │   │   │   ├── _main.scss
│   │   │   │   ├── _menu.scss
│   │   │   │   └── _wrapper.scss
│   │   │   ├── libs
│   │   │   │   ├── _breakpoints.scss
│   │   │   │   ├── _functions.scss
│   │   │   │   ├── _html-grid.scss
│   │   │   │   ├── _mixins.scss
│   │   │   │   ├── _vars.scss
│   │   │   │   └── _vendor.scss
│   │   │   ├── main.scss
│   │   │   └── noscript.scss
│   │   └── webfonts
│   │       ├── fa-brands-400.eot
│   │       ├── fa-brands-400.svg
│   │       ├── fa-brands-400.ttf
│   │       ├── fa-brands-400.woff
│   │       ├── fa-brands-400.woff2
│   │       ├── fa-regular-400.eot
│   │       ├── fa-regular-400.svg
│   │       ├── fa-regular-400.ttf
│   │       ├── fa-regular-400.woff
│   │       ├── fa-regular-400.woff2
│   │       ├── fa-solid-900.eot
│   │       ├── fa-solid-900.svg
│   │       ├── fa-solid-900.ttf
│   │       ├── fa-solid-900.woff
│   │       └── fa-solid-900.woff2
│   ├── card.css
│   ├── card.html
│   ├── elements.html
│   ├── generic.html
│   ├── images
│   │   ├── banner.jpg
│   │   ├── pic01.jpg
│   │   ├── pic02.jpg
│   │   ├── pic03.jpg
│   │   ├── pic04.jpg
│   │   ├── pic05.jpg
│   │   ├── pic06.jpg
│   │   ├── pic07.jpg
│   │   ├── pic08.jpg
│   │   ├── pic09.jpg
│   │   ├── pic10.jpg
│   │   └── pic11.jpg
│   ├── index.html
│   ├── landing.html
│   ├── LICENSE.txt
│   ├── README.md
│   ├── README.txt
│   └── test.html
├── LICENSE
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── __pycache__
│   │   └── env.cpython-39.pyc
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 601c51ce752d_add_column_cn_to_users.py
│       ├── e7628200c5af_change_column_password_to_users.py
│       └── __pycache__
│           ├── 601c51ce752d_add_column_cn_to_users.cpython-39.pyc
│           └── e7628200c5af_change_column_password_to_users.cpython-39.pyc
├── nginx.conf
├── README.md
├── requirements.txt
└── run.py
```

---
## 自動檢測程式碼中的 import 並安裝
### 使用 pipreqs 工具：

pipreqs 可以掃描程式碼，檢測使用到的依賴包並生成 requirements.txt。
安裝 pipreqs：
```bash
pip install pipreqs
```
在程式碼所在目錄生成依賴列表：
```bash
pipreqs /path/to/your/code
```
生成的 requirements.txt 文件會包含程式碼中所有需要的依賴包。
安裝這些依賴：
```bash
pip install -r requirements.txt
```

### 使用 autopip 工具（快速安裝缺少的依賴）：

autopip 會根據程式碼中的 import 嘗試自動安裝缺少的依賴。
安裝 autopip：
```bash
pip install autopip
```
使用 autopip 執行程式碼：
```bash
autopip python your_script.py
```