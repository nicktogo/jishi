# 项目招募平台 - 同济济市

一个让同济师生方便交流项目，促进合作的平台

## Table of Contents

- [Requirements](#requirements)
- [Framework](#framework)
- [Get Started](#get-started)
- [Dependences Installation](#dependences-installation)
   - [windows](#windows)
   - [os x](#os-x)
- [Configuration](#configuration)
- [Usage](#usage)



## Requirements

- Python 2.* >= 2.7.9
- Flask >= 0.10.1

## Framework
  - [Flask](http://docs.jinkan.org/docs/flask/)
  - [Python](https://www.python.org/)
    
## Get Started

```shell
mkdir sse
cd sse
git clone https://github.com/tztztztztz/jishi.git
```

## Dependences Installation

### windows
  - [MySQLdb-python install](http://www.codegood.com/archives/129)
  - [Flask install](http://docs.jinkan.org/docs/flask/installation.html)
  
### os x
  ```shell
  pip install flask
  pip install MySQL-python
  ```
## Configuration
`sse/app/module/db/config.json`
```json
{
  "mysql": {
    "host":"localhost",
    "port":"3306",
    "database":"jishi",
    "user":"root",
    "password":""
  },
  "mongo": {
    "host":"localhost",
    "port":"3306",
    "database":"test",
    "user":"root",
    "password":""
  },
  "redis": {
    "host":"localhost",
    "port":"3306",
    "database":"test",
    "user":"root",
    "password":""
  }
}
```
## Usage

```shell
python run.py
```
see your websit at `http://localhost:5000` on your brower
