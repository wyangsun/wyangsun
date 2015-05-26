
CREATE TABLE `user` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `name` char(20) NOT NULL,
  `password` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
);

insert into user values(1,'wy1','917571464dcb4a7851b8ca7aefbf610a');

CREATE TABLE `hostinfo` (
  `hid` int(20) AUTO_INCREMENT,
  `wan_ip` char(15) DEFAULT NULL,
  `lan_ip` char(15) DEFAULT NULL,
  `hostname` char(20) DEFAULT NULL,
  `groupname` char(20) DEFAULT 'other',
  PRIMARY KEY (`hid`)
);

CREATE TABLE `commandhistory` (
  `cid` int(20) AUTO_INCREMENT,
  `hosts` char(20) DEFAULT NULL,
  `module` char(20) DEFAULT NULL,
  `command` char(160) DEFAULT NULL,
  `datetime` char(20) DEFAULT NULL,
  PRIMARY KEY (`cid`)
);

CREATE TABLE `playbook` (
  `pid` int(20) AUTO_INCREMENT,
  `bookname` char(40) DEFAULT NULL,
  `bookpage` int(10) DEFAULT NULL,
  `hosts` char(20) DEFAULT NULL,
  `module` char(20) DEFAULT NULL,
  `command` char(160) DEFAULT NULL,
  PRIMARY KEY (`pid`)
);
