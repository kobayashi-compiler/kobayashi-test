# Structure

```
x86
├── nginx
│   ├── duck.conf
│   └── nyars.conf
├── systemd
│   └── duck.service
└── wsgi
    ├── compiler2021
    |   └── .git
    ├── kobayashi-compiler
    |   └── .git
    ├── testcases -> compiler2021
    │   ├── function_test2020
    │   ├── function_test2021
    │   ├── h_funtional
    │   ├── performance_test2021
    │   ├── judge.py
    │   └── kslib.h
    ├── duck.ini
    ├── duck.py
    ├── judge.sh
    └── wsgi.py
```

```
raspi
├── nginx
│   ├── duck.conf
│   └── nyars.conf
├── systemd
│   └── duck.service
└── wsgi
    ├── compiler2021
    |   └── .git
    ├── testcases -> compiler2021
    │   ├── function_test2020
    │   ├── function_test2021
    │   ├── h_funtional
    │   └── performance_test2021
    ├── duck.ini
    ├── duck.py
    ├── libsysy.a -> compiler2021
    └── wsgi.py
```

Submit new issue if errors occurred!

ref: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04